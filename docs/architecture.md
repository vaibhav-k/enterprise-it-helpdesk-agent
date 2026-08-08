# Enterprise IT Helpdesk Agent — Architecture

## Overview

The Enterprise IT Helpdesk Agent is a secure FastAPI backend designed to evolve into an AI-powered enterprise IT support platform.

The architecture combines:

* JWT-based application authentication
* Application-level authorization
* Azure Managed Identity
* Azure RBAC
* Azure Blob Storage
* Azure Key Vault
* Azure OpenAI
* Identity-based Azure authentication
* AI service abstraction

The application is developed **without Docker** and does not store Azure credentials in source code.

---

## High-Level Architecture

```text
                         Employee
                            |
                            v
                    ┌───────────────┐
                    │ FastAPI API   │
                    └───────┬───────┘
                            |
              ┌─────────────┴─────────────┐
              |                           |
              v                           v
       Authentication               Authorization
              |                           |
              └─────────────┬─────────────┘
                            |
                            v
                     Helpdesk Agent
                            |
                            v
                       AI Service
                            |
                            v
                  Azure OpenAI Service
                            |
                            v
                  DefaultAzureCredential
                            |
                    Managed Identity
                            |
                        Azure RBAC
                            |
             ┌──────────────┼──────────────┐
             |              |              |
             v              v              v
       Blob Storage     Key Vault      Azure Services
```

---

## Application Layers

### API Layer

Location:

```text
app/api/
```

Responsibilities:

* Expose REST endpoints
* Validate requests
* Authenticate users
* Enforce authorization
* Return API responses

Current APIs include:

* Authentication
* Chat
* Configuration
* Tickets
* Health

---

## Agent Layer

Location:

```text
app/agents/
```

The agent layer contains helpdesk orchestration logic.

Current component:

```text
app/agents/helpdesk_agent.py
```

Responsibilities:

* Receive user requests
* Coordinate AI services
* Apply helpdesk-specific behavior
* Prepare for future tools
* Prepare for knowledge retrieval

The agent should not contain Azure SDK authentication logic.

---

## AI Service Layer

Location:

```text
app/services/
```

The AI service layer isolates AI provider integration from the rest of the application.

Architecture:

```text
Helpdesk Agent
      |
      v
  AI Service
      |
      v
Azure OpenAI Service
```

Provider-specific SDK and authentication code remains inside the service layer.

This keeps the agent independent from the Azure OpenAI SDK implementation.

---

## Azure OpenAI Architecture

Azure OpenAI access uses identity-based authentication.

```text
Helpdesk Agent
      |
      v
Azure OpenAI Service
      |
      v
DefaultAzureCredential
      |
      ├───────────────┐
      |               |
      v               v
 Azure CLI      Managed Identity
 Local          Azure Hosting
```

No Azure OpenAI API key is required by the application.

---

## Azure Identity Architecture

### Local Development

```text
Developer
    |
    v
az login
    |
    v
DefaultAzureCredential
    |
    v
Azure SDK
    |
    v
Azure Resource
```

### Azure Deployment

```text
Azure Application
    |
    v
System-Assigned Managed Identity
    |
    v
Azure RBAC
    |
    v
Azure Resource
```

The same application credential abstraction supports both environments.

---

## Knowledge Base Architecture

The knowledge base uses Azure Blob Storage.

```text
Helpdesk Agent
      |
      v
Knowledge Service
      |
      v
Azure Blob Storage
      |
      v
IT Documentation
```

Blob Storage access uses:

```text
DefaultAzureCredential
```

The application does not store storage account credentials.

Future development will add RAG retrieval on top of this foundation.

---

## Key Vault Architecture

Azure Key Vault access is identity-based.

```text
Application
     |
     v
Key Vault Service
     |
     v
DefaultAzureCredential
     |
     v
Managed Identity
     |
     v
Azure Key Vault
```

Key Vault should only contain secrets that genuinely require secret storage.

---

## Security Boundaries

### User Boundary

The application validates:

* Authentication
* User identity
* User role
* API permissions

### Application Boundary

FastAPI controls:

* Request validation
* Authentication dependencies
* Application authorization
* Service orchestration

### Azure Boundary

Azure controls:

* Managed Identity
* RBAC
* Resource authorization
* Key Vault access
* Storage access
* Azure OpenAI access

---

## Defense in Depth

The application has two distinct authorization layers.

### Application Authorization

```text
    User
      |
      v
    JWT
      |
      v
    Role
      |
      v
  Permission
      |
      v
API Endpoint
```

### Azure Authorization

```text
Application
     |
     v
Managed Identity
     |
     v
Azure RBAC
     |
     v
Azure Resource
```

Being authorized to call an application endpoint does not automatically grant access to Azure resources.

---

## AI Request Flow

Current target flow:

```text
      Employee
      |
      v
      POST /chat
      |
      v
JWT Authentication
      |
      v
Application Authorization
      |
      v
Helpdesk Agent
   |
   v
AI Service
   |
   v
Azure OpenAI
   |
   v
Response
```

Future flow:

```text
Employee
   |
   v
Chat API
   |
   v
Helpdesk Agent
   |
   ├── Knowledge Retrieval
   |        |
   |        v
   |   Blob Storage
   |
   ├── Ticket Tools
   |
   ├── Employee Tools
   |
   v
Azure OpenAI
   |
   v
Helpdesk Response
```

---

## Design Principles

### Identity-Based Authentication

Azure services should use:

```text
DefaultAzureCredential
```

instead of embedded credentials.

### Least Privilege

Azure identities should receive only the permissions required for their specific operation.

### Separation of Responsibilities

```text
API
 |
 v
Agent
 |
 v
Service
 |
 v
Azure SDK
```

Each layer should have a clearly defined responsibility.

### Provider Isolation

AI provider-specific implementation belongs inside the AI service layer.

### Secure Configuration

Configuration is loaded through application settings and environment variables.

Secrets must not be hardcoded.

---

## Current Architecture Status

### Completed

* FastAPI backend
* Application authentication
* Application authorization
* Managed Identity foundation
* Blob Storage integration
* Key Vault integration
* AI agent abstraction
* Azure OpenAI identity-based service foundation

### Current

* Azure OpenAI integration

### Planned

* RAG knowledge retrieval
* AI tool calling
* ITSM integration
* Automated ticket workflows
* Production Azure deployment
