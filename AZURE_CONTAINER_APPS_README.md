# NutriFit Agents API - Azure Container Apps Deployment Guide

This guide provides step-by-step instructions for deploying the NutriFit Agents API to Azure Container Apps.

## 🚀 Quick Start

### Prerequisites

- Azure CLI installed and configured
- Docker installed
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

### 2. **Deploy with Script**

```bash
# Make script executable
chmod +x deploy-azure-container-apps.sh

# Run deployment
./deploy-azure-container-apps.sh
```

### 3. **Manual Deployment Steps**

If you prefer manual deployment:

```bash
# 1. Login to Azure
az login

# 2. Create Resource Group
az group create --name nutrifit-rg --location eastus

# 3. Create Container Registry
az acr create --resource-group nutrifit-rg --name nutrifitacr --sku Basic --admin-enabled true

# 4. Build and push image
az acr login --name nutrifitacr
docker build -f Dockerfile.prod -t nutrifitacr.azurecr.io/nutrifit-agents-api:latest .
docker push nutrifitacr.azurecr.io/nutrifit-agents-api:latest

# 5. Create Container Apps Environment
az containerapp env create --name nutrifit-env --resource-group nutrifit-rg --location eastus

# 6. Create Container App
az containerapp create \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --environment nutrifit-env \
  --image nutrifitacr.azurecr.io/nutrifit-agents-api:latest \
  --registry-server nutrifitacr.azurecr.io \
  --registry-username $(az acr credential show --name nutrifitacr --query username --output tsv) \
  --registry-password $(az acr credential show --name nutrifitacr --query passwords[0].value --output tsv) \
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

## 🔧 Configuration Options

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

### **Resource Allocation**

```bash
# Update resource allocation
az containerapp update \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --cpu 2.0 \
  --memory 4Gi
```

### **Environment Variables**

```bash
# Add/update environment variables
az containerapp update \
  --name nutrifit-agents-api \
  --resource-group nutrifit-rg \
  --set-env-vars DEBUG=false LOG_LEVEL=info
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

### **Monitor Performance**

```bash
# Get metrics
az monitor metrics list \
  --resource $(az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query id --output tsv) \
  --metric "ReplicaCount" \
  --interval PT1M
```

## 🔄 CI/CD with GitHub Actions

### **Setup GitHub Secrets**

Add these secrets to your GitHub repository:

- `AZURE_CREDENTIALS`: Service principal credentials
- `ACR_USERNAME`: Azure Container Registry username
- `ACR_PASSWORD`: Azure Container Registry password
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

### **Automatic Deployment**

The GitHub Actions workflow will automatically:
1. Build the Docker image
2. Push to Azure Container Registry
3. Deploy to Azure Container Apps
4. Test the deployment
5. Comment on PRs with deployment info

## 🛠️ Troubleshooting

### **Common Issues**

1. **Container fails to start**
   ```bash
   # Check logs
   az containerapp logs show --name nutrifit-agents-api --resource-group nutrifit-rg
   
   # Check environment variables
   az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query properties.template.containers[0].env
   ```

2. **Health check failures**
   ```bash
   # Test health endpoint
   curl -f "https://your-app-url.azurecontainerapps.io/health"
   
   # Check probe configuration
   az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query properties.template.containers[0].probes
   ```

3. **Scaling issues**
   ```bash
   # Check scaling rules
   az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --query properties.template.scale
   
   # Check current replicas
   az containerapp revision show --name nutrifit-agents-api --resource-group nutrifit-rg --revision latest --query properties.replicas
   ```

### **Debug Commands**

```bash
# Get detailed app information
az containerapp show --name nutrifit-agents-api --resource-group nutrifit-rg --output json

# Check ingress configuration
az containerapp ingress show --name nutrifit-agents-api --resource-group nutrifit-rg

# List all revisions
az containerapp revision list --name nutrifit-agents-api --resource-group nutrifit-rg --output table
```

## 🔒 Security Best Practices

1. **Use Azure Key Vault for secrets**
   ```bash
   # Store secrets in Key Vault
   az keyvault secret set --vault-name nutrifit-kv --name azure-openai-api-key --value "your-api-key"
   
   # Reference from Container App
   az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
     --set-env-vars AZURE_OPENAI_API_KEY=secretref:azure-openai-api-key
   ```

2. **Network Security**
   ```bash
   # Use internal ingress for internal access
   az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
     --ingress internal
   ```

3. **Identity-based authentication**
   ```bash
   # Use managed identity
   az containerapp identity assign --name nutrifit-agents-api --resource-group nutrifit-rg \
     --system-assigned
   ```

## 📈 Performance Optimization

### **Auto-scaling Configuration**

```bash
# Configure HTTP-based scaling
az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
  --scale-rule-name http-scaling \
  --scale-rule-type http \
  --scale-rule-http-concurrency 100 \
  --scale-rule-http-concurrency-target 50
```

### **Resource Optimization**

```bash
# Optimize for cost
az containerapp update --name nutrifit-agents-api --resource-group nutrifit-rg \
  --min-replicas 0 \
  --max-replicas 5 \
  --cpu 0.5 \
  --memory 1Gi
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
1. Check Azure Container Apps documentation
2. Review application logs
3. Test API endpoints
4. Check Azure Monitor for metrics
5. Review this deployment guide

## 🔗 Useful Links

- [Azure Container Apps Documentation](https://docs.microsoft.com/en-us/azure/container-apps/)
- [Azure CLI Container Apps Commands](https://docs.microsoft.com/en-us/cli/azure/containerapp)
- [Azure Container Registry](https://docs.microsoft.com/en-us/azure/container-registry/)
- [GitHub Actions for Azure](https://github.com/marketplace?type=actions&query=azure) 
