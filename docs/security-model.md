# Security Model


## Authentication

Implemented using:

- JWT tokens
- Password hashing
- Bearer authentication


## Authorization

Roles:

employee:
- Create tickets


admin:
- Manage tickets


## Azure Access

Application never stores:

- Storage keys
- Connection strings
- Secrets


Uses:

DefaultAzureCredential

with:

Managed Identity in Azure
Azure CLI locally