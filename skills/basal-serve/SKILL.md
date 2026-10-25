---
name: basal-serve
description: Use when a task needs a typed, calibrated decision from a local basal server (text, image, scan, screenshot or audio up to 30 seconds), when choosing between basal-2.0 (text) and basal-omni (media) models, writing basal questions with allowed answers, fitting confidence thresholds, or evaluating basal on the user's own data. Trigger on basal-serve, basal-2.0, basal-omni, POST /v1/systemone, /v1/basal, decision from a document photo, classification of a recording, extraction of fields from document text, verification of claims against a source. Use it even if the user does not name the model but asks for a local, calibrated, multiple-choice decision from text or media.
version: 0.5.1
author: Radoskop
license: MIT
metadata:
  tags: [basal, basal-serve, basal-2.0, basal-omni, decisions, calibration, inference]
---

# basal-serve

Basal answers typed questions about state you supply — a Choice among
options you define, a Noul (probability a statement is true), a Score on
levels, a Multi, an Act or Tool with error costs — returning calibrated
probabilities. It does not write free text. **basal-2.0** for text-only
decisions, **basal-omni** for media. Companion skill `basal-strategies`
covers the community decision process; this skill covers the connection.

## Live docs first

The engine and models change faster than this file. Read the relevant page
as part of the task and copy JSON shapes from it, never from memory:

- API reference (request/response, question types, extensions):
  [API.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/API.md);
  task types: [TASKS.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/TASKS.md);
  media: [OMNI.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/OMNI.md);
  calibration: [CALIBRATION.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/CALIBRATION.md);
  serving: [INSTALL.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/INSTALL.md).
- Model, benchmark and serving pages: [basal.si5.pl/models](https://basal.si5.pl/models/) and
  [basal.si5.pl/serwer-inferencji](https://basal.si5.pl/serwer-inferencji/).
- If live access is unavailable, say so and leave out version-dependent
  details rather than guessing them.

## Workflow

1. **Start from the decision logic.** Write the truth table or rules that
   decide the outcome; list their inputs. Inputs needing language or media
   understanding make good questions; arithmetic, dates and exact lookups
   belong in code. Give every combination of answers an outcome, including
   the case where a Noul lands between thresholds.
2. **Define the questions and allowed answers before running anything.**
   Freeze the wording and label list under a version label (`codebook v1`);
   change it only by creating `v2`, never silently.
3. **Test on the user's real data** before adopting anything: representative
   cases, hard cases, and cases whose answer is "no" or "nothing fits".
   Fit any threshold with `basal-calibrate` on labeled examples — see
   Confidence below. Record model name, weights revision, engine version,
   mode and calibration file with every result.
4. **Route uncertain cases to a human** (`act`/`tool` with `max_error`
   answering `"deferred": true`). Report automatic and escalated counts
   separately. Publish nothing community-facing without owner approval of
   the exact text.

## Writing questions

- List allowed answers explicitly; include "none of these" or "not
determinable" when media may be unreadable.
- One judgment per question. Two conditions joined by "or"/"and" work better
  as two questions; ask a Noul per statement when more than one can be true
  (a Choice would split probability between them).
- Ask the concrete, observable thing a person could point to; write plainly
  — option descriptions belong in `criteria`, not in the question.
- Bundle questions that share the state into one request (SOAM): the state
  is read once and questions run in parallel. Questions cannot see each
  other's answers, so context belongs in the state or in that question.
- Write questions in the language of the media; pass `"lang"` when the state
  text does not show it.
- When a model judges independently of human votes (hybrid confirmation in
  `basal-strategies`), keep the votes, tallies and discussion out of the
  `state` entirely.

## Model routing

Re-read the live model page before relying on this; size never replaces a
test on the actual task.

| Input | Family | Notes |
|---|---|---|
| Text only | basal-2.0 (mini 1.5B → max 11B) | NVIDIA GPU, Mac MLX, Ollama, llama.cpp; pico 0.8B runs on CPU (812 MB GGUF) |
| Image, audio, or both | basal-omni (mini 4B, max 12B, ultra 31B) | NVIDIA GPU, `--mode eager --media on`, bf16; mini ~16 GB, max ~24 GB, ultra 59 GB weights |

Omnis: mini reads recordings best, max/ultra read document images best, ultra takes no audio; 1.1-max is the experimental-task build. Decision types and exact fields: [API.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/API.md); escalation semantics: `act`/`tool` with `max_error` refuse below the certified threshold — that is the safe default, not an error.

## Hard limits

1. Audio: WAV/FLAC/OGG/MP3, max 30 s per clip, max 8 media items and 20 MB
   each per request; longer recordings must be cut by the application.
2. No video input — the application extracts frames and the audio track.
3. Ultra (31B) reads text and images only, no audio; every `-GGUF`, `-MLX`
   and `-FP8` port is text only.
4. Media need an NVIDIA GPU in `--mode eager --media on` with bf16 weights;
   media travel base64 in the request. MCP tools have no media parameter —
   media go through the HTTP API only.
5. Omni calibration is fitted on text; media answers carry
   `"calibration": "text"` and their confidence is unverified until tested
   on the user's data. Published media benchmarks are small samples (5 runs
   per modality) — never present them as general accuracy. Werdykt measures
   text decisions only, for every model including omni.

## Confidence and thresholds

A probability is a calibrated ranking signal, not a guarantee, and it is
valid only for the model version, question design and data type it was
fitted on. Never reuse a text threshold for images or audio. The shipped
calibration files certify 5% target thresholds only — no 1% threshold is
certified except `choice` on basal-2.0-max-GGUF (ollama) — so `max_error:
0.01` defers everything else; use 0.05 or certify your own
([CALIBRATION.md](https://raw.githubusercontent.com/rkinas/basal/main/docs/CALIBRATION.md)).

**Checkable vs value questions.** Where a correct answer exists and can be
checked later (rule compliance, category, claim-vs-source), fit a threshold
with `basal-calibrate` on ≥50 labeled decisions per question type (~100
planned so fit and held-out sets both work; `basal-calibrate` splits its own
input 70/30, so keep a separate held-out set), and let it gate automation.
On value questions nothing labels the truth: report the number as an
opinion, start no action from it, never present it as a chance of being
right. Adopt a model only if it beats the user's existing baseline on the
held-out set at an acceptable escalation rate; repeat after any change of
model, engine, mode, calibration, wording or label list.

Every reported number needs: sample size, labeling method, model and engine
version, threshold, and a reproducible link; small samples get that caveat
in the same sentence.

## When an answer looks wrong

Check in order: the payload as actually sent; the state (could a person
answering from it alone make the call?); whether the right answer is among
the options; the question scope (can it be broken into smaller judgments);
the wording. A `422 ... 0 options` or field error usually means the running
server is older than the templates (task expansion arrived in 2.4 — check
`release_date` in `/v1/models`); compare versions first, field names
second. A template counts as "Tested" only with a dated, reproducible run
against a live server — say so when claiming it.

## Privacy

Run inference locally; never send media to an external API for this
purpose. Voice recordings of people are personal data — confirm consent
before processing community recordings. Keep machine paths, hostnames and
credentials out of reports and this repository.
