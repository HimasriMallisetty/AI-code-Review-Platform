# AI Code Review Platform

A Django REST API that accepts code submissions and returns AI-generated
code review feedback — quality score, issues found, and suggestions —
powered by the Claude API.

## Tech stack
- Python, Django, Django REST Framework
- Anthropic Claude API (code review engine)
- PostgreSQL (via Docker) or SQLite (local dev)
- Docker & Docker Compose

## API Endpoints
| Method | Endpoint                          | Description                          |
|--------|------------------------------------|---------------------------------------|
| GET    | `/api/reviews/`                   | List all code reviews                 |
| POST   | `/api/reviews/`                   | Submit code, runs AI review synchronously |
| GET    | `/api/reviews/{id}/`              | Get a single review                   |
| POST   | `/api/reviews/{id}/re_review/`    | Re-run AI review on existing submission |

### Example request
```bash
curl -X POST http://localhost:8000/api/reviews/ \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Login function",
    "language": "python",
    "code_snippet": "def login(u,p):\n  if u==\"admin\" and p==\"1234\":\n    return True"
  }'
```

---

## Option A: Run locally (fastest for development)

1. **Clone/unzip and enter the backend folder**
```bash
   cd ai-code-review-platform/backend
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate      # on Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
   pip install -r requirements.txt
```

4. **Set up environment variables**
```bash
   cp .env.example .env
```
   Open `.env` and paste in your `ANTHROPIC_API_KEY` (get one from
   https://console.anthropic.com/). Leave the DB settings as-is to use SQLite.

5. **Run migrations**
```bash
   python manage.py migrate
```

6. **Create an admin user (optional, for `/admin/`)**
```bash
   python manage.py createsuperuser
```

7. **Run the dev server**
```bash
   python manage.py runserver
```

8. Visit `http://127.0.0.1:8000/api/reviews/` to see the API, or
   `http://127.0.0.1:8000/admin/` for the admin panel.

---

## Option B: Run with Docker (matches production setup)

1. **Set your API key** as an environment variable before starting:
```bash
   export ANTHROPIC_API_KEY=your-key-here     # on Windows: set ANTHROPIC_API_KEY=your-key-here
```

2. **Build and start everything (backend + Postgres)**
```bash
   docker compose up --build
```

3. **Run migrations inside the container** (in a separate terminal, once containers are up)
```bash
   docker compose exec backend python manage.py migrate
   docker compose exec backend python manage.py createsuperuser
```

4. Visit `http://localhost:8000/api/reviews/`

---

## Project structure
ai-code-review-platform/
├── backend/
│ ├── manage.py
│ ├── config/ # Django settings, URLs, WSGI
│ ├── reviews/ # Main app: models, views, serializers
│ │ └── services/ # AI review logic (Claude API integration)
│ ├── requirements.txt
│ └── .env.example
├── docker-compose.yml
├── Dockerfile
└── README.md

## Next steps / ideas to extend this
- Add a `POST /api/reviews/{id}/re_review/` rate limit (avoid re-running AI reviews repeatedly)
- Add user authentication (DRF Token or JWT) so reviews are tied to accounts
- Add async processing (Celery + Redis) instead of synchronous AI calls, so submission returns instantly and review completes in the background
- Add a simple React/frontend to submit code and display results visually
- Add support for reviewing full files/diffs, not just snippets
