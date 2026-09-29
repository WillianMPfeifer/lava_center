---
name: fix-flaky-test
description: Identifica e corrige a causa de testes instáveis (flaky tests) que passam às vezes e falham outras vezes. Use quando um teste não tem comportamento consistente, falha de forma intermitente, ou apresenta resultados diferentes a cada execução.
---

# Skill: fix-flaky-test

Você está executando a skill **fix-flaky-test** que diagnostica e estabiliza testes com comportamento intermitente.

## O que fazer

1. **Coletar informações** (se não fornecidas pelo usuário):
   - Caminho do arquivo de teste
   - Output de uma execução que falhou (se disponível)
   - Com que frequência falha (sempre, às vezes, raramente)?
   - Em que ambiente falha (CI, local, ambos)?

2. **Ler o arquivo de teste** completo

3. **Identificar padrões de flakiness** consultando as categorias em **instructions.md**

4. **Analisar a causa raiz**:
   - Verificar dependências de tempo (timeouts, `Date.now()`, delays)
   - Verificar dependências de estado externo
   - Verificar isolamento entre testes
   - Verificar condições de corrida

5. **Aplicar correções** de estabilização

6. **Executar múltiplas vezes** para confirmar estabilidade (mínimo 5 execuções)

7. **Reportar** causa identificada e correções aplicadas

## Consulte

- **instructions.md**: Padrões de flakiness e técnicas de estabilização
