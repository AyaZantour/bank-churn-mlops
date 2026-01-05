#!/bin/bash

RESOURCE_GROUP="rg-mlops"
LOCATION="francecentral"
ACR_NAME="acrmlops$(whoami)$(date +%s)"


# Création du Container Registry
echo "Création du Container Registry..."
az acr create \
  --resource-group $RESOURCE_GROUP \
  --name $ACR_NAME \
  --sku Basic \
  --admin-enabled true \
  --location $LOCATION

echo "✅ Container Registry créé : $ACR_NAME"

# Se connecter au registry
echo "Connexion au registry..."
az acr login --name $ACR_NAME

# Vérification de la connexion au registry
echo "Vérification de la connexion..."
az acr check-health --name $ACR_NAME --ignore-errors
