# Instruções: map-coverage

Mapeia gaps entre o que existe na aplicação e o que está coberto por testes.

---

## Fluxo de Trabalho

### 1. Entender o projeto

Pergunte se não fornecido:
- **Tipo de projeto?** API REST / UI Web / Mobile / Full-stack
- **Onde ficam os endpoints ou rotas?** Caminho do diretório da aplicação
- **Onde ficam os testes?** Caminho do diretório de testes
- **Framework de testes?** Playwright, Jest, Cypress, etc.

### 2. Mapear a aplicação

#### Para projetos de API REST

Use comandos para extrair rotas e métodos:

```bash
# Buscar definições de rotas em Express/Node
grep -r "router\.\(get\|post\|put\|delete\|patch\)" src/ --include="*.js" -h | sort

# Buscar decorators de rotas (NestJS, Spring-style)
grep -r "@\(Get\|Post\|Put\|Delete\|Patch\)" src/ --include="*.ts" -h | sort

# Buscar rotas em arquivos de configuração
grep -r "path:" src/ --include="*.yaml" --include="*.json" | grep -v node_modules
```

Organize o resultado em uma tabela:

| Método | Endpoint | Arquivo | Mapeado? |
|---|---|---|---|
| GET | /users | src/routes/users.js | ☐ |
| POST | /users | src/routes/users.js | ☐ |
| GET | /users/:id | src/routes/users.js | ☐ |

#### Para projetos de UI

```bash
# Buscar rotas de página (React Router, Next.js, etc.)
grep -r "path=\|Route\|<Link" src/ --include="*.jsx" --include="*.tsx" -h

# Buscar páginas em Next.js
find src/pages -name "*.tsx" -o -name "*.jsx" | sort

# Buscar componentes principais
find src/components -name "*.tsx" -o -name "*.jsx" | sort
```

### 3. Mapear os testes existentes

```bash
# Listar todos os arquivos de teste
find tests/ -name "*.spec.*" -o -name "*.test.*" | sort

# Extrair o que está sendo testado em cada arquivo
grep -r "describe\|test(" tests/ --include="*.js" --include="*.ts" -h | grep -v "//\|^\s*//"

# Para Playwright — listar tags por arquivo
grep -r "@" tests/ --include="*.spec.js" -h | grep "test(" | sort
```

Organize em uma tabela:

| Arquivo de Teste | Endpoint/Feature Testada | Cenários |
|---|---|---|
| tests/users/get-user.spec.js | GET /users/:id | 200, 404, 401 |
| tests/users/create-user.spec.js | POST /users | 201, 400 |

### 4. Cruzar e identificar gaps

Compare as duas tabelas e classifique cada endpoint/feature:

| Status | Critério |
|---|---|
| ✅ Coberto | Tem testes para happy path E principais negativos |
| ⚠️ Parcial | Tem algum teste mas falta happy path OU negativos |
| ❌ Sem cobertura | Nenhum arquivo de teste encontrado |

**Gaps importantes a identificar:**
- Endpoints de escrita (POST, PUT, DELETE) sem testes
- Endpoints que retornam apenas 200, sem testar erros
- Features críticas (autenticação, pagamento, permissões) com cobertura parcial

### 5. Priorizar

Sugira ordem de automação baseada em:

1. **Alta prioridade**: endpoints críticos sem nenhuma cobertura (autenticação, dados sensíveis, operações destrutivas)
2. **Média prioridade**: endpoints com cobertura parcial (faltam cenários negativos)
3. **Baixa prioridade**: features auxiliares sem cobertura
4. **Opcional**: endpoints de leitura com dados não-críticos

### 6. Apresentar o relatório

```markdown
## Relatório de Cobertura — [nome do projeto]
**Data:** [data]

### Resumo

| Status | Quantidade | Percentual |
|---|---|---|
| ✅ Coberto | X | X% |
| ⚠️ Parcial | X | X% |
| ❌ Sem cobertura | X | X% |
| **Total** | **X** | **100%** |

---

### ❌ Sem Cobertura (prioridade alta)

| Endpoint/Feature | Método | Por que é crítico |
|---|---|---|
| /auth/login | POST | Fluxo de autenticação principal |
| /users/:id | DELETE | Operação destrutiva sem proteção testada |

---

### ⚠️ Cobertura Parcial

| Endpoint/Feature | O que tem | O que falta |
|---|---|---|
| GET /users/:id | Cenário 200 | Falta 404, 401 |
| POST /products | Cenário 201, 400 | Falta 409 (duplicado) |

---

### ✅ Bem Coberto

| Endpoint/Feature | Cenários testados |
|---|---|
| GET /users | 200, 401, filtros |
| POST /users | 201, 400, 409, 401 |

---

### Recomendações

**Próximos 3 testes a criar (maior impacto):**
1. `POST /auth/login` — fluxo principal sem nenhuma cobertura
2. `DELETE /users/:id` — operação crítica sem proteção testada
3. `GET /users/:id` — existe mas falta cenários negativos

**Comando para criar o próximo teste:**
[instrução específica para o framework do projeto]
```

---

## Dicas por Tipo de Projeto

### API REST com Playwright
```bash
# Contar spec files por diretório
find tests/ -name "*.spec.js" | xargs dirname | sort | uniq -c | sort -rn

# Ver quais status codes estão sendo testados
grep -r "toBe(" tests/ --include="*.spec.js" -h | grep -oP "\d{3}" | sort | uniq -c | sort -rn
```

### Frontend com Jest/RTL
```bash
# Buscar componentes sem arquivo de teste par
find src/components -name "*.tsx" | while read f; do
  test_file="${f%.tsx}.test.tsx"
  [ ! -f "$test_file" ] && echo "SEM TESTE: $f"
done
```

### Cypress E2E
```bash
# Listar specs por feature
find cypress/e2e -name "*.cy.js" | sort

# Ver páginas visitadas nos testes
grep -r "cy.visit" cypress/ -h | grep -oP '(?<=visit\()[^)]+' | sort | uniq
```
