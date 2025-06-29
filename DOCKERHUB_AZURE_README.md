# NutriFit Agents API - Docker Hub + Azure Container Apps CI/CD Guide

This guide provides step-by-step instructions for deploying the NutriFit Agents API using Docker Hub as the container registry and Azure Container Apps for hosting.

## 🚀 Quick Start

### Prerequisites

- Azure CLI installed and configured
- Docker installed and configured
- Docker Hub account
- Azure subscription with Container Apps enabled
- Azure OpenAI service configured

### 1. **Environment Setup**

Set your Azure OpenAI environment variables:

```bash
export AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com/"
export AZURE_OPENAI_API_KEY="your-api-key-here"
export AZURE_OPENAI_API_VERSION="2024-02-15-preview"
export AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
```

### 2. **Docker Hub Setup**

1. **Create Docker Hub Account** (if you don't have one):
   - Go to [Docker Hub](https://hub.docker.com/)
   - Sign up for a free account

2. **Login to Docker Hub**:
   ```bash
   docker login
   # Enter your Docker Hub username and password
   ```

3. **Create Access Token** (for CI/CD):
   - Go to Docker Hub → Account Settings → Security
   - Create a new access token
   - Save the token for GitHub Actions

### 3. **Deploy with Script**

```bash
# Update the script with your Docker Hub username
# Edit deploy-dockerhub-azure.sh and change:
# DOCKER_HUB_USERNAME="your-dockerhub-username"

# Make script executable
chmod +x deploy-dockerhub-azure.sh

# Run deployment
./deploy-dockerhub-azure.sh
```

### 4. **Manual Deployment Steps**

If you prefer manual deployment:

```bash
# 1. Login to Azure
az login

# 2. Create Resource Group
az group create --name nutrifit-rg --location eastus

# 3. Build and push image to Docker Hub
docker build -f Dockerfile.prod -t your-dockerhub-username/nutrifit-agents-api:latest .
docker push your-dockerhub-username/nutrifit-agents-api:latest

# 4. Create Container Apps Environment
az containerapp env create --name nutrifit-env --resource-group nutrifit-rg --location eastus

# 5. Create Container App
az containerapp create \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --environment nutrifit-env \
  --image your-dockerhub-username/nutrifit-agents-api:latest \
  --target-port 5000 \
  --ingress external \
  --min-replicas 1 \
  --max-replicas 10 \
  --cpu 1.0 \
  --memory 2Gi \
  --env-vars FLASK_APP=main.py FLASK_ENV=production \
  --secrets azure-openai-endpoint="$AZURE_OPENAI_ENDPOINT" azure-openai-api-key="$AZURE_OPENAI_API_KEY" azure-openai-api-version="$AZURE_OPENAI_API_VERSION" azure-openai-deployment="$AZURE_OPENAI_DEPLOYMENT" \
  --env-vars AZURE_OPENAI_ENDPOINT=secretref:azure-openai-endpoint AZURE_OPENAI_API_KEY=secretref:azure-openai-api-key AZURE_OPENAI_API_VERSION=secretref:azure-openai-api-version AZURE_OPENAI_DEPLOYMENT=secretref:azure-openai-deployment
```

## 🔄 CI/CD with GitHub Actions

### **Setup GitHub Secrets**

Add these secrets to your GitHub repository:

- `AZURE_CREDENTIALS`: Service principal credentials
- `DOCKER_HUB_USERNAME`: Your Docker Hub username
- `DOCKER_HUB_TOKEN`: Your Docker Hub access token
- `AZURE_OPENAI_ENDPOINT`: Azure OpenAI endpoint
- `AZURE_OPENAI_API_KEY`: Azure OpenAI API key
- `AZURE_OPENAI_API_VERSION`: Azure OpenAI API version
- `AZURE_OPENAI_DEPLOYMENT`: Azure OpenAI deployment name

### **Create Service Principal**

```bash
# Create service principal
az ad sp create-for-rbac --name "nutrifit-deploy" --role contributor \
  --scopes /subscriptions/{subscription-id}/resourceGroups/nutrifit-rg \
  --sdk-auth

# Copy the output to GitHub secrets as AZURE_CREDENTIALS
```

### **Docker Hub Access Token**

1. Go to Docker Hub → Account Settings → Security
2. Click "New Access Token"
3. Give it a name (e.g., "GitHub Actions")
4. Copy the token and add it to GitHub secrets as `DOCKER_HUB_TOKEN`

### **Automatic Deployment**

The GitHub Actions workflow will automatically:
1. Build the Docker image
2. Push to Docker Hub with both commit SHA and latest tags
3. Deploy to Azure Container Apps
4. Test the deployment
5. Comment on PRs with deployment info

## 🔧 Configuration Options

### **Update Docker Hub Username**

In the deployment script:
```bash
# Edit deploy-dockerhub-azure.sh
DOCKER_HUB_USERNAME="your-actual-dockerhub-username"
```

In the Azure Container Apps YAML:
```yaml
# Edit azure-container-apps.yaml
image: your-actual-dockerhub-username/nutrifit-agents-api:latest
```

### **Image Tagging Strategy**

The CI/CD pipeline uses:
- `your-username/nutrifit-agents-api:latest` - Latest stable version
- `your-username/nutrifit-agents-api:{commit-sha}` - Specific commit version

### **Scaling Configuration**

```bash
# Update scaling rules
az containerapp update \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --min-replicas 2 \
  --max-replicas 20 \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 50
```

## 📊 Monitoring & Management

### **View Application Status**

```bash
# Get application URL
az containerapp show \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --query properties.configuration.ingress.fqdn \
  --output tsv

# Check revision status
az containerapp revision list \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --output table
```

### **View Logs**

```bash
# Stream logs
az containerapp logs show \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --follow

# Get recent logs
az containerapp logs show \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --tail 100
```

### **Docker Hub Image Management**

```bash
# List your images on Docker Hub
docker images your-dockerhub-username/nutrifit-agents-api

# Pull latest image locally
docker pull your-dockerhub-username/nutrifit-agents-api:latest

# Remove old images
docker rmi your-dockerhub-username/nutrifit-agents-api:old-tag
```

## 🛠️ Troubleshooting

### **Common Issues**

1. **Docker Hub Authentication**
   ```bash
   # Check if logged in to Docker Hub
   docker info | grep Username
   
   # Re-login if needed
   docker logout
   docker login
   ```

2. **Image Push Failures**
   ```bash
   # Check Docker Hub rate limits (free accounts have limits)
   # Consider upgrading to paid plan for higher limits
   
   # Verify image exists locally
   docker images | grep nutrifit-agents-api
   ```

3. **Container App Image Pull Issues**
   ```bash
   # Check if image exists on Docker Hub
   curl -f "https://hub.docker.com/v2/repositories/your-username/nutrifit-agents-api/tags/"
   
   # Verify image name in Container App
   az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query properties.template.containers[0].image
   ```

### **Debug Commands**

```bash
# Test Docker Hub access
docker pull hello-world
docker push your-username/test-image:latest

# Check Azure Container Apps configuration
az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --output json

# Verify environment variables
az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query properties.template.containers[0].env
```

## 🔒 Security Best Practices

1. **Docker Hub Security**
   - Use access tokens instead of passwords
   - Regularly rotate access tokens
   - Use private repositories for sensitive images
   - Enable 2FA on Docker Hub account

2. **Image Security**
   ```bash
   # Scan images for vulnerabilities
   docker scan your-username/nutrifit-agents-api:latest
   
   # Use specific image tags instead of latest
   az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
     --image your-username/nutrifit-agents-api:v1.0.0
   ```

3. **Azure Security**
   ```bash
   # Use Azure Key Vault for secrets
   az keyvault secret set --vault-name nutrifit-kv --name azure-openai-api-key --value "your-api-key"
   
   # Reference from Container App
   az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
     --set-env-vars AZURE_OPENAI_API_KEY=secretref:azure-openai-api-key
   ```

## 📈 Performance Optimization

### **Docker Hub Optimization**

```bash
# Use multi-stage builds to reduce image size
# The Dockerfile.prod already includes this optimization

# Use .dockerignore to exclude unnecessary files
# This is already configured in the project

# Use specific base images
# Using python:3.11-slim for smaller size
```

### **Azure Container Apps Optimization**

```bash
# Optimize for cost
az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
  --min-replicas 0 \
  --max-replicas 5 \
  --cpu 0.5 \
  --memory 1Gi

# Configure auto-scaling
az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 100 \
  --scale-rule-http-concurrency-target 50
```

## 🎯 Testing Your Deployment

```bash
# Get your app URL
APP_URL=$(az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query properties.configuration.ingress.fqdn --output tsv)

# Test health endpoint
curl -f "https://$APP_URL/health"

# Test status endpoint
curl -f "https://$APP_URL/status"

# Test workflow endpoint
curl -X POST "https://$APP_URL/workflow/create_complete_plan" \
  -H "Content-Type: application/json" \
  -d '{
    "inbody_image_url": "https://example.com/inbody-scan.jpg",
    "client_country": "Egypt",
    "goals": "Weight loss and muscle building",
    "allergies": "Lactose intolerant"
  }'
```

## 📞 Support

For issues and questions:
1. Check Docker Hub documentation
2. Review Azure Container Apps logs
3. Test API endpoints
4. Check GitHub Actions workflow logs
5. Review this deployment guide

## 🔗 Useful Links

- [Docker Hub Documentation](https://docs.docker.com/docker-hub/)
- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [GitHub Actions for Docker](https://github.com/marketplace?type=actions&query=docker)
- [Azure CLI Container Apps Commands](https://docs.microsoft.com/en-us/cli/azure/containerapp) 
