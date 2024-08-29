#!/bin/sh

. $_SRC_DIR/dev-env/99.env.sh

az login

# Create a resource group if it doesn't exist, i.e. create-or-update
az group create --name $AZ_RESOURCE_GROUP --location $AZ_LOCATION

# Failing, some CLI issue
az storage account create --name $AZ_STORAGE_ACCOUNT --resource-group $AZ_RESOURCE_GROUP --location $AZ_LOCATION --sku Standard_LRS