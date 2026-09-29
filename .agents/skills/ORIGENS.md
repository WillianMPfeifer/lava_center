# Origens

De onde veio cada skill deste pacote. Serve para atualizar por diff em vez de
reimportar tudo: você compara sua cópia contra a origem e escolhe o que traz.

Última revisão: 2026-08-24

## Processo — envelhece devagar, revisar 1x por ano

Descrevem disciplina de engenharia, não tecnologia. Markdown desatualizado não
quebra, só envelhece.

| Skill | Origem |
|---|---|
| using-superpowers, brainstorming, writing-plans, executing-plans | obra/superpowers |
| subagent-driven-development, dispatching-parallel-agents | obra/superpowers |
| test-driven-development, systematic-debugging | obra/superpowers |
| requesting-code-review, receiving-code-review | obra/superpowers |
| verification-before-completion, finishing-a-development-branch | obra/superpowers |
| using-git-worktrees, writing-skills | obra/superpowers |
| grilling, grill-me, grill-with-docs | mattpocock/skills @ 5b15a47 |
| domain-modeling, codebase-design | mattpocock/skills @ 5b15a47 |
| resolving-merge-conflicts, handoff, to-questionnaire, wait-what | mattpocock/skills @ 5b15a47 |
| frontend-design | Anthropic (skill pública) |
| create-bdd-scenario, fix-flaky-test, map-coverage, review-test | qazando/skills-qas @ 18a3e01 |

## Acopladas a tecnologia externa — revisar a cada 3-4 meses

Dependem de coisas que versionam.

| Skill | Acoplada a |
|---|---|
| ui-styling | shadcn/ui, Tailwind |
| design-system | tokens, Tailwind |
| slides | Chart.js, scripts do design-system |

## Modificações locais

- `grill-me` e `grill-with-docs`: corpo reescrito. O original chamava a "Skill
  tool" do Claude Code, que não existe no Antigravity.
- `wait-what`, `handoff`, `to-questionnaire`: removidos os campos
  `disable-model-invocation` e `argument-hint`, que o Antigravity ignora. O `handoff`
  teve sua instrução tornada agnóstica sem depender da "Skill tool".
- `slides`: caminhos `.claude/skills/` trocados por `.agents/skills/`.
- Removidas as pastas `agents/openai.yaml` das skills do Pocock.

## Removidos de propósito

- `design`, `brand`, `banner-design`: trabalho de identidade visual, feito fora
  da IDE. O `design` também duplicava `slides` e `banner-design` byte a byte.
- `ui-ux-pro-max`: catálogo de 67 estilos com passo obrigatório de gerar o
  design system por busca. É a fórmula que o `frontend-design` existe para
  evitar, e vencia o gatilho dele. Uma pasta, dá para devolver quando quiser.
- `debug-failing-test` (qazando): colide com `systematic-debugging`, que é mais
  rigoroso — proíbe correção antes da causa raiz.
