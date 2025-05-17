# Text to BigQuery

This project provides an API that converts natural language questions into Google BigQuery-compatible SQL queries.

## Purpose

- Accepts natural language questions from users
- Converts these questions to BigQuery-compatible SQL using the qwen3 model via ollama
- Returns the generated SQL query to the user
- Users can then execute the query in BigQuery Studio

The service does NOT execute SQL against any database - it only generates SQL for users to run themselves.

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /text-to-sql`: Converts natural language to BigQuery SQL

## Development

### Requirements

- Docker and Docker Compose
- An ollama setup with the qwen3 model

### Setup

This project uses Docker for local development.

```bash
# Start the application
docker-compose up
```

The API will be available at http://localhost:8000

### Testing

Use Docker Compose to test the application:

```bash
# Start the services
docker-compose up -d

# Test the health endpoint
curl http://localhost:8000/health

# Test the text-to-sql endpoint
curl -X POST \
  http://localhost:8000/text-to-sql \
  -H "Content-Type: application/json" \
  -d '"Show me all users who signed up last month"'
```

The response will contain a BigQuery-compatible SQL query that can be copied and pasted into BigQuery Studio.

## Development Notes

- The application runs with hot-reload enabled for local development
- API implemented with FastAPI
- Uses the qwen3 model via ollama for natural language to SQL conversion
- Runs on port 8000 by default