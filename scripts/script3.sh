#!/bin/bash

# VARIABLES — VERY IMPORTANT (use the SAME name from script2 output)
RESOURCE_GROUP="rg-mlops"
LOCATION="francecentral"
ACR_NAME="acrmlopsasus1766059224"   # <-- UPDATE WITH YOUR REAL ACR NAME

echo "Récupération de l'URL du registry..."
ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv | tr -d '\r')
echo "Login Server nettoyé : '$ACR_LOGIN_SERVER'"

echo "Tagging des images..."
docker tag bank-churn-api:v1 $ACR_LOGIN_SERVER/bank-churn-api:v1
docker tag bank-churn-api:v1 $ACR_LOGIN_SERVER/bank-churn-api:latest

echo "Pushing des images..."
docker push $ACR_LOGIN_SERVER/bank-churn-api:v1
docker push $ACR_LOGIN_SERVER/bank-churn-api:latest

echo "Vérification des images dans ACR..."
az acr repository list --name $ACR_NAME --output table
az acr repository show-tags --name $ACR_NAME --repository bank-churn-api --output table











#code loul


# # Récupérer l'URL du registry (CORRECTION DU RETOUR CHARIOT)
# echo "Récupération de l'URL du registry..."
# ACR_LOGIN_SERVER=$(az acr show --name $ACR_NAME --query loginServer --output tsv | tr -d '\r')
# echo "Login Server nettoyé : '$ACR_LOGIN_SERVER'"

# # Tagger l'image pour ACR
# echo "Tagging des images..."
# docker tag bank-churn-api:v1 $ACR_LOGIN_SERVER/bank-churn-api:v1
# docker tag bank-churn-api:v1 $ACR_LOGIN_SERVER/bank-churn-api:latest

# # Pousser les images vers ACR
# echo "Pushing des images vers ACR..."
# docker push $ACR_LOGIN_SERVER/bank-churn-api:v1
# docker push $ACR_LOGIN_SERVER/bank-churn-api:latest

# # Vérification
# echo "Vérification des images dans ACR..."
# az acr repository list --name $ACR_NAME --output table
# az acr repository show-tags --name $ACR_NAME --repository bank-churn-api --output table