# Enterprise IT Helpdesk Agent

A secure, Azure-ready enterprise IT Helpdesk backend built with **Python, FastAPI, JWT authentication, role-based authorization, and Azure identity-based resource access**.

The project is being developed incrementally with a strong focus on:

* Authentication
* Authorization
* Managed identities
* Azure RBAC
* Least privilege
* Secure configuration
* Knowledge-base integration
* AI agent architecture
* Production-ready engineering practices

> **Current scope:** The application does not use Microsoft Entra ID for end-user authentication. Application users are currently managed through the internal development user repository. Azure Managed Identity is used for application-to-Azure authentication.

---

# Project Vision

The goal is to build an internal IT Helpdesk Agent capable of:

* Creating and managing IT support tickets
* Authenticating employees
* Applying role-based permissions
* Searching enterprise knowledge
* Accessing Azure resources securely
* Providing AI-powered IT assistance
* Integrating with future ITSM workflows
* Supporting production enterprise security requirements

---

# Architecture

The current high-level architecture is:

```text
                         Employee
                            |
                            v
                    +---------------+
                    |   FastAPI API |
                    +-------+-------+
                            |
                +-----------+-----------+
                |                       |
                v                       v
         Authentication          Authorization
                |                       |
                v                       v
              JWT                  Role/Permission
                                        |
                                        v
                              +-------------------+
                              | Helpdesk Services |
                              +---------+---------+
                                        |
                       +----------------+----------------+
                       |                                 |
                       v                                 v
                Azure Services                     AI Services
                       |                                 |
              +--------+--------+                        |
              |                 |                        |
              v                 v                        v
         Blob Storage       Key Vault              AI Provider
              |
              v
       Knowledge Base
```

---

# Technology Stack

## Backend

* Python 3.12+
* FastAPI
* Pydantic
* Pydantic Settings
* Uvicorn

## Authentication

* JWT
* Password hashing
* Internal user repository
* FastAPI security dependencies

## Authorization

* Role-based authorization
* Permission-based access control
* Protected API endpoints

## Azure

* Azure Identity
* `DefaultAzureCredential`
* Azure Blob Storage
* Azure Key Vault
* Azure RBAC
* Application Insights / OpenTelemetry

## AI Architecture

* AI service abstraction
* Helpdesk agent layer
* Provider-independent design
* Azure OpenAI integration planned

## Development Tools

* Git
* GitHub
* Visual Studio Code
* Pylance
* Ruff
* Mypy
* Pytest
* Azure CLI

---

# Current Development Status

| Component                      | Status      |
| ------------------------------ | ----------- |
| Repository foundation          | Completed   |
| Python environment             | Completed   |
| Configuration management       | Completed   |
| Azure identity foundation      | Completed   |
| JWT authentication             | Completed   |
| Password hashing               | Completed   |
| User repository                | Completed   |
| Role-based authorization       | Completed   |
| Ticket API                     | Completed   |
| Azure Blob Storage integration | Completed   |
| Azure Key Vault integration    | Completed   |
| Security logging foundation    | Completed   |
| Helpdesk agent abstraction     | Completed   |
| AI service abstraction         | Completed   |
| Chat API foundation            | Completed   |
| Azure OpenAI integration       | In progress |
| RAG knowledge retrieval        | Planned     |
| ITSM integration               | Planned     |
| Production hardening           | Planned     |

---

# Identity Model

The project intentionally separates **user authentication** from **Azure resource authentication**.

## Application User Authentication

```text
Employee
   |
   v
Login API
   |
   v
User Repository
   |
   v
Password Verification
   |
   v
  JWT
   |
   v
Protected API
```

The current application does not require Microsoft Entra ID for employee login.

---

# Azure Application Identity

Azure resources are accessed using:

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

Authenticate locally:

```powershell
az login
```

Verify:

```powershell
az account show
```

## Azure Hosting

Production Azure hosting is designed to use managed identity:

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

This avoids storing Azure credentials inside the application.

---

# Authentication

The application uses JWT authentication for protected APIs.

Login flow:

```text
POST /auth/login
       |
       v
Username + Password
       |
       v
User Repository
       |
       v
Password Verification
       |
       v
JWT Access Token
       |
       v
Authorization: Bearer <token>
```

Example:

```http
Authorization: Bearer <access-token>
```

Protected routes validate the JWT before processing the request.

---

# Authorization

Authentication determines:

```text
Who are you?
```

Authorization determines:

```text
What are you allowed to do?
```

The application uses role-based permissions.

Example:

```text
Employee
   |
   +--> ticket:create
   +--> ticket:read
   +--> chat:use
   +--> knowledge:read
```

