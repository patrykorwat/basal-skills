# Decision systems — literature map (arXiv, 2026-10-24)

Background material for a community thread on decision systems for
parliaments (the "basal" community). Each block is one **family** of decision
systems: the core problem, anchor papers (IDs verifiable at
`https://arxiv.org/abs/<id>`), and why it matters for the thread. Every entry
comes from live arXiv API queries on 2026-10-24 — nothing from memory. This
note is the design space the thread can draw from; the measurement of the
status quo (Sejm roll-calls) lives in the sejmbench repo.

## 0. The thread's thesis in one paragraph

Every decision system answers four questions: **who decides**
(qualification/lottery/representation), **how we aggregate** (voting rule /
delegation / market), **what we know before deciding** (epistemics: jury
theorems, wisdom of crowds, prediction markets), and **how we verify after
the fact** (backtests, oversight). The literature has mature components for
each question — what is missing is measurement that says which component
*works*. Hence the natural bridge to SejmBench: the benchmark is the
verification layer for the status quo, and the map below shows what could be
tested on it tomorrow.

## 1. Preference aggregation — computational social choice

Core: the mathematics of voting rules. There is no "natural" winner — there
is a rule, and every rule has known failure modes (impossibility theorems,
manipulation, vote buying).

- **2410.14078** — Computational Social Choice: Parameterized Complexity and Challenges. A survey of computational-hardness problems in socchoice.
- **2602.20074** — Computational Social Choice: Research & Development. The state of the field.
- **2608.25444** — Continuous Computational Social Choice: A Case Study in Bribery. Vote buying as a modeled problem — manipulation resistance is a hard system property, not a detail.

**For the thread:** before anyone proposes "a better parliament vote", the
question is: which rule, resistant to what, and do we know its failure
modes. Socchoice gives the vocabulary so these discussions are not just
vibes.

## 2. Epistemics — when the group knows more

Core: the conditions under which aggregating independent judgments beats a
single expert — and when it breaks.

- **2108.00733** — On the probability of the Condorcet Jury Theorem or the Miracle of Aggregation. The classic: with independent judgments of p>1/2 accuracy, majorities are near-infallible — but the assumptions are strict.
- **2408.00317 / 2510.18062** — Condorcet's Jury Theorem (with) Abstention. The abstention variant: non-voters change the mathematics — direct language for debating turnout and abstentions.
- **2603.29866** — Beyond AI advice — independent aggregation boosts human-AI accuracy. Independent aggregation of judgments (human and AI) beats joint discussion fitted to a single panel.
- **2610.28539** — Humans Correct Their Judgments Through Debate, but Weaker AI Models Do Not. Debate fixes humans; weaker models yield to the group.

**For the thread:** "more heads" is not enough — **independence** of
judgments is what counts. That is the evaluation criterion for every idea:
does the system protect independence of judgment, or dissolve it (room
effect, cascades, party-line pressure)?

## 3. Deliberation and AI as the representative

Core: decision quality grows with conversation quality, but human attention
is limited — AI enters as mediator or proxy.

- **2603.16260** — Human/AI Collective Intelligence for Deliberative Democracy (CI4DD). A framework: AI as an augmentation tool for collective intelligence in deliberation, human-centred by design.
- **2605.24413** — Habermolt: Delegating Deliberation to AI Representatives. AI not only mediates — it represents a citizen in deliberation. The boundary question: to whom is the agent loyal.
- **2503.05830** — AI-Enhanced Deliberative Democracy and the Future of the Collective Will. The political vision with AI in the loop.

**For the thread:** a decision system for a parliament does not have to start
by changing the vote — it can start by changing **preparation**: AI-mediated
deliberation at the agenda level, instead of walked-in drafts from the
back office.

## 4. Delegation — liquid democracy

Core: direct voting plus handing your vote to someone you trust on the topic.
Delegation as a first-class mechanism, not an exception.

- **2206.13904** — A Contribution to the Defense of Liquid Democracy. A defense against power-concentration critiques — with an honest look at where the risk is real.
- **2506.09789** — Delegations as Adaptive Representation Patterns. Delegations as adaptive patterns of representation — influence is dynamic, not fixed.
- **2309.01090** — Liquid Democracy in DPoS Blockchains. Deployments in practice (DPoS blockchains) — what happens to delegation when it is actually used.

**For the thread:** the Polish mandate setup (free mandate + party
discipline) is de facto frozen delegation without a right of recall. Liquid
democracy provides the vocabulary to name this and to design alternatives
(topic-specific delegation, recallability).

## 5. Decision markets and quadratic voting

Core: aggregating information through stakes — those who know more have an
incentive to participate; voting has no such incentive.

- **1409.0264** — Nash Equilibria for Quadratic Voting. QV: the cost of a vote grows quadratically with the number of votes — equilibrium theory.
- **2308.04345** — Fair and Inclusive Participatory Budgeting: Voter Experience with Cumulative and Quadratic Voting. QV in budget practice — voter experience matters.
- **2103.10011** — Securities Based Decision Markets. Futarchy: "we vote on values, the market bets on means" — the formalization.
- **2303.10857** — Proxy Forecasting to Avoid Stochastic Decision Rules in Decision Markets. The futarchy problem: a decision cannot be a random function of a price — proxy forecasts are needed.
- **2503.03312** — How manipulable are prediction markets? Market manipulation resistance — the eternal question.

**For the thread:** the family of price-as-signal mechanisms. In Poland it
faces hard questions (capital concentration = concentration of "votes"), but
as an information source for decisions it is a mature topic.

