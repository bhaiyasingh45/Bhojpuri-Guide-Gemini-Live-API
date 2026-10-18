# Bhojpuri Guide (Gemini Live API)

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then put your GEMINI_API_KEY in .env
uvicorn server:app --reload --port 8000
```
Open http://localhost:8000 (localhost is allowed to use the microphone; any other host needs HTTPS).

## Health check
`GET /health` returns `{"status":"ok","regions":[...],"web_search":true|false}` (it only says whether a Tavily key is set, never the key).

## Web search
The model has a `web_search` tool backed by Tavily. Add `TAVILY_API_KEY` to your env file; without it the tool replies that search is not configured. The UI status line shows the query while a search runs.

## Regions
A dropdown under the top bar switches the destination: **India** (guide speaks Bhojpuri, Indian places) or **Abu Dhabi** (guide speaks Arabic, mosques/museums such as Sheikh Zayed Grand Mosque and Louvre Abu Dhabi). The browser connects to `/ws?region=india|abudhabi`; `server.py` picks the matching system prompt (`REGIONS`). Switching while live restarts the session in the new language. Verified 2026-10-15 that the Live model answers in Arabic with audio.

## Traveller name
Both guides are told the traveller is "Bhaiya Ji" and must always use that name (Bhojpuri: भइया जी, Arabic: بهَيَّا جي). Edit the "THE TRAVELLER'S NAME" block in each prompt in `server.py` to change it.

## Tests
```bash
pip install -r requirements-dev.txt
python -m pytest tests
```
Covers the health endpoint, the language/name guardrails in the prompts, and the search tool without a key. No network or real API keys are used.

## Notes
- Audio-only Live sessions are limited to 15 minutes unless you add session management.
- Use headphones to avoid echo.

## UI
Single page in `static/index.html` (no build step): mobile-app layout (full screen on phones, phone-shaped frame on desktop) with a bottom tab bar (Talk / Places / Chat), pulsing mic button while live, and an "A product from Bhaiya & Company" footer.

## Images
The browser tab icon is `static/favicon.svg`.

Place photos in `static/img/` (16 files, 330px wide) were downloaded from the lead images of the matching English Wikipedia articles (Wikimedia Commons; each file keeps its own CC / public-domain licence, so check the file's Commons page and credit the author before any public release). Articles used: Dashashwamedh Ghat, Taj Mahal, Jaipur, Mahabodhi Temple, India Gate, Golden Temple, Kerala backwaters, Goa, Sheikh Zayed Grand Mosque, Louvre Abu Dhabi, Qasr Al Watan, Emirates Palace, Qasr Al Hosn, Yas Island, Corniche (Abu Dhabi), Saadiyat Island. The Talk tab hero shows the Taj Mahal (India) or Sheikh Zayed Grand Mosque (Abu Dhabi) by default and changes to the photo and name of whichever place you tap.
