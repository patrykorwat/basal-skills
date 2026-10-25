---
name: basal-serve
description: Use when a task needs a typed, calibrated decision from a local basal server (text, image, scan, screenshot or audio up to 30 seconds), when choosing between basal-2.0 (text) and basal-omni (media) models, writing basal questions with allowed answers, fitting confidence thresholds, or evaluating basal on the user's own data. Trigger on basal-serve, basal-2.0, basal-omni, POST /v1/systemone, /v1/basal, decision from a document photo, classification of a recording, extraction of fields from document text, verification of claims against a source. Use it even if the user does not name the model but asks for a local, calibrated, multiple-choice decision from text or media.
version: 0.3.0
author: Radoskop
license: MIT
metadata:
  tags: [basal, basal-serve, basal-2.0, basal-omni, decisions, calibration, inference]
---

# basal-serve

Guidance for using the basal decision models through a local `basal-serve`.
Basal returns a choice among answers that the caller defines, with
calibrated probabilities; it does not write free text. Two families:
**basal-2.0** for text-only decisions, **basal-omni** for media. The engine
is at 2.4.1 (2026-10-23); models move fast, so the live docs beat this file.

Companion skill: `basal-strategies` covers the community decision process
(when to ask, methods, register). This skill covers the connection: what to
send, to which model, with which guarantee. Shared principles — sources,
frozen definitions, no machine paths, owner approval before publishing —
are in the repository README.

## Read the live docs first

- Start with the model and server pages: <https://basal.si5.pl/models/> and
  <https://basal.si5.pl/serwer-inferencji/> (schema reference included).
  For engine internals, read the raw docs targeted:
  `https://raw.githubusercontent.com/rkinas/basal/main/docs/API.md`,
  `TASKS.md`, `OMNI.md`, `CALIBRATION.md`, `INSTALL.md`.
- Before writing an integration, read the current API page and the schema
  section relevant to the design; copy JSON shapes from the docs, never
  from memory.
- If live access is unavailable, use the local references below, state that
  limitation, and avoid inventing version-dependent details.

| Task | Start here |
|---|---|
| Pick a family and model | `references/model-routing.md`, then the live model page |
| Write the request | `references/query-templates.md`, then `docs/API.md` |
| Choose or fit a threshold | `references/evaluation-protocol.md`, then `docs/CALIBRATION.md` |
| Diagnose a failure | Versions section below, then `references/tested-results.md` |

## Workflow

1. Check the input. Text only → basal-2.0, not omni. Read
   `references/model-routing.md` to pick family and model.
2. Define the questions and the allowed answers before running anything.
   Read `references/query-templates.md`. Freeze the category list under a
   version label.
3. If a confidence threshold is needed, fit it on labeled examples from the
   user's own process (`basal-calibrate`). Read
   `references/evaluation-protocol.md`. Never reuse a text threshold for
   media.
4. Run inference locally:
   `basal-serve --model <weights> --mode eager --media on --port 8000`
   (media only; text runs in vllm mode). Media travel in the `media` field
   of the HTTP request (base64). Record model name, engine version, mode
   and calibration file with every result.
5. Route results below the threshold to a human (`act` or `tool` questions
   with `max_error`, which answer `"deferred": true`). The error target must
   come from calibration on your labeled data and your cost of a wrong
   action — the 0.05 seen in examples is a placeholder, not a default.
   Report counts of automatic and escalated cases separately.
6. Publish nothing community-facing without explicit owner approval of the
   exact text.

## Hard limits to state to the user

1. Audio: WAV, FLAC, OGG or MP3, at most 30 s per clip; at most 8 media items
   and 20 MB each per request. Longer recordings must be cut by the
   application.
2. No video input. The application extracts frames and the audio track first.
3. The ultra model (31B) reads text and images only, with no audio. Every
   `-GGUF`, `-MLX` and `-FP8` port is text only.
4. Media need an NVIDIA GPU, `--mode eager --media on`, bf16 weights.
   Approximate memory: mini ~16 GB, max ~24 GB, ultra 59 GB of weights (an
   80 GB card for long states). Text-only basal-2.0 also runs on Mac (MLX),
   Ollama and llama.cpp; pico has an 812 MB GGUF that runs on CPU.
5. Omni's calibration comes from text; media answers carry
   `"calibration": "text"`. Its confidence values on images and audio are
   unverified until tested on the user's data.
6. Media benchmark results come from small samples (5 runs per modality). Do
   not present them as general accuracy.
7. Werdykt measures text decisions only — every model, including omni, gets
   text there. Never quote it as the quality of image or audio reading.
8. MCP tools have no media parameter; images and audio go through the HTTP
   API only.

## Confidence

A probability from basal is a calibrated score, not a guarantee. Treat it as
a ranking signal for escalation. A threshold is valid only for the model
version, question design and data type it was fitted on.

**Checkable vs value questions.** Calibration means something only where a
correct answer exists and can be checked later (rule compliance, category,
claim-vs-source): there, a certified threshold may gate automation. On value
questions nothing labels the truth, so no `max_error` has empirical basis and
"confidence" measures the model's assertiveness, not accuracy: report the
number as an opinion, start no action from it, and never present it as a
chance of being right. `basal-strategies` owns this distinction; this skill
enforces it at request level.

## Versions

Models and engine change quickly. Do not copy benchmark numbers into this
skill or into posts without a link and a read date. Link to the benchmark
page (`basal.si5.pl/benchmark/`) and the Hugging Face model card, and state
the date they were read. Record in every result log: model name and weights
revision, engine version, mode, calibration file, codebook version. Results
from different versions are not comparable without stating the difference.

**Diagnosing 422 before assuming a broken server:** templates were copied
from engine 2.4.1 docs (read 2026-10-24); a `422 ... 0 options` or field
error usually means the running server is older than that (check
`release_date` in `/v1/models` — task expansion arrived in 2.4). Compare
versions first, field names second, server health last. What actually passed
on our builds: `references/tested-results.md`.

## Privacy

1. Run inference locally. Do not send media to an external API for this
   purpose.
2. Voice recordings of people are personal data. Confirm that the speakers
   consented before processing recordings from the community.
3. Keep machine paths, hostnames and credentials out of this repository.

## Reporting results

Every reported number needs: sample size, labeling method, model and engine
version, threshold, and a link to the data or fixture it can be reproduced
from. If the sample is small, say so in the same sentence as the number.
