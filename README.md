# Enterprise IT Helpdesk Agent

A secure, modular enterprise IT helpdesk backend built with **Python, FastAPI, and Microsoft Azure**.

The project demonstrates enterprise application patterns including:

* JWT-based authentication
* Role-based authorization
* Least-privilege security
* Azure Managed Identity
* Azure RBAC
* Azure Blob Storage integration
* Azure Key Vault integration
* Audit logging and monitoring
* AI-ready helpdesk agent architecture
* Automated testing and code quality validation

The application is developed **without Docker** using a standard Python virtual environment workflow.

---

# Project Vision

The goal is to build an internal IT Helpdesk Agent capable of:

* Handling employee IT requests
* Creating and managing support tickets
* Accessing enterprise knowledge resources
* Providing authenticated employee assistance
* Using Azure resources securely
* Supporting AI-powered troubleshooting
* Integrating with future ITSM platforms

The architecture is designed so that AI, RAG, and ITSM capabilities can be added without redesigning the security foundation.

---

# Technology Stack

## Backend

* Python 3.12+
* FastAPI
* Pydantic
* Pydantic Settings
* SQLAlchemy foundation

## Authentication and Security

* JWT authentication
* Password hashing
* Role-based access control
* Application-level permissions
* Azure Managed Identity
* Azure RBAC
* Least-privilege design

## Azure

* Azure Identity
* Azure Blob Storage
* Azure Key Vault
* Azure Monitor / Application Insights foundation

## AI Architecture

* Helpdesk Agent
* AI Service abstraction
* Provider-independent AI interface
* Azure OpenAI integration planned

## Development Tools

* pytest
* Ruff
* Black
* Pylance
* Visual Studio Code
* Azure CLI

---

# Current Development Status

| Capability                | Status      |
| ------------------------- | ----------- |
| Repository foundation     | ✅ Completed |
| Configuration management  | ✅ Completed |
| Azure identity foundation | ✅ Completed |
| JWT authentication        | ✅ Completed |
| Password security         | ✅ Completed |
| Role-based authorization  | ✅ Completed |
| Ticket API                | ✅ Completed |
| Azure Blob Storage        | ✅ Completed |
| Azure Key Vault           | ✅ Completed |
| Azure RBAC model          | ✅ Completed |
| Least-privilege model     | ✅ Completed |
| Audit logging             | ✅ Completed |
| Monitoring foundation     | ✅ Completed |
| AI service abstraction    | ✅ Completed |
| Helpdesk agent            | ✅ Completed |
| Protected chat API        | ✅ Completed |
| Azure OpenAI integration  | ⏳ Next      |
| RAG knowledge retrieval   | ⏳ Planned   |
| ITSM automation           | ⏳ Planned   |

---

# Architecture

## High-Level Architecture

```text
                         Employee
                            |
                            v
                    +---------------+
                    |   FastAPI API  |
                    +-------+-------+
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
       Authentication   Authorization    Audit
             |              |              |
             +--------------+--------------+
                            |
                            v
                    Application Services
                            |
             +--------------+--------------+
             |              |              |
             v              v              v
        Ticket Service  Knowledge      AI Agent
                         Service           |
             |              |              |
             |              v              v
             |        Azure Blob      AI Service
             |                           |
             |                           v
             |                     Azure OpenAI
             |
             v
       Application Data
```

Azure resource access is performed through the Azure identity layer:

```text
Application
    |
DefaultAzureCredential
    |
Managed Identity
    |
Azure RBAC
    |
Azure Resource
```

---

# Authentication Flow

The current development authentication model uses the application's internal user repository.

```text
Employee
    |
    v
Login API
    |
    v
Username / Password
        |
        v
Password Verification
        |
        v
JWT Access Token
    |
    v
Protected API
```

Protected endpoints validate the JWT before processing the request.

---

# Authorization Model

The application separates authentication from authorization.

## Authentication

Answers:

```text
Who are you?
```

## Authorization

Answers:

```text
What are you allowed to do?
```

The application uses role-based permissions:

```text
       User
        |
        v
        Role
        |
        v
    Permission
        |
        v
Protected Endpoint
```

Example:

```text
Employee
    |
    +-- ticket:create
    +-- ticket:view

Admin
    |
    +-- ticket:create
    +-- ticket:view
    +-- user:manage
```

---

# Azure Identity Architecture

Azure credentials are not stored in application source code.

The application uses:

```text
DefaultAzureCredential
```

## Local Development

