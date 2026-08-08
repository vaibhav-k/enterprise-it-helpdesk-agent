# Enterprise IT Helpdesk Agent — Development Guide

## Overview

This document explains how to set up, run, test, and contribute to the Enterprise IT Helpdesk Agent.

The project is developed **without Docker** and uses a standard Python virtual environment workflow.

Current development areas include:

* Application configuration
* JWT authentication
* Application authorization
* Azure Managed Identity
* Azure Blob Storage
* Azure Key Vault
* Azure OpenAI integration
* Identity-based Azure authentication
* Automated testing
* Static type checking

---

## Development Environment

### Requirements

Install:

* Python 3.12+
* Git
* Visual Studio Code
* Azure CLI

Verify Python:

```powershell
python --version
```

Verify Git:

```powershell
git --version
```

Verify Azure CLI:

```powershell
az --version
```

---

## Repository Setup

Clone the repository:

```powershell
git clone https://github.com/vaibhav-k/enterprise-it-helpdesk-agent.git
```

Move into the project directory:

```powershell
cd enterprise-it-helpdesk-agent
```

---

## Python Environment Setup

### Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

### Activate Virtual Environment

```powershell
.venv\Scripts\activate
```

Confirm the Python environment:

```powershell
python --version
```

The terminal should show the active virtual environment:

```text
(.venv)
```

---

## Install Dependencies

Install project dependencies:

```powershell
pip install -r requirements.txt
```

Verify installed packages:

```powershell
pip list
```

---

## Environment Configuration

Create a local environment file:

```powershell
copy .env.example .env
```

The application uses environment variables for configuration.

Example Azure OpenAI configuration:

```env
AZURE_OPENAI_ENDPOINT=""
AZURE_OPENAI_DEPLOYMENT=""
AZURE_OPENAI_API_VERSION=""
AZURE_OPENAI_ENABLED="false"
```

The application does **not** use an Azure OpenAI API key.

Do not add:

```env
AZURE_OPENAI_API_KEY
```

Never commit:

```text
.env
```

Only the following template should be committed:

```text
.env.example
```

---

## Azure Development Authentication

The application uses:

```text
DefaultAzureCredential
```

This provides a common authentication abstraction for local development and Azure hosting.

### Local Development

```text
Developer Machine
        |
        v
    Azure CLI
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

Authenticate with Azure:

```powershell
az login
```

Verify the active Azure account:

```powershell
az account show
```

### Azure Hosting

```text
Azure Application
        |
        v
Managed Identity
        |
        v
DefaultAzureCredential
        |
        v
    Azure RBAC
        |
        v
 Azure Resource
```

The same application authentication abstraction is used in both environments.

---

## Azure OpenAI Configuration

The Azure OpenAI integration requires:

```text
AZURE_OPENAI_ENDPOINT
AZURE_OPENAI_DEPLOYMENT
AZURE_OPENAI_API_VERSION
AZURE_OPENAI_ENABLED
```

Example:

```env
AZURE_OPENAI_ENDPOINT="https://<resource-name>.openai.azure.com"
AZURE_OPENAI_DEPLOYMENT="<deployment-name>"
AZURE_OPENAI_API_VERSION="<api-version>"
AZURE_OPENAI_ENABLED="true"
```

These values identify the Azure OpenAI resource and deployment.

They are not authentication credentials.

Authentication is handled through:

```text
DefaultAzureCredential
```

---

## Running the Application

Start the FastAPI development server:

```powershell
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger API documentation:

```text
http://localhost:8000/docs
```

---

## Testing

Run all tests:

```powershell
pytest -v
```

Run a specific test:

```powershell
pytest tests/test_azure_openai.py -v
```

---

## Static Analysis

### Ruff

Run:

```powershell
ruff check .
```

### Mypy

Run:

```powershell
mypy .
```

### Python Compilation

Run:

```powershell
python -m compileall app
```

---

## Recommended Validation

Before committing code, run:

```powershell
ruff check .
python -m compileall app
mypy .
pytest -v
```

All checks should pass before creating a commit.

---

## VS Code

