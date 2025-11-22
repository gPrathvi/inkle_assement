# Inkle Backend API

A Django REST API for a simple social app including users, posts, social graph (follow/block), activities, and notifications. Comes with a smoke test and ready-to-use Postman collection.

## Requirements
- Python 3.10+
- pip

## Quick start
```
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver 0.0.0.0:8000
```

- Health check: http://localhost:8000/health/
- OpenAPI schema: http://localhost:8000/api/schema/
- Swagger UI: http://localhost:8000/api/docs/

## Environment variables
- SECRET_KEY (default: development-insecure-secret)
- DEBUG (default: True)
- ALLOWED_HOSTS (default: localhost,127.0.0.1)
- DATABASE_URL (default: sqlite:///db.sqlite3)
- FRONTEND_ORIGINS or FRONTEND_ORIGIN (default: http://localhost:3000)
- CORS_ALLOW_ALL_ORIGINS (default: False)

## Smoke test (end-to-end)
A basic flow that signs up/logs in a user, creates/likes/unlikes/deletes a post.

In a separate terminal with the server running:
```
python scripts/smoke_test.py
```
Expected output (abbreviated):
- Signup: 201 on first run, 400 on re-runs (user exists) — expected
- Login OK
- Me GET/PATCH: 200
- Create Post: 201
- List Posts: 200
- Like: 201 (idempotent re-run: 200 already liked)
- Unlike: 204
- Delete Post: 204
- Smoke test complete.

## Using Postman
Postman assets are under `docs/postman/`:
- Collection: `docs/postman/inkle_api.postman_collection.json`
- Environment: `docs/postman/inkle_local.postman_environment.json`
- **Complete Documentation**: [`docs/POSTMAN_DOCUMENTATION.md`](docs/POSTMAN_DOCUMENTATION.md)

Steps:
1) Start the API server as above.
2) Import both the collection and the environment into Postman.
3) Select the "Inkle Local" environment (base_url defaults to http://localhost:8000).
4) Run "Auth & Users > Signup" (first run 201; re-runs 400 — OK).
5) Run "Auth & Users > Login (JWT)". The collection is configured to auto-store `access_token` in the selected environment.
6) Use endpoints in folders: Posts, Comments, Social, Activity & Notifications.
   - Replace sample IDs (e.g., 10, 20, 2) with actual IDs created in your session where needed.

For detailed endpoint documentation and complete testing workflows, see the [Postman Documentation](docs/POSTMAN_DOCUMENTATION.md).

## Endpoints (high-level)
- Auth: `/api/auth/signup/`, `/api/auth/login/`, `/api/auth/refresh/`
- Users: `/api/users/me/`, `/api/users/search/`
- Posts: `/api/posts/`, `/api/posts/{id}/like/` (POST like, DELETE unlike)
- Comments: `/api/comments/`
- Social: `/api/users/{id}/follow/`, `/api/users/{id}/block/`
- Activity & Notifications: `/api/feed/`, `/api/notifications/`, `/api/notifications/{id}/read/`

## Notes
- Default permissions require JWT auth (SimpleJWT) for most endpoints.
- SQLite is used by default. To use Postgres set `DATABASE_URL` accordingly.
- The `Unlike` action has been implemented on the same URL as `Like` with DELETE method.
