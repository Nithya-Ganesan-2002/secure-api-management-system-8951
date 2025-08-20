# Project Repository

This repository contains a production-ready Flask backend API with:
- JWT authentication and role-based access control (RBAC)
- Modular blueprints and service layer
- SQLAlchemy ORM and Marshmallow validation/serialization
- RESTful CRUD for Students, Rooms, Products, and admin Users
- Filtering, sorting, pagination
- Swagger/OpenAPI docs via flask-smorest
- Centralized error handling
- Environment-based configuration via `.env`

## Getting Started

1. Create and populate environment file:
   cp backend_api/.env.example backend_api/.env
   # Edit values as needed (DATABASE_URL, JWT_SECRET_KEY, etc.)

2. Install dependencies:
   pip install -r backend_api/requirements.txt

3. Run the API:
   cd backend_api
   python run.py

By default the server runs on http://0.0.0.0:3001
Docs are available at /docs

## Environment Variables

See `backend_api/.env.example` for all supported variables (database URL, JWT, OpenAPI settings).

## Database

- Uses SQLAlchemy. For development the default is SQLite. For production set `DATABASE_URL` to your Postgres DSN (e.g., `postgresql+psycopg2://user:pass@host:5432/dbname`).
- This demo auto-creates tables on startup. For production use migrations (Alembic).

## Security

- Change `JWT_SECRET_KEY` in production.
- Restrict `CORS_ORIGINS` to trusted domains.
