# VLM Clothing Analysis App

A FastAPI application for clothing analysis using Ollama's vision models.

## Docker Setup

### Prerequisites
- Docker Engine
- Docker Compose
- Git

### Installation
1. Clone the repository:
```bash
git clone https://github.com/ahosnyyy/vlm-clothing.git
cd vlm-clothing
```

2. Build and start containers:
```bash
docker compose up --build -d
```

3. Pull required Ollama model (after containers are running):
```bash
docker compose exec ollama ollama pull gemma3:12b
```

### Accessing the Application
- API: `http://localhost:8000`
- Ollama: `http://localhost:11434`

### Common Commands
```bash
# View logs
docker compose logs -f

# Stop containers
docker compose down

# Update the application
git pull
docker compose up --build -d
```

## Development
For development with live reload:
```bash
docker compose up
```

## Production
For production deployment:
- Set `DEBUG=False` in docker-compose.yml
- Remove volume mounts
- Consider adding Nginx reverse proxy
