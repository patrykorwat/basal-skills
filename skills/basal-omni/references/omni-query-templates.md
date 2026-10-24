# Query templates

Field names and request formats are copied from the engine documentation
(`github.com/rkinas/basal`, `docs/API.md`, `docs/INSTALL.md`, `docs/TASKS.md`;
read 2026-10-24, engine 2.4.1). If the docs change, trust the docs over the
JSON below — never write requests from memory.

Every question is defined by four things: the media input, the question text
(`instructions`), the allowed answers (`criteria` / `claims` / `schema`), and
the schema type. Define all four before running a model.

## Rules for writing questions

1. List allowed answers explicitly. Include an option for "none of these" or
   "not determinable" when the media may be unreadable.
2. Write one question per decision. Several questions about one state go in
   one request and share the state (SOAM) — faster than separate calls, same
   answers.
3. Keep answer labels short and mutually exclusive for `choice`.
4. Freeze the wording and label list under a version label such as
   `codebook v1`. Change them only by creating `v2`. Never edit a frozen
   version silently.
5. Write questions in the language of the media. Polish and English are
   supported; pass `"lang"` when the state text does not show the language.

## Serving for media (basal-omni)

```bash
uv pip install "basal[media] @ https://github.com/rkinas/basal/archive/refs/tags/v2.4.1.tar.gz"
basal-serve --model Remek/basal-omni-1.0-mini --mode eager --media on --port 8000   # or -1.0-max
```

## Base request shape (`POST /v1/systemone`)

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

Text example (from the engine README):

```bash
curl -s localhost:8000/v1/systemone -H 'content-type: application/json' -d '{
  "state": "Klient: od wczoraj nie mogę zalogować się do bankowości internetowej, system pokazuje błąd hasła.",
  "questions": {
    "dept":   {"type": "choice", "instructions": "Do którego działu skierować zgłoszenie?",
               "criteria": {"cards": "Reklamacje kart", "online": "Wsparcie bankowości elektronicznej", "loans": "Kredyty"}},
    "urgent": {"type": "noul", "instructions": "Czy klient nie może korzystać z usługi?"}}}'
```

Media example (a receipt; from `docs/INSTALL.md` — same shape for any scan;
for audio use `{"type": "audio", "data": "<base64>"}`, WAV/FLAC/OGG/MP3 up to
30 s, max 8 items / 20 MB each per request):

```bash
IMG=$(base64 < paragon.jpg | tr -d '\n')
curl -s localhost:8000/v1/systemone -H 'content-type: application/json' -d '{
  "state": "", "lang": "pl",
  "media": [{"type": "image", "data": "'"$IMG"'"}],
  "questions": {
    "card": {"type": "noul", "instructions": "Czy zapłacono kartą?"},
    "vat":  {"type": "choice", "instructions": "Jaka jest najwyższa stawka VAT na paragonie?",
             "criteria": {"23": "23%", "8": "8%", "5": "5%", "0": "0% lub zwolniony"}}}}'
```

Each answer carries `probabilities` (calibrated) and `confidence`; media
answers additionally carry `"calibration": "text"` — see the evaluation
protocol before automating.

## Templates for the community decision process

### Classify a proposal (choice)

Input: text of a proposal, or a screenshot of a Discord thread (then
`"state": ""` plus the image in `media`).

Question: what type of decision does this proposal ask for. Answers:
`yes_no_vote`, `prioritization`, `budget`, `missing_expertise`,
`prediction`, `process_change`, `other` — use the playbook categories from
the `basal-strategies` skill references so the labels match the decision
register. Add
`unclear` whenever the screenshot may be unreadable.

### Check a claim against a source (verify, experimental)

Task endpoint (`POST /v1/basal`), shape from `docs/TASKS.md`:

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
`supported` blocks the claim until a human checks it — this implements the
rule that every number links to its source.

### Extract fields from a scan (extract, experimental)

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
questions over the image instead, and check extracted values against the
original image on a sample before trusting the rest.

### Classify a short recording (choice)

Input: audio up to 30 s in `media`. Question: what does the speaker ask for.
Answers: defined per process, always with an `unclear` option.

### Escalation (act)

```jsonc
{"type": "act", "instructions": "...",
 "criteria": {"true": "...", "false": "..."},
 "costs": {"auto": {"wrong": 99, "right": 0}, "human": {"true": 15, "false": 15}},
 "max_error": 0.05}
```

`"deferred": true` means the case goes to a person; report those counts
separately.

## What not to ask

1. Requests for summaries or free text. basal does not generate text. Use a
   generative model for that and use basal to check (`verify`) or route the
   result.
2. Questions whose answers depend on information outside the media, unless
   that information is added as state text in the same call.
3. Arithmetic inside a decision — compute it in code or use `"facts": "auto"`
   for Polish dates and amounts.
