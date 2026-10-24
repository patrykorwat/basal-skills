# Systemy decyzyjne — mapa literatury (arXiv, 2026-10-24)

Materiał otwierający wątek o systemach decyzyjnych dla parlamentu
(społeczność basal). Każdy blok to jedna **rodzina** systemów decyzyjnych:
rdzeń problemu + prace kotwiczne (ID weryfikowalne pod
`https://arxiv.org/abs/<id>`) + dlaczego to ma znaczenie dla wątku. Wszystkie
pozycje pochodzą z żywych zapytań do API arXiva w dniu 2026-10-24 — nic z
pamięci. Notatka to „raj": przestrzeń projektowa, z której wątek może czerpać;
pomiar status quo (roll-call Sejmu) żyje w repo sejmbench.

## 0. Teza wątku w jednym akapicie

Każdy system decyzyjny odpowiada na cztery pytania: **kto decyduje** (kwalifikacja/losowanie/reprezentacja), **jak agregujemy** (reguła głosowania/delegacja/rynek), **co wiemy zanim zdecydujemy** (epistemia: jury theorem, mądrość tłumu, rynki predykcyjne) i **jak sprawdzamy po fakcie** (backtest, nadzór). Literatura ma dojrzałe komponenty dla każdego z tych pytań — brakuje pomiaru, który mówi, który komponent *działa*. Stąd naturalny pomost do SejmBench: benchmark jest warstwą weryfikacji dla status quo, a mapa poniżej pokazuje, co można by na nim testować jutro.

## 1. Agregacja preferencji — computational social choice

Rdzeń: matematyka reguł głosowania. Nie ma „naturalnego" zwycięzcy — jest reguła, a każda reguła ma pułapki (twierdzenia o niemożliwości, manipulacja, kupowanie głosów).

- **2410.14078** — Computational Social Choice: Parameterized Complexity and Challenges. Przegląd problemów trudności obliczeniowej w socchoice.
- **2602.20074** — Computational Social Choice: Research & Development. Stan pola badawczego.
- **2608.25444** — Continuous Computational Social Choice: A Case Study in Bribery. Kupowanie głosów jako modelowany problem — odporność na manipulację to twarda własność systemu, nie detal.

**Dla wątku:** zanim padnie propozycja „lepszego głosowania w Sejmie", pytanie brzmi: jaka reguła, odporna na co, i poznaliśmy jej pułapki. Socchoice daje słownik, żeby te rozmowy nie były tylko wibracjami.

## 2. Epistemia — kiedy grupa wie więcej

Rdzeń: warunki, w których agregacja niezależnych sądów przekracza jakość pojedynczego eksperta — i kiedy się psuje.

- **2108.00733** — On the probability of the Condorcet Jury Theorem or the Miracle of Aggregation. Klasyczne twierdzenie: przy niezależnych sądach o p>1/2 większość jest niemal nieomylna — ale założenia są surowe.
- **2408.00317 / 2510.18062** — Condorcet's Jury Theorem (with) Abstention. Wariant z absencją: niegłosujący zmieniają matematykę — bezpośredni język dla debaty o frekwencji i wstrzymujących się.
- **2603.29866** — Beyond AI advice — independent aggregation boosts human-AI accuracy. Niezależna agregacja osądów (ludzkich i AI) bije wspólną dyskusję z dopasowaniem do jednej rady.
- **2610.28539** — Humans Correct Their Judgments Through Debate, but Weaker AI Models Do Not. Debata naprawia ludzi; słabsze modele ulegają shearingowi grupy.

**Dla wątku:** „więcej głów" nie wystarczy — liczy się **niezależność** sądów. To jest kryterium oceny każdego pomysłu: czy system chroni niezależność osądów, czy ją kasuje (efekt sali, kaskady, presja linii klubowej).

## 3. Deliberacja i AI jako przedstawiciel

Rdzeń: jakość decyzji rośnie z jakością rozmowy, ale uwaga ludzka jest ograniczona — AI wchodzi jako mediator albo pełnomocnik.

- **2603.16260** — Human/AI Collective Intelligence for Deliberative Democracy (CI4DD). Ramy: AI jako narzędzie augmentacji zbiorowej inteligencji w deliberacji, z podejściem human-centred.
- **2605.24413** — Habermolt: Delegating Deliberation to AI Representatives. AI nie tylko mediuje — reprezentuje obywatela w deliberacji. Pytanie graniczne: komu agent jest wierny.
- **2503.05830** — AI-Enhanced Deliberative Democracy and the Future of the Collective Will. Wizja polityczna z AI w pętli.

**Dla wątku:** system decyzyjny dla sejmu nie musi zaczynać od zmiany głosowania — może od zmiany **przygotowania** decyzji: AI-mediated deliberacja na poziomie agendy, zamiast walked-in projektów z gabinetu.

## 4. Delegacja — płynna demokracja

Rdzeń: głos bezpośredni + oddawanie głosu komuś, komu ufam w tym temacie. Delegacja jako mechanizm pierwszej klasy, nie wyjątek.

- **2206.13904** — A Contribution to the Defense of Liquid Democracy. Obrona wobec zarzutów o koncentrację władzy — plus uczciwe pokazanie, gdzie ryzyko jest realne.
- **2506.09789** — Delegations as Adaptive Representation Patterns. Delegacje jako adaptacyjne wzorce reprezentacji — wpływ jest dynamiczny, nie stały.
- **2309.01090** — Liquid Democracy in DPoS Blockchains. Wdrożenia w praktyce (blockchain DPoS) — co się dzieje z delegacją, gdy jest realnie używana.

**Dla wątku:** polski układ mandatu (wolny mandat + dyscyplina klubowa) to de facto zamrożona delegacja bez prawa odwołania. Liquid democracy daje słownictwo, by to nazwać i zaprojektować alternatywy (delegacja tematyczna, odwoływalność).

## 5. Rynki decyzyjne i kwadratowe głosowanie

Rdzeń: agregacja informacji przez stawki — ci, którzy wiedzą więcej, mają bodziec, by w to wchodzić; głosowanie tego bodźca nie ma.

- **1409.0264** — Nash Equilibria for Quadratic Voting. QV: koszt głosu rośnie kwadratowo z liczbą głosów — teoria równowagi.
- **2308.04345** — Fair and Inclusive Participatory Budgeting: Voter Experience with Cumulative and Quadratic Voting. QV w praktyce budżetów — doświadczenie wyborcy ma znaczenie.
- **2103.10011** — Securities Based Decision Markets. Futarchy: „głosujemy nad wartościami, rynek stawia nad środkami" — formalizacja.
- **2303.10857** — Proxy Forecasting to Avoid Stochastic Decision Rules in Decision Markets. Problem futarchy: decyzja nie może być losową funkcją kursu — potrzebne proxy-prognozy.
- **2503.03312** — How manipulable are prediction markets? Odporność rynków na manipulację — the eternal question.

**Dla wątku:** rodzina mechanizmów z ceną jako sygnałem. W Polsce wystawione na trudne pytania (koncentracja kapitału = koncentracja „głosu"), ale jako źródło informacji dla decyzji — dojrzały temat.

## 6. Losowanie — panel obywatelski jako organ

Rdzeń: losowanie (sortycja) zamiast elekcji dla części funkcji — epistemiczna różnorodność zamiast rywalizacji.

- **2006.10498** — Neutralizing Self-Selection Bias in Sampling for Sortition. Kluczowy problem praktyczny: kogo losujemy, gdy nie każdy przychodzi — korekta biasu samo-selekcji.
- **2604.02712** — Maximally Random Sortition. Ile losowości optymalnie.
- **2506.15716** — Alternates, Assemble! Selecting Optimal Alternates for Citizens' Assemblies. Zastępcy — logistyka ciągłości panelu.

**Dla wątku:** assemblies obywatelskie to jedyna rodzina, która przeszła z teorii do realnych wdrożeń w ostatnich latach (Irlandia, Francja) — warto znać ich ograniczenia (self-selection!) zanim ktoś je wpisze do konstytucji.

## 7. Budżet obywatelski — wielozwycięskie agregacje w praktyce

Rdzeń: nie „za/przeciw", tylko wybór portfela projektów — inni klasa reguł (multi-winner, proporcjonalność).

- **2003.00606** — Participatory Budgeting: Models and Approaches. Modelowe podstawy PB.
- **2012.06539** — Pabulib: A Participatory Budgeting Library. Biblioteka instancji PB (polski rodowód — warszawskie data) — realne dane do badań nad regułami.
- **2603.09660** — Proportionality Degree in Participatory Budgeting. Miara proporcjonalności reguł PB — jak mierzyć uczciwość podziału.

**Dla wątku:** PB jest najbliższym obywatelowi systemem decyzyjnym (polskie miasta go mają) i naturalnym poligonem: tu reguły można zmieniać bez rewolucji i mierzyć skutki.

## 8. LLM jako uczestnik decyzji — co już wiemy

Rdzeń: modele językowe wchodzą w systemy decyzyjne jako agenci, mediatorzy i agregatory — i mają zmierzone wady.

- **2312.14877** — Robust Knowledge Extraction from LLMs using Social Choice Theory. Socchoice (rankingi zamiast pojedynczych odpowiedzi) stabilizuje odpowiedzi LLM — agregacja jako narzędzie niezawodności.
- **2505.05016** — The Pitfalls of Growing Group Complexity: LLMs and Social Choice-Based Aggregation. LLM-y zero-shot **błędnie liczą** reguły agregacji przy rosnącej liczbie uczestników — dokładnie tam, gdzie system decyzyjny potrzebuje precyzji.
- **2604.07667** — From Debate to Decision: Conformal Social Choice. Zgoda w debacie agentów ≠ poprawność; potrzebna kalibracja decyzji (act-vs-escalate).
- **2508.08242** — Bringing Everyone to the Table: LLM-Facilitated Group Decision Making. Eksperyment: LLM jako facylitator decyzji grupy ludzi.
- **2606.31762** — Investigating LLM-Powered Dissenting Minority Support in Power-Imbalanced Group Decision-Making. Czy AI wspiera mniejszość w grupach o nierównej władzie — albo pogłębia hegemonię.
- **2608.08199** — Persuasive and Compliant Tendencies Predict Group Decision-Making in Humans and Language Models. Te same tendencje (uległość, perswazyjność) przewidują zachowanie ludzi i modeli — dowód, że modele importują ludzkie patologie decyzji.

**Dla wątku:** jeśli system decyzyjny dla sejmu ma mieć AI w pętli, to trzeba wiedzieć, **gdzie modele zawodzą**: agregacja liczbowa (poprawność), konformizm (niezależność), wsparcie mniejszości (fairness). To są testowalne hipotezy — i naturalne rozszerzenia benchmarku.

## 9. Governance samej AI — systemy decyzyjne dla agentów

- **2412.17114** — Decentralized Governance of Autonomous AI Agents (ETHOS). Ramy nadzoru nad autonomicznymi agentami; istniejące akty (EU AI Act, NIST) nie pokrywają agentowej autonomii.
- **2510.21117** — DAO-AI: Evaluating Collective Decision-Making through Agentic AI in Decentralized Governance. Agenci w DAO — mierzenie jakości decyzji hybrydowych.
- **2605.23628** — How Hard is it to Rig a Benchmark? A Social Choice Analysis of Leaderboard Robustness. Benchmark = wybory: datasety jako wyborcy, modele jako kandydaci; gaming leaderboardu = manipulacja wyborcza. Uzasadnienie frozen-fixture z pierwszej zasady.

**Dla wątku:** refleksja w lustrze — zanim naprawiamy systemy decyzyjne ludzi, sprawdźmy, czy nasze własne narzędzia pomiaru (benchmarki, rankingi) same są odporne na manipulację.

## 10. Co z tego wynika dla wątku (synteza)

1. **Przestrzeń projektowa jest gotowa:** agregacja (socchoice), epistemia (jury/mądrość tłumu), deliberacja (AI-mediated), delegacja (liquid), sygnał cenowy (QV/futarchy), losowanie (sortycja), portfel (PB). Każda rodzina ma teorię i narzędzia.
2. **Brakuje warstwy pomiaru:** literatura proponuje systemy, ale rzadko mierzy je na realnych, frozen danych decyzji. SejmBench daje taki pomiar dla status quo (roll-call) — wątek może więc pytać: *jaki eksperyment na benchmarku odróżniłoby te rodziny?*
3. **Najtwardsze hipotezy na start** (testowalne na danych Sejmu):
   - dyscyplina klubowa jako „zdegenerowana delegacja" — ile informacji głosu pochłania linia klubu (mierzalne: rebellion rate, spójność);
   - absencja i wstrzymanie jako trzeci głos — czy jury theorem z absencją (2408.00317) opisuje Sejm;
   - konformizm modeli vs konformizm radnych — czy LLM-agenci przejmują patologie, które widzimy w danych (2608.08199).
4. **Red line:** żadna rodzina nie jest „odpowiedzią" — każdy mechanizm ma zbadane pułapki (manipulacja, samoselekcja, koncentracja). Rzetelny wątek pokazuje obie strony; to jest też styl Radoskopu: „ZA i nad czym", nie „przeciw".

## Metoda

Zapytania do `export.arxiv.org/api/query` (2026-10-24): computational social
choice; liquid democracy; quadratic voting; futarchy / decision markets;
prediction markets; deliberative democracy + AI; citizens' assembly; collective
intelligence; judgment aggregation; sortition; decentralized governance +
blockchain; LLM + social choice; Condorcet jury theorem; participatory
budgeting; wisdom of the crowd + AI; approval/ranked choice; LLM + group
decision; epistemic democracy. Abstrakty kluczowych pozycji czytane w całości
z API. Każdy ID weryfikowalny: `https://arxiv.org/abs/<id>`.
