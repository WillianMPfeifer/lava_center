---
trigger: always_on
---

## 🧪 Projeto Cypress E2E — Módulo Educação

Este projeto usa Cypress + Cucumber (BDD) com arquitetura desacoplada em camadas. Respeite rigorosamente a estrutura existente.

---

## 🏗️ Arquitetura — Estrutura de Pastas (NÃO ALTERAR)

```
cypress/
├── e2e/              → arquivos .feature (Gherkin em PT-BR)
└── support/
    ├── api/          → chamadas REST (pré-condições e massa de dados)
    ├── commands/     → custom commands Cypress globais
    ├── elements/     → SOMENTE seletores CSS organizados por página
    ├── fixtures/     → massa de dados estática em JSON
    ├── page-objects/ → ações e comportamentos de cada página
    ├── steps/        → tradução Gherkin → Page Object
    └── utils/        → helpers genéricos sem Cypress
```

Nunca crie pastas fora dessa estrutura. Se identificar necessidade, pergunte antes. [RÍGIDO]

---

## 📐 Responsabilidade de cada camada

- elements/: somente seletores CSS. Sem lógica nenhuma. [RÍGIDO]
- page-objects/: somente ações (clicar, digitar, validar). Sem seletores inline — sempre importar de elements/. [RÍGIDO]
- steps/: somente tradução de step Gherkin em chamada de método do Page Object. Sem lógica direta. [RÍGIDO]
- commands/: somente custom commands globais reutilizáveis (cy.loginViaApi, etc). [RÍGIDO]
- api/: somente chamadas REST para autenticação, pré-condições e criação de massa. [RÍGIDO]
- fixtures/: somente dados estáticos em JSON. [RÍGIDO]
- utils/: helpers genéricos sem uso de Cypress (formatadores, geradores). [RÍGIDO]

---

## 📁 Nomenclatura de arquivos

Novos módulos devem seguir o mesmo nome base em todas as camadas: [RÍGIDO]
- lesson-record.feature
- lesson-record-elements.js
- lesson-record.js (page-object)
- lesson-record.js (steps)
- lesson-record-api.js (se necessário)

Formato: kebab-case. Sufixo -elements apenas na camada elements.

---

## 🧩 BDD & Gherkin

- Todos os arquivos .feature escritos em português brasileiro (Feature, Scenario, Given, When, Then, And). [RÍGIDO]
- Linguagem de programação (JS, variáveis, funções) sempre em inglês. [RÍGIDO]
- Cada cenário deve ser atômico e independente — nunca depender do estado de outro cenário. [RÍGIDO]
- Pré-condições criadas via api/ com chamadas REST, não pela UI. [RÍGIDO]
- Para cada feature, sugerir cenários de happy path + ao menos um fluxo negativo relevante. [SUGESTIVO]

---

## 🔍 Seletores

- Seletores CSS sempre centralizados em elements/. Nunca inline no page-object ou steps. [RÍGIDO]
- Preferir CSS selectors. XPath apenas quando não houver alternativa CSS viável. [RÍGIDO]
- Nunca usar cy.wait() com tempo fixo. Usar cy.intercept() com alias ou assertions de visibilidade. [RÍGIDO]

---

## 🔐 Autenticação

- Login sempre via api/auth-api.js + custom command (cy.loginViaApi). [RÍGIDO]
- Nunca automatizar o fluxo de login pela UI em testes que não sejam o próprio teste de login. [RÍGIDO]

---

## 📊 Relatórios

- O projeto usa Mochawesome/Allure. O fluxo completo é: npm test (limpa + executa + gera relatório).
- Ao finalizar uma implementação, lembrar o usuário de rodar npm test para validar os resultados. [SUGESTIVO]

---

## 🚀 Fluxo de implementação de novos módulos

Para qualquer nova feature, seguir esta ordem:
1. Gerar o .feature com cenários Gherkin em PT-BR para revisão
2. Aguardar confirmação antes de gerar o código
3. Gerar em ordem: elements → page-object → steps
4. Se necessário, gerar métodos em api/ para pré-condições
5. Sugerir fixture JSON se houver massa de dados estática

---

## ✅ Boas práticas a seguir sempre

- Evitar cy.wait() estático
- Usar CSS selectors como padrão
- Centralizar seletores (DRY)
- Steps limpos e simples — sem lógica
- Page objects com responsabilidade única
- Cenários independentes e atômicos
- PT-BR para linguagem de negócio (Gherkin)
- Inglês para linguagem de programação (JS)