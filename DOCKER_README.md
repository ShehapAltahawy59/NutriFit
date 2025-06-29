# NutriFit Agents API - Docker Deployment Guide

This guide provides instructions for deploying the NutriFit Agents API using Docker.

## Prerequisites

- Docker installed on your system
- Docker Compose (optional, for easier deployment)
- Azure OpenAI API credentials

## Quick Start

### 1. Environment Setup

Create a `.env` file in the root directory with your Azure OpenAI credentials:

```bash
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_KEY=your-api-key-here
AZURE_OPENAI_API_VERSION=2024-02-15-preview
AZURE_OPENAI_DEPLOYMENT=your-deployment-name
```

### 2. Build and Run with Docker Compose (Recommended)

```bash
# Build and start the application
docker-compose up --build

# Run in detached mode
docker-compose up -d --build

# View logs
docker-compose logs -f

# Stop the application
docker-compose down
```

### 3. Build and Run with Docker

```bash
# Build the image
docker build -t nutrifit-agents-api .

# Run the container
docker run -d \
  --name nutrifit-api \
  -p 5000:5000 \
  --env-file .env \
  nutrifit-agents-api

# View logs
docker logs -f nutrifit-api

# Stop the container
docker stop nutrifit-api
```

## Production Deployment

### Using Production Dockerfile

```bash
# Build production image
docker build -f Dockerfile.prod -t nutrifit-agents-api:prod .

# Run production container
docker run -d \
  --name nutrifit-api-prod \
  -p 5000:5000 \
  --env-file .env \
  nutrifit-agents-api:prod
```

### Using Docker Compose for Production

```bash
# Build and run production version
docker-compose -f docker-compose.prod.yml up -d --build
```

## Configuration Options

### Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `AZURE_OPENAI_ENDPOINT` | Azure OpenAI endpoint URL | Yes | - |
| `AZURE_OPENAI_API_KEY` | Azure OpenAI API key | Yes | - |
| `AZURE_OPENAI_API_VERSION` | Azure OpenAI API version | Yes | 2024-02-15-preview |
| `AZURE_OPENAI_DEPLOYMENT` | Azure OpenAI deployment name | Yes | - |
| `FLASK_ENV` | Flask environment | No | production |
| `FLASK_APP` | Flask application file | No | main.py |

### Port Configuration

The API runs on port 5000 by default. You can change this by modifying the port mapping:

```bash
# Change port to 8080
docker run -p 8080:5000 nutrifit-agents-api
```

### Volume Mounts

```bash
# Mount logs directory
docker run -v ./logs:/app/logs nutrifit-agents-api

# Mount custom configuration
docker run -v ./config:/app/config nutrifit-agents-api
```

## Health Checks

The container includes health checks that monitor the API status:

```bash
# Check container health
docker ps

# View health check logs
docker inspect nutrifit-api | grep Health -A 10
```

## Monitoring and Logs

### View Application Logs

```bash
# Docker Compose
docker-compose logs -f nutrifit-api

# Docker
docker logs -f nutrifit-api
```

### Monitor Resource Usage

```bash
# Container stats
docker stats nutrifit-api

# Resource usage details
docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}\t{{.NetIO}}"
```

## Troubleshooting

### Common Issues

1. **Container fails to start**
   ```bash
   # Check logs
   docker logs nutrifit-api
   
   # Verify environment variables
   docker exec nutrifit-api env | grep AZURE
   ```

2. **Health check failures**
   ```bash
   # Check if API is responding
   curl http://localhost:5000/health
   
   # Restart container
   docker restart nutrifit-api
   ```

3. **Memory issues**
   ```bash
   # Increase memory limit
   docker run --memory=2g nutrifit-agents-api
   ```

### Debug Mode

For debugging, you can run the container in interactive mode:

```bash
# Run with bash shell
docker run -it --rm nutrifit-agents-api bash

# Check Python environment
python -c "import sys; print(sys.path)"
python -c "from Agents import *; print('Agents imported successfully')"
```

## Security Considerations

1. **Non-root user**: The container runs as a non-root user for security
2. **Environment variables**: Sensitive data should be passed via environment variables
3. **Network isolation**: Use Docker networks to isolate containers
4. **Regular updates**: Keep base images and dependencies updated

## Scaling

### Horizontal Scaling

```bash
# Scale with Docker Compose
docker-compose up --scale nutrifit-api=3

# Load balancer configuration (example with nginx)
version: '3.8'
services:
  nginx:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - nutrifit-api
  
  nutrifit-api:
    build: .
    environment:
      - AZURE_OPENAI_ENDPOINT=${AZURE_OPENAI_ENDPOINT}
      - AZURE_OPENAI_API_KEY=${AZURE_OPENAI_API_KEY}
      - AZURE_OPENAI_API_VERSION=${AZURE_OPENAI_API_VERSION}
      - AZURE_OPENAI_DEPLOYMENT=${AZURE_OPENAI_DEPLOYMENT}
```

## API Testing

Once deployed, test the API:

```bash
# Health check
curl http://localhost:5000/health

# Status check
curl http://localhost:5000/status

# Test workflow
curl -X POST http://localhost:5000/workflow/create_complete_plan \
  -H "Content-Type: application/json" \
  -d '{
    "inbody_image_url": "https://example.com/inbody-scan.jpg",
    "client_country": "Egypt",
    "goals": "Weight loss and muscle building",
    "allergies": "Lactose intolerant"
  }'
```

## Support

For issues and questions:
1. Check the application logs
2. Verify environment variables
3. Test API endpoints
4. Review this documentation

## License

This project is licensed under the MIT License. 
