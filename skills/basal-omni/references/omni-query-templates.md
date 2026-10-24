# Query templates

Field names and request formats are copied from the engine documentation
(`github.com/rkinas/basal`: `docs/API.md`, `docs/INSTALL.md`, `docs/TASKS.md`;
read 2026-10-24, engine 2.4.1). If the docs change, trust the docs over the
JSON below. Never write requests from memory.

Every question is defined by four things: the media input, the question text
(`instructions`), the allowed answers (`criteria` / `claims` / `schema`), and
the schema type. Define all four before running a model.

## Rules for writing questions

1. List allowed answers explicitly. Include an option for "none of these" or
   "not determinable" when the media may be unreadable.
2. Write one question per decision. Several questions about one state go in
   one request and share the state; per `docs/API.md` this is faster than
   separate calls and gives the same answers (SOAM).
3. Keep `choice` labels short and mutually exclusive.
4. Freeze wording and label list under a version label such as
   `codebook v1`. Change them only by creating `v2`. Never edit a frozen
   version silently.
5. Write questions in the language of the media. Polish and English are
   supported; pass `"lang"` when the state text does not show the language.

## Endpoints

`POST /v1/systemone` answers every decision type. `POST /v1/basal` is the
same endpoint and additionally expands the experimental task types
(`classify`, `verify`, `compress`, `extract`); task types are accepted on
both endpoints and a request may mix task and decision questions
(`docs/TASKS.md`). Canonical practice: decisions to `/v1/systemone`, task
requests to `/v1/basal`.

## Serving

```bash
uv pip install "basal[media] @ https://github.com/rkinas/basal/archive/refs/tags/v2.4.1.tar.gz"
# general decisions:
basal-serve --model Remek/basal-omni-1.0-mini --mode eager --media on --port 8000   # or -1.0-max
# task types (classify/verify/compress/extract), trained on the task formats:
basal-serve --model Remek/basal-omni-1.1-max --mode eager --media on --port 8000
```

`basal-omni-pico` is text only despite the name. Media need an NVIDIA GPU
with `--media on`.

## Base request shape (`POST /v1/systemone`)

The block is annotated (jsonc), not valid JSON: strip the `//` comments or
use the field table below it.

```jsonc
{
  "state": "text or JSON",
  "questions": {
    "name": {"type": "choice", "instructions": "...",
             "criteria": {"key": "description", "other": "..."}},
    "yesno": {"type": "noul", "instructions": "..."}
  },
  "media": [{"type": "image", "data": "<base64>"}],  // optional, --media on only
  "detail": "high",   // optional: small print, 1,120 tokens/image (default 280)
  "lang": "pl"        // optional
}
```

| field | meaning |
|---|---|
| `state` | context text or JSON; empty when the media carries the input |
| `questions` | named, typed questions (see `omni-routing.md` for the type table) |
| `media` | list of `{type: image\|audio, data: base64}`; audio WAV/FLAC/OGG/MP3 up to 30 s, max 8 items, 20 MB each |
| `detail` | `high` reads small print; 1,120 tokens per image instead of 280 |
| `lang` | `pl` or `en`; needed when the state text does not show the language |
| `facts` | `auto` adds computed Polish dates and amounts (not shown above) |

## Examples

Text (from the engine README):

```bash
curl -s localhost:8000/v1/systemone -H 'content-type: application/json' -d '{
  "state": "Klient: od wczoraj nie mogę zalogować się do bankowości internetowej, system pokazuje błąd hasła.",
  "questions": {
    "dept":   {"type": "choice", "instructions": "Do którego działu skierować zgłoszenie?",
               "criteria": {"cards": "Reklamacje kart", "online": "Wsparcie bankowości elektronicznej", "loans": "Kredyty"}},
    "urgent": {"type": "noul", "instructions": "Czy klient nie może korzystać z usługi?"}}}'
```

Image (a receipt; same shape for any scan). Do not inline the base64 into
`-d '...'`: one shell argument is capped near 128 KB on Linux and an encoded
photo exceeds it, which fails with `Argument list too long`. Build the body
in a file instead:

```bash
jq -n --rawfile img <(base64 -w0 paragon.jpg) '{
  state: "", lang: "pl", detail: "high",
  media: [{type: "image", data: $img}],
  questions: {
    card: {"type": "noul", "instructions": "Czy zapłacono kartą?"},
    vat:  {"type": "choice", "instructions": "Jaka jest najwyższa stawka VAT na paragonie?",
           "criteria": {"23": "23%", "8": "8%", "5": "5%", "0": "0% lub zwolniony"}}}}' > request.json
curl -s localhost:8000/v1/systemone -H 'content-type: application/json' -d @request.json
```

For audio use `{"type": "audio", "data": "<base64>"}`. Each answer carries
`probabilities` (calibrated) and `confidence`; media answers additionally
carry `"calibration": "text"`, see the calibration rule below.

