# AI Report Generation Service

A FastAPI-based service that generates detailed reports using AI. The service allows users to submit a topic and receive a structured report with multiple sections, all processed asynchronously.

## Features

- Asynchronous report generation
- Real-time progress tracking
- Redis-based job state management
- OpenAI API integration for content generation
- RESTful API with OpenAPI documentation
- Containerized deployment ready

## Prerequisites

- Python 3.9+
- Redis server
- OpenAI API key

## Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd aether-fullstack
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

4. Create a `.env` file from the example:
   ```bash
   cp .env.example .env
   ```

5. Update the `.env` file with your OpenAI API key and any other necessary configurations.

## Running the Application

1. Start the Redis server:
   ```bash
   # On Linux/macOS
   redis-server
   
   # On Windows (if installed via Chocolatey)
   redis-server
   ```

2. Start the FastAPI application:
   ```bash
   uvicorn app.main:app --reload
   ```

3. The API will be available at `http://localhost:8000`
4. Access the interactive API documentation at `http://localhost:8000/docs`

## API Endpoints

### Start a Report Generation

```http
POST /api/v1/reports
Content-Type: application/json

{
  "topic": "The Roman Empire"
}
```

Response (202 Accepted):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending",
  "progress": 0.0
}
```

### Check Report Status

```http
GET /api/v1/reports/{job_id}
```

Response (200 OK):
```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "processing",
  "progress": 0.5
}
```

### Successful Report Response

```json
{
  "job_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "completed",
  "progress": 1.0,
  "report": {
    "topic": "The Roman Empire",
    "outline": ["I. The Rise of Rome", "II. The Roman Republic", "III. The Roman Empire"],
    "sections": {
      "I. The Rise of Rome": "...detailed content...",
      "II. The Roman Republic": "...detailed content...",
      "III. The Roman Empire": "...detailed content..."
    }
  }
}
```

## Development

### Running Tests

```bash
pytest
```

### Code Formatting

```bash
black .
```

### Linting

```bash
flake8
```

## Deployment

### Docker

1. Build the Docker image:
   ```bash
   docker build -t ai-report-service .
   ```

2. Run the container:
   ```bash
   docker run -p 8000:8000 --env-file .env ai-report-service
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | OpenAI API key | - |
| `API_BASE_URL` | OpenAI API base URL | `https://api.openai.com/v1` |
| `MODEL_NAME` | OpenAI model to use | `gpt-4` |
| `REDIS_HOST` | Redis host | `localhost` |
| `REDIS_PORT` | Redis port | `6379` |
| `REDIS_DB` | Redis database number | `0` |
| `HOST` | Application host | `0.0.0.0` |
| `PORT` | Application port | `8000` |
| `DEBUG` | Enable debug mode | `False` |

## License

MIT

My Assessment for Aether's FSE 
