# Evaluation protocol for the user's own data

Published media results come from small samples (5 runs per modality), and
the omni calibration is fitted on text — media answers carry
`"calibration": "text"`. Your data decides.

## Steps

0. If you have no labeled, checkable dataset yet, measure first: collect
   30–50 decisions with known answers (rule compliance, categories, claims
   vs sources) and compare the model's verdicts to humans before anything
   enters the process. On value questions there is no dataset to fit, so
   skip automation entirely (see the checkable/value rule).
1. Collect labeled examples from the real process. Practical floor: the
   engine's `basal-calibrate` needs at least 50 labeled decisions per
   question type for a full fit (`--min-per-type 50`; below that, down to 10,
   it blends with the shipped file). Plan about 100 per question type so both
   the fitting set and the held-out set have usable numbers per type. State
   the actual size in every report.
2. Label with a written guide. If two people label, report their agreement
   before reporting model accuracy.
3. Split into a fitting set and a held-out set. Fit the threshold only on the
   fitting set. Note: `basal-calibrate` splits its own input 70/30 into FIT
   and CERT internally — your held-out set must be separate from that file.
4. Run each candidate model on the held-out set: mini and max for audio, max
   and ultra for images, as applicable.
5. Report per question: accuracy, accuracy among cases above the threshold,
   share of cases escalated to a human, and the 95 percent confidence
   interval.
6. Compare with a baseline the user already has (rules, a larger general
   model, manual work). A model is chosen only if it beats the baseline on
   the held-out set at an acceptable escalation rate.
7. Repeat after any change of model, engine version, mode, calibration file,
   question wording or label list.

## Calibration

Use `basal-calibrate` instead of choosing thresholds by hand:

```bash
basal-calibrate labelled.jsonl --model Remek/basal-omni-1.0-max --mode eager    # writes CALIBRATION.custom.json
basal-serve --model Remek/basal-omni-1.0-max --mode eager --media on --calibration CALIBRATION.custom.json
```

The calibration file knows the model it was fitted on. Record the file name
and date in the result log.

## Result log fields

1. Date and operator.
2. Model name and weights revision.
3. Engine version and mode.
4. Calibration file.
5. Codebook version and question wording.
6. Dataset name, size and labeling method.
7. Metrics with confidence intervals.
8. Decision: adopted, rejected, or needs more data.

## Do not

1. Reuse a threshold fitted on text for images or audio.
2. Compare numbers from different codebook versions without stating the
   difference.
3. Report a result from fewer than 30 examples per class as an accuracy
   figure. Report it as an observation. (The 30 matches the engine's own
   minimum for fitting a label-set threshold, `--min-per-set`; the 100 per
   question type is our convention, not a published requirement — adjust to
   what `basal-calibrate` reports for your data.)
