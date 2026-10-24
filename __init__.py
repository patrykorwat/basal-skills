"""basal-skills: Hermes plugin for the basal decision engine.

Registers two tools (basal_decide, basal_health) that talk to a local
basal-serve, and bundles the two skills shipped in this repo. Stdlib only.
"""

import base64
import json
import urllib.error
import urllib.request
from pathlib import Path

DECIDE_TYPES = {"choice", "noul", "score", "multi", "act", "tool"}
TASK_TYPES = {"classify", "verify", "compress", "extract"}
ALL_TYPES = DECIDE_TYPES | TASK_TYPES
MAX_MEDIA_BYTES = 20 * 1024 * 1024
DEFAULT_URL = "http://127.0.0.1:8000"


def _post(url: str, path: str, payload: dict, timeout: int = 300) -> dict:
    req = urllib.request.Request(
        url.rstrip("/") + path,
        data=json.dumps(payload).encode("utf-8"),
        headers={"content-type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:2000]
        return {"ok": False, "error": f"HTTP {exc.code}", "detail": detail}
    except Exception as exc:  # noqa: BLE001 - surface every transport failure
        return {
            "ok": False,
            "error": f"{type(exc).__name__}: {exc}",
            "hint": f"is basal-serve running at {url}? Start it per the "
            "basal-omni skill (eager --media on for media requests).",
        }


def _get(url: str, path: str, timeout: int = 15):
    req = urllib.request.Request(url.rstrip("/") + path, method="GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        body = resp.read().decode("utf-8")
        return json.loads(body) if body.strip() else {}


def _encode_media(media, errors: list) -> list:
    items = []
    for i, m in enumerate(media or []):
        if not isinstance(m, dict) or m.get("type") not in ("image", "audio"):
            errors.append(f"media[{i}]: need {{type: image|audio, path: ...}}")
            continue
        p = Path(str(m.get("path", ""))).expanduser()
        if not p.is_file():
            errors.append(f"media[{i}]: not a readable file: {p}")
            continue
        size = p.stat().st_size
        if size > MAX_MEDIA_BYTES:
            errors.append(f"media[{i}]: {p.name} is {size} bytes, limit 20 MB")
            continue
        items.append({"type": m["type"], "data": base64.b64encode(p.read_bytes()).decode()})
    return items


def _validate(questions: dict) -> tuple:
    """Return (endpoint, errors). Questions must pass before any request."""
    errors = []
    if not isinstance(questions, dict) or not questions:
        return "/v1/systemone", ["questions: non-empty object required"]
    endpoints = set()
    for name, q in questions.items():
        if not isinstance(q, dict):
            errors.append(f"{name}: must be an object with a type")
            continue
        qtype = q.get("type")
        if qtype not in ALL_TYPES:
            errors.append(f"{name}: unknown type {qtype!r}; use one of {sorted(ALL_TYPES)}")
            continue
        endpoints.add("/v1/basal" if qtype in TASK_TYPES else "/v1/systemone")
        if qtype in ("choice", "multi") and not isinstance(q.get("criteria"), (dict, list)):
            errors.append(f"{name}: {qtype} needs criteria (dict of key->description, or list)")
        if qtype == "score" and not isinstance(q.get("criteria"), list):
            errors.append(f"{name}: score needs criteria as an ordered list of levels")
        if qtype == "act" and not isinstance(q.get("costs"), dict):
            errors.append(f"{name}: act needs costs (action -> outcome costs); add a human/defer action")
        if qtype == "tool" and not q.get("tools"):
            errors.append(f"{name}: tool needs tools (OpenAI/MCP/Anthropic definitions)")
        if qtype == "verify" and not isinstance(q.get("claims"), dict):
            errors.append(f"{name}: verify needs claims as a dict of key -> claim text")
        if qtype == "extract" and not isinstance(q.get("schema"), dict):
            errors.append(f"{name}: extract needs a JSON schema dict")
        if qtype == "classify" and not isinstance(q.get("labels"), list):
            errors.append(f"{name}: classify needs labels (list of name+rubric)")
        if "max_error" in q and q["max_error"] not in (0.01, 0.05, 0.1):
            errors.append(f"{name}: max_error should be 0.01, 0.05 or 0.1")
    if len(endpoints) > 1:
        errors.append("cannot mix question types from /v1/systemone and /v1/basal in one request")
        endpoints = {"/v1/systemone"}
    return (endpoints.pop() if endpoints else "/v1/systemone"), errors


def basal_decide(args: dict) -> str:
    url = str(args.get("url") or DEFAULT_URL)
    errors: list = []
    questions = args.get("questions") or {}
    endpoint, errors = _validate(questions)
    payload: dict = {"state": args.get("state", ""), "questions": questions}
    if isinstance(payload["state"], dict):
        pass  # server serialises JSON states itself
    media = _encode_media(args.get("media"), errors)
    if media:
        payload["media"] = media
    for key in ("lang", "detail", "facts"):
        if args.get(key):
            payload[key] = args[key]
    if errors:
        return json.dumps({"ok": False, "errors": errors,
                           "note": "nothing was sent; fix the questions first"})
    result = _post(url, endpoint, payload)
    if "answers" in result or "model" in result:
        return json.dumps({"ok": True, "endpoint": endpoint, "response": result})
    return json.dumps({"ok": False, "endpoint": endpoint, "response": result})


def basal_health(args: dict) -> str:
    url = str(args.get("url") or DEFAULT_URL)
    try:
        health = _get(url, "/health")
        models = _get(url, "/v1/models").get("models", [])
        return json.dumps({
            "ok": True,
            "url": url,
            "status": health.get("status"),
            "running": health.get("running"),
            "queued": health.get("queued"),
            "models": [{"name": m.get("name"), "mode": m.get("mode")} for m in models],
        })
    except Exception as exc:  # noqa: BLE001
        return json.dumps({"ok": False, "url": url,
                           "error": f"{type(exc).__name__}: {exc}",
                           "hint": "start basal-serve, e.g. "
                           "basal-serve --model Remek/basal-omni-1.0-mini "
                           "--mode eager --media on --port 8000"})


DECIDE_SCHEMA = {
    "name": "basal_decide",
    "description": (
        "Ask a local basal-serve (github.com/rkinas/basal) for typed, "
        "calibrated decisions over text, images or audio. One call answers "
        "named questions over one shared state. Types: choice, noul, score, "
        "multi, act, tool via /v1/systemone; classify, verify, compress, "
        "extract via /v1/basal. Media (images/audio up to 30 s) travel as "
        "local file paths and are base64-encoded here. Answers carry "
        "calibrated probabilities; media answers carry calibration=text and "
        "need validation on your own data first. Load the basal-omni skill "
        "for question design and thresholds before automating."
    ),
    "parameters": {
        "type": "object",
        "properties": {
            "url": {"type": "string",
                    "description": f"Server base URL, default {DEFAULT_URL}"},
            "state": {"type": "string",
                      "description": "Context text or JSON; empty when the media carries the input"},
            "questions": {"type": "object",
                          "description": "Named typed questions, e.g. "
                          '{"dept": {"type": "choice", "instructions": "...", '
                          '"criteria": {"cards": "Reklamacje kart", "online": "Bankowo\u015b\u0107"}}; '
                          'escalation: {"act", "costs": {...}, "max_error": 0.05}'},
            "media": {"type": "array",
                      "items": {"type": "object",
                                "properties": {"type": {"enum": ["image", "audio"]},
                                               "path": {"type": "string"}}},
                      "description": "Local files for the request; audio max 30 s, 20 MB each, max 8 items"},
            "lang": {"type": "string", "enum": ["pl", "en"]},
            "detail": {"type": "string", "enum": ["default", "high"],
                       "description": "high reads small print (1,120 tokens/image)"},
            "facts": {"type": "string", "enum": ["off", "auto"],
                      "description": "auto adds computed Polish dates and amounts to the state"},
        },
        "required": ["questions"],
    },
}

HEALTH_SCHEMA = {
    "name": "basal_health",
    "description": ("Check a local basal-serve: /health (running, queued) and "
                    "the served model and mode. Run before first use of "
                    "basal_decide."),
    "parameters": {
        "type": "object",
        "properties": {"url": {"type": "string",
                               "description": f"Server base URL, default {DEFAULT_URL}"}},
    },
}


def register(ctx):
    ctx.register_tool(name="basal_decide", toolset="basal",
                      schema=DECIDE_SCHEMA, handler=basal_decide)
    ctx.register_tool(name="basal_health", toolset="basal",
                      schema=HEALTH_SCHEMA, handler=basal_health)
    skills_dir = Path(__file__).parent / "skills"
    for child in sorted(skills_dir.iterdir()):
        skill_md = child / "SKILL.md"
        if child.is_dir() and skill_md.exists():
            ctx.register_skill(child.name, skill_md)
