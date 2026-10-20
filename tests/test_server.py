import asyncio
import os
import sys
from pathlib import Path

# server.py reads the key at import time; tests never call Gemini, so a dummy is enough.
os.environ.setdefault("GEMINI_API_KEY", "test-key")
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import server  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402


def test_health_lists_regions():
    r = TestClient(server.app).get("/health")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] == "ok"
    assert set(body["regions"]) == {"india", "abudhabi"}


def test_prompts_lock_language_and_name():
    india = server.REGIONS["india"]["prompt"]
    arabic = server.REGIONS["abudhabi"]["prompt"]
    assert "Speak ONLY in Bhojpuri" in india
    assert "Speak ONLY in Arabic" in arabic
    for prompt in (india, arabic):
        assert "STRICT" in prompt
        assert "Bhaiya Ji" in prompt


def test_web_search_without_key_reports_not_configured(monkeypatch):
    monkeypatch.setattr(server, "TAVILY_API_KEY", None)
    result = asyncio.run(server.web_search("taj mahal timings"))
    assert "not configured" in result["error"]


def test_live_config_has_search_tool_for_each_region():
    for region in server.REGIONS:
        cfg = server.live_config(region)
        assert cfg.tools, region


def test_web_search_rejects_empty_query(monkeypatch):
    monkeypatch.setattr(server, "TAVILY_API_KEY", "dummy")
    for q in ("", "   ", None):
        assert asyncio.run(server.web_search(q))["error"] == "Empty search query."
