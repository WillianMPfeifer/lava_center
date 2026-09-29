---
name: map-coverage
description: Mapeia a cobertura de testes de um projeto, identificando endpoints, features ou componentes que não possuem testes. Use quando o usuário quiser saber o que está sem cobertura, identificar gaps de testes, priorizar o que automatizar, ou ter uma visão geral do estado dos testes.
---

# Skill: map-coverage

Você está executando a skill **map-coverage** que varre o projeto e identifica gaps entre o que existe na aplicação e o que está coberto por testes.

## O que fazer

1. **Coletar informações** (se não fornecidas pelo usuário):
   - Diretório da aplicação (onde ficam os endpoints/rotas/componentes)
   - Diretório dos testes
   - Tipo de projeto (API REST, UI, misto)

2. **Mapear o que existe na aplicação**:
   - Listar endpoints (API) ou páginas/componentes (UI)
   - Extrair rotas, métodos HTTP, nomes de features

3. **Mapear o que está coberto por testes**:
   - Listar arquivos de teste existentes
   - Extrair endpoints/features testados de cada arquivo

4. **Cruzar e identificar gaps**:
   - O que está na aplicação mas sem nenhum teste
   - O que tem testes mas cobertura parcial (falta happy path ou negativos)
   - O que está bem coberto

5. **Priorizar e apresentar** o relatório de cobertura com recomendações

## Consulte

- **instructions.md**: Como realizar o mapeamento e estruturar o relatório