Administrative permissions are separated:

```text
Admin
   |
   +--> ticket:manage
   +--> user:read
   +--> user:manage
   +--> configuration:read
```

Authorization is enforced server-side.

---

# Ticket Workflow

```text
Employee
   |
   v
JWT Authentication
   |
   v
Authorization
   |
   v
Ticket API
   |
   v
Ticket Service
   |
   v
Helpdesk Ticket
```

The backend validates the authenticated user before allowing protected ticket operations.

---

# Knowledge Base

The knowledge base is designed around Azure Blob Storage.

```text
Helpdesk Agent
      |
      v
Knowledge Service
      |
      v
DefaultAzureCredential
      |
      v
Managed Identity
      |
      v
 Azure RBAC
      |
      v
Azure Blob Storage
      |
      v
IT Documentation
```

The application should use read-only access where only document retrieval is required.

Recommended role:

```text
Storage Blob Data Reader
```

---

# Key Vault

Sensitive application configuration can be retrieved from Azure Key Vault.

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
Azure RBAC
    |
    v
Azure Key Vault
```

Recommended access for secret retrieval:

```text
Key Vault Secrets User
```

The application should not require secret-management permissions unless explicitly needed.

---

# AI Helpdesk Agent

The project contains an AI-ready architecture.

```text
Employee
    |
    v
Chat API
    |
    v
Helpdesk Agent
    |
    v
AI Service
    |
    v
AI Provider
```

The AI service is separated from the API and agent layers.

This allows the provider implementation to evolve without tightly coupling the application API to a specific AI SDK.

## Current AI Architecture

```text
app/
├── agents/
│   └── helpdesk_agent.py
│
├── services/
│   └── ai_service.py
│
├── models/
│   └── chat.py
│
└── api/
    └── chat.py
```

The next major AI milestone is Azure OpenAI integration.

---

# Security Model

The application follows defense in depth.

```text
User Authentication
        |
        v
JWT Validation
        |
        v
Application Authorization
        |
        v
Azure Identity
        |
        v
Azure RBAC
        |
        v
Azure Resource
```

Security principles include:

* No secrets in source code
* Environment-based configuration
* JWT validation
* Server-side authorization
* Managed identity for Azure access
* Least-privilege permissions
* Protected Azure resources
* Security-focused logging

See:

```text
docs/security-model.md
```

for the detailed security model.

---

# Least Privilege

Permissions should be limited to the smallest scope required.

For example:

```text
Required:
Storage Blob Data Reader
```

Avoid unnecessarily broad permissions:

```text
Owner
Contributor
```

Every new permission should have:

1. A documented purpose
2. A defined security boundary
3. A documented compromise impact
4. A review for permission reduction

---

# Configuration

Application configuration is managed through environment variables.

Create the local configuration file:

```powershell
copy .env.example .env
```

The `.env` file must never be committed.

Example configuration:

```env
APP_NAME="Enterprise IT Helpdesk Agent"
ENVIRONMENT="development"

JWT_SECRET="local-development-secret"
JWT_ALGORITHM="HS256"
JWT_EXPIRY_MINUTES=480

AZURE_STORAGE_ACCOUNT="storage-account"
AZURE_CONTAINER="knowledge-base"

KEYVAULT_NAME="keyvault-name"
```

Production secrets should be managed through appropriate Azure services rather than committed configuration files.

---

# Repository Structure

```text
enterprise-it-helpdesk-agent/
│
├── app/
│   ├── agents/
│   │   └── helpdesk_agent.py
│   │
│   ├── api/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── configuration.py
│   │   └── tickets.py
│   │
│   ├── core/
│   │   ├── azure_identity.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   └── security.py
│   │
│   ├── database/
│   │   └── users.py
│   │
│   ├── middleware/
│   │
│   ├── models/
│   │   ├── chat.py
│   │   ├── ticket.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── keyvault_service.py
│   │   └── storage_service.py
│   │
│   └── main.py
│
├── docs/
│   ├── architecture.md
│   ├── development.md
│   └── security-model.md
│
├── tests/
│   ├── test_azure_identity.py
│   ├── test_config.py
│   ├── test_token.py
│   └── test_users.py
│
├── .env.example
├── .gitignore
├── pyproject.toml
├── requirements.txt
└── README.md
```

---

# Local Development

The project does not use Docker.

## Requirements

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

# Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

---

# Install Dependencies

```powershell
python -m pip install --upgrade pip
pip install -r requirements.txt
```

---

# Configure Environment

```powershell
copy .env.example .env
```

Update `.env` with local development values.

Never commit:

```text
.env
```

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

Swagger documentation:

```text
http://localhost:8000/docs
```

ReDoc:

```text
http://localhost:8000/redoc
```

---

# Testing

Run the complete test suite:

```powershell
pytest
```

Run with verbose output:

```powershell
pytest -v
```

Run a specific test:

```powershell
pytest tests/test_token.py
```

---

# Code Quality

## Ruff

Run:

```powershell
ruff check .
```

Automatically fix supported issues:

```powershell
ruff check . --fix
```

---

# Mypy

Run:

```powershell
mypy .
```

The project uses static typing to catch problems before runtime.

---

# Python Compilation

Run:

```powershell
python -m compileall app
```

---

# Recommended Validation

Before committing:

```powershell
ruff check .
mypy .
pytest
python -m compileall app
```

All checks should pass before pushing changes.

---

# Development Workflow

Development is organized into small, documented steps.

For each development step:

```text
Implement
   |
   v
