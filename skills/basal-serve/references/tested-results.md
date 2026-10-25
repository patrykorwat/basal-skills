# Tested results log

What has actually run against a live basal server, and on what. Update this
file whenever a template passes or fails for real; "Tested" claims elsewhere
must point here.

| date | engine | model / mode | template / type | result |
|---|---|---|---|---|
| 2026-10-24 | 2.3.0 (`release_date` 2026-10-05) | basal-omni-1.0-ultra-FP8 / vllm | `choice` + `noul`, SOAM, text | passed, 181 ms, conf 0.99999 |
| 2026-10-24 | same | same | `act` + `max_error`, text | passed, chose `human` per cost matrix |
| 2026-10-24 | same | same | `facts: auto`, text | passed |
| 2026-10-24 | same | same | `verify` (`/v1/basal`) | failed 422 "0 options" — build predates task expansion; retest on 2.4.1 |
| 2026-10-24 | same | same | `classify` (`/v1/basal`) | failed 422, same cause |
| 2026-10-25 | same (2.3.0) | basal-omni-1.0-ultra-FP8 / vllm | `choice` + `noul`, text, real data (2 pinned SejmBench divisions, club-level state) | passed; 4/4 noul probes matched code-computed ground truth at conf >0.9999. The `choice` vote-type question was unnecessary: division type follows from the title via code (titles are quasi-controlled strings), and noul/score questions need no category list at all — basal needs typed answers, not codebooks, unless `choice` is genuinely required |
| — | — | — | image / audio media | not tested (ultra-FP8 vllm is text-only) |
| — | — | — | `score`, `multi`, `tool` | not tested |

Rules: a template is "Tested" only with a dated row above; a failure stays
in the log until a pass replaces it on a newer engine. Media rows need the
eager-mode server that accepts them.
