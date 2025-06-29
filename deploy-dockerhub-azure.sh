#!/bin/bash

# Azure Container Apps Deployment Script for NutriFit Agents API (Docker Hub)
# Prerequisites: Azure CLI, Docker, Docker Hub account

set -e

# Configuration Variables
RESOURCE_GROUP="nutrifit"
LOCATION="uaenorth"
CONTAINER_APP_NAME="nutrifit-agents-api"
ENVIRONMENT_NAME="nutrifit-env"
IMAGE_NAME="nutrifit-agents-api"
DOCKER_HUB_USERNAME="shehap62"  # Change this to your Docker Hub username
IMAGE_TAG="latest"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}🚀 Starting Azure Container Apps Deployment with Docker Hub${NC}"

# Check if Azure CLI is installed
if ! command -v az &> /dev/null; then
    echo -e "${RED}❌ Azure CLI is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if Docker is installed
if ! command -v docker &> /dev/null; then
    echo -e "${RED}❌ Docker is not installed. Please install it first.${NC}"
    exit 1
fi

# Check if logged in to Azure
if ! az account show &> /dev/null; then
    echo -e "${YELLOW}⚠️  Not logged in to Azure. Please run 'az login' first.${NC}"
    exit 1
fi

# Check if logged in to Docker Hub (improved check)
echo -e "${YELLOW}🔍 Checking Docker Hub login status...${NC}"
if ! grep -q "index.docker.io" ~/.docker/config.json; then
    echo -e "${GREEN}✅ Docker Hub login detected${NC}"
else
    echo -e "${YELLOW}⚠️  Docker Hub login not detected. Attempting to login...${NC}"
    echo -e "${YELLOW}Please enter your Docker Hub credentials when prompted:${NC}"
    docker login
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Step 0: Register required Azure providers (if possible)
echo -e "${YELLOW}🔧 Checking Azure providers...${NC}"
if az provider show -n Microsoft.App --query registrationState -o tsv 2>/dev/null | grep -q "Registered"; then
    echo -e "${GREEN}✅ Azure providers already registered${NC}"
else
    echo -e "${YELLOW}⚠️  Attempting to register Azure providers...${NC}"
    echo -e "${YELLOW}Note: This requires Owner/Contributor permissions. If it fails, please register manually:${NC}"
    echo -e "${YELLOW}az provider register -n Microsoft.App --wait${NC}"
    echo -e "${YELLOW}az provider register -n Microsoft.OperationalInsights --wait${NC}"
    echo -e "${YELLOW}az provider register -n Microsoft.Insights --wait${NC}"
    echo -e "${YELLOW}az provider register -n Microsoft.OperationsManagement --wait${NC}"
    
    # Try to register providers, but don't fail if it doesn't work
    az provider register -n Microsoft.App --wait || echo -e "${YELLOW}⚠️  Could not register Microsoft.App${NC}"
    az provider register -n Microsoft.OperationalInsights --wait || echo -e "${YELLOW}⚠️  Could not register Microsoft.OperationalInsights${NC}"
    az provider register -n Microsoft.Insights --wait || echo -e "${YELLOW}⚠️  Could not register Microsoft.Insights${NC}"
    az provider register -n Microsoft.OperationsManagement --wait || echo -e "${YELLOW}⚠️  Could not register Microsoft.OperationsManagement${NC}"
fi

# Step 1: Create Resource Group
echo -e "${YELLOW}📦 Creating Resource Group...${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Step 2: Build and Push Docker Image to Docker Hub
echo -e "${YELLOW}🐳 Building and pushing Docker image to Docker Hub...${NC}"

# Build the production image
echo -e "${YELLOW}Building Docker image...${NC}"
docker build -f Dockerfile.prod -t $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG .

# Push the image to Docker Hub
echo -e "${YELLOW}Pushing image to Docker Hub...${NC}"
docker push $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG

echo -e "${GREEN}✅ Docker image pushed to Docker Hub successfully${NC}"

# Step 3: Create Container Apps Environment
echo -e "${YELLOW}🌍 Creating Container Apps Environment...${NC}"
az containerapp env create \
    --name $ENVIRONMENT_NAME \
    --resource-group $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Step 4: Create Container App
echo -e "${YELLOW}🚀 Creating Container App...${NC}"

