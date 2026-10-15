# Bhojpuri Guide (Gemini Live API)

## Run
```bash
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env          # then put your GEMINI_API_KEY in .env
uvicorn server:app --reload --port 8000
```
Open http://localhost:8000 (localhost is allowed to use the microphone; any other host needs HTTPS).

## Web search
The model has a `web_search` tool backed by Tavily. Add `TAVILY_API_KEY` to your env file; without it the tool replies that search is not configured. The UI status line shows the query while a search runs.

## Notes
- Audio-only Live sessions are limited to 15 minutes unless you add session management.
- Use headphones to avoid echo.

## UI
Single page in `static/index.html` (no build step): mobile-app layout (full screen on phones, phone-shaped frame on desktop) with a bottom tab bar (Talk / Places / Chat), pulsing mic button while live, and an "A product from Bhaiya & Company" footer.
