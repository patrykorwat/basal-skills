# Model routing

Sources: `github.com/rkinas/basal` README and docs, and the model and
benchmark pages at `basal.si5.pl`, read 2026-10-24, engine 2.4.1. Releases
change this table — re-read both before relying on it.

## Which family

| Input | Family | Notes |
|---|---|---|
| Text only | basal-2.0 | mini 1.5B, 4.5B, max 11B. NVIDIA GPU (`fast` mode), Mac with MLX, Ollama, llama.cpp; FP8 / GGUF / MLX ports. |
| Text only, smallest | basal-omni-pico | 0.8B (Qwen3.5); CPU or small GPU; text only despite the omni name. |
| Image, audio, or both with text | basal-omni | mini 4B (Gemma 4 E4B), max 12B, ultra 31B. NVIDIA GPU, `--mode eager --media on`. |

## Which omni model

| Need | Model | Reason |
|---|---|---|
| Recordings | mini | Reads recordings better than max per the published notes (small sample — still test on your data). |
| Document images | max or ultra | Max reads document images better than mini; ultra reads images best. |
| Audio and image in one request | mini or max | Ultra does not accept audio. |
| Experimental tasks (`classify`, `verify`, `compress`, `extract`) | 1.1-max | Extra training on the task formats; slightly behind 1.0-max on general decisions (Werdykt 0.821 vs 0.823), which stays the default. |
| Highest text accuracy, images too | ultra | Werdykt 0.879, the highest of the basal models. |
| Limited memory | mini | About 16 GB; max about 24 GB; ultra 59 GB of bf16 weights. |

Model size does not replace a test on the actual task. Run the evaluation
protocol (`omni-evaluation-protocol.md`) before choosing.

## Choosing by decision type

| Need | Type | Endpoint |
|---|---|---|
| One answer from a fixed list (2–255 options) | `choice` | `POST /v1/systemone` |
| Yes or no with a not-enough-information option | `noul` | `POST /v1/systemone` |
| Numeric rating: ordered levels + expected level | `score` | `POST /v1/systemone` |
| Several labels may apply | `multi` | `POST /v1/systemone` |
| Action with different costs for errors; human escalation | `act` + `max_error` | `POST /v1/systemone` |
| Selecting the next agent tool | `tool` + `max_error` | `POST /v1/systemone` |
| Labels with rubrics / claim checking / passage selection / schema fields | `classify` / `verify` / `compress` / `extract` | `POST /v1/basal` (experimental) |

Escalation: `act` or `tool` with `"max_error": 0.05` answers `"deferred":
true` below the certified confidence threshold. Without a threshold certified
for the question type and error target, every automatic action is refused —
which is the safe default, not an error.

Exact request and response fields: `docs/API.md` in `rkinas/basal`; the task
shapes: `docs/TASKS.md`. Both are copied into
`omni-query-templates.md` (read 2026-10-24).