```text
Developer Machine
        |
        v
Azure CLI Login
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

## Azure Hosting

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

This allows the same application code to work in development and Azure-hosted environments.

### Benefits

* No Azure credentials in source code
* No storage account keys
* No application secrets for Azure authentication
* Identity-based access
* RBAC enforcement
* Least-privilege permissions

---

# Azure Blob Storage

Azure Blob Storage provides the foundation for the enterprise knowledge base.

```text
Helpdesk Agent
      |
      v
Knowledge Service
      |
      v
Azure Identity
      |
      v
Azure Blob Storage
      |
      v
IT Documentation
```

The application uses identity-based authentication rather than storage account keys.

---

# Azure Key Vault

Key Vault provides secure secret retrieval.

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

The application should never hardcode production secrets.

---

# AI Helpdesk Agent

The AI foundation is implemented using separate agent and service layers.

```text
Employee
    |
    v
POST /chat
    |
    v
HelpdeskAgent
    |
    v
AIService
    |
    v
AI Provider
```

The current AI provider is a placeholder implementation.

The next phase will replace it with Azure OpenAI:

```text
HelpdeskAgent
    |
    v
AIService
    |
    v
Azure OpenAI
```

The API and agent layers should not need to change when the provider is replaced.

---

# Knowledge and AI Roadmap

The future RAG architecture is:

```text
Employee
    |
    v
Helpdesk Agent
    |
    +------------------+
    |                  |
    v                  v
AI Service       Knowledge Service
    |                  |
    v                  v
Azure OpenAI      Blob / Search
    |                  |
    +--------+---------+
             |
             v
       Grounded Response
```

Future capabilities include:

* Enterprise document retrieval
* Context-aware troubleshooting
* Knowledge-grounded responses
* IT policy assistance
* Automated ticket creation

---

# Monitoring and Auditing

The application includes an audit and logging foundation.

```text
          HTTP Request
                |
                v
         Audit Middleware
                |
                v
        Application Logging
                |
                v
          OpenTelemetry
                |
                v
Azure Monitor / Application Insights
```

Security-relevant events include:

* Authentication events
* Failed authentication
* API requests
* Authorization failures
* Application errors

Production monitoring will be expanded as the application moves toward deployment.

---

# Security Model

The project follows defense-in-depth principles.

## Application Security

* JWT authentication
* Password hashing
* Role-based authorization
* Protected API endpoints
* Request validation

## Azure Security

* Managed Identity
* Azure RBAC
* Key Vault
* Identity-based resource access

## Least Privilege

Only the minimum required permissions should be granted.

For example:

```text
Required: Storage Blob Data Reader
```

Preferred over:

```text
Storage Contributor
```

and:

```text
Owner
```

unless those permissions are explicitly required.

---

# Configuration

Application configuration is managed using Pydantic Settings.

Local configuration:

```text
.env
```

Example configuration:

```text
APP_NAME
ENVIRONMENT
JWT_SECRET
JWT_ALGORITHM
JWT_EXPIRY_MINUTES
AZURE_STORAGE_ACCOUNT
AZURE_CONTAINER
KEYVAULT_NAME
```

The `.env` file must never be committed.

Only:

```text
.env.example
```

belongs in source control.

---

# Repository Structure

```text
enterprise-it-helpdesk-agent/
|
├── app/
│   |
│   ├── agents/
│   │   ├── __init__.py
│   │   └── helpdesk_agent.py
│   |
│   ├── api/
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── configuration.py
│   │   ├── knowledge.py
│   │   └── tickets.py
│   |
│   ├── core/
│   │   ├── azure_identity.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   |
│   ├── database/
│   │   └── users.py
│   |
│   ├── middleware/
│   │   └── audit.py
│   |
│   ├── models/
│   │   ├── chat.py
│   │   ├── ticket.py
│   │   └── user.py
│   |
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── blob_storage.py
│   │   └── key_vault.py
│   |
│   └── main.py
|
├── docs/
│   ├── architecture.md
│   ├── development.md
│   └── security-model.md
|
├── tests/
│   ├── test_azure_identity.py
│   ├── test_config.py
│   ├── test_token.py
│   └── test_users.py
|
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# Local Development

## Requirements

Install:

* Python 3.12+
* Git
* Visual Studio Code
* Azure CLI

Python 3.14 is currently used for development.

Verify:

```powershell
python --version
```

---

## Create Virtual Environment

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

## Install Dependencies

```powershell
pip install -r requirements.txt
```

---

## Configure Environment

```powershell
copy .env.example .env
```

Update `.env` with local development values.

Never commit `.env`.

---

# Run the Application

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

OpenAPI:

```text
http://localhost:8000/openapi.json
```

---

# Testing

Run all tests:

```powershell
pytest -v
```

Run test collection:

```powershell
pytest --collect-only -v
```

Run a specific test:

```powershell
pytest tests/test_token.py -v
```

