---
name: review-test
description: Revisa a qualidade de arquivos de teste e aponta problemas. Use quando o usuário quiser revisar, auditar ou melhorar testes existentes, verificar se testes seguem boas práticas, ou obter feedback sobre qualidade de um spec file.
---

# Skill: review-test

Você está executando a skill **review-test** que revisa arquivos de teste e fornece feedback estruturado com problemas e melhorias.

## O que fazer

1. **Coletar o arquivo** (se não fornecido pelo usuário):
   - Caminho do arquivo de teste a ser revisado
   - Contexto: framework usado (Playwright, Jest, Cypress, etc.)

2. **Ler e analisar o arquivo** completamente

3. **Revisar em múltiplas dimensões**:
   - Estrutura e organização
   - Isolamento e independência entre testes
   - Cleanup de dados de teste
   - Asserções e cobertura de comportamento
   - Nomenclatura e legibilidade
   - Boas práticas do framework

4. **Classificar os problemas encontrados**:
   - Crítico: pode causar falsos positivos/negativos ou instabilidade
   - Importante: viola boas práticas significativas
   - Sugestão: melhorias de legibilidade ou manutenibilidade

5. **Apresentar relatório** com problemas encontrados e versão corrigida (se necessário)

## Consulte

- **instructions.md**: Checklist completo de revisão por dimensão
