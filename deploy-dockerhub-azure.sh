#!/bin/bash

# Azure Container Apps Deployment Script for NutriFit Agents API (Docker Hub)
# Prerequisites: Azure CLI, Docker, Docker Hub account

set -e

# Configuration Variables
RESOURCE_GROUP="nutrifit-rg"
LOCATION="eastus"
CONTAINER_APP_NAME="nutrifit-agents-api"
ENVIRONMENT_NAME="nutrifit-env"
IMAGE_NAME="nutrifit-agents-api"
DOCKER_HUB_USERNAME="your-dockerhub-username"  # Change this to your Docker Hub username
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

# Check if logged in to Docker Hub
if ! docker info | grep -q "Username"; then
    echo -e "${YELLOW}⚠️  Not logged in to Docker Hub. Please run 'docker login' first.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ Prerequisites check passed${NC}"

# Step 1: Create Resource Group
echo -e "${YELLOW}📦 Creating Resource Group...${NC}"
az group create \
    --name $RESOURCE_GROUP \
    --location $LOCATION \
    --output table

# Step 2: Build and Push Docker Image to Docker Hub
echo -e "${YELLOW}🐳 Building and pushing Docker image to Docker Hub...${NC}"

# Build the production image
docker build -f Dockerfile.prod -t $DOCKER_HUB_USERNAME/$IMAGE_NAME:$IMAGE_TAG .

# Push the image to Docker Hub
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
sleep 30  # Wait for the app to be ready

# Test health endpoint
if curl -f "https://$APP_URL/health" > /dev/null 2>&1; then
    echo -e "${GREEN}✅ Health check passed${NC}"
else
    echo -e "${RED}❌ Health check failed${NC}"
fi

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