## Compatibility matrix

Documented means the docs state it; Tested means it ran in this project.
Everything else is untested: assume nothing until your own check.

| question type | text | image | audio | basis |
|---|---|---|---|---|
| `choice`, `noul` | yes | yes | yes | documented (INSTALL.md example) |
| `score`, `multi`, `act`, `tool` | yes | untested | untested | `media` is request-level, no per-type note |
| `classify`, `verify`, `compress`, `extract` | yes | untested | untested | TASKS.md measures text sets only |
| model `ultra` | yes | yes | **no** | documented (model card + README) |
| model `mini`, `max` | yes | yes | yes | documented (`--media on`) |

Text decisions (`choice`, `noul`, `act`, `facts: auto`) were Tested on
basal-omni-1.0-ultra-FP8 in vllm mode on 2026-10-24. Task types were not:
that build did not expand them (engine 2.3.0, `release_date` 2026-10-05);
retest after upgrading to 2.4.1.

## Templates for the community decision process

### Classify a proposal (choice)

Input: text of a proposal, or a screenshot of a Discord thread (then
`"state": ""` plus the image in `media`, with `detail: "high"`).

Question: what type of decision does this proposal ask for. Labels mirror
the eight situations of the `basal-strategies` playbook, so the classifier
and the decision register share one vocabulary: `yes_no_vote`,
`prioritization`, `budget`, `missing_expertise`, `prediction`,
`polarizing_decision`, `ai_in_loop`, `process_change`, plus `other` and
`unclear` as separate options.

### Check a claim against a source (verify, experimental)

Serve `basal-omni-1.1-max` for task types. Shape from `docs/TASKS.md`:

```jsonc
{
  "state": "<the source text, or the source plus the draft>",
  "questions": {
    "claims": {"type": "verify",
               "claims": {"claim1": "<claim from the draft post>"}}
  }
}
```

Verdict per claim: `supported` / `contradicted` / `not_stated`, with
probabilities. Use before publishing any number. A result other than
`supported` blocks the claim until a human checks it; this implements the
rule that every number links to its source.

### Extract fields from document text (extract, experimental)

`extract` fills a JSON schema with values copied exactly from the document,
with character offsets; it does not rephrase. Shape from `docs/TASKS.md`:

```jsonc
{
  "state": "<document text>",
  "questions": {
    "inv": {"type": "extract", "schema": {"type": "object", "properties": {
      "invoice_number": {"type": "string", "description": "the invoice number"},
      "gross_total": {"type": "number"},
      "payment_method": {"enum": ["transfer", "card", "cash"]}}}}}
}
```

Known limits (engine 2.1 tasks): `extract` does not yet return lists of
objects (line items) and does not read text fields out of an image. For a
scan of a resolution or minutes, ask the needed fields as `choice` / `noul`
questions over the image (with `detail: "high"`), and check extracted
values against the original image on a sample before trusting the rest.

### Classify a short recording (choice)

Input: audio up to 30 s in `media`. Question: what does the speaker ask for.
Answers: defined per process, always with `unclear`.

### Escalation (act)

The numbers below are placeholders, not recommendations. Costs are in your
own unit (currency, review minutes, reputation points); choose them so a
wrong automatic action costs clearly more than a human review.

```jsonc
{"type": "act", "instructions": "...",
 "criteria": {"true": "...", "false": "..."},
 "costs": {"auto": {"wrong": "<COST_WRONG>", "right": 0},
           "human": {"true": "<COST_REVIEW>", "false": "<COST_REVIEW>"}},
 "max_error": 0.05}
```

The `<...>` entries stand for numbers (the cost of a wrong automatic action
and of one human review); replace them before sending.

`max_error` is the tolerated error rate. The answer carries `"deferred":
true` (and `refused` names the automatic action) whenever the confidence
falls below the threshold certified for that question type and target;
without a certified threshold every automatic action is refused, which is
the safe default, not an error. Report deferred counts separately. An `act`
question over media is untested; ask it as a text question over an `noul`
readout of the media instead.

## Calibration rule for media answers

A media answer carries `"calibration": "text"` whenever the temperatures and
thresholds were fitted on text. Treat the flag as a hard gate: do not
automate such answers until validated on your own labeled media, and serve
the server with your own `--calibration` file once that validation exists
(`docs/CALIBRATION.md`). Write templates so each request can be logged as
one JSONL line with its gold answer; `basal-calibrate` consumes that file
(one request per line, since release 2.2).

## What not to ask

1. Summaries or free text. basal does not generate text; use a generative
   model for that, then use basal to check (`verify`) or route the result.
2. Answers that depend on information outside the media, unless that
   information is added as state text in the same call.
3. Arithmetic inside a decision: compute it in code, or use `"facts": "auto"`
   for Polish dates and amounts.
