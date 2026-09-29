---
name: saude-ui-reference
description: Mapeamento técnico detalhado do módulo de Saúde (Acolhimento, Atendimento Clínico, seletores Angular Material, loadings, endpoints e payloads).
---

# 🏥 Referência Técnica: Módulo de Saúde (Acolhimento & Atendimento Clínico)

Este documento centraliza a especificação técnica completa (seletores CSS, estrutura de autocompletes, ciclo de carregamento assíncrono do Angular, endpoints REST e payloads) extraída diretamente do código-fonte do frontend (`c:\Digi\frontend`).

---

## 1. Seletores e Identificadores de UI

### 1.1 Listagem de Atendimentos (`ListaAtendimentoComponent`)
*Arquivo:* `src/app/saude/atendimento/components/abertura-atendimento/lista-atendimento/lista-atendimento.component.html`

- **Abas de Atendimento (`mat-tab-group`):**
  - Container: `mat-tab-group`
  - Aba 0 - Recepção: `div[role="tab"]:nth-child(1)` (ícone `room_service`)
  - Aba 1 - Enfermagem: `div[role="tab"]:nth-child(2)` (ícone `group`)
  - Aba 2 - Atendimento Clínico: `div[role="tab"]:nth-child(3)` (ícone `local_hospital`)
  - Aba 3 - Observação: `div[role="tab"]:nth-child(4)` (ícone `content_paste`)
  - Aba 4 - Medicação: `div[role="tab"]:nth-child(5)` (ícone `healing`)
  - Aba 5 - Finalizados: `div[role="tab"]:nth-child(6)` (ícone `history`)
- **Botões da Barra Superior:**
  - Botão Novo: `button[color="primary"]:has(mat-icon:contains("add"))` ou `button:contains("Novo")`
  - Botão Atualizar Dados: `button:has(mat-icon:contains("cached"))`
- **Tabela e Linhas (`mat-table`):**
  - Tabela: `table[mat-table]`
  - Linha de dados: `tr[mat-row]` ou `tr.linha-tabela`
  - Célula de Nome do Paciente: `td.p-celula-listagem-pacientes p.p-coluna-texto-listagem`
  - Checkbox da linha: `tr[mat-row] mat-checkbox`
- **Ações da Linha (coluna `opcoes`):**
  - **Confirmar Presença (Recepção - Aba 0):** `button:has(mat-icon:contains("check"))`
  - **Chamar Paciente no Painel:** `button:has(mat-icon:contains("notifications_active"))`
  - **Atender Paciente (Acolhimento / Clínico - Abas 1 a 4):**
    - Seletor genérico: `button:has(mat-icon[aria-label="Consultar"])` ou `button[mattooltip="Atender Paciente"]`
    - **Seletor com escopo por paciente (Recomendado):**
      `tr[mat-row]:contains("${nomeDoPaciente}") button:has(mat-icon[aria-label="Consultar"])`
  - **Visualizar Atendimento (Aba 5):** `button:has(mat-icon:contains("remove_red_eye"))`
  - **Transferir Profissional:** `button:has(mat-icon:contains("transfer_within_a_station"))`
  - **Cancelar Atendimento:** `button:has(mat-icon:contains("cancel"))`
- **Filtros e Chips (`spd-filtros-requisicao`):**
  - Container de chips: `spd-filtros-requisicao:not(.p-oculto) mat-chip-list`
  - Chip ativo por nome: `spd-filtros-requisicao:not(.p-oculto) mat-chip.chip-filtro:contains("Paciente")`
  - Popover do filtro aberto: `mat-card.card-filtro`
  - Input de busca no popover: `mat-card.card-filtro input[placeholder="Buscar..."]`
  - Botão Filtrar no popover: `mat-card.card-filtro button:contains("Filtrar")`
  - Botão Limpar no popover: `mat-card.card-filtro button:contains("Limpar")`

---

### 1.2 Componentes de Autocomplete (`spd-autocomplete` e `spd-autocomplete-multiplo`)
*Arquivos:* `autocomplete.component.html` e `autocomplete-multiplo.component.html`

