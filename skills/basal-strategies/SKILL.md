---
name: basal-strategies
description: "Use when running or designing a group decision for the basal community (Discord or any channel using basal models): a vote or quorum question, prioritization, budget allocation, delegation, prediction poll, sortition panel, deciding whether an AI may judge a proposal, building or reviewing a decision register, or checking whether a model should be asked at all. Trigger on głosowanie, kworum, rejestr decyzji, ocena propozycji przez AI, decyzja społeczności, sortition, QV, Equal Shares, delegacja."
version: 1.1.0
author: Radoskop
license: MIT
metadata:
  tags: [community, discord, decisions, poland]
---

# basal-strategies

Decide **what to decide how** — and, when basal models are involved, whether
to ask them at all. For the technical side (how to ask, which model,
thresholds) use the companion skill `basal-serve`; this skill owns the
decision situations, their conditions, and the vocabulary. Status: methods
are grounded in the literature map, but none has yet run in a real basal
thread — treat the applicability numbers as untested until one does.

## Hard rules (apply in every situation, before the playbook)

1. **Code runs the voting rule, never the model.** Tallying, quorum,
   aggregation: a script computes. A model that is asked to aggregate
   miscomputes as the group grows.
2. **The AI judges independently, before human votes are visible to it.**
   Enforce technically: the request `state` must not contain human votes or
   discussion that reveals them (`basal-serve` states this as a request rule).
3. **An AI verdict is never decisive.** Agreement of AI majority and human
   majority shortens the process; disagreement always goes to a named human
   tie-breaker who did not vote in the first round. Treating an AI verdict
   as decisive is the main failure mode this skill guards against.
4. **Checkable questions only for automation.** Where a correct answer is
   verifiable (compliance with a rule, a category, a claim against a source),
   a calibrated result may gate automation. On value questions there is no
   labeled ground truth, so no threshold is empirical: the model's number is
   advisory, starts no action, and is never reported as accuracy.
5. **Community-facing content is published only after explicit owner
   approval** of the exact text.

## Decision-systems toolkit (read before deciding or writing on the topic)

`references/decision-methods-playbook.md` — **the practical layer**: for each
decision situation — the method as numbered steps, the conditions under
which it holds (minimum participants, data, infrastructure), the receipts
(arXiv IDs), and the traps.

`references/decision-systems-map.md` — **the evidence base**: distilled
findings from 34 papers (one concrete finding per paper; every ID verifiable
at `https://arxiv.org/abs/<id>`), 10 families. The synthesis holds the
testable hypotheses that double as day-one discussion starters; the 60-second
section gives the whole map. Findings mix RCTs, simulations, surveys and
position papers — read the evidence type before transferring anything to a
small Discord.

## From situation to basal request (bridge)

| Situation | Ask basal? | Question type | Gate for acting automatically |
|---|---|---|---|
| yes/no, compliance-checkable | yes | `noul` | threshold certified by `basal-calibrate` on labeled examples; else human |
| classify proposal to register category | yes | `choice` (codebook labels) | same gate; `unclear` label must exist |
| check a claim in a draft post | yes | `verify` (task) | `supported` required; anything else blocks |
| prioritize / budget / delegation / panel | no | — | code or people per the playbook; the model may only draft options |
| value question, no ground truth | advisory only | `noul`/`choice` | never act on it; report as opinion |

The category labels come from the codebook version recorded in the decision
register — pass them explicitly in the request; do not hardcode them.

## Content discipline

1. **Never publish community-facing content without explicit owner approval**
   of the exact text — drafts live untracked (gitignored) until approved.
2. Tone: rigorous, zero emotional civic-tech narration. "For what and how",
   never "who blocked".
3. Every number in a post must be reproducible from the linked repo's data
   (fixtures/manifest); nothing fabricated, ever.
4. Post in digestible parts (Discord message limit ~2000 chars); lead with
   the problem, then the artifact, then how to participate; end with open
   questions that invite the community to shape the spec.

## Community-thread tracking

Open questions put to the community and their answers are register entries
(status `proposed`/`decided`, review dates), not lines in this file — keep
them there so this skill does not rot.

## What to learn before deeper engagement (do not guess)

- Channel culture, moderation style, member count, and what post formats
  land well — observe first, then record; never invent community norms.
  Member count gates several methods (see each method's conditions).