Recommended extensions:

* Python
* Pylance
* Ruff

The project uses strict type checking and static analysis.

Configuration is maintained in:

```text
pyproject.toml
```

and:

```text
.vscode/settings.json
```

---

## Application Structure

```text
app/
├── agents/
│   └── helpdesk_agent.py
│
├── api/
│   ├── auth.py
│   ├── chat.py
│   ├── configuration.py
│   └── tickets.py
│
├── core/
│   ├── azure_identity.py
│   ├── config.py
│   ├── logging.py
│   └── security.py
│
├── database/
│   └── users.py
│
├── models/
│   ├── chat.py
│   ├── ticket.py
│   └── user.py
│
└── services/
    ├── ai_service.py
    ├── azure_openai_service.py
    ├── keyvault_service.py
    └── storage_service.py
```

---

## Azure OpenAI Service Design

Azure OpenAI access is isolated inside the service layer.

```text
Chat API
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
```

The agent does not directly create Azure OpenAI clients.

This keeps provider-specific implementation details isolated from application and agent logic.

---

## Development Milestones

### Step 1 — Repository Foundation

Completed:

* Python project structure
* Dependency management
* Git configuration

### Step 2 — Configuration Management

Completed:

* Pydantic Settings
* Environment variables
* Application configuration

### Step 3 — Azure Identity Foundation

Completed:

* `DefaultAzureCredential`
* Managed Identity-ready design
* Azure CLI development authentication

### Step 4 — User Repository and Password Security

Completed:

* User model
* Password hashing
* User repository
* User roles

### Step 5 — Authentication API

Completed:

* Login API
* JWT generation
* Token validation
* Authentication dependency

### Step 6 — Helpdesk Ticket API

Completed:

* Ticket model
* Protected ticket API
* JWT-protected routes
* Authorization foundation

### Step 7 — Azure Blob Storage

Completed:

* Blob Storage service
* Identity-based authentication
* Knowledge base endpoint
* Storage security documentation

### Step 8 — Azure Key Vault

Completed:

* Key Vault service
* Identity-based authentication
* Secret retrieval pattern
* Key Vault security documentation

### Step 9 — Application Authorization

Completed:

* Application roles
* Permission model
* Protected endpoints
* Employee/Admin separation

### Step 10 — Azure RBAC and Least Privilege

Completed:

* Azure RBAC model
* Managed Identity permission model
* Least privilege documentation
* Resource access boundaries

### Step 11 — Production Hardening Foundation

Completed:

* Application logging
* Audit logging foundation
* Monitoring integration foundation
* Security validation workflow

### Step 12 — AI-Ready Application Architecture

Completed:

* Chat model
* Chat API
* Helpdesk Agent
* AI service abstraction

### Step 13.1 — Azure OpenAI Identity-Based Service

Current:

* Azure OpenAI configuration
* Azure OpenAI service boundary
* `DefaultAzureCredential` integration
* API-key-free authentication design
* Azure OpenAI service validation test

---

## Development Workflow

### 1. Implement

Follow:

* Type hints
* Small modules
* Clear responsibilities
* Dependency injection
* Secure defaults

### 2. Test

```powershell
pytest -v
```

### 3. Static Analysis

```powershell
ruff check .
mypy .
```

### 4. Compile

```powershell
python -m compileall app
```

### 5. Update Documentation

Update relevant files:

```text
README.md
docs/development.md
docs/architecture.md
docs/security-model.md
```

### 6. Commit

Example:

```powershell
git add .
git commit -m "feat: add azure openai identity based service foundation"
git push origin main
```

---

## Security Development Rules

Always:

* Use environment variables for configuration.
* Never commit secrets.
* Do not use Azure service keys when Managed Identity is appropriate.
* Use `DefaultAzureCredential` for Azure authentication.
* Keep Azure RBAC permissions minimal.
* Validate authenticated users.
* Apply application-level authorization.
* Do not expose Key Vault secrets unnecessarily.
* Keep Azure SDK code inside service boundaries.
* Maintain automated tests.
* Run Ruff and mypy before commits.