- **Comportamento Assíncrono:**
  - `spd-autocomplete`: Possui `debounceTime(500)` (aguarda 500ms antes de emitir a requisição).
  - `spd-autocomplete-multiplo`: Disparo imediato no `keyup`.
- **Seletores:**
  - Input: `input[name="autocomplete${nomeCampo}"]`
    - Paciente: `input[name="autocompletepaciente"]`
    - Profissional: `input[name="autocompletevinculoProfissional"]`
    - CID-10: `input[name="autocompletecid10"]`
    - CIAP-2: `input[name="autocompleteciap2"]`
    - Especialidade: `input[name="autocompleteespecialidadeAtendida"]`
    - Procedimento: `input[name="autocompleteprocedimento"]`
    - Medicamento: `input[name="autocompletematerialServico"]`
  - Painel Suspenso de Resultados: `.cdk-overlay-pane .mat-autocomplete-panel`
  - Item de resultado: `mat-option.p-option-autocomplete`
  - Texto do resultado: `span.p-conteudo-autocomplete`
  - Chip selecionado: `mat-chip.p-mat-chip` (simples) ou `mat-chip.p-mat-chip-multiplo` (múltiplo)
  - Botão Limpar Seleção: `mat-icon[matChipRemove]`

---

### 1.3 Modal de Abertura de Atendimento (`CadastroAberturaAtendimentoComponent`)
*Arquivo:* `cadastro-abertura-atendimento.component.html`

- **Container:** `mat-dialog-container`
- **Campos:**
  - Paciente: `input[name="autocompletepaciente"]`
  - Tipo de Atenção: `mat-select[name="tipo"]` (`'P'` = Atenção Básica, `'E'` = Especializada)
  - Tipo de Atendimento: `mat-select[name="tipoAtendimento"]` (`'A'` = Atendimento, `'P'` = Procedimento)
  - Profissional: `input[name="autocompletevinculoProfissional"]`
  - Especialidade: `input[name="autocompleteespecialidadeAtendida"]`
  - Fila de Atendimento: `input[name="autocompletefilaAtendimentoClinico"]`
  - Motivo: `input[name="autocompletemotivoAtendimento"]`
  - Via de Chegada: `input[name="autocompleteviaChegada"]`
  - Observações: `textarea#observacoes[name="observacoes"]`
- **Botões de Ação:**
  - Salvar (Recepção - status `AC`): `mat-dialog-container button[type="submit"]:contains("Salvar")`
  - Salvar e Confirmar (Enfermagem `AG` ou Clínico `AL`): `mat-dialog-container button[type="button"]:contains("Salvar e Confirmar")`
  - Fechar: `mat-dialog-container button[type="button"]:contains("Fechar")`

---

### 1.4 Central de Atendimento Clínico / Acolhimento (`CentralAtendimentoClinicoComponent`)
*Arquivo:* `central-atendimento-clinico.component.html`

- **Menu Lateral de Navegação entre Abas:**
  - Dados Iniciais: `a.botao_menu_lateral:contains("Dados Iniciais")`
  - Acolhimento: `a.botao_menu_lateral:contains("Acolhimento")`
  - Sinais Vitais: `a.botao_menu_lateral:contains("Sinal Vital")`
  - Antropometria: `a.botao_menu_lateral:contains("Antropometria")`
  - SOAP: `a.botao_menu_lateral:contains("SOAP")`
  - Anamnese: `a.botao_menu_lateral:contains("Anamnese")`
  - Físico (Exame Físico): `a.botao_menu_lateral:contains("Físico")`
  - Solicitação de Exame: `a.botao_menu_lateral:contains("Solicitação Exame")`
  - Avaliação de Exame: `a.botao_menu_lateral:contains("Avaliação de Exame")`
  - Prescrições: `a.botao_menu_lateral:contains("Prescrições")`
  - Atestado: `a.botao_menu_lateral:contains("Atestado")`
  - Encaminhamento: `a.botao_menu_lateral:contains("Encaminhamento")`
  - Evolução: `a.botao_menu_lateral:contains("Evolução")`
  - Lançamento de Produção: `a.botao_menu_lateral:contains("Lançamento de Produção")`
