# Basal decision register — template and process

A lightweight register for decisions the basal community makes (process,
tooling, events, standards). The point: basal improves its own decision
process with the same discipline it discusses — capture, decide, review.

## File convention

Keep one register file per year (`decisions-2026.md`), append-only. Never
edit a decided entry; supersede it with a new one.

## Entry template

```
## BASAL-<NNN> — <title>
- date: YYYY-MM-DD
- proposer: <name/handle>
- status: proposed | discussed | decided | superseded (by BASAL-<NNN>)
- options considered: <A; B; C — one line each>
- decision: <what was decided, one sentence>
- consent: <unanimous / majority / quorum note — if decided>
- owner: <who executes>
- review: <YYYY-MM-DD — when to check whether it worked>
- outcome: <filled at review: worked / partial / failed, one line>
- related research: <decision-systems-map.md family, if applicable>
```

## Process rules

1. Anyone can propose; a proposal enters the register with status
   `proposed` — being in the register is not being agreed.
2. Every `decided` entry carries a review date. A decision without a review
   date is not a decision, it is a hope.
3. At review, fill `outcome` honestly; failures stay in the register (they
   are the experience base the process learns from).
4. When a decision touches a mechanism discussed in the literature map
   (voting rule, delegation, sortition…), link the family — the community
   can then check practice against theory.
5. The register is the source for periodic retrospectives (e.g. quarterly):
   what we decided, what worked, what we would decide differently.

## Worked example

```
## BASAL-001 — Weekly thread summary posts
- date: 2026-10-24
- proposer: karmelki90
- status: decided
- options considered: daily digest; weekly digest; no digest
- decision: weekly digest every Monday, compiled from the register + thread.
- consent: unanimous (8 present)
- owner: karmelki90
- review: 2026-11-24 — did digests increase thread participation?
- outcome:
- related research: §2 epistemics (independent aggregation of judgments)
```
