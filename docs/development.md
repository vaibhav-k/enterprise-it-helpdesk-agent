# Enterprise IT Helpdesk Agent Development Guide

## Overview

This document explains how to set up, run, test, and contribute to the Enterprise IT Helpdesk Agent project.

The project is developed without Docker and uses a standard Python virtual environment workflow.

---

# Development Environment

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

# Repository Setup

Clone the repository:

```powershell
git clone https://github.com/vaibhav-k/enterprise-it-helpdesk-agent.git
```

Move into the project folder:

```powershell
cd enterprise-it-helpdesk-agent
```

---

# Python Environment Setup

## Create Virtual Environment

Windows:

```powershell
python -m venv .venv
```

Activate:

```powershell
.venv\Scripts\activate
```

Verify:

```powershell
python --version
```

The terminal prompt should display:

```text
(.venv)
```

---

# Install Dependencies

Install project dependencies:

```powershell
pip install -r requirements.txt
```

Verify installation:

```powershell
pip list
```

---

# Environment Configuration

Create a local configuration file:

```powershell
copy .env.example .env
```

Example:

```env
APP_NAME="Enterprise IT Helpdesk Agent"

JWT_SECRET="local-development-secret"

JWT_ALGORITHM="HS256"

JWT_EXPIRY_MINUTES=480

AZURE_STORAGE_ACCOUNT="storage-account"

AZURE_CONTAINER="knowledge-base"

KEYVAULT_NAME="keyvault-name"

ENVIRONMENT="development"

ENABLE_AUDIT_LOGGING=true
```

Never commit:

```text
.env
```

Only commit:

```text
.env.example
```

---

# Azure Development Setup

## Login

```powershell
az login
```

Verify the active account:

```powershell
az account show
```

The application authenticates using:

```text
DefaultAzureCredential
```

### Local Development

```text

Developer Machine

        |

Azure CLI Login

        |

DefaultAzureCredential

        |

Azure SDK Client

```

### Azure Deployment

```text

Application

        |

Managed Identity

        |

DefaultAzureCredential

        |

Azure Resource

```

---

# Running the Application

Start the development server:

```powershell
uvicorn app.main:app --reload
```

Application:

```text
http://localhost:8000
```

Swagger UI:

```text
http://localhost:8000/docs
```

OpenAPI schema:

```text
http://localhost:8000/openapi.json
```

---

# Validation

## Compile Python Files

```powershell
python -m compileall app
```

## Ruff

```powershell
ruff check .
```

## Git Status

```powershell
git status
```

## Run the API

```powershell
uvicorn app.main:app --reload
```

Verify:

* Home endpoint (`/`)
* Swagger UI (`/docs`)
* Authentication
* Ticket API
* Knowledge API
* Admin API

---

# VS Code Configuration

Recommended extensions:

* Python
* Pylance
* Ruff

Project configuration:

```text
pyproject.toml
```

```text
.vscode/settings.json
```

---

# Development Workflow

Each feature follows the same workflow.

## 1. Create Feature

Example:

```text
Add Azure Blob Storage service
```

## 2. Implement

Follow these guidelines:

* Type hints
* Docstrings
* Small modules
* Separation of concerns
* Pylance clean
* Ruff clean

## 3. Update Documentation

Update relevant files:

```text
README.md

docs/
    architecture.md
    security-model.md
    development.md
```

## 4. Validate

Run:

```powershell
python -m compileall app
ruff check .
```

## 5. Commit

Example:

```powershell
git add .

git commit -m "feat: add azure blob storage integration"
```

---

# Current Development Milestones

## Step 1 — Repository Foundation

Completed:

* Python project structure
* Dependency management
* Git configuration

## Step 2 — Configuration Management

Completed:

* Pydantic Settings
* Environment variables
* Application configuration

## Step 3 — Azure Identity Foundation

Completed:

* DefaultAzureCredential
* Azure identity abstraction
* Managed Identity ready architecture
* Azure CLI authentication support

## Step 4 — User Repository and Password Security

Completed:

* User model
* Password hashing
* User repository
* Role support

## Step 5 — Authentication API

Completed:

* Login endpoint
* JWT generation
* Password verification
* Protected authentication flow

## Step 6 — Helpdesk Ticket API

Completed:

* Ticket models
* Ticket API
* Protected endpoints
* JWT authentication

## Step 7 — Azure Blob Storage Integration

Completed:

* Blob Storage service
* Knowledge base endpoint
* Managed Identity authentication
* Storage security model

## Step 8 — Azure Key Vault Integration

Completed:

* Key Vault service
* Secret retrieval
* Managed Identity authentication
* Key Vault RBAC documentation

## Step 9 — Authorization Model

Completed:

* Application RBAC
* Permission model
* Employee/Admin roles
* Protected endpoints

## Step 10 — Azure RBAC and Least Privilege

Completed:

* Azure RBAC model
* Managed Identity permission mapping
* Least privilege review
* Resource access boundaries
* Security documentation

## Step 11 — Production Security Hardening

Completed:

* Structured logging
* Audit middleware
* Authentication event logging
* Monitoring architecture
* Application Insights integration foundation

## Step 12 — AI Helpdesk Agent Foundation

Completed:

* AI service abstraction
* Helpdesk agent layer
* Chat endpoint
* Mock AI implementation

---

# Upcoming Development

## Step 13 — RAG Knowledge Base

Planned:

* Knowledge retrieval
* Document search
* Context generation

## Step 14 — ITSM Integration

Planned:

* Ticket workflow automation
* External ITSM integration
* Service operations

---

# Git Commit Convention

Use conventional commit format:

Feature:

```text
feat: add feature name
```

Documentation:

```text
docs: update documentation
```

Maintenance:

```text
chore: update tooling
```

Bug Fix:

```text
fix: correct issue description
```

Refactoring:

```text
refactor: improve internal implementation
```

---

# Security Development Rules

Always:

* Use environment variables
* Avoid hardcoded secrets
* Use Managed Identity for Azure authentication
* Apply least privilege principles
* Protect endpoints with authentication and authorization
* Review RBAC assignments before deployment
* Keep documentation synchronized with implementation
* Ensure the project remains free of Pylance and Ruff errors before committing