Refactor
   |
   v
 Test
   |
   v
Run Ruff
   |
   v
Run Mypy
   |
   v
Update Documentation
   |
   v
Git Commit
   |
   v
Git Push
```

Documentation should be updated whenever architecture, security, configuration, or development procedures change.

---

# Documentation

Important documentation:

| Document                 | Purpose                                                     |
| ------------------------ | ----------------------------------------------------------- |
| `docs/development.md`    | Development workflow and setup                              |
| `docs/architecture.md`   | Application and Azure architecture                          |
| `docs/security-model.md` | Authentication, authorization, identity and least privilege |

---

# Development Roadmap

## Phase 1 — Repository Foundation

Completed:

* Python project structure
* Git repository
* Dependency management
* Development environment

## Phase 2 — Configuration and Security

Completed:

* Pydantic Settings
* Environment configuration
* Password hashing
* JWT authentication
* Protected API endpoints

## Phase 3 — Authorization

Completed:

* Application roles
* Permission model
* Protected endpoints
* Employee/Admin separation

## Phase 4 — Azure Identity

Completed:

* Azure Identity integration
* `DefaultAzureCredential`
* Managed Identity-ready architecture
* Azure CLI development authentication

## Phase 5 — Azure Services

Completed:

* Azure Blob Storage integration
* Azure Key Vault integration
* Identity-based Azure access
* Least-privilege security model

## Phase 6 — Helpdesk Agent Foundation

Completed:

* Chat request/response models
* Chat API
* Helpdesk agent abstraction
* AI service abstraction

## Phase 7 — Azure OpenAI

**Current development step**

Planned:

* Azure OpenAI client integration
* Secure Azure authentication
* Model configuration
* Chat completion workflow
* AI service error handling
* AI request/response logging
* Token and request safeguards

## Phase 8 — Knowledge Retrieval

Planned:

* Knowledge-base retrieval
* Document processing
* RAG pipeline
* Retrieval authorization
* Grounded AI responses

## Phase 9 — ITSM Automation

Planned:

* Ticket creation through AI
* Ticket classification
* Priority detection
* Assignment workflows
* ITSM integration

## Phase 10 — Production Hardening

Planned:

* Azure RBAC deployment
* Application monitoring
* Security alerting
* Audit logging
* Dependency scanning
* Security testing
* Production identity integration

---

# Git Commit Convention

Use Conventional Commits.

Feature:

```text
feat: add feature name
```

Bug fix:

```text
fix: correct issue description
```

Documentation:

```text
docs: update documentation
```

Refactoring:

```text
refactor: improve component name
```

Testing:

```text
test: add authentication tests
```

Maintenance:

```text
chore: update dependencies
```

Example:

```powershell
git add .
git commit -m "feat: integrate azure openai service"
git push origin main
```

---

# Security Rules

Always:

* Never commit `.env`
* Never hardcode secrets
* Never log passwords
* Never log access tokens
* Validate JWTs before protected operations
* Enforce authorization on the backend
* Use managed identity for Azure resources
* Prefer Azure RBAC over shared credentials
* Use the smallest required permission
* Keep Azure access read-only where possible
* Update security documentation when permissions change

---

# Project Principles

## Secure by Default

Security controls should be part of the application architecture rather than added later.

## Least Privilege

Every identity should receive only the permissions it requires.

## Separation of Responsibilities

Authentication, authorization, business logic, Azure services, and AI services should remain independently testable.

## Provider Abstraction

AI providers should be accessed through an application service layer rather than directly from API routes.

## Documentation as Code

Architecture and security documentation should evolve with the implementation.

## Small Commits

Each development step should produce a focused, reviewable Git commit.

---

# License

This project is currently intended as an enterprise IT Helpdesk Agent development project.

Add an explicit open-source license before publishing the repository for external reuse.
