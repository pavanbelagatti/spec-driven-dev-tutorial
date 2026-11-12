# spec-driven-dev-tutorial

A tiny notification service used to demo **spec-driven development** with [Port](https://port.io).

Specs are written and approved in Port. When a spec is approved, Port opens a GitHub
issue in this repo containing the full spec. A developer or a coding agent implements
it here and opens a pull request.

## The service

A small Flask app that sends transactional emails. Emails are not really sent: a fake
sender records them so tests can check what went out.

| Endpoint | What it does |
| --- | --- |
| `GET /health` | Returns `{"status": "ok"}` |
| `POST /password-reset` | Sends a password reset email to `{"email": "..."}` |
| `POST /welcome-email` | Sends a welcome email to `{"email": "..."}` |

**Known gap:** `/password-reset` has no rate limit, so anyone can flood an inbox.
That is the first spec in the tutorial ("Rate-limit password reset emails").

## Run it

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

pytest                           # run the tests
python -m app.main               # start on http://localhost:5000
```

Try it:

```bash
curl -X POST localhost:5000/password-reset \
  -H "Content-Type: application/json" -d '{"email": "ada@example.com"}'
```

## Layout

```
app/
  __init__.py       create_app()
  routes.py         HTTP endpoints
  email_sender.py   fake email provider
  main.py           local entry point
tests/
  test_notifications.py
AGENTS.md           rules for coding agents working from a spec
```

## How a spec becomes code

1. Someone files a spec in Port (problem, acceptance criteria, non-goals, constraints).
2. Port's `spec_readiness` scorecard checks it is complete.
3. A reviewer sets the spec's status to **Approved**.
4. Port opens an issue here with the spec.
5. A developer or agent implements it, following `AGENTS.md`, and opens a PR.
6. The PR link is saved back on the spec in Port.