- **Botões do Cabeçalho Superior:**
  - Voltar: `button:contains("Voltar")`
  - Finalizar Acolhimento: `button:contains("Finalizar Acolhimento")` (visível em status `EM` ou `AG`)
  - Encaminhar para Observação: `button:contains("Encaminhar para Observação")`
  - Encaminhar para Medicação: `button:contains("Encaminhar para Medicação")`
  - Encerrar Atendimento: `button.cor-menu-lateral:contains("Encerrar Atendimento")`

---

### 1.5 Mapeamento Detalhado por Subtela / Aba

#### A. Acolhimento (`CadastroAcolhimentoComponent`)
- Motivo: `textarea#motivoAtendimento[name="motivoAtendimento"]`
- Classificação de Risco: `mat-select[name="classificacaoRisco"]`
- Sinais vitais e antropometria são componentes embutidos.

#### B. Sinais Vitais (`CadastroSinalVitalComponent`)
- Temperatura: `input#temperatura[name="temperatura"]`
- Pressão Sistólica: `input#pressaoSistolica[name="pressaoSistolica"]`
- Pressão Diastólica: `input#pressaoDiastolica[name="pressaoDiastolica"]`
- FR (Frequência Respiratória): `input#fr[name="fr"]`
- FC (Frequência Cardíaca): `input#fc[name="fc"]`
- Glicemia Capilar: `input#glicemiaCapilar[name="glicemiaCapilar"]`
- Coleta: `mat-select[name="flagColeta"]` (`true` / `false`)
- SatO2: `input#satO2[name="satO2"]`
- SatCO2: `input#satCo2[name="satCo2"]`
- Pulso: `input#pulso[name="pulso"]`
- Arrítmico: `mat-select[name="flagArritmico"]` (`true` / `false`)
- Botão Novo: `button:contains("Novo")`

#### C. Antropometria (`CadastroAntropometriaComponent`)
- Classificação de Risco: `mat-select[name="classificacaoRisco"]` (Valores: `'A'`, `'B'`, `'C'`, `'D'`, `'E'`, `'F'`)
- Peso (kg): `input#peso[name="peso"]`
- Altura (cm): `input#altura[name="altura"]`
- IMC: `input#imc[name="imc"]` (calculado automaticamente)
- Quadril: `input#quadril[name="quadril"]`
- Cintura: `input#cintura[name="cintura"]`
- Vacina em Dia: `mat-select[name="flagVacinaEmDia"]`
- Botão Novo: `button:contains("Novo")`

#### D. SOAP (`CadastroSoapComponent`)
- CID-10 (Múltiplo): `input[name="autocompletecid10"]`
- CIAP-2 (Múltiplo): `input[name="autocompleteciap2"]`
- Subjetivo: `textarea#subjetivo[name="subjetivo"]`
- Objetivo: `textarea#objetivo[name="objetivo"]`
- Avaliação: `textarea#avaliacao[name="avaliacao"]`
- Plano: `textarea#plano[name="plano"]`
- Diagnóstico: `textarea#diagnostico[name="diagnostico"]`
- Botão Novo: `button:contains("Novo")`

#### E. Anamnese (`CadastroAnamneseComponent`)
- Queixa Principal: `textarea#queixaPrincipal[name="queixaPrincipal"]`
- Observação: `textarea#observacao[name="observacao"]`
- Sintomatologia: `textarea#sintomatologia[name="sintomatologia"]`
- Época de Início: `textarea#epocaInicio[name="epocaInicio"]`
- Evolução: `textarea#evolucao[name="evolucao"]`
- Viroses: `textarea#viroses[name="viroses"]`
- Histórico: `textarea#historico[name="historico"]`
- Onde Dói: `textarea#doi[name="doi"]`
- Quando Começou: `textarea#comecou[name="comecou"]`
- Como Começou: `textarea#como[name="como"]`
- Como Evolui: `textarea#comoEvolui[name="comoEvolui"]`
- Tipo de Dor: `textarea#tipoDor[name="tipoDor"]`
- Qual Duração: `textarea#qualDuracao[name="qualDuracao"]`
- Dor que se Espalha: `textarea#dorQueSeEspalha[name="dorQueSeEspalha"]`

