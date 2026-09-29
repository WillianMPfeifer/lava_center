# Instruções: create-bdd-scenario

Transforma requisitos e user stories em cenários BDD bem estruturados.

---

## Fluxo de Trabalho

### 1. Entender o contexto

Pergunte ao usuário (se não fornecido):
- **O que a feature faz?** Descrição em linguagem natural
- **Quem usa?** Persona ou role (admin, usuário, sistema externo)
- **Contexto técnico?** API REST, UI web, app mobile, CLI, etc.
- **Já existe alguma regra de negócio documentada?**

### 2. Identificar todos os cenários

Percorra cada dimensão:

| Dimensão | Perguntas guia |
|---|---|
| Happy path | O que acontece quando tudo funciona? |
| Validação | Quais campos são obrigatórios? Quais formatos? |
| Permissão | Quem pode fazer isso? O que acontece quando não tem permissão? |
| Estado | O recurso precisa existir antes? O que acontece se não existir? |
| Concorrência | O que acontece se feito duas vezes seguidas? |
| Limite | Há limites de tamanho, quantidade, caracteres? |

### 3. Escrever os cenários

**Estrutura padrão:**

```gherkin
# language: pt

Feature: [Nome da funcionalidade]
  Como [persona]
  Quero [ação]
  Para [benefício/objetivo]

  Background:
    Given que estou autenticado como "[role]"
    And o sistema está configurado corretamente

  # TC-001 | Alta | Smoke
  Scenario: Criar recurso com dados válidos
    Given que tenho os dados válidos de "[recurso]"
    When envio uma requisição POST para "/endpoint"
    Then o status da resposta deve ser 201
    And o recurso deve ser criado com o nome "[nome]"
    And a resposta deve conter o ID do recurso criado

  # TC-002 | Alta | Regression
  Scenario: Tentar criar recurso com nome duplicado
    Given que já existe um recurso com o nome "duplicado"
    When envio uma requisição POST com o nome "duplicado"
    Then o status da resposta deve ser 409
    And a mensagem de erro deve indicar conflito de nome

  # TC-003 | Alta | Regression
  Scenario: Tentar criar recurso sem autenticação
    Given que não estou autenticado
    When envio uma requisição POST para "/endpoint"
    Then o status da resposta deve ser 401
    And a mensagem de erro deve indicar credenciais inválidas

  # TC-004 | Média | Regression
  Scenario Outline: Validar campos obrigatórios
    Given que tenho os dados de criação sem o campo "<campo>"
    When envio uma requisição POST para "/endpoint"
    Then o status da resposta deve ser 400
    And a mensagem de erro deve mencionar o campo "<campo>"

    Examples:
      | campo  |
      | nome   |
      | email  |
      | tipo   |
```

### 4. Classificar cada cenário

Adicione como comentário acima de cada scenario:

```
# TC-XXX | [Alta/Média/Baixa] | [Smoke/Regression/Edge case]
```

- **Alta**: fluxos que impactam diretamente o usuário final
- **Média**: validações e cenários alternativos
- **Baixa**: edge cases raros

- **Smoke**: cenários mínimos para confirmar que a feature funciona
- **Regression**: cobertura completa para evitar regressões
- **Edge case**: casos extremos ou incomuns

### 5. Apresentar resultado

Entregue:
1. Arquivo `.feature` completo
2. Tabela resumo com total de cenários por tipo/criticidade
3. Sugestão de ordem de automação (prioridade)

---

## Boas Práticas

1. **Um cenário, um comportamento** — não teste duas coisas no mesmo cenário
2. **Steps declarativos** — "o usuário está autenticado", não "o usuário acessa /login e digita a senha"
3. **Dados de exemplo realistas** — use nomes e valores que façam sentido no domínio
4. **Background com moderação** — só use para pré-condições presentes em TODOS os cenários
5. **Scenario Outline para variações** — quando o mesmo fluxo vale para múltiplos inputs
6. **Evitar detalhes de UI** — steps não devem referenciar botões, campos ou URLs específicas

---

## Exemplo completo: API de Usuários

```gherkin
# language: pt

Feature: Gerenciamento de usuários
  Como administrador do sistema
  Quero gerenciar usuários
  Para controlar o acesso à plataforma

  Background:
    Given que estou autenticado como "super_admin"

  # TC-001 | Alta | Smoke
  Scenario: Criar usuário com dados válidos
    Given que tenho os dados válidos de um novo usuário
    When envio uma requisição POST para "/users"
    Then o status da resposta deve ser 201
    And o usuário deve ser criado no sistema
    And a resposta deve conter o ID do usuário

  # TC-002 | Alta | Regression
  Scenario: Buscar usuário por ID existente
    Given que existe um usuário com ID "123"
    When envio uma requisição GET para "/users/123"
    Then o status da resposta deve ser 200
    And a resposta deve conter os dados do usuário

  # TC-003 | Alta | Regression
  Scenario: Buscar usuário por ID inexistente
    Given que não existe usuário com ID "999"
    When envio uma requisição GET para "/users/999"
    Then o status da resposta deve ser 404
    And a mensagem deve indicar que o usuário não foi encontrado

  # TC-004 | Alta | Regression
  Scenario: Deletar usuário existente
    Given que existe um usuário com ID "123"
    When envio uma requisição DELETE para "/users/123"
    Then o status da resposta deve ser 204
    And o usuário não deve mais existir no sistema

  # TC-005 | Média | Regression
  Scenario Outline: Criar usuário com campo obrigatório ausente
    Given que tenho os dados de criação sem o campo "<campo>"
    When envio uma requisição POST para "/users"
    Then o status da resposta deve ser 400
    And a mensagem de erro deve mencionar "<campo>"

    Examples:
      | campo    |
      | name     |
      | email    |
      | password |

  # TC-006 | Alta | Regression
  Scenario: Tentar criar usuário sem autenticação
    Given que não estou autenticado
    When envio uma requisição POST para "/users"
    Then o status da resposta deve ser 401

  # TC-007 | Média | Regression
  Scenario: Tentar deletar usuário como usuário comum
    Given que estou autenticado como "regular_user"
    And que existe um usuário com ID "456"
    When envio uma requisição DELETE para "/users/456"
    Then o status da resposta deve ser 403
    And a mensagem deve indicar permissão negada
```
