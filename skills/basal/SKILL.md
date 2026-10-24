---
name: basal
description: "Use when engaging the basal Polish AI community (Discord)."
version: 1.0.0
author: Radoskop
license: MIT
metadata:
  tags: [community, discord, outreach, poland]
---

# basal

Improve the **basal** community's decision-making process (Discord group) —
run proven decision methods (`references/decision-methods-playbook.md`),
grounded in the research map (`references/decision-systems-map.md`) and the
community's own experience: capture proposals and outcomes in a decision
register, track the current thread (decision systems for parliaments;
SejmBench, `github.com/radoskoppl/sejmbench`, is the measurement layer), and
keep community-facing content disciplined.

## Decision-systems toolkit (read before deciding or writing on the topic)

`references/decision-methods-playbook.md` — **the practical layer**: for each
decision situation (yes/no vote, prioritization, budget, missing expertise,
predictions, polarizing decisions, AI in the loop, process change) — the
method as numbered steps, the receipts (arXiv IDs), and the traps.

`references/decision-systems-map.md` — **the evidence base**: distilled
findings from 34 papers (one concrete finding per paper; every ID verifiable
at `https://arxiv.org/abs/<id>`), 10 families. The synthesis (§10) holds the
testable hypotheses that double as day-one discussion starters; §0a gives
the whole map in 60 seconds. Read the playbook to act, the map for receipts.

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

Keep a running list of the open questions put to the community and their
answers (they steer the roadmap). For SejmBench the current ones:

- vote-type classification (layer 1): who labels — hand gold standard vs rules?
- fixture count for v0.3 (proposal: 50, stratified by margin × type)
- which models to test first: PL-native or large general ones?

## What to learn before deeper engagement (do not guess)

- Channel culture, moderation style, and what post formats land well —
  observe first, then record here; never invent community norms.
