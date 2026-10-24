---
name: basal-omni
description: Use when a task needs a typed decision from an image, scan, screenshot or audio recording (up to 30 seconds), or when choosing between basal-2.0 and basal-omni models, writing basal questions with allowed answers, fitting confidence thresholds, or evaluating basal on the user's own data. Trigger on basal-omni, basal-serve, POST /v1/systemone, decision from a document photo, classification of a recording, extraction of fields from a scan, verification of claims against a source. Use it even if the user does not name the model but asks for a local, calibrated, multiple-choice decision from media.
version: 0.1.0
author: Radoskop
license: MIT
metadata:
  tags: [basal, basal-omni, decisions, multimodal, calibration, inference]
---

# basal-omni

Guidance for using the basal decision models on media input. basal-omni
receives text, images or audio and returns a choice among answers that the
caller defines, with calibrated probabilities. It does not write free text.
The models are experimental; the engine is at 2.4.1 (2026-10-23), and ultra
and 1.1-max joined the omni family on 2026-10-17.

Companion skill: `basal-strategies` covers the community decision process
(Discord, methods, register). This skill covers model use. Shared principles — sources,
frozen definitions, no machine paths, owner approval before publishing — are
in the repository README.

## Workflow

1. Check the input. Text only → basal-2.0, not omni. Read
   `references/omni-routing.md` to pick a model.
2. Define the questions and the allowed answers before running anything.
   Read `references/omni-query-templates.md`. Freeze the category list under
   a version label.
3. If a confidence threshold is needed, fit it on labeled examples from the
   user's own process (`basal-calibrate`). Read
   `references/omni-evaluation-protocol.md`. Never reuse a text threshold for
   media.
4. Run inference locally:
   `basal-serve --model Remek/basal-omni-1.0-mini --mode eager --media on --port 8000`;
   media travel in the `media` field of the HTTP request (base64). Record
   model name, engine version, mode and calibration file with every result.
5. Route results below the threshold to a human (`act` or `tool` questions
   with `max_error`, which answer `"deferred": true`). Report counts of
   automatic and escalated cases separately.
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
   80 GB card for long states).
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

## Versions

Models and engine change quickly. Do not copy benchmark numbers into this
skill or into posts without a link and a read date. Link to the benchmark
page (`basal.si5.pl/benchmark/`) and the Hugging Face model card, and state
the date they were read. Record with every result: model name and weights
revision, engine version, mode, calibration file, codebook version. Results
from different versions are not comparable without stating the difference.

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
