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

> **Current scope:** The application does not use Microsoft Entra ID for end-user authentication. Application users are currently managed through the internal development user repository. Azure Managed Identity is used for application-to-Azure authentication. Azure OpenAI integration is implemented, including retry/backoff for transient failures, per-user/per-IP rate limiting, server-side chat session persistence, and propagation of the authenticated user's identity into every Azure OpenAI request for audit and abuse-monitoring purposes.

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
* Azure OpenAI integration (Microsoft Entra ID auth, with an opt-in local-development API key fallback)
* Retry with exponential backoff + jitter for transient Azure OpenAI failures
* Per-user chat rate limiting and per-IP login rate limiting
* Server-side chat session persistence
* End-user identity propagation to Azure OpenAI (`user` field) for traceability

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
| Azure OpenAI integration       | Completed   |
| Retry / backoff (Azure OpenAI) | Completed   |
| Rate limiting (login, chat)    | Completed   |
| Chat session persistence       | Completed   |
| AI request identity propagation| Completed   |
| RAG knowledge retrieval        | Planned     |
| ITSM integration               | Planned     |
| Production hardening           | Planned     |

> Rate limiting and session persistence are in-memory and process-local today (see `app/core/rate_limit.py` and `app/database/sessions.py`). They are correct for a single running instance but need a shared backing store (e.g. Redis) before horizontal scaling.

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

