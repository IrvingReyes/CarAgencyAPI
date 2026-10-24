# Car Agency API

Catalog API for a used-car dealership and repair shop. It lists vehicles for sale, including vehicles that need repair or are sold for parts, so other workshops can buy them.

Sales and repairs are managed in Odoo, which keeps this catalog updated through the API.

Built with FastAPI, SQLModel and PostgreSQL.

## Run with Docker

Requirements: Docker with Docker Compose.

```bash
docker compose up -d --build
```

This starts PostgreSQL and the API. On startup the API applies the database migrations and loads sample vehicles if the table is empty.

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

| Method | Path | Description |
|---|---|---|
| GET | `/vehicles/` | List vehicles. Optional filters: `brand`, `available`, `sold`, `condition` (repeatable) |
| GET | `/vehicles/{id}` | Get a vehicle |
| POST | `/vehicles/` | Create a vehicle |
| PUT | `/vehicles/{id}/condition` | Update a vehicle's condition |

Vehicle conditions: `operational`, `needs_repair`, `in_repair`, `parts_only`.