# Check if Container App exists, update if yes, create if no
if az containerapp show --name $CONTAINER_APP_NAME --resource-group $RESOURCE_GROUP --output none 2>/dev/null; then
    echo -e "${YELLOW}📝 Updating existing Container App...${NC}"
    
    # Update the container app with new image and environment variables
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --image $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG \
        --set-env-vars FLASK_APP=main.py FLASK_ENV=production
    
    # Update secrets separately
    echo -e "${YELLOW}🔐 Updating secrets...${NC}"
    az containerapp secret set \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --secrets \
            azure-openai-endpoint="$AZURE_OPENAI_ENDPOINT" \
            azure-openai-api-key="$AZURE_OPENAI_API_KEY" \
            azure-openai-api-version="$AZURE_OPENAI_API_VERSION" \
            azure-openai-deployment="$AZURE_OPENAI_DEPLOYMENT"
    
    # Update environment variables that reference secrets
    az containerapp update \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --set-env-vars \
            AZURE_OPENAI_ENDPOINT=secretref:azure-openai-endpoint \
            AZURE_OPENAI_API_KEY=secretref:azure-openai-api-key \
            AZURE_OPENAI_API_VERSION=secretref:azure-openai-api-version \
            AZURE_OPENAI_DEPLOYMENT=secretref:azure-openai-deployment
else
    echo -e "${YELLOW}🆕 Creating new Container App...${NC}"
    
    # Create the container app using Docker Hub image
    az containerapp create \
        --name $CONTAINER_APP_NAME \
        --resource-group $RESOURCE_GROUP \
        --environment $ENVIRONMENT_NAME \
        --image $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG \
        --target-port 5000 \
        --ingress external \
        --min-replicas 1 \
        --max-replicas 10 \
        --cpu 1.0 \
        --memory 2Gi \
        --env-vars \
            FLASK_APP=main.py \
            FLASK_ENV=production \
        --secrets \
            azure-openai-endpoint="$AZURE_OPENAI_ENDPOINT" \
            azure-openai-api-key="$AZURE_OPENAI_API_KEY" \
            azure-openai-api-version="$AZURE_OPENAI_API_VERSION" \
            azure-openai-deployment="$AZURE_OPENAI_DEPLOYMENT" \
        --env-vars \
            AZURE_OPENAI_ENDPOINT=secretref:azure-openai-endpoint \
            AZURE_OPENAI_API_KEY=secretref:azure-openai-api-key \
            AZURE_OPENAI_API_VERSION=secretref:azure-openai-api-version \
            AZURE_OPENAI_DEPLOYMENT=secretref:azure-openai-deployment \
        --output table
fi

# Step 5: Get the application URL
echo -e "${YELLOW}🔍 Getting application URL...${NC}"
APP_URL=$(az containerapp show \
    --name $CONTAINER_APP_NAME \
    --resource-group $RESOURCE_GROUP \
    --query properties.configuration.ingress.fqdn \
    --output tsv)

echo -e "${GREEN}🎉 Deployment completed successfully!${NC}"
echo -e "${GREEN}🌐 Application URL: https://$APP_URL${NC}"
echo -e "${GREEN}📊 Health Check: https://$APP_URL/health${NC}"
echo -e "${GREEN}📈 Status Check: https://$APP_URL/status${NC}"
echo -e "${GREEN}🐳 Docker Hub Image: $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG${NC}"

# Step 6: Test the deployment
echo -e "${YELLOW}🧪 Testing deployment...${NC}"
echo -e "${YELLOW}Waiting for application to be ready...${NC}"
sleep 90  # Increased wait time for container to fully start

# Test health endpoint with retries
max_attempts=5
attempt=1

while [ $attempt -le $max_attempts ]; do
    echo -e "${YELLOW}Health check attempt $attempt/$max_attempts...${NC}"
    if curl -f --max-time 30 "https://$APP_URL/ping" > /dev/null 2>&1 || curl -f --max-time 30 "https://$APP_URL/health" > /dev/null 2>&1; then
        echo -e "${GREEN}✅ Health check passed!${NC}"
        break
    else
        echo -e "${RED}❌ Health check attempt $attempt failed${NC}"
        if [ $attempt -eq $max_attempts ]; then
            echo -e "${YELLOW}⚠️  All health check attempts failed, but deployment may still be successful${NC}"
            echo -e "${YELLOW}The application might need more time to start up${NC}"
        else
            sleep 30  # Wait before retry
            attempt=$((attempt + 1))
        fi
    fi
done

echo -e "${GREEN}🎯 Deployment Summary:${NC}"
echo -e "${GREEN}   Resource Group: $RESOURCE_GROUP${NC}"
echo -e "${GREEN}   Container App: $CONTAINER_APP_NAME${NC}"
echo -e "${GREEN}   Environment: $ENVIRONMENT_NAME${NC}"
echo -e "${GREEN}   Docker Hub Image: $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG${NC}"
echo -e "${GREEN}   URL: https://$APP_URL${NC}"

echo -e "${YELLOW}📝 Next steps:${NC}"
echo -e "${YELLOW}   1. Test the API endpoints${NC}"
echo -e "${YELLOW}   2. Set up monitoring and logging${NC}"
echo -e "${YELLOW}   3. Configure custom domain (optional)${NC}"
echo -e "${YELLOW}   4. Set up CI/CD pipeline with GitHub Actions${NC}" 
