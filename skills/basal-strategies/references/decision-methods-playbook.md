# Decision methods — practical playbook for basal

The actionable layer of `decision-systems-map.md`. For each decision
situation the community actually faces: **the method, how to run it, the
receipts, the traps.** Papers are cited only as receipts — you do not need to
open arXiv to run any of this.

How to use: identify your decision situation below, run the steps as written,
record the outcome in the decision register with a review date. Come back to
the map only when you want the receipts.

## 1. Yes/no group decision (the default case)

Method: **independent vote + hybrid confirmation** (2603.29866, 2108.00733,
2408.00317).

1. State the decision and the options BEFORE any discussion. Members vote
   independently — anonymous, no seeing others' votes first.
2. Get one AI judgment: a model reads the same options and votes
   independently. Do not show it the human votes first.
3. If the human majority and the AI agree → accept, skip the debate.
4. If they disagree → one discussion round, then a named tie-breaker (a
   person who did not vote in round 1) decides.
5. Register the outcome with a review date (+30d default).

Why it works: majority competence is conditional on independence — the
"miracle of aggregation" fails almost surely as a prior (2108.00733), so
independence is a mechanism you run, not a hope you have. Note on low
turnout: in the abstention math, not voting is rational when the vote feels
pivotality-free (2408.00317) — if turnout dies, fix the framing (make the
decision feel mattering), don't guilt people into voting.

Traps: debate improves strong human judges but can degrade weak AI judges
(2610.28539) — never let two weak models argue and call it a verdict.

## 2. Prioritizing many options (roadmap, topics, features)

Method: **quadratic voting, computed by code** (1409.0264, 2308.04345,
2505.05016).

1. List the N options; give every member 100 voice credits.
2. Casting k votes on one option costs k² credits (members only express
   intensity; the script computes costs and sums).
3. Sum per option → ranking. Record it.

Rules: the arithmetic is done by a script, never by a model (zero-shot LLMs
miscompute aggregation as groups grow, 2505.05016). QV's inefficiency decays
like 1/n — it gets better with scale, so for small groups plain approval
voting is fine. The adoption killer is UI friction: keep the poll dead
simple (2308.04345). Concrete for basal: a pinned poll + a tiny script is a
5-minute setup.

## 3. Allocating a budget (community fund, prizes)

Method: **Method of Equal Shares** (2003.00606, 2603.09660, 2012.06539).

1. Split the budget into equal per-member shares.
2. Each member's share goes to the projects they approve; a project is
   funded when its supporters' shares cover its cost; unused shares return.
3. Choose between Equal Shares and Phragmén on usability, not fairness —
   their quantitative proportionality is equivalent (2603.09660).

Concrete: Pabulib (pabulib.org) ships real instances in .pb format and
Polish city data — copy a working setup instead of inventing one
(2012.06539).

## 4. Decisions needing expertise the group lacks

Method: **per-topic, revocable delegation** (2206.13904, 2506.09789,
2309.01090).

1. Default stays direct voting.
2. For a defined domain (e.g. "model licensing"), a member may delegate
   their vote to a named person FOR THAT TOPIC, revocable at any time.
3. Constraints: one delegate per domain, no open transitive chains (cap at
   one hop), public delegate list.

Evidence: the strongest formal critique of liquid democracy has "little or
no relevance" when sensible constraints are in place (2206.13904); LD runs
at production scale in DPoS chains (2309.01090); delegation churn is normal
— design for revocation, not forever-proxies (2506.09789).

## 5. Factual questions with verifiable outcomes ("will X happen?")

Method: **prediction poll with a proper scoring rule** (2103.10011,
2303.10857, 2503.03312).

1. Write a resolvable question: deadline + named source of truth.
2. Members submit probabilities (0–100%), optionally with small stakes or
   reputation points.
3. At resolution, score with a proper scoring rule (log score) and publish
   the scoreboard.
4. Act only on aggregates with enough participants — thin markets are
   manipulable and shock effects persist ~60 days (2503.03312).

Trap: classic decision markets require stochastic decision rules
(sometimes a suboptimal action must be taken). If you need deterministic
execution, use proxy-forecasting variants with incentive compatibility
(2303.10857).

## 6. Contentious, polarizing decisions

Method: **random panel with pre-planned alternates** (2006.10498,
2604.02712, 2506.15716).

1. Define the decision scope; invite the whole eligible pool.
2. Sample the panel maximizing randomness under explicit constraints
   (diversity, quotas), with the selection algorithm published in advance —
   maximal randomness and auditability go together (2604.02712).
3. Account for refusals: either correct self-selection bias statistically
   (2006.10498) or pre-select alternates by expected dropout (2506.15716).
4. The panel deliberates; its decision enters the register with a review
   date.

## 7. Using AI in the loop — rules of engagement

Evidence: 2312.14877, 2505.05016, 2604.07667, 2508.08242, 2606.31762,
2608.08199.

1. The AI never runs the voting rule — code does (2505.05016).
2. AI drafts options and counterarguments; the group decides.
3. Aggregate many ranked AI answers instead of trusting one (2312.14877).
4. Consensus among AIs is not correctness — calibrate before acting
   (2604.07667).
5. Expect facilitation gains in information sharing, not in decision
   quality (2508.08242).
6. Supporting a minority: AI counterarguments raised satisfaction;
   AI-mediated messaging raised participation but lowered psychological
   safety — pick the trade-off knowingly (2606.31762).
7. Model "personality" is measurable (persuasion vs compliance) and predicts
   group outcomes — profile before assigning roles (2608.08199).

## 8. Deciding on the process itself

Method: **register + review + supersede** (2605.23628).

1. Every process decision gets a register entry with a review date.
2. Reviews are honest: worked / partial / failed — failures stay in the
   register; they are the experience base.
3. When a decision affects measurement (benchmarks, leaderboards), freeze
   fixtures and version definitions — benchmark gaming is election
   manipulation, provably (2605.23628).
4. Revisit the process quarterly: what we decided, what worked, what we
   would decide differently.

## Quick chooser

| Situation | Method | Section |
|---|---|---|
| yes/no group decision | independent vote + hybrid confirmation | 1 |
| prioritize many options | quadratic voting (computed by code) | 2 |
| allocate a budget | Method of Equal Shares | 3 |
| need missing expertise | per-topic revocable delegation | 4 |
| verifiable prediction | scoring-rule prediction poll | 5 |
| polarizing decision | random panel + alternates | 6 |
| AI in the loop | rules of engagement | 7 |
| change the process itself | register + review | 8 |
