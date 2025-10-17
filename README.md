# Coach Backend

Baseball coaching backend powered by Django and Django REST Framework. It stores game situations, generates strategic recommendations for the next play, and exposes them through a JSON API that future web and mobile clients can consume. A React-based single-page application is available in the `frontend/` directory to capture a play scenario and display the engine's recommendation.

## Getting Started

1. Create a virtual environment and install dependencies:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Apply the initial database migration:
   ```bash
   python manage.py migrate
   ```
3. Run the development server:
   ```bash
   python manage.py runserver
   ```
4. Visit `http://localhost:8000/` for the built-in coaching dashboard, or continue to the sections below to work with the API or React SPA.

### Django coaching dashboard

The root route (`/`) renders a server-side form that mirrors the API contract. Submit the game context to view recommendations and optionally persist them to history without leaving the Django site.

### Frontend (React single-page app)

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```
2. Start the development server (make sure the Django API is running on `http://localhost:8000`):
   ```bash
   npm run dev
   ```
3. Open the URL printed in the console (default `http://localhost:5173`) to use the interface.
4. To target a different API host, create a `.env.local` file in `frontend/` with `VITE_API_BASE_URL="http://your-host:port"`.

## Running Tests

```bash
python manage.py test
```

## API Overview

All endpoints are nested under `/api/` and return JSON responses.

- `POST /api/recommendations/` – Generate defensive and offensive plans for the current situation. Include `save_to_history: true` in the payload to persist the recommendation to the play log.
- `GET /api/plays/` – Retrieve recorded play history (newest first).
- `POST /api/plays/` – Manually add a play to the log, for example after recording the actual outcome.
- `GET /api/plays/<id>/` – Inspect a single stored play.

### Recommendation request

```json
{
  "offense_team": "Visitors",
  "defense_team": "Home",
  "inning": 7,
  "half_inning": "top",
  "outs": 2,
  "balls": 1,
  "strikes": 1,
  "runners_on_first": true,
  "runners_on_second": false,
  "runners_on_third": true,
  "score_difference": 0,
  "context_notes": "Tie game, late inning leverage.",
  "save_to_history": true
}
```

### Recommendation response

```json
{
  "pitch_call": "Four-seam fastball up to give the catcher a high strike to throw on.",
  "catcher_plan": "If the runner on first breaks, throw through to second for the final out. Third baseman shades toward the line until the runner commits home, then stays home.",
  "defensive_alignment": {
    "infield": "Corners back, middle ready to cover second on potential steal.",
    "outfield": "No-doubles alignment—corners on the lines, outfield a step deeper.",
    "battery": "Pound the zone early and control the running game."
  },
  "offensive_signs": {
    "hitter": "Take all the way until a strike is thrown.",
    "runner": "Time up the pitcher; create a rundown to score the runner from third if signaled."
  },
  "key_points": [
    "Top of the 7 inning, count 1-1 with 2 out(s).",
    "Expect the offense to create movement with first-and-third pressure.",
    "Win the inning by taking the sure out at second; keep third base home to freeze the runner.",
    "High leverage: protect the lines and keep everything in front."
  ]
}
```

## Customising Strategy

- Update the rule-based engine in `playcalling/recommendations.py` to add new heuristics or integrate machine learning later.
- The `GamePlay` model in `playcalling/models.py` captures both context and recommended actions, making it suitable for building datasets to train future models or for replay review.

## Next Steps

- Layer authentication/permissions on the API before exposing it publicly.
- Add role-aware views to the Django dashboard (coach vs. analyst) as authorization gets introduced.
- Expose web and mobile clients using the `/api/` contract defined here.
- Replace the deterministic engine with analytics-driven recommendations as data accumulates.
