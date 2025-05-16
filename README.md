# BigQuery Text-to-SQL Microservice

A FastAPI-based microservice that converts natural language queries into BigQuery SQL using Qwen3 LLM.

## Features

- Convert natural language queries to BigQuery SQL
- Manage database schemas via API
- Health check endpoint for monitoring
- Structured logging
- Containerized deployment

## Prerequisites

- Python 3.11+
- Redis (for schema storage)
- Qwen3 running in Ollama (for text-to-SQL conversion)

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd text-to-bigquery
   ```

2. Create and activate a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: .\venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy the example environment file and update it with your settings:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. Start Redis (required for schema storage):
   ```bash
   # Using Docker
   docker run --name redis -p 6379:6379 -d redis
   ```

6. Start the Qwen3 service using Ollama:
   ```bash
   # Install Ollama if not already installed
   # See: https://ollama.ai/
   
   # Pull and run Qwen3
   ollama pull qwen:7b
   ollama serve
   ```

## Running the Application

1. Start the FastAPI application:
   ```bash
   uvicorn main:app --reload
   ```

2. The API will be available at `http://localhost:8000`

3. Access the interactive API documentation at `http://localhost:8000/api/v1/docs`

## API Endpoints

- `GET /api/v1/health` - Health check endpoint
- `POST /api/v1/generate-sql` - Generate SQL from natural language
- `GET /api/v1/schema` - Get the current database schema
- `PUT /api/v1/schema` - Update the database schema

## Development

### Code Formatting

This project uses `black` for code formatting and `isort` for import sorting.

```bash
# Install development dependencies
pip install black isort

# Format code
black .
isort .
```

### Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest --cov=app tests/
```

## Deployment

### Docker

Build the Docker image:

```bash
docker build -t text-to-sql-api .
```

Run the container:

```bash
docker run -d --name text-to-sql-api -p 8000:8000 --env-file .env text-to-sql-api
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
