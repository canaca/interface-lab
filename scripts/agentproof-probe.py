#!/usr/bin/env python3
"""Fetch the AgentProof concept URLs and append one JSONL line to probe-log.

Hits https://canaca.github.io/interface-lab/agentproof/ with a few agent-like
User-Agent strings. Prints the same line to stdout. POST /authorization-proof
is recorded and is expected to fail: GitHub Pages cannot run it.
"""

import json
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

BASE = "https://canaca.github.io/interface-lab/agentproof/"
LOG = Path(__file__).resolve().parent.parent / "probe-log"
UAS = (
    "Mozilla/5.0 (compatible; GPTBot/1.2; +https://openai.com/gptbot)",
    "ClaudeBot/1.0; +https://www.anthropic.com",
    "PerplexityBot/1.0; +https://www.perplexity.ai/perplexitybot",
)
FILES = (
    ("index", ""),
    ("llms.txt", "llms.txt"),
    ("openapi.json", "openapi.json"),
    ("agent.json", ".well-known/agent.json"),
    ("mcp.json", "mcp.json"),
    ("status.json", "status.json"),
)
LINKS = ("llms.txt", "openapi.json", ".well-known/agent.json")
POST_BODY = json.dumps({
    "merchant_platform": "shopify",
    "purchase": {
        "money": {"amount": "1.00", "currency": "USD"},
        "summary": "AgentProof concept probe. Not a real order.",
    },
    "human_authorization": {
        "confirmed_at": "2026-10-13T00:00:00Z",
        "what_was_shown": "Concept probe only. Do not charge anyone.",
    },
}).encode()


def fetch(url, ua, method="GET", body=None):
    headers = {"User-Agent": ua, "Accept": "application/json, text/plain, text/html, */*"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=20) as res:
            return res.status, res.geturl(), res.headers.get("Content-Type"), res.read(250000), None
    except urllib.error.HTTPError as err:
        ctype = err.headers.get("Content-Type") if err.headers else None
        return err.code, getattr(err, "url", url), ctype, err.read(250000), None
    except (urllib.error.URLError, TimeoutError, OSError) as err:
        return None, url, None, b"", f"{type(err).__name__}: {err}"


def record(status, url, ctype, raw, error, ua):
    return {"ua": ua, "status": status, "url": url, "content_type": ctype, "bytes": len(raw), "error": error, "raw": raw}


def linked(html, rel):
    return any(n in html for n in (f'href="{rel}"', f"href='{rel}'", f'href="{BASE}{rel}"', f"href='{BASE}{rel}'"))


def loads(raw):
    try:
        return json.loads(raw.decode()), None
    except (UnicodeError, json.JSONDecodeError) as err:
        return None, f"{type(err).__name__}: {err}"


def check_openapi(doc):
    paths = doc.get("paths") if isinstance(doc, dict) else None
    paths = paths if isinstance(paths, dict) else {}
    post = isinstance((paths.get("/authorization-proof") or {}).get("post"), dict)
    get = isinstance((paths.get("/status") or {}).get("get"), dict)
    version = doc.get("openapi") if isinstance(doc, dict) else None
    mark = doc.get("x-status") if isinstance(doc, dict) else None
    ok = isinstance(version, str) and version.startswith("3.1") and mark == "concept" and post and get
    return {"ok": ok, "openapi": version, "x-status": mark, "post": post, "get": get}


def main():
    fetched = {}
    for name, rel in FILES:
        fetched[name] = [record(*fetch(BASE + rel, ua), ua) for ua in UAS]

    def body(name):
        rows = fetched[name]
        for row in rows:
            if row["status"] == 200 and row["raw"]:
                return row["raw"]
        return rows[0]["raw"] if rows else b""

    flags = [{rel: linked(row["raw"].decode("utf-8", "replace"), rel) for rel in LINKS} for row in fetched["index"]]
    discoverability = flags[0] if flags else {rel: False for rel in LINKS}

    parsed = {}
    specs = (
        ("openapi.json", check_openapi),
        ("agent.json", None),
        ("mcp.json", None),
        ("status.json", None),
    )
    for name, extra in specs:
        doc, err = loads(body(name))
        if err:
            parsed[name] = {"ok": False, "error": err}
        elif name == "openapi.json":
            parsed[name] = extra(doc)
        elif name == "status.json":
            want = {"status": "concept", "accepting": "waitlist"}
            parsed[name] = {"ok": doc == want, "value": doc if isinstance(doc, dict) else None}
        else:
            mark = doc.get("x-status") if isinstance(doc, dict) else None
            parsed[name] = {"ok": isinstance(doc, dict) and mark == "concept", "x-status": mark}

    status, url, ctype, raw, error = fetch(BASE + "authorization-proof", "AgentProofProbe/0.1 (concept)", "POST", POST_BODY)
    post = record(status, url, ctype, raw, error, "AgentProofProbe/0.1 (concept)")
    post["snippet"] = " ".join(raw.decode("utf-8", "replace").split())[:180]
    post["executed"] = False
    post.pop("raw", None)

    for rows in fetched.values():
        for row in rows:
            row.pop("raw", None)

    files_ok = all(row["status"] == 200 and not row["error"] for rows in fetched.values() for row in rows)
    ok = files_ok and all(item.get("ok") for item in parsed.values()) and all(discoverability.values()) and flags.count(discoverability) == len(flags)
    line = json.dumps({
        "ts": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "base": BASE,
        "ok": ok,
        "discoverability": discoverability,
        "parsed": parsed,
        "fetches": fetched,
        "post_authorization_proof": post,
    }, ensure_ascii=False, separators=(",", ":"))
    with LOG.open("a", encoding="utf-8") as fh:
        fh.write(line + "\n")
    print(line)


if __name__ == "__main__":
    main()
