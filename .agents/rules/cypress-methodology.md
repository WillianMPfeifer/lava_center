---
trigger: always_on
---

# 📘 Metodologia de Implementação E2E — Cypress + Cucumber (BDD)

Diretrizes arquiteturais, padrões de código e boas práticas obrigatórias para agentes e desenvolvedores.

---

## 🏛️ 1. Arquitetura em 5 Camadas

```
cypress/
├── e2e/              # Camada 1: BDD Specs (.feature em Gherkin PT-BR)
└── support/
    ├── elements/     # Camada 2: Seletores CSS puros organizados por domínio
    ├── page-objects/ # Camada 3: Ações, fluxos de UI e asserções (POM)
    ├── steps/        # Camada 4: Bindings Gherkin -> Chamadas POM
    ├── api/          # Camada 5: Serviços REST (auth e pré-condições)
    ├── commands/     # Custom Commands Cypress globais
    ├── fixtures/     # Massa de dados estática em JSON
    └── utils/        # Geradores de dados dinâmicos e formatadores puros
```

### 🧭 Responsabilidade e Proibições

| Camada | Pasta | Responsabilidade | O que NUNCA fazer |
| :--- | :--- | :--- | :--- |
| **BDD Features** | `cypress/e2e/` | Especificação de negócio em Gherkin PT-BR. | Não colocar seletores, IDs, tags HTML ou comandos técnicos. |
| **Elements** | `cypress/support/elements/` | Centralizar **exclusivamente** seletores CSS como strings/funções. | **PROIBIDO** comandos Cypress (`cy.get`, `cy.click`) ou lógica. |
| **Page Objects** | `cypress/support/page-objects/` | Ações de UI, cliques, preenchimentos e asserções. | **PROIBIDO** seletores inline sem centralização em `elements/`. |
| **Steps** | `cypress/support/steps/` | Tradução de step Gherkin para método no Page Object. | **PROIBIDO** seletores inline, comandos `cy.get` ou lógica complexa. |
| **API** | `cypress/support/api/` | Chamadas HTTP REST (`cy.request`) para auth e dados. | Não fazer asserções de UI. |
| **Commands** | `cypress/support/commands/` | Comandos reutilizáveis (`cy.loginViaApi`, etc.). | Não criar commands específicos de uma única tela. |
| **Utils** | `cypress/support/utils/` | Funções puras JS (CPF, CNPJ, CNS, Faker). | Não acoplar comandos Cypress dentro de utilitários puros. |

---

## 🏷️ 2. Convenções de Nomenclatura e Idioma

### 2.1 Idioma [RÍGIDO]
- **Código Técnico (JS, classes, métodos, seletores, arquivos):** Sempre em **Inglês**.
- **Linguagem de Negócio (Features, Gherkin, cenários, passos):** Sempre em **Português Brasileiro (PT-BR)**.
- **Documentação e Respostas ao Usuário:** Sempre em **Português Brasileiro (PT-BR)**.

### 2.2 Nomenclatura de Arquivos (`kebab-case`)
- Feature: `cypress/e2e/student/criar-aluno.feature`
- Elements: `cypress/support/elements/student/create-student-elements.js`
- Page Object: `cypress/support/page-objects/student/create-studentPOM.js`
- Steps: `cypress/support/steps/student/create-studentSteps.js`
- API: `cypress/support/api/auth-api.js`

### 2.3 Nomenclatura de Código
- **Classes:** `PascalCase` (ex: `CreateStudentPage`, `CreateStudentElements`, `GlobalPage`).
- **Métodos:** `camelCase` iniciando com verbo de ação:
  - Interação: `insert...`, `fill...`, `select...`, `click...`, `type...`, `handle...`
  - Navegação: `navigateTo...`, `access...`, `to...Tab`
  - Validação: `validate...`, `verify...`, `check...`
- **Constantes Globais:** `UPPER_SNAKE_CASE`.

---

## 🥒 3. BDD & Gherkin (`cypress/e2e/`)