#### F. Exame Físico (`CadastroExameFisicoComponent`)
- Percussão: `input[name="autocompletepercussao"]`
- Ausculta: `textarea#ausculta[name="ausculta"]`
- Dismorfias: `textarea#dismorfias[name="dismorfias"]`
- Distúrbios: `textarea#disturbios[name="disturbios"]`
- Lesão Cutânea: `textarea#lesaoCutanea[name="lesaoCutanea"]`
- Cateter: `textarea#cateter[name="cateter"]`
- Modelo Estrutural: `textarea#modeloEstrutural[name="modeloEstrutural"]`
- Espessura: `textarea#espessura[name="espessura"]`
- Consistência: `textarea#consistencia[name="consistencia"]`
- Volume: `textarea#volume[name="volume"]`
- Dureza: `textarea#dureza[name="dureza"]`

#### G. Prescrições / Receita (`CadastroReceitaComponent`)
- Descritivo da Receita: `textarea#descritivo[name="descritivo"]`
- Botão Incluir Medicamento: `button:contains("Incluir Medicamento/Materiais")`
- Modal de Medicamento (`CadastroReceitaMaterialComponent`):
  - Tipo: `mat-select[name="tipo"]` (`'M'` Material, `'R'` Rename, `'E'` Específico)
  - Medicamento / Material: `input[name="autocompletematerialServico"]`
  - Quantidade: `input[name="quantidade"]`
  - Unidade Temporal: `mat-select[name="unidadeTemporal"]`
  - Uso Contínuo: `mat-select[name="flagUsoContinuo"]`
  - Salvar Medicamento: `mat-dialog-container button[type="submit"]:contains("Salvar")`

#### H. Atestado (`CadastroAtestadoComponent`)
- Tipo de Atestado: `mat-select[name="tipoAtestado"]`
  - Comparecimento: `'CO'`
  - Clínico: `'CL'`
  - Sanidade: `'SA'`
  - Em Branco: `'BR'`
- Dias Afastados: `input#diasAfastados[name="diasAfastados"]`
- Horas Afastadas: `input#horasAfastadas[name="horasAfastadas"]`
- CID-10: `input[name="autocompletecid10"]`
- Condição do Paciente: `mat-select[name="condicaoPaciente"]`
- Aptidão do Paciente: `mat-select[name="aptidaoPaciente"]`
- Está Apto: `textarea#estaApto[name="estaApto"]`
- Observação: `textarea#observacao[name="observacao"]`
- Botão Novo: `button:contains("Novo")`

#### I. Encaminhamento (`CadastroEncaminhamentoAtendimentoComponent`)
- Local: `input[name="local"]`
- Situação do Paciente: `mat-select[name="situacaoPaciente"]`
- CID-10: `input[name="autocompletecid10"]`
- Classificação de Risco: `mat-select[name="classificacaoRiscoEncaminhamento"]`
- Classificação de Prioridade: `mat-select[name="classificacaoPrioridade"]`
- Transporte: `mat-select[name="transporteEncaminhamento"]`
- Motivo: `input[name="motivoEncaminhamento"]`
- Observação: `textarea#observacao[name="observacao"]`
- Botão Novo: `button:contains("Novo")`

#### J. Avaliação de Exame (`CadastroResultadoExameComponent`)
- Procedimento / Material: `input[name="autocompletematerialServico"]`
- Profissional: `input[name="autocompleteprofissional"]`
- Laboratório: `input[name="autocompletelaboratorio"]`
- Avaliação: `textarea#avaliacao[name="avaliacao"]`
- Botão Novo: `button:contains("Novo")`

