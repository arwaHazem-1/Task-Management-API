# Task-Management-API
A clean and well-structured Task Management REST API built with FastAPI, SQLModel, and SQLite. Supports full CRUD operations, filtering, searching, and data validation with documentation. Ideal for learning backend development and API design best practices.

## How to run

```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

## Docs

- Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)
- Redoc: [http://localhost:8000/redoc](http://localhost:8000/redoc)

## Example usage

```bash
# Add a task
curl -X POST "http://localhost:8000/tasks" -H "Content-Type: application/json" -d '{"title": "Do homework"}'

# List tasks
curl "http://localhost:8000/tasks"

# Get one task
curl "http://localhost:8000/tasks/1"

# Update a task
curl -X PUT "http://localhost:8000/tasks/1" -H "Content-Type: application/json" -d '{"status": "completed"}'

# Delete a task
curl -X DELETE "http://localhost:8000/tasks/1"
```

## Notes

- Uses SQLite for storage.
- Titles are required and must not be empty.
- Filtering by status and priority is supported.

---

ARWA HAZEM