Protected routes validate the JWT before processing the request. `POST /auth/login` itself is intentionally unauthenticated — it does not check any `Authorization` header, since a client must be able to reach it before it has a token. It is rate-limited per client IP instead (see [Rate limiting](#rate-limiting)) to slow credential-guessing attempts.

## Development Users

The in-memory user repository is seeded automatically on startup (`seed_users()`, called from `app/main.py`) with two accounts:

| Username   | Password       | Role     |
| ---------- | -------------- | -------- |
| `employee` | `Password123!` | employee |
| `admin`    | `Admin123!`    | admin    |

This repository is explicitly a development placeholder (see `app/database/users.py`) and is planned to be replaced by a real identity provider or database-backed store.

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

The next major AI milestone is grounded RAG-based knowledge retrieval (see `docs/architecture.md` and Phase 8 below).

---

# Chat Reliability, Sessions, and Identity

Four capabilities harden the chat path beyond a single request/response call:

## Retry with backoff

Transient Azure OpenAI failures (HTTP 429 rate limits, 5xx server errors, timeouts, connection errors) are retried automatically with exponential backoff and jitter, honoring a server-supplied `Retry-After` header when present. Non-transient failures (bad request, authentication, not found) are never retried. Configured via:

```env
AZURE_OPENAI_MAX_RETRIES=3
AZURE_OPENAI_RETRY_BASE_SECONDS=0.5
AZURE_OPENAI_RETRY_MAX_SECONDS=8.0
```

See `app/services/ai_service.py`.

## Rate limiting

An in-memory, per-process sliding-window limiter protects two endpoints:

* `POST /auth/login` — limited per client IP, to slow credential-guessing attempts against an unauthenticated endpoint.
* `POST /chat` — limited per authenticated user, since it is the most expensive and most abuse-sensitive operation in the app.

Both return `429 Too Many Requests` with a `Retry-After` header once exceeded. Configured via:

```env
RATE_LIMIT_LOGIN_MAX_REQUESTS=5
RATE_LIMIT_LOGIN_WINDOW_SECONDS=60
RATE_LIMIT_CHAT_MAX_REQUESTS=20
RATE_LIMIT_CHAT_WINDOW_SECONDS=60
```

This limiter is correct for a single running instance. A horizontally scaled deployment needs a shared store (e.g. Redis), or should enforce limits at a gateway (e.g. Azure API Management) in front of the app. See `app/core/rate_limit.py`.

## Chat session persistence

`POST /chat` no longer requires the client to resend the full conversation on every call. Omit `session_id` to start a new session (the response includes the new `session_id`); pass it back on subsequent calls to continue the same conversation using server-side history.

```text
POST /chat              {"message": "..."}                          -> new session
POST /chat              {"message": "...", "session_id": "<id>"}    -> continues it
GET  /chat/sessions                                                  -> list your own sessions
GET  /chat/sessions/{id}                                              -> full message history
DELETE /chat/sessions/{id}                                            -> delete a session
```

Sessions are strictly scoped to their owner: requesting another user's `session_id` returns `404`, not `403`, so the endpoint never confirms whether a given ID even exists. History is capped per session (`SESSION_MAX_MESSAGES`) and per user (`SESSION_MAX_PER_USER`) to bound memory use and the tokens sent to Azure OpenAI on every turn. Like the rate limiter, this store is in-memory and process-local — see `app/database/sessions.py`.

```env
SESSION_MAX_MESSAGES=20
SESSION_MAX_PER_USER=20
```

## Identity propagation

The authenticated user's identity flows from the JWT through `HelpdeskAgent.process_request` into `AIService.generate_response`, which passes it as Azure OpenAI's documented `user` field on every completion request. This makes every Azure OpenAI call traceable back to the employee who triggered it, for audit and abuse-monitoring purposes. It is deliberately scoped as *observability propagation*, not delegated authorization — the call is still made under the application's own Azure identity (`DefaultAzureCredential` or the local API-key fallback), not a per-user credential. Full delegated, per-user Azure authorization would require a materially different identity model (see Microsoft Entra Agent ID, below).

Each request logs:

```text
INFO ai_service azure_openai_request user=<username>
```

---

# Microsoft Entra Agent ID

This application does **not** implement Microsoft Entra Agent ID (dedicated per-agent identity) or register itself as a non-Foundry agent via an Entra agent identity blueprint. The `HelpdeskAgent` class is a plain in-process Python object with no Entra presence of its own — it borrows the application's own Azure identity for every outbound call. Adopting Entra Agent ID would mean provisioning an agent identity blueprint via Microsoft Graph and giving the agent a credential distinct from the app's hosting identity; this is a meaningful, currently-preview-product undertaking, not a small code change, and is intentionally out of scope for now.

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

# Required. The application refuses to start if this is blank.
JWT_SECRET="local-development-secret"
JWT_ALGORITHM="HS256"
JWT_EXPIRY_MINUTES=480

AZURE_STORAGE_ACCOUNT="storage-account"
AZURE_CONTAINER="knowledge-base"

KEYVAULT_NAME="keyvault-name"

# Required. The application refuses to start if either is blank.
AZURE_OPENAI_ENDPOINT="https://your-resource.openai.azure.com"
AZURE_OPENAI_DEPLOYMENT="your-deployment-name"
AZURE_OPENAI_API_VERSION="2024-10-21"
AZURE_OPENAI_TIMEOUT_SECONDS=30
AZURE_OPENAI_MAX_TOKENS=800

# Optional, local development only. Leave blank everywhere else —
# Microsoft Entra ID / managed identity is the supported auth path.
# Only set this if you are blocked on an RBAC grant for the
# "Cognitive Services OpenAI User" role and someone with access to
# the resource has given you its key.
AZURE_OPENAI_API_KEY=""

# Retry / backoff for transient Azure OpenAI failures.
AZURE_OPENAI_MAX_RETRIES=3
AZURE_OPENAI_RETRY_BASE_SECONDS=0.5
AZURE_OPENAI_RETRY_MAX_SECONDS=8.0

# Rate limiting (in-memory, per-process).
RATE_LIMIT_LOGIN_MAX_REQUESTS=5
RATE_LIMIT_LOGIN_WINDOW_SECONDS=60
RATE_LIMIT_CHAT_MAX_REQUESTS=20
RATE_LIMIT_CHAT_WINDOW_SECONDS=60

# Chat session persistence (in-memory, per-process).
SESSION_MAX_MESSAGES=20
SESSION_MAX_PER_USER=20

# Knowledge base retrieval limits.
KNOWLEDGE_MAX_DOCUMENTS=5
KNOWLEDGE_MAX_DOCUMENT_CHARS=12000
KNOWLEDGE_MAX_CONTEXT_CHARS=40000
```

Production secrets should be managed through appropriate Azure services rather than committed configuration files. See `.env.example` for the full, documented list of settings.

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
│   │   ├── admin.py
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── configuration.py
│   │   ├── health.py
│   │   ├── knowledge.py
│   │   └── tickets.py
│   │
│   ├── core/
│   │   ├── azure_identity.py
│   │   ├── config.py
│   │   ├── logging.py
│   │   ├── permissions.py
│   │   ├── rate_limit.py
│   │   └── security.py
│   │
│   ├── database/
│   │   ├── sessions.py
│   │   └── users.py
│   │
│   ├── middleware/
│   │   └── audit.py
│   │
│   ├── models/
│   │   ├── auth.py
│   │   ├── chat.py
│   │   ├── knowledge.py
│   │   ├── ticket.py
│   │   └── user.py
│   │
│   ├── services/
│   │   ├── ai_service.py
│   │   ├── keyvault_service.py
│   │   ├── knowledge_service.py
│   │   └── storage_service.py
│   │
│   └── main.py
│
├── docs/
│   ├── architecture.md
│   ├── azure-rbac.md
│   ├── development.md
│   ├── least-privilege-review.md
│   └── security-model.md
│
├── tests/
│   ├── test_auth_rate_limit.py
│   ├── test_azure_identity.py
│   ├── test_azure_openai.py
│   ├── test_chat.py
│   ├── test_config.py
│   ├── test_helpdesk_agent.py
│   ├── test_knowledge_service.py
│   ├── test_rate_limit.py
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

Run the complete test suite (48 tests as of this writing):

```powershell
pytest
```

Run with verbose output:

```powershell
pytest -v
```

Run a specific test file:

```powershell
pytest tests/test_token.py
```

Run just the retry/backoff tests:

```powershell
pytest tests/test_azure_openai.py -k retry -v
```

Run just the rate limiting tests:

```powershell
pytest tests/test_rate_limit.py tests/test_auth_rate_limit.py -v
```

## A note on in-memory state and `--reload`

The user repository, ticket store, rate limiter, and chat session store are all process-local, in-memory state (deliberately — they are development placeholders, documented as such in their respective modules). This has one important consequence when testing manually with `uvicorn --reload`: **any file-timestamp change in the watched directory restarts the worker process and silently resets all of this state**, including counters mid-way through a rate-limit test. This isn't limited to deliberate edits — background activity like OneDrive/cloud-sync, antivirus scanning, or search indexing touching files in the project directory can trigger an unwanted reload.

If a rate limit, session, or ticket test behaves unexpectedly (e.g. a rate limit that should trigger on request 21 never does), first check the server console for `WatchFiles detected changes... Reloading...` appearing between requests. If so, rerun the same test against a server started **without** `--reload`:

```powershell
uvicorn app.main:app --port 8000
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

Completed:

* Azure OpenAI client integration (v1 API, Microsoft Entra ID auth via `DefaultAzureCredential`)
* Local-development API key fallback for RBAC-blocked developers
* Model configuration (`max_completion_tokens`, not the deprecated `max_tokens`)
* Chat completion workflow
* AI service error handling
* AI request/response logging
* Token and request safeguards (message length limits, retrieval size limits)

## Phase 7.5 — Reliability, Sessions, and Identity

**Current development step**

Completed:

* Retry with exponential backoff + jitter for transient Azure OpenAI failures
* Per-user chat rate limiting and per-IP login rate limiting
* Server-side chat session persistence, scoped per user
* End-user identity propagation into Azure OpenAI requests

Planned:

* Replace in-memory rate limiter and session store with a shared backing store (e.g. Redis) for multi-instance deployments
* Structured, per-request correlation IDs across the audit log, session store, and AI service log lines

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