#### K. Solicitação de Exame (`CadastroSolicitacaoExameComponent`)
- Procedimento: `input[name="autocompleteprocedimento"]`
- Procedimento Específico: `input[name="autocompleteprocedimentoEpecifico"]`
- Classificação de Prioridade: `mat-select[name="classificacaoPrioridade"]`
- Observação: `textarea#observacao[name="observacao"]`
- Botão Novo: `button:contains("Novo")`

#### L. Evolução (`CadastroEvolucaoComponent`)
- Visibilidade: `mat-select[name="visibilidade"]`
- Observação: `textarea#observacao[name="observacao"]`
- Botão Novo: `button:contains("Novo")`

#### M. Lançamento de Produção (`CadastroFichaProcedimentoComponent`)
- Quantidade Aferições Pressão: `input[name="numeroPressao"]`
- Quantidade Aferições Glicemia: `input[name="numeroGlicemia"]`
- Quantidade Aferições Temperatura: `input[name="numeroTemperatura"]`
- Quantidade Aferições Altura: `input[name="numeroAltura"]`

---

## 2. Loadings e Ciclo Assíncrono

1. **Overlay Global (`spd-carregando`):**
   - Removido do DOM via `*ngIf`.
   - Asserção: `cy.get('spd-carregando', { timeout: 20000 }).should('not.exist')`
2. **Barra de Progresso (`mat-progress-bar`):**
   - Permanece no DOM com `[style.display]="processando ? 'block' : 'none'"`.
   - Asserção: `cy.get('mat-progress-bar', { timeout: 20000 }).should('not.be.visible')`
3. **Salvamento Automático:**
   - Interval de 2000ms.
   - Status: `p:contains("Enviando Informações..")` e `p:contains("Última vez em")`.

---

## 3. APIs e Endpoints Oficiais (`saudeEndpoints`)

| Funcionalidade | Método | Endpoint Backend |
| :--- | :---: | :--- |
| **Listagem de Atendimentos** | `GET` | `**/saude/atendimentos-clinicos**` |
| **Abertura de Atendimento** | `POST` | `**/saude/atendimentos-clinicos**` |
| **Atualização de Status** | `POST` | `**/saude/atendimentos-status**` |
| **Acolhimento** | `POST` | `**/saude/acolhimentos**` |
| **Sinais Vitais** | `POST` | `**/saude/sinais-vitais**` |
| **Antropometria** | `POST` | `**/saude/antropometrias**` |
| **SOAP** | `POST` | `**/saude/soaps**` |
| **Anamnese** | `POST` | `**/saude/anamneses**` |
| **Exame Físico** | `POST` | `**/saude/exames-fisicos**` |
| **Prescrição (Receita)** | `POST` | `**/saude/receitas**` |
| **Medicamento da Receita** | `POST` | `**/saude/receitas-materiais**` |
| **Atestado** | `POST` | `**/saude/atestados**` |
| **Encaminhamento** | `POST` | `**/saude/encaminhamentos-atendimentos**` |
| **Solicitação de Exame** | `POST` | `**/saude/solicitacoes-exames**` |
| **Avaliação de Exame** | `POST` | `**/saude/resultados-exames**` |
| **Evolução** | `POST` | `**/saude/evolucoes**` |
| **Ficha de Procedimento** | `POST` | `**/saude/fichas-procedimentos**` |
| **Desfecho / Encerramento** | `POST` | `**/saude/desfechos-atendimentos**` |
| **Autocomplete Pacientes** | `GET` | `**/saude/pacientes-autocomplete**` |
| **Autocomplete Profissionais** | `GET` | `**/saude/vinculos-profissionais**` |
| **Autocomplete CID-10** | `GET` | `**/saude/cids10**` |
| **Autocomplete CIAP-2** | `GET` | `**/saude/ciaps2**` |
| **Autocomplete Medicamentos** | `GET` | `**/saude/materiais-servico-autocomplete**` |

---

## 4. Feedbacks e Notificações

- Container: `.cdk-overlay-pane mat-snack-bar-container`
- Mensagens de sucesso:
  - Salvar formulários: `"Dados salvos com sucesso"`
  - Confirmar presença: `"Atendimento confirmado com sucesso"`
  - Excluir registro: `"Registro excluído com sucesso"`