## 6. Sortition — the citizens' panel as an organ

Core: lottery (sortition) instead of election for some functions —
epistemic diversity instead of competition.

- **2006.10498** — Neutralizing Self-Selection Bias in Sampling for Sortition. The key practical problem: whom do we sample when not everyone shows up — correcting self-selection bias.
- **2604.02712** — Maximally Random Sortition. How much randomness is optimal.
- **2506.15716** — Alternates, Assemble! Selecting Optimal Alternates for Citizens' Assemblies. Alternates — the logistics of panel continuity.

**For the thread:** citizens' assemblies are the only family that moved from
theory to real deployments in recent years (Ireland, France) — know their
limits (self-selection!) before anyone writes them into a constitution.

## 7. Participatory budgeting — multi-winner aggregation in practice

Core: not "for/against" but choosing a portfolio of projects — a different
class of rules (multi-winner, proportionality).

- **2003.00606** — Participatory Budgeting: Models and Approaches. The model foundations of PB.
- **2012.06539** — Pabulib: A Participatory Budgeting Library. A library of PB instances (Polish origin — Warsaw data) — real data for research on rules.
- **2603.09660** — Proportionality Degree in Participatory Budgeting. A proportionality measure for PB rules — how to measure fairness of allocation.

**For the thread:** PB is the decision system closest to the citizen
(Polish cities run it) and a natural testbed: rules can be changed there
without a revolution, and effects can be measured.

## 8. LLMs as decision participants — what we already know

Core: language models enter decision systems as agents, mediators, and
aggregators — with measured weaknesses.

- **2312.14877** — Robust Knowledge Extraction from LLMs using Social Choice Theory. Socchoice (rankings instead of single answers) stabilizes LLM responses — aggregation as a reliability tool.
- **2505.05016** — The Pitfalls of Growing Group Complexity: LLMs and Social Choice-Based Aggregation. Zero-shot LLMs **miscompute** aggregation rules as the group grows — exactly where a decision system needs precision.
- **2604.07667** — From Debate to Decision: Conformal Social Choice. Agreement in agent debate ≠ correctness; decisions need calibration (act-vs-escalate).
- **2508.08242** — Bringing Everyone to the Table: LLM-Facilitated Group Decision Making. An experiment: an LLM facilitating a human group's decision.
- **2606.31762** — Investigating LLM-Powered Dissenting Minority Support in Power-Imbalanced Group Decision-Making. Does AI support minorities in power-imbalanced groups — or deepen dominance.
- **2608.08199** — Persuasive and Compliant Tendencies Predict Group Decision-Making in Humans and Language Models. The same tendencies (compliance, persuadability) predict behavior of humans and models — evidence that models import human decision pathologies.

**For the thread:** if a parliamentary decision system is to have AI in the
loop, we need to know **where models fail**: numerical aggregation
(accuracy), conformity (independence), minority support (fairness). These
are testable hypotheses — and natural benchmark extensions.

## 9. Governing AI itself — decision systems for agents

- **2412.17114** — Decentralized Governance of Autonomous AI Agents (ETHOS). Oversight frameworks for autonomous agents; existing acts (EU AI Act, NIST) do not cover agent autonomy.
- **2510.21117** — DAO-AI: Evaluating Collective Decision-Making through Agentic AI in Decentralized Governance. Agents in DAOs — measuring hybrid decision quality.
- **2605.23628** — How Hard is it to Rig a Benchmark? A Social Choice Analysis of Leaderboard Robustness. A benchmark is an election: datasets as voters, models as candidates; leaderboard gaming = electoral manipulation. The first-principles justification for frozen fixtures.

**For the thread:** a mirror check — before fixing human decision systems,
verify that our own measurement instruments (benchmarks, leaderboards) are
themselves manipulation-resistant.

## 10. What follows for the thread (synthesis)

1. **The design space is ready:** aggregation (socchoice), epistemics
   (jury/wisdom of crowds), deliberation (AI-mediated), delegation (liquid),
   price signals (QV/futarchy), sortition, portfolios (PB). Every family has
   theory and tools.
2. **The measurement layer is missing:** the literature proposes systems but
   rarely measures them on real, frozen decision data. SejmBench provides
   that measurement for the status quo (roll-calls) — so the thread can ask:
   *which experiment on the benchmark would separate these families?*
3. **The hardest starter hypotheses** (testable on Sejm data):
   - party discipline as degenerate delegation — how much information the
     party line absorbs from a vote (measurable: rebellion rate, cohesion);
   - absence as a third vote — does the jury theorem with abstention
     (2408.00317) describe the Sejm;
   - model conformity vs councilor conformity — do LLM agents import the
     pathologies we see in the data (2608.08199).
4. **Red line:** no family is "the answer" — every mechanism has studied
   failure modes (manipulation, self-selection, concentration). A rigorous
   thread shows both sides; this is also the Radoskop style: "for what and
   how", never "against".

## Method

Queries against `export.arxiv.org/api/query` (2026-10-24): computational
social choice; liquid democracy; quadratic voting; futarchy / decision
markets; prediction markets; deliberative democracy + AI; citizens'
assembly; collective intelligence; judgment aggregation; sortition;
decentralized governance + blockchain; LLM + social choice; Condorcet jury
theorem; participatory budgeting; wisdom of the crowd + AI; approval/ranked
choice; LLM + group decision; epistemic democracy. Abstracts of key papers
read in full from the API. Every ID verifiable at
`https://arxiv.org/abs/<id>`.
