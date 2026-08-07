# Enterprise IT Helpdesk Agent Development Guide


## Overview

This document explains how to set up, run, test, and contribute to the Enterprise IT Helpdesk Agent project.

The project is developed without Docker and uses a standard Python virtual environment workflow.


# Development Environment


## Requirements

Install:

- Python 3.12+
- Git
- Visual Studio Code
- Azure CLI


Verify Python:

```powershell
python --version
````

Verify Git:

```powershell
git --version
```

Verify Azure CLI:

```powershell
az --version
```

# Repository Setup

Clone repository:

```powershell
git clone https://github.com/vaibhav-k/enterprise-it-helpdesk-agent.git
```

Move into project folder:

```powershell
cd enterprise-it-helpdesk-agent
```

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

Confirm environment:

```powershell
python --version
```

The terminal should show:

```
(.venv)
```

# Install Dependencies

Install project packages:

```powershell
pip install -r requirements.txt
```

Verify:

```powershell
pip list
```

# Environment Configuration

The application uses environment variables for configuration.

Create local configuration:

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
```

Important:

Never commit:

```
.env
```

The repository only contains:

```
.env.example
```

# Azure Development Setup

## Login to Azure

```powershell
az login
```

Verify account:

```powershell
az account show
```

The application uses:

```
DefaultAzureCredential
```

Authentication selection:

## Local Development

```

Developer Machine

        |

Azure CLI Login

        |

DefaultAzureCredential

        |

Azure SDK Client

```

## Azure Hosting

```

Application

        |

Managed Identity

        |

DefaultAzureCredential

        |

Azure Resource

```

# Running the Application

Start FastAPI:

```powershell
uvicorn app.main:app --reload
```

Application:

```
http://localhost:8000
```

Swagger API documentation:

```
http://localhost:8000/docs
```

# Testing

## Python Compilation Check

Before committing:

```powershell
python -m compileall app
```

Expected:

```
Listing 'app'...
```

# VS Code Configuration

Recommended extensions:

* Python
* Pylance
* Ruff

The project uses strict type checking.

Configured in:

```
pyproject.toml
```

and:

```
.vscode/settings.json
```

# Development Workflow

Each feature follows this process:

## 1. Create Feature

Example:

```
Add Azure identity service
```

## 2. Implement Code

Follow:

* Type hints
* Documentation strings
* Small modules
* Clear separation of responsibilities

## 3. Update Documentation

Update relevant files:

```
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
```

## 5. Commit

Example:

```powershell
git add .

git commit -m "feat: add azure managed identity credential foundation"
```

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
* Managed Identity ready design
* Azure CLI development support

## Step 4 — User Repository and Password Security

Completed:

* User model created
* Password hashing implemented
* User repository added
* Role field introduced

## Step 5 — Authentication API

Completed:

* Login API created
* JWT token generation added
* Authentication flow implemented
* Token response model added

## Step 6 — Helpdesk Ticket API

Completed:

* Ticket model created
* Protected ticket API added
* JWT protected routes implemented
* Authorization foundation added

## Step 7 — Azure Blob Storage Integration

Completed:

* Azure Blob Storage service added
* Managed Identity authentication connected
* Knowledge base endpoint created
* Storage security model documented

## Step 8 — Azure Key Vault Integration

Completed:

- Key Vault service added
- Managed Identity authentication reused
- Secret retrieval pattern implemented
- Key Vault RBAC documented

## Step 9 — Authorization Model

Completed:

- RBAC permission model added
- Role permissions defined
- Protected endpoints implemented
- Employee/Admin separation added

# Upcoming Development Steps


## Step 10 — Azure RBAC and Least Privilege

Completed:

- Azure RBAC model documented
- Managed Identity permissions defined
- Least privilege review added
- Resource access boundaries documented


## Step 11 — Production Hardening

Planned:

- Azure RBAC deployment
- Audit logging
- Application monitoring
- Security validation

# Git Commit Convention

Use conventional commit format:

Feature:

```
feat: add feature name
```

Documentation:

```
docs: update documentation
```

Maintenance:

```
chore: update tooling
```

Bug fix:

```
fix: correct issue description
```

# Security Development Rules

Always:

* Use environment variables
* Avoid hardcoded secrets
* Use managed identity for Azure access
* Keep permissions minimal
* Review RBAC assignments
* Update documentation with architecture changes
