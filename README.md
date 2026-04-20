# 🚀 FastAPI App

A simple, production-ready REST API built with FastAPI.

## Features

- ✅ Full CRUD for `items` resource
- ✅ Automatic interactive docs (`/docs` and `/redoc`)
- ✅ Request validation via Pydantic
- ✅ Health check endpoint
- ✅ In-memory data store (swap for a real DB easily)

## Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the server
uvicorn main:app --reload
```

The API will be live at: **http://127.0.0.1:8000**

## Endpoints

| Method | Path            | Description         |
|--------|-----------------|---------------------|
| GET    | /               | Welcome message     |
| GET    | /health         | Health check        |
| GET    | /items          | List all items      |
| GET    | /items/{id}     | Get item by ID      |
| POST   | /items          | Create a new item   |
| PUT    | /items/{id}     | Update an item      |
| DELETE | /items/{id}     | Delete an item      |

## Example Usage

```bash
# Create an item
curl -X POST http://localhost:8000/items \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "description": "A useful widget", "price": 9.99}'

# List all items
curl http://localhost:8000/items

# Update an item
curl -X PUT http://localhost:8000/items/1 \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget Pro", "price": 19.99, "in_stock": true}'

# Delete an item
curl -X DELETE http://localhost:8000/items/1
```

## Project Structure

```
fastapi-app/
├── main.py          # App entry point + all routes
├── requirements.txt # Dependencies
└── README.md        # This file
```

## Next Steps

- Add a real database (SQLite via SQLAlchemy, PostgreSQL, etc.)
- Split routes into separate `routers/` modules
- Add authentication (JWT with `python-jose`)
- Write tests with `pytest` + `httpx`
