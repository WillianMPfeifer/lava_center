# Instruções: fix-flaky-test

Diagnostica e estabiliza testes com comportamento intermitente.

---

## Fluxo de Trabalho

### 1. Coletar contexto

Pergunte se não fornecido:
- Com que frequência falha? (1 em 10 execuções? 5 em 10?)
- Falha no CI mas passa local? Ou ambos?
- O erro é sempre o mesmo ou varia?
- Alguma mudança recente no código ou ambiente?

### 2. Identificar o padrão

Leia o teste e o output de falha. Classifique em uma categoria abaixo.

---

## Categorias de Flakiness

### A. Dependência de Tempo / Race Condition

**Sintomas:**
- Falha com "timeout" ou "element not found" intermitentemente
- Passa quando há delay artificial, falha quando remove
- Falha mais em CI (ambiente mais lento)

**Causas:**
- Operação assíncrona sem await adequado
- Polling sem espera mínima
- Verificar resultado antes da operação propagar

**Correções:**

```javascript
// ❌ Sem espera pela propagação
await createResource(authToken, request, data);
const result = await getResource(authToken, request, data.name);
expect(result.status()).toBe(200); // pode ser 404 se API é eventual consistent

// ✅ Com retry até estabilizar
const waitForResource = async (request, name, maxAttempts = 5) => {
  for (let i = 0; i < maxAttempts; i++) {
    const res = await request.get(`/resources/${name}`, { headers });
    if (res.status() === 200) return res;
    await new Promise(resolve => setTimeout(resolve, 500));
  }
  throw new Error(`Resource ${name} not found after ${maxAttempts} attempts`);
};

// ✅ Para Playwright UI: use waitFor
await page.waitForSelector(".success-message");
await expect(page.locator(".data-table")).toBeVisible();
```

---

### B. Dado Compartilhado / Poluição de Estado

**Sintomas:**
- Passa quando roda sozinho, falha em suíte completa
- Falha com 409 (conflict) ou dados inesperados no corpo
- Comportamento depende da ordem de execução

**Causas:**
- Cleanup não executado corretamente
- Dados com nome fixo reusados entre testes
- Estado global mutado por um teste e lido por outro

**Correções:**

```javascript
// ❌ Nome fixo
const data = { name: "test-resource" };

// ✅ Nome único por execução
const uniqueSuffix = `${Date.now()}-${Math.random().toString(36).slice(2, 7)}`;
const data = { name: `test-resource-${uniqueSuffix}` };

// ❌ Cleanup sem tratamento de falha
test.afterEach(async ({ request }) => {
  await deleteResource(authToken, request, createdId); // quebra se já foi deletado
});

// ✅ Cleanup robusto
test.afterEach(async ({ request }) => {
  if (createdId) {
    try {
      await deleteResource(authToken, request, createdId);
    } catch (e) {
      console.log(`Cleanup skipped: ${e.message}`);
    } finally {
      createdId = null;
    }
  }
});
```

---

### C. Token / Autenticação Expirada

**Sintomas:**
- Falha com 401 de forma intermitente
- Passa no início da suíte, falha nos testes finais
- Mais comum em suítes longas

**Causas:**
- Token obtido uma vez e reusado por toda a suíte
- TTL do token menor que a duração da suíte

**Correções:**

```javascript
// ❌ Token obtido uma vez para toda a suíte
let authToken;
test.beforeAll(async ({ request }) => {
  authToken = await TokenHelper.getToken(request); // pode expirar
});

// ✅ Token renovado antes de cada teste
let authToken;
test.beforeEach(async ({ request }) => {
  authToken = await TokenHelper.getToken(request); // sempre fresco
});
```

---

### D. Dependência de Ambiente / Dados Externos

**Sintomas:**
- Passa em staging, falha em prod (ou vice-versa)
- Falha quando outro processo altera o banco
- Falha em datas/horários específicos

**Causas:**
- Teste depende de dados de seed que podem ser alterados
- Teste depende de feature flag ou configuração variável
- Uso de `new Date()` sem controle (horário de verão, timezone)

**Correções:**

```javascript
// ❌ Depende de dado de seed com ID fixo
const result = await request.get("/users/1"); // usuário ID 1 pode não existir

// ✅ Cria e gerencia seu próprio dado
const user = await createUser(authToken, request, userData);
createdUserId = user.id;
const result = await request.get(`/users/${createdUserId}`);

// ❌ Lógica baseada em data atual
const isWeekend = new Date().getDay() === 0 || new Date().getDay() === 6;
if (isWeekend) test.skip();

// ✅ Mock de data ou evitar dependência temporal
// Use dados que não dependem de contexto temporal
```

---

### E. Paralelismo / Concorrência

**Sintomas:**
- Passa quando roda em serial (`--workers=1`), falha em paralelo
- Falha com 409 (conflict) mesmo com `Date.now()`
- Erros de banco de dados (deadlock, unique constraint)

**Causas:**
- `Date.now()` não é suficientemente único com múltiplos workers
- Testes disputam o mesmo recurso compartilhado

**Correções:**

```javascript
// ❌ Date.now() pode colidir com workers paralelos
const name = `test-${Date.now()}`;

// ✅ Adicionar worker ID ou sufixo aleatório
const workerId = process.env.TEST_WORKER_INDEX || "0";
const name = `test-${Date.now()}-w${workerId}-${Math.random().toString(36).slice(2, 6)}`;

// ✅ Ou usar crypto para UUID
const { randomUUID } = require("crypto");
const name = `test-${randomUUID()}`;
```

---

### F. Cleanup Insuficiente no beforeEach

**Sintomas:**
- Primeiro teste passa, segundo falha com dados do primeiro
- `createdId` tem valor de execução anterior

**Correções:**

```javascript
// ❌ Variável não resetada
let createdId;

test.afterEach(async () => {
  if (createdId) {
    await deleteResource(createdId);
    // esqueceu: createdId = null
  }
});

// ✅ Reset explícito
let createdId;

test.beforeEach(() => {
  createdId = null; // garante estado limpo
});

test.afterEach(async () => {
  if (createdId) {
    try { await deleteResource(createdId); } catch {}
    createdId = null;
  }
});
```

---

## 3. Executar para Confirmar Estabilidade

Execute o teste múltiplas vezes seguidas:

```bash
# Playwright — executar 5 vezes
for i in {1..5}; do
  echo "=== Execução $i ==="
  npx playwright test caminho/arquivo.spec.js --reporter=list
done

# Playwright — usar repeat-each
npx playwright test caminho/arquivo.spec.js --repeat-each=5 --reporter=list
```

O teste só está estável quando passar em todas as execuções.

---

## 4. Reportar

```
## Resultado: fix-flaky-test — [nome do arquivo]

**Categoria de flakiness:** [categoria identificada]
**Causa raiz:** [explicação clara]
**Correções aplicadas:**
  - [mudança 1]
  - [mudança 2]
**Validação:** ✅ Passou em X/5 execuções consecutivas
```
