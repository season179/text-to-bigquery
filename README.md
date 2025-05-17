# Text to BigQuery

This project provides APIs to convert natural language text to BigQuery and SQL.

## API Endpoints

- `GET /health`: Health check endpoint
- `POST /text-to-sql`: Converts natural language to SQL (implementation pending)

## Development

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

## Development Notes

- The application runs with hot-reload enabled for local development
- API implemented with FastAPI
- Runs on port 8000 by default