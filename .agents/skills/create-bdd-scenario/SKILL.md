---
name: create-bdd-scenario
description: Gera cenários BDD (Given/When/Then) a partir de um requisito, user story, ou descrição de funcionalidade. Use quando o usuário quiser criar casos de teste, escrever cenários de teste, transformar requisitos em testes, ou documentar comportamento esperado de uma feature.
---

# Skill: create-bdd-scenario

Você está executando a skill **create-bdd-scenario** que transforma requisitos e user stories em cenários BDD estruturados.

## O que fazer

1. **Coletar informações** (se não fornecidas pelo usuário):
   - Descrição da funcionalidade ou user story
   - Contexto: tipo de sistema (API, UI, mobile, etc.)
   - Persona/role envolvido (admin, usuário comum, etc.)

2. **Analisar e identificar cenários**:
   - Happy path (fluxo principal de sucesso)
   - Fluxos alternativos válidos
   - Cenários negativos (entradas inválidas, permissões, etc.)
   - Edge cases relevantes

3. **Gerar cenários BDD** seguindo o padrão:
   - **Feature**: nome da funcionalidade
   - **Background**: pré-condições comuns (se houver)
   - **Scenario** / **Scenario Outline** com Examples (para variações)
   - Steps: Given / When / Then / And / But

4. **Classificar e priorizar** cada cenário:
   - Criticidade: Alta / Média / Baixa
   - Tipo: Smoke / Regression / Edge case
   - ID sequencial (TC-001, TC-002, etc.)

5. **Apresentar resultado** formatado e pronto para uso

## Regras de qualidade

- Cada cenário testa UMA única coisa
- Steps devem ser declarativos (o QUE, não o COMO)
- Evitar detalhes de implementação nos steps
- Nomes de cenários em português claro e legível
- Cobrir: sucesso, falha de validação, permissão negada, recurso não encontrado

## Consulte

- **instructions.md**: Guia completo de como escrever BDD de qualidade
