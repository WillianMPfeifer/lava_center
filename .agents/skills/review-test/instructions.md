# Instruções: review-test

Revisa arquivos de teste em múltiplas dimensões e gera um relatório de qualidade.

---

## Fluxo de Trabalho

### 1. Coletar o arquivo

Se o usuário não forneceu o arquivo:
- Peça o caminho do arquivo
- Pergunte o framework (Playwright, Jest, Cypress, Vitest, etc.)

Leia o arquivo completo antes de iniciar a revisão.

### 2. Aplicar o Checklist de Revisão

Avalie cada item do checklist abaixo e registre achados.

---

## Checklist de Revisão

### A. Estrutura e Organização

- [ ] O arquivo testa apenas um endpoint/componente/feature?
- [ ] Os testes estão agrupados em `describe` com nome descritivo?
- [ ] A ordem dos testes faz sentido (happy path → erros → edge cases)?
- [ ] Os nomes dos testes descrevem claramente o comportamento esperado?
- [ ] O arquivo tem um único `describe` de nível superior?

**Problemas comuns:**
- Múltiplos endpoints no mesmo arquivo sem agrupamento
- Nomes genéricos como `"test 1"` ou `"should work"`
- Mistura de cenários positivos e negativos sem organização

---

### B. Isolamento e Independência

- [ ] Cada teste pode ser executado de forma independente?
- [ ] Testes não compartilham estado mutável entre si?
- [ ] A ordem de execução dos testes não afeta o resultado?
- [ ] Variáveis de escopo do `describe` são resetadas no `beforeEach`?

**Problemas comuns:**
- `let id = null` no escopo do describe, não resetado entre testes
- Um teste dependendo de dado criado por outro
- Variável de auth token não renovada entre testes

---

### C. Setup e Cleanup

- [ ] Existe `beforeEach` para autenticação e setup necessário?
- [ ] Existe `afterEach` para deletar dados criados durante o teste?
- [ ] O cleanup usa `try-catch` para não quebrar se o dado não existir?
- [ ] Dados de teste usam identificadores únicos (timestamp, UUID)?
- [ ] O cleanup remove TODOS os dados criados, não só o principal?

**Problemas comuns:**
```javascript
// ❌ Sem cleanup
test("criar usuário", async ({ request }) => {
  const user = await createUser(authToken, request, data);
  // dados ficam no banco
});

// ✅ Com cleanup
test("criar usuário", async ({ request }) => {
  const user = await createUser(authToken, request, data);
  createdId = user.id; // afterEach vai limpar
});
```

---

### D. Asserções

- [ ] Cada teste tem pelo menos uma asserção explícita?
- [ ] O status code é sempre verificado?
- [ ] O corpo da resposta é verificado quando relevante?
- [ ] Asserções são específicas (não apenas `toBeDefined()`)?
- [ ] Testes negativos verificam a mensagem de erro, não só o status?

**Problemas comuns:**
```javascript
// ❌ Asserção fraca
expect(response.status()).toBe(200);

// ✅ Asserção completa
expect(response.status()).toBe(200);
const body = await response.json();
expect(body).toHaveProperty("name", expectedName);
expect(body).toHaveProperty("id");
```

---

### E. Dados de Teste

- [ ] Dados de teste são únicos (evitam conflito com execuções paralelas)?
- [ ] Não há dados hardcoded que dependem de estado do ambiente?
- [ ] IDs e valores fixos são justificados (ex: dados de seed)?
- [ ] Dados sensíveis não estão no código (senhas, tokens)?

**Problemas comuns:**
```javascript
// ❌ Nome fixo (falha se rodar duas vezes)
const data = { name: "meu-teste" };

// ✅ Nome único
const data = { name: `test-user-${Date.now()}` };
```

---

### F. Legibilidade e Manutenibilidade

- [ ] Imports estão corretos e organizados?
- [ ] Paths relativos são válidos?
- [ ] Não há código comentado sem motivo?
- [ ] Não há `console.log` de debug esquecido?
- [ ] Funções auxiliares têm nomes que descrevem a intenção?

---

### G. Tags e Metadados (se aplicável)

- [ ] Tags de identificação estão presentes (ex: `@TC-001`)?
- [ ] Tags de tipo estão corretas (`@regression`, `@smoke`)?
- [ ] Tags de módulo/repositório estão presentes?
- [ ] Não há tags duplicadas?

---

## 3. Montar o Relatório

Estruture o relatório assim:

```
## Revisão: [nome do arquivo]

### Resumo
- Total de testes: X
- Problemas críticos: X
- Problemas importantes: X
- Sugestões: X
- Nota geral: [Precisa de ajustes / Bom / Excelente]

### Problemas Encontrados

#### 🔴 Crítico
**[Nome do problema]**
Linha X: [descrição do problema]
Impacto: [o que pode acontecer de errado]
Correção:
\```javascript
// antes
...
// depois
...
\```

#### 🟡 Importante
...

#### 🔵 Sugestão
...

### Versão Corrigida
[Arquivo completo com todas as correções aplicadas, se houver problemas críticos ou importantes]
```

---

## Classificação dos Problemas

| Severidade | Quando usar |
|---|---|
| 🔴 Crítico | Falso positivo/negativo, dados sujos, testes dependentes, sem cleanup |
| 🟡 Importante | Asserções fracas, nomes ruins, dados fixos, imports errados |
| 🔵 Sugestão | Organização, comentários, refatoração, boas práticas opcionais |
