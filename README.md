# Car Agency API

Catalog API for a used-car dealership and repair shop. It lists vehicles for sale, including vehicles that need repair or are sold for parts, so other workshops can buy them.

Sales and repairs are managed in Odoo, which keeps this catalog updated through the API.

Built with FastAPI, SQLModel and PostgreSQL.

## Run with Docker

Requirements: Docker with Docker Compose.

Create the `.env` file and set at least `SECRET_KEY` (and the first user's credentials):

```bash
cp .env.example .env
python -c "import secrets; print(secrets.token_urlsafe(32))"  # paste the output as SECRET_KEY
```

Start the services:

```bash
docker compose up -d --build
```

This starts PostgreSQL and the API. On startup the API applies the database migrations, creates the first user from `FIRST_USER_EMAIL` / `FIRST_USER_PASSWORD` if it does not exist, and loads sample vehicles if the table is empty.

Stop everything:

```bash
docker compose down
```

To also delete the database data, add `-v`.

## Local URLs

| URL | Description |
|---|---|
| http://localhost:8000 | API (health check) |
| http://localhost:8000/docs | Interactive docs (Swagger UI) |
| http://localhost:8000/redoc | Docs (ReDoc) |
| `localhost:5433` | PostgreSQL (user, password and database: `car_agency`) |

## Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/tokens` | | Get an access token and a refresh token |
| POST | `/tokens/refresh` | | Get a new token pair using the refresh token |
| GET | `/vehicles/` | | List vehicles. Optional filters: `brand`, `available`, `sold`, `condition` (repeatable) |
| GET | `/vehicles/{id}` | | Get a vehicle |
| POST | `/vehicles/` | Bearer | Create a vehicle |
| PUT | `/vehicles/{id}/condition` | Bearer | Update a vehicle's condition |

Vehicle conditions: `operational`, `needs_repair`, `in_repair`, `parts_only`.

## Authentication

Request a token with the user's credentials:

```http
POST /tokens
Content-Type: application/json

{"email": "odoo@example.com", "password": "..."}
```

```json
{
  "data": {
    "token": "<access token>",
    "refreshToken": "<refresh token>",
    "tokenExpiryTime": "2026-10-24T22:30:00Z",
    "refreshTokenExpiryTime": "2026-10-31T22:00:00Z"
  }
}
```

Send the access token on protected requests:

```http
Authorization: Bearer <access token>
```

When the access token expires, get a new pair without sending the credentials again:

```http
POST /tokens/refresh
Content-Type: application/json

{"token": "<access token>", "refreshToken": "<refresh token>"}
```

In `/docs`, use the **Authorize** button and paste the access token.