---

# Code Quality

Run Ruff:

```powershell
ruff check .
```

Automatically fix supported issues:

```powershell
ruff check . --fix
```

Compile the application:

```powershell
python -m compileall app
```

The project should pass:

```text
Ruff
Pylance
Python compilation
pytest
```

before changes are committed.

---

# Azure Development

Login:

```powershell
az login
```

Verify the active account:

```powershell
az account show
```

The application uses:

```text
DefaultAzureCredential
```

for Azure SDK authentication.

---

# Development Workflow

Each development step follows:

```text
Implement
    |
    v
Update Tests
    |
    v
Update Documentation
    |
    v
Ruff
    |
    v
Compile
    |
    v
Pytest
    |
    v
Git Commit
```

Example:

```powershell
ruff check .
python -m compileall app
pytest -v
```

Then commit:

```powershell
git add .
git commit -m "feat: add feature description"
git push origin main
```

---

# Development Roadmap

## Step 1 — Repository Foundation

Completed:

* Python project structure
* Dependency management
* Git configuration

## Step 2 — Configuration Management

Completed:

* Pydantic Settings
* Environment configuration
* `.env` support

## Step 3 — Azure Identity Foundation

Completed:

* `DefaultAzureCredential`
* Azure CLI development authentication
* Managed Identity-ready architecture

## Step 4 — User and Password Security

Completed:

* User model
* Password hashing
* User repository
* Role support

## Step 5 — Authentication

Completed:

* Login API
* JWT generation
* Password verification
* Protected authentication flow

## Step 6 — Helpdesk Tickets

Completed:

* Ticket model
* Ticket API
* Protected ticket endpoints

## Step 7 — Azure Blob Storage

Completed:

* Blob Storage service
* Managed Identity authentication
* Knowledge base endpoint

## Step 8 — Azure Key Vault

Completed:

* Key Vault service
* Secret retrieval pattern
* Managed Identity authentication

## Step 9 — Authorization

Completed:

* Application RBAC
* Employee/Admin roles
* Permission model
* Protected administrative endpoints

## Step 10 — Least Privilege

Completed:

* Azure RBAC model
* Managed Identity permissions
* Resource access boundaries
* Least-privilege security review

## Step 11 — Security Hardening

Completed:

* Structured logging
* Audit middleware
* Authentication event logging
* Monitoring foundation

## Step 12 — AI Helpdesk Agent Foundation

Completed:

* Chat request/response models
* AI service abstraction
* Helpdesk agent orchestration
* Protected `/chat` endpoint
* AI workflow foundation

## Step 13 — Azure OpenAI Integration

Next:

* Azure OpenAI client
* Managed Identity authentication
* Model configuration
* Production AI service
* Prompt management
* AI error handling
* AI service tests

## Step 14 — RAG Knowledge Base

Planned:

* Document ingestion
* Chunking
* Embeddings
* Vector/search layer
* Context retrieval
* Grounded responses

## Step 15 — ITSM Automation

Planned:

* Ticket automation
* Workflow orchestration
* ITSM integration
* Agent actions
* Approval workflows

---

# Security Rules

Always:

* Use environment variables for local configuration
* Never commit `.env`
* Never hardcode secrets
* Use Managed Identity for Azure resources
* Use Azure RBAC
* Apply least privilege
* Protect sensitive endpoints
* Validate authentication and authorization
* Audit security-relevant operations
* Keep dependencies and documentation synchronized

Never:

* Commit passwords
* Commit API keys
* Commit Azure credentials
* Use `Owner` when a narrower role is sufficient
* Store production secrets in source code

---

# Documentation

Project documentation is maintained in:

```text
docs/
├── architecture.md
├── development.md
└── security-model.md
```

When architecture or security behavior changes, update the relevant documentation in the same commit.

---

# Git Commit Convention

Use Conventional Commit-style messages.

Feature:

```text
feat: add azure openai service
```

Bug fix:

```text
fix: correct jwt validation
```

Refactoring:

```text
refactor: simplify authentication service
```

Documentation:

```text
docs: update architecture documentation
```

Tests:

```text
test: add chat endpoint coverage
```

Maintenance:

```text
chore: update dependencies
```

---

# Project Status

The project has completed its **identity, authentication, authorization, Azure resource access, least-privilege, monitoring, and AI-agent foundation**.

The next major development milestone is:

```text
Azure OpenAI Integration
```

followed by:

```text
RAG Knowledge Base
        |
        v
ITSM Automation
        |
        v
Production Hardening
```

The long-term goal is a secure, auditable enterprise IT support agent capable of combining employee identity, enterprise knowledge, AI reasoning, and controlled ITSM actions.