1. Cabeçalho com `# language: pt`.
2. Tag da funcionalidade no topo (ex: `@student`).
3. `Contexto:` com autenticação via API (`Dado que o usuário está autenticado via API`).
4. Tag `@smoke` nos fluxos felizes principais.
5. Uso de DataTables com `rowsHash()`.
6. Tokens dinâmicos:
   - `<dinamico>`: Gera dado válido e único em tempo de execução via `Geradores`.
   - `<vazio>`: Campo não deve ser digitado/preenchido.
7. **Atomicidade & Limpeza:** Cenários 100% independentes com teardown ao final.

```gherkin
# language: pt
@student
Funcionalidade: Criar aluno

    Contexto:
        Dado que o usuário está autenticado via API

    @smoke
    Cenário: Criar um novo aluno com sucesso
        Dado que eu estou na página de criação de alunos
        Quando o usuário clicar em + Novo
        E eu preencho os dados de identificação da Pessoa Física:
            | Nome        | Aluno Teste <dinamico> |
            | CPF         | <dinamico>             |
            | Nascimento  | 2010-05-15             |
            | Sexo        | Masculino              |
        E clico no botão 'Salvar'
        Então eu devo ver uma mensagem de sucesso 'Dados Salvos com sucesso'
        Quando eu filtrar e excluir o aluno recém criado com o nome "Aluno Teste" para limpeza de dados
        Então eu devo ver uma mensagem de sucesso 'Dados Excluídos com sucesso'
```

---

## 🎯 4. Elements (`cypress/support/elements/`)

Apenas seletores CSS. Sem comandos Cypress.

```javascript
class CreateStudentElements {
    nameInput() { return 'mat-form-field input[placeholder="Busque pelo nome"]'; }
    cpfInput() { return 'input[name="cpf"]'; }
    birthDateInput() { return 'spd-data:has(label:contains("Data de Nascimento")) input'; }
    sexTypeSelect() { return 'mat-form-field mat-select[name="sexo"]'; }
    sexTypeOption(sexo) { return `mat-option:contains("${sexo}")`; }
    naturalPersonTab() { return 'div[role="tab"]:contains("Pessoa Física")'; }
    dataTab() { return 'div[role="tab"]:contains("Dados")'; }
}
export default CreateStudentElements;
```

---

## 📄 5. Page Object Model (`cypress/support/page-objects/`)

Centraliza ações, interações e validações de UI. Reutiliza `GlobalPage` e `Geradores`.

```javascript
import CreateStudentElements from "../../elements/student/create-student-elements";
const createStudentElem = new CreateStudentElements();
import GlobalPage from "../globalPOM";
const globalPage = new GlobalPage();
import Geradores from "../../utils/gerator-utils";

class CreateStudentPage {
    insertStudentName(name) {
        const finalName = Geradores.gerarNomeDinamico(name);
        cy.intercept('GET', '**/alunos-autocomplete*').as('autocompleteRequest');
        cy.get(createStudentElem.nameInput()).clear().type(finalName);
        if (finalName.length > 2) {
            cy.wait('@autocompleteRequest', { timeout: 15000 });
        }
        cy.wrap(finalName).as('createdStudentName');
    }

    insertCpf(cpf) {
        if (cpf !== undefined && cpf !== null) {
            const finalCpf = cpf === '<dinamico>' ? Geradores.gerarCpf(true) : cpf;
            cy.get(createStudentElem.cpfInput()).clear().type(finalCpf);
        }
    }

    selectSexType(sex) {
        cy.get(createStudentElem.sexTypeSelect()).should('be.visible').click();
        cy.get(createStudentElem.sexTypeOption(sex)).should('be.visible').first().click();
    }

    clickSaveButton(action) {
        globalPage.saveRegister(action);
    }
}
export default CreateStudentPage;
```

---

## 🔗 6. Steps (`cypress/support/steps/`)

Apenas ponte entre Gherkin e métodos POM. Sem lógica direta ou seletores.

```javascript
import { Given, When, Then } from "@badeball/cypress-cucumber-preprocessor";
import CreateStudentPage from "../../page-objects/student/create-studentPOM";
const createStudent = new CreateStudentPage();
import MovimentStudentPage from "../../page-objects/student/moviment-studentPOM";
const movimentStudent = new MovimentStudentPage();

Given("que eu estou na página de criação de alunos", () => {
    createStudent.navigateToStudentSection("Alunos");
    createStudent.validateStudentTitle("Alunos");
});

When("eu preencho os dados de identificação da Pessoa Física:", (dataTable) => {
    const data = dataTable.rowsHash();
    createStudent.insertStudentName(data.Nome);
    createStudent.insertCpf(data.CPF);
    createStudent.insertBirthDate(data.Nascimento);
    createStudent.selectSexType(data.Sexo);
});

When("eu filtrar e excluir o aluno recém criado com o nome {string} para limpeza de dados", () => {
    cy.get('@createdStudentName').then((nomeExato) => {
        movimentStudent.filterByStudentName('Nome contém', nomeExato);
        movimentStudent.deleteStudent();
    });
});
```

---

## ⏱️ 7. Proibição de Waits Estáticos [RÍGIDO]

- **NUNCA** use `cy.wait(tempo_em_ms)` estático para aguardar carregamentos.
- **Alternativas Obrigatórias:**
  1. **Intercepts de Backend:**
     ```javascript
     cy.intercept('POST', '**/alunos').as('saveStudentReq');
     cy.get(globalElem.saveButton()).click();
     cy.wait('@saveStudentReq', { timeout: 15000 }).its('response.statusCode').should('eq', 200);
     ```
  2. **Ausência de Loading & Visibilidade:**
     ```javascript
     cy.get('mat-progress-spinner', { timeout: 15000 }).should('not.exist');
     cy.get(selector).should('be.visible').and('not.be.disabled').click();
     ```
  3. **Exceções:** `cy.wait(500)` apenas para término de animações CSS do Angular Material quando não há evento de DOM, devendo conter comentário justificativo.

---

## 🔐 8. Autenticação & Sessão

- **Testes de Fluxo:** Usar autenticação via API com `cy.loginViaApi()` + `cy.session()` e injeção de cookies (`userToken`, `refreshToken`).
- **Teste de UI:** Apenas `cypress/e2e/login/login.feature` testa formulário de login visualmente.
- **Credenciais:** Mapeadas em `cypress.env.json` (no `.gitignore`) e `cypress/support/fixtures/users.json`.

---

## 🛠️ 9. Utilitários & Custom Commands

- **`Geradores` (`gerator-utils.js`):** `gerarCpf(comPontuacao)`, `gerarCnpj()`, `gerarCns()`, `gerarNomeDinamico()`, `gerarRg()`, `gerarPisPasep()`, `gerarTituloEleitor()`, `gerarReservista()`.
- **Custom Commands:**
  - `cy.typeIfNotEmpty(text)`: Digita apenas se o valor for preenchido (ignora `<vazio>`).
  - `cy.pressEscape()`: Fecha overlays/dropdowns abertos do Angular Material.
  - Overwrite `cy.type`: Delay padrão de 15ms para estabilidade em CI.

---

## 🔄 10. Fluxo de Implementação de Novas Features

1. **Feature Gherkin (PT-BR):** Criar `.feature` e apresentar para validação do usuário.
2. **Elements:** Mapear seletores CSS puros na pasta `elements/`.
3. **Page Object:** Criar ações, interações e asserções na pasta `page-objects/`.
4. **Steps:** Criar bindings em `steps/` repassando dados ao POM.
5. **API / Fixtures:** Criar pré-condições REST se necessário.

---

## ⚠️ 11. Execução no Terminal [RÍGIDO]

- **NUNCA** execute comandos de teste no terminal (`cypress run`, `npm test`, etc.) de forma automática.
- **SEMPRE** pergunte e aguarde confirmação explícita do usuário antes de executar qualquer comando.
