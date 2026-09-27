# Documentation

Reference material for the humans using this repository. The skills themselves do not
read these files — they read their own `references/` directories at the stages the
controller specifies. Nothing here changes the behavior of a run.

| Document | Read it when |
|---|---|
| [`schema.md`](schema.md) | You need the normative Idea Dossier format: sections, lifecycle values, entry modes, ID namespaces, claim typing, evidence levels `E0`–`E5`, gates `G0`–`G11`, and the gate-result-to-decision routing table. Every rule cites the file and line it comes from, and gaps in the template are recorded as gaps rather than invented. |
| [`architecture.md`](architecture.md) | You want to see how a run flows: the twelve stages and four phases, what the skill reads at startup versus per stage, the two-skill pipeline with the dossier as the interface artifact, and a measured context-budget table. |
| [`faq.md`](faq.md) | You are deciding whether this is for you, wondering why the output is so heavy, or asking what it explicitly does not do. |
| [`contributing-a-pattern-card.md`](contributing-a-pattern-card.md) | You want to add a structural pattern card or change the routing rules. Includes the card anatomy, eligibility rules, and the required eval expectation. |
| [`release-checklist.md`](release-checklist.md) | You are preparing a public release, or reviewing the maintainer's disclosure and provenance decisions. Ordered by cost of getting it wrong. |

Related, outside this directory:

- [`../PERSONALIZE.md`](../PERSONALIZE.md) — replacing the six `personal-*.md` slots.
- [`../profiles/README.md`](../profiles/README.md) — what a profile is and how to contribute one.
- [`../evals/README.md`](../evals/README.md) — running Tier 1 and Tier 2, and what structural grading cannot tell you.
- [`../evals/results/README.md`](../evals/results/README.md) — how a published Tier-2 pass rate is recorded, and the honest-reporting rules for one.
- [`../CHANGELOG.md`](../CHANGELOG.md) — dossier schema versions and their migration notes, plus the consistency repairs.
- [`../CONTRIBUTING.md`](../CONTRIBUTING.md) — the change rules, including the eval-expectation requirement and the schema freeze.
- [`../skills/time-series-model-ideation/SKILL.md`](../skills/time-series-model-ideation/SKILL.md) — the controller itself, which is the real specification.

## How authoritative is each file?

The ordering matters when two documents disagree:

1. `skills/time-series-model-ideation/assets/idea-dossier-template.md` — the sole
   authority on output structure, fields, enums, and field order.
2. `skills/time-series-model-ideation/SKILL.md` — the stage controller, entry modes,
   phases, router, and gate semantics.
3. `skills/*/references/*.md` — stage protocols, which may only fill the fields the
   template already defines.
4. Everything in this directory — explanation for humans, never a rule.

If you find a contradiction between levels 1–3, that is a bug: `docs/schema.md` has a
*Known inconsistencies* section for exactly this, and a pull request recording one is
welcome even if you do not fix it.
