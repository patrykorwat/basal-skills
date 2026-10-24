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

Engage the **basal** Polish AI community (Discord group) — thread tracking,
content discipline, and outreach workflows (current thread: SejmBench,
`github.com/radoskoppl/sejmbench`).

## Decision-systems landscape (read before writing on the topic)

`references/decision-systems-map.md` — a map of the
decision-systems literature (10 families: social choice, jury theorems,
deliberation × AI, liquid democracy, QV/futarchy, sortition, participatory
budgeting, LLM-as-decision-participant, AI governance, benchmark gaming).
Each family: core question, anchor arXiv IDs (verified via live API), and
what it implies for the thread. The synthesis (§10) holds the testable
hypotheses that double as day-one discussion starters.

## Content discipline (from Radoskop practice, kept everywhere)

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
