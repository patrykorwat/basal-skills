# Decision systems — distilled research map (arXiv, 2026-10-24)

Built for the basal community: **every paper below carries its actual
finding** — read this instead of the papers. Each ID is verifiable at
`https://arxiv.org/abs/<id>`. Distillation level: full abstracts of every
listed paper were read via the live arXiv API on 2026-10-24; a few abstracts
were truncated by the API — for those, only the visible text is distilled.
Full PDFs were not read, so do not quote numbers beyond what appears here
without opening the paper. The measurement of the status quo (Sejm
roll-calls) lives in the sejmbench repo.

## 0. The four questions every decision system must answer

**who decides** (qualification / lottery / representation), **how we
aggregate** (voting rule / delegation / market), **what we know before
deciding** (epistemics), and **how we verify after the fact** (backtests,
oversight). The literature has mature components for each — what is missing
is measurement that says which component *works*. SejmBench is that
measurement layer for the status quo.

## 0a. The whole map in 60 seconds — ten rules

1. Majority competence is **conditional**, not automatic: the "miracle of
   aggregation" fails almost surely as a prior (2108.00733). Protect and
   measure independence of judgments.
2. Purely rational turnout collapses to zero-cost voters only; participation
   rides on voters' (overestimated) sense of pivotality (2408.00317,
   2510.18062). Perceived mattering is a design input, not a side effect.
3. Independent aggregation beats advising: human and AI judge separately;
   agreement accepts, disagreement goes to a human tie-break (2603.29866).
4. Debate improves human judges; weaker LLM judges gain nothing and can lose
   accuracy (2610.28539). Debate is for strong judges.
5. Never let an LLM execute the voting rule itself — zero-shot aggregation
   miscomputes as groups grow (2505.05016). Rules run in code; aggregating
   ranked answers stabilizes models (2312.14877).
6. Consensus among agents is not correctness — calibrate act-vs-escalate
   decisions (2604.07667).
7. LLM facilitation raised information sharing in an RCT but did not fix a
   hidden-profile task (2508.08242). Facilitation moves process inputs, not
   necessarily outcomes.
8. AI support for minorities is a measurable trade-off: counterarguments
   raised satisfaction, mediated messages raised participation but lowered
   psychological safety (2606.31762).
9. Thin prediction markets are manipulable; price-shock effects persisted
   ~60 days; liquidity is a security parameter (2503.03312).
10. Benchmarks are elections: gaming is shift-bribery (NP-hard, but
    tempting) — freeze fixtures, version definitions (2605.23628).

## 1. Preference aggregation — computational social choice

Core: the mathematics of voting rules; every rule has known failure modes.

- **2410.14078** — *Parameterized Complexity and Challenges*. Finding:
  multi-winner determination and hedonic games are computationally hard
  (survey + open-challenge list). Use: complexity is a design constraint —
  "optimal voting rule at scale" claims are suspect.
- **2602.20074** — *COMSOC: Research & Development*. Finding: the field's
  own call to move from theorems to implemented, tested decision systems,
  with named roadblocks. Use: validates the thesis — deployment and
  measurement, not more theory, is the gap.
- **2608.25444** — *Continuous COMSOC: Bribery*. Finding: bribery and
  control attacks analyzed with society as a continuum of infinitesimal
  agents (statistical-mechanics style). Use: manipulation analysis scales
  analytically — design anti-bribery in from the start.

**For the thread:** before proposing "a better parliament vote": which rule,
resistant to what, with known failure modes. Socchoice is the vocabulary.

## 2. Epistemics — when the group knows more

Core: conditions under which aggregating independent judgments beats a
single expert — and when it breaks.

- **2108.00733** — *Miracle of Aggregation*. Finding: a measure-theoretic
  prior — "enough voters → majority competent" fails almost surely prima
  facie; competent aggregation needs evidence of voter competence or
  modified decision rules. Use: crowd wisdom is never a default; demand
  independence and competence evidence.
- **2408.00317** — *Jury Theorem with Abstention*. Finding: with fully
  rational abstention (pivotality = tie probability), only zero-cost voters
  participate; boundedly rational overestimation of pivotality restores
  non-trivial turnout, but victory is not assured when pivotality estimates
  depend strongly on victory margins. Use: participation rides on perceived
  mattering — and absences are informative, not noise.
