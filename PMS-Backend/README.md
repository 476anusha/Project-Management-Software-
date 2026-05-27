# PMS - Project Management System

A modern project management tool built with FastAPI, React, and PostgreSQL.

## Tech Stack

**Backend:**
- FastAPI
- SQLAlchemy (async)
- PostgreSQL (Neon)
- Alembic
- asyncpg

**Frontend:**
- React
- Tailwind CSS
- TanStack Query

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure Environment

Copy `.env.example` to `.env` and update with your settings:

```bash
cp .env.example .env
```

Update the `DATABASE_URL` with your Neon PostgreSQL connection string.

### 3. Initialize Database

```bash
# Initialize Alembic
alembic init alembic

# Create initial migration
alembic revision --autogenerate -m "Initial migration"

# Apply migrations
alembic upgrade head
```

### 4. Run the Application

```bash
# Development mode with auto-reload
uvicorn app.main:app --reload

# Or use the main.py directly
python -m app.main
```

The API will be available at `http://localhost:8000`

- API Documentation: `http://localhost:8000/docs`
- Alternative docs: `http://localhost:8000/redoc`

## Project Structure

```
your-project/
├── app/
│   ├── api/              # API endpoints
│   ├── models/           # SQLAlchemy models
│   ├── schemas/          # Pydantic schemas
│   ├── core/             # Core configuration
│   ├── utils/            # Utility functions
│   └── main.py           # FastAPI app
├── alembic/              # Database migrations
├── tests/                # Tests
├── .env                  # Environment variables
└── requirements.txt      # Python dependencies
```

## Models

The project includes 18 database models:
- Users & Sessions
- Workspaces & Roles
- Projects & Issues
- Comments & Attachments
- Labels & Workflows
- Boards & Notifications
- Activity & Audit Logs

## Development

Start by running the server and check the health endpoint:

```bash
curl http://localhost:8000/health
```

## Next Steps

1. Configure Alembic for your database
2. Create API endpoints in `app/api/`
3. Define Pydantic schemas in `app/schemas/`
4. Implement business logic and authentication
