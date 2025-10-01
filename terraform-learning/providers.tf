# This file tells Terraform which cloud provider to use
# and what version of Terraform we need

terraform {
  required_version = ">= 1.5"
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 4.0"
    }
  }
}

# Configure the Azure Provider
provider "azurerm" {
  subscription_id = "2c99f8c4-d28c-467b-8b03-15255b312d55"
  features {
    resource_group {
      prevent_deletion_if_contains_resources = false
    }
  }
}