- **2510.18062** — *On CJT with Abstention*. Finding: pivotality beliefs
  decide equilibria — weakly vanishing beliefs produce multiple stable
  near-tie elections; strongly vanishing beliefs produce the trivial
  equilibrium; below a sharp threshold the majority-preferred candidate
  wins with probability → 1. Use: near-tie, low-turnout systems can be a
  stable fixed point — change beliefs, not exhortation.
- **2603.29866** — *Beyond AI advice*. Finding: the Hybrid Confirmation Tree
  (human and AI judge independently; agreement accepted, disagreement →
  second human breaks the tie) outperformed AI-as-advisor on all 10 datasets
  including medical and misinformation tasks. Use: independence as a
  mechanism, not a norm — separate judgments, then combine.
- **2610.28539** — *Debate: humans vs weaker models*. Finding: debate raised
  accuracy for human judges (weighted voting best); weaker LLM judges gained
  nothing and sometimes lost accuracy; single-expert consultancy did not
  help. Use: debate is for strong judges; judge diversity matters.

**For the thread:** "more heads" is not enough — independence is what
counts. Does the system protect independence of judgment, or dissolve it
(room effect, cascades, party-line pressure)?

## 3. Deliberation and AI as the representative

Core: decision quality grows with conversation quality, but human attention
is limited — AI enters as mediator or proxy.

- **2603.16260** — *CI4DD*. Finding: framework chapter — AI as augmentation
  inside human-centred deliberation design. Use: vocabulary, not measured
  claims; do not cite as evidence.
- **2605.24413** — *Habermolt*. Finding: a public platform where AI agents
  deliberate on behalf of users ("AI-delegated deliberation"), evaluated on
  representation / aggregation / revision; the alignment challenges are
  qualitatively new and under-theorized. Use: whenever AI speaks for
  someone, define whose interests it optimizes.
- **2503.05830** — *AI-Enhanced Deliberative Democracy*. Finding:
  preferences are context-shaped and rarely objectively captured (the
  opinion-poll analogy); AI innovations work as discovery tools, with
  warnings against binding decisions, gradual disempowerment, and
  post-rationalizing outcomes. Use: AI-derived "collective will" informs,
  never binds.

**For the thread:** a decision system doesn't have to start by changing the
vote — it can start by changing **preparation**: AI-mediated deliberation at
the agenda level, instead of walked-in drafts from the back office.

## 4. Delegation — liquid democracy

Core: direct voting plus handing your vote to someone you trust on the
topic — delegation as a first-class mechanism.

- **2206.13904** — *Defense of Liquid Democracy*. Finding: rebuts the
  Caragiannis–Micha critique — the α-delegation model's assumptions are
  incorrect, the pathological delegation structures do not occur in real
  implementations, and optimality is moot when constraints guarantee correct
  results; the critique "has little or no relevance" for real systems. Use:
  concentration risk is a design parameter (constraints), not a fatal flaw.
- **2506.09789** — *Adaptive Representation Patterns*. Finding: LiquidFeedback
  data shows delegation structures are not static — influence adapts across
  issues and time, re-examining the transitive power-accumulation concern
  empirically. Use: design for delegation churn (per-topic, revocable), not
  one fixed proxy forever.
- **2309.01090** — *LD in DPoS Blockchains*. Finding: first empirical study
  of liquid democracy at production scale (DPoS chains, millions of users).
  Use: production-scale evidence exists — look there before theorizing.

**For the thread:** the Polish mandate setup (free mandate + party
discipline) is de facto frozen delegation without a right of recall. Liquid
democracy gives the vocabulary to name it and design alternatives.

## 5. Decision markets and quadratic voting

Core: aggregating information through stakes — knowledge gets an incentive;
voting has none.

- **1409.0264** — *Nash Equilibria for QV*. Finding: equilibria characterized
  for binary decisions with quadratic vote cost; expected inefficiency of
  any equilibrium decays like 1/n. Use: QV improves with electorate size —
  good at scale, weak for tiny groups.
- **2308.04345** — *QV in Participatory Budgeting*. Finding: QV/cumulative
  voting implemented on the Stanford PB platform; voters prefer simple
  methods, but expressive cumulative voting became preferred over the
  simpler k-ranking; the interface elements were found useful. Use: the
  adoption blocker is interface friction, not voter appetite.
- **2103.10011** — *Securities Based Decision Markets*. Finding: a
  securities implementation of decision markets with the same expected
  payoffs as scoring-rule markets (realized payoff distribution differs).
  Use: futarchy is implementable on trading infrastructure.
- **2303.10857** — *Proxy Forecasting*. Finding: standard decision markets
  need stochastic decision rules — sometimes a suboptimal action must be
  taken; three peer-prediction-style mechanisms achieve incentive
  compatibility with deterministic rules. Use: the classic futarchy
  objection has candidate fixes — a design choice, not a dealbreaker.
- **2503.03312** — *Manipulability of Prediction Markets*. Finding: field
  experiment — price shocks across 817 markets; effects visible ~60 days
  later and fade over time; more traders, volume, and external probability
  anchors make markets harder to manipulate. Use: liquidity is a security
  parameter; thin community markets are the vulnerable ones.

**For the thread:** the price-as-signal family. In Poland it faces hard
questions (capital concentration = concentration of "votes"), but as an
information source it is mature.

## 6. Sortition — the citizens' panel as an organ

Core: lottery instead of election for some functions — epistemic diversity
over competition.

- **2006.10498** — *Self-Selection Bias*. Finding: not every invitee accepts;
  an algorithm neutralizes the resulting bias in panel composition. Use:
  assembly legitimacy math must model refusal, not just the draw.
- **2604.02712** — *Maximally Random Sortition*. Finding: max-entropy panel
  sampling with per-member probability constraints; properties include
  manipulation resistance and transparency; benchmarked on real assembly
  lotteries (intersectional diversity, quota satisfaction). Use: "random"
  can be maximally random and auditable — demand both.
- **2506.15716** — *Alternates*. Finding: alternate selection as
  optimization — estimate dropout probabilities from history, minimize
  expected misrepresentation. Use: dropout threatens representation more
  than the draw; pre-plan alternates.

**For the thread:** citizens' assemblies moved from theory to real
deployments (Ireland, France) — know their limits (self-selection) before
anyone writes them into a constitution.

## 7. Participatory budgeting — multi-winner aggregation in practice

Core: not "for/against" but choosing a portfolio of projects.

- **2003.00606** — *PB Models and Approaches*. Finding: survey + model axes
  (divisible vs indivisible projects, funding limits); preference
  elicitation is the central challenge. Use: PB's hard part is eliciting
  real preferences, not counting them.
- **2012.06539** — *Pabulib*. Finding: open .pb-format library of real PB
  instances (pabulib.org, Polish origin). Use: real data exists — test rules
  on it before proposing changes to real budgets.
- **2603.09660** — *Proportionality Degree in PB*. Finding: tight
  proportionality-degree bounds for MES and Phragmén — quantitatively equal
  despite MES's stronger axiomatic guarantees; experiments on real datasets
  mirror the theory. Use: between the popular rules, fairness ties — choose
  on other criteria (usability, cost, explainability).

**For the thread:** PB is the decision system closest to the citizen (Polish
cities run it) and a natural testbed — rules can change without revolution,
and effects are measurable.

## 8. LLMs as decision participants — what we already know

Core: language models enter decision systems as agents, mediators, and
aggregators — with measured weaknesses.

- **2312.14877** — *Robust Knowledge Extraction*. Finding: repeated ranking
  queries + Partial Borda aggregation stabilize LLM answers in high-stakes
  settings. Use: aggregate many ranked answers; never trust a single
  response.
- **2505.05016** — *Growing Group Complexity*. Finding: zero-shot LLMs
  miscompute aggregation rules as group size grows. Use: rules run in code,
  models judge items — never the reverse.
- **2604.07667** — *Conformal Social Choice*. Finding: converts agent-debate
  consensus into calibrated act-vs-escalate decisions; agreement is not
  correctness. Use: add a calibration layer between debate and action.
- **2508.08242** — *LLM-Facilitated Group Decision Making*. Finding:
  pre-registered RCT (1,475 participants, 281 groups, hidden-profile task):
  GPT-4o facilitation raised minimum engagement and information sharing;
  attitudes were unaffected; final decisions did NOT improve. The GRAIL
  platform was open-sourced. Use: facilitation moves process inputs, not
  necessarily outcomes — measure outcomes, not vibes.
- **2606.31762** — *Dissenting Minority Support*. Finding: 96 participants /
  24 groups: AI counterarguments created a more flexible atmosphere and
  higher satisfaction; AI-mediated messaging increased minority
  participation but reduced psychological safety (the "support paradox").
  Use: how you support minorities is a measurable trade-off, not a slogan.
- **2608.08199** — *Persuasive and Compliant Tendencies*. Finding:
  DecisionQE + the Werewolf testbed: persuasion does not significantly
  improve group outcomes; compliance-oriented models give more stable
  cooperation — with a dual effect (cooperation in honest roles, better
  concealment in adversarial roles). Use: model "personality" is measurable
  and consequential — include behavioral tendencies in model selection and
  safety checks.

**For the thread:** if a parliamentary decision system has AI in the loop,
know where models fail: numerical aggregation (accuracy), conformity
(independence), minority support (fairness) — all testable.

## 9. Governing AI itself — decision systems for agents

- **2412.17114** — *ETHOS*. Finding: proposes a global registry of AI agents,
  dynamic risk classification, proportional oversight, soulbound tokens,
  zero-knowledge proofs, decentralized justice, and mandatory insurance;
  argues EU AI Act / NIST do not cover agent autonomy. Use: agent oversight
  architecture exists on paper — DAO mechanisms are the testbed.
- **2510.21117** — *DAO-AI*. Finding: first empirical agentic-AI voter over
  3K+ real DAO proposals; interpretable, auditable signals; strong alignment
  with human and token-weighted outcomes. Use: agent voters are measurable —
  the open question is whether mimicking human outcomes is the right target.
- **2605.23628** — *Rigging a Benchmark*. Finding: benchmark gaming = shift
  bribery (datasets as voters, models as candidates); NP-hard under Borda
  count and mean win rate. Use: freeze fixtures, version definitions — and
  expect motivated attempts anyway.

**For the thread:** the mirror check — before fixing human decision systems,
verify that our own measurement instruments are manipulation-resistant.

## 10. What follows for the thread (synthesis)

1. **The design space is ready:** aggregation (socchoice), epistemics
   (jury/wisdom of crowds), deliberation (AI-mediated), delegation (liquid),
   price signals (QV/futarchy), sortition, portfolios (PB) — every family
   has theory and tools.
2. **The measurement layer is missing:** the literature proposes systems but
   rarely measures them on real, frozen decision data. SejmBench provides
   that for the status quo — the thread can ask: *which experiment on the
   benchmark would separate these families?*
3. **The hardest starter hypotheses** (testable on Sejm data):
   - party discipline as degenerate delegation — how much information the
     party line absorbs from a vote (rebellion rate, cohesion);
   - absence as a third vote — does the jury theorem with abstention
     (2408.00317, 2510.18062) describe the Sejm;
   - model conformity vs councilor conformity — do LLM agents import the
     pathologies visible in the data (2608.08199).
4. **Red line:** no family is "the answer" — every mechanism has studied
   failure modes (manipulation, self-selection, concentration). A rigorous
   thread shows both sides: "for what and how", never "against".

## Method

Queries against `export.arxiv.org/api/query` (2026-10-24): computational
social choice; liquid democracy; quadratic voting; futarchy / decision
markets; prediction markets; deliberative democracy + AI; citizens'
assembly; collective intelligence; judgment aggregation; sortition;
decentralized governance + blockchain; LLM + social choice; Condorcet jury
theorem; participatory budgeting; wisdom of the crowd + AI; approval/ranked
choice; LLM + group decision; epistemic democracy. Full abstracts of every
paper listed here were read from the API; a few abstracts were truncated by
the API response — findings for those are limited to the visible text. Full
PDFs were not read. Every ID verifiable at `https://arxiv.org/abs/<id>`.
