# Enterprise IT Helpdesk Agent Architecture

## Overview

The Enterprise IT Helpdesk Agent is a secure, modular backend application designed to evolve into an AI-powered enterprise IT support platform running on Microsoft Azure.

The current implementation focuses on:

* Secure FastAPI backend
* JWT authentication
* Role-based authorization (RBAC)
* Azure Managed Identity integration
* Azure Blob Storage access
* Azure Key Vault integration
* Audit logging and monitoring foundation
* AI-ready service architecture

---

# High-Level Architecture

```text
                     Employee

                         |

                         |

                  FastAPI Backend

                         |

      ----------------------------------------

      |            |            |            |

 Authentication  Authorization  Services   Logging

      |            |            |            |

      ----------------------------------------

                         |

                  Business Layer

                         |

              Azure Identity Layer

                         |

             DefaultAzureCredential

                         |

      ----------------------------------------

      |                |                  |

 Azure Blob Storage   Key Vault   Azure Monitor
```

---

# Application Structure

```text
app/

├── api/
├── core/
├── database/
├── middleware/
├── models/
├── services/
└── agents/
```

Each layer has a single responsibility.

---

# API Layer

Location:

```text
app/api/
```

Responsibilities:

* REST API endpoints
* Request validation
* Response generation
* Authentication
* Authorization

Current APIs:

* Health
* Authentication
* Tickets
* Knowledge Base
* Configuration
* Administration

---

# Core Layer

Location:

```text
app/core/
```

Responsibilities:

* Application configuration
* JWT security
* Password hashing
* Authorization helpers
* Azure authentication
* Logging

Components:

* `config.py`
* `security.py`
* `azure_identity.py`
* `permissions.py`
* `logging.py`

---

# Database Layer

Location:

```text
app/database/
```

Responsibilities:

* User repository
* Data access abstraction

Current implementation:

* In-memory user repository

Future:

* SQLAlchemy
* Azure SQL Database

---

# Models

Location:

```text
app/models/
```

Responsibilities:

* Request models
* Response models
* Domain models

Current models include:

* User
* Authentication
* Ticket

---

# Middleware

Location:

```text
app/middleware/
```

Responsibilities:

* Request auditing
* Request logging
* Monitoring hooks

Current middleware:

* AuditMiddleware

---

# Azure Identity Architecture

The application never stores Azure credentials.

Authentication uses:

```text
DefaultAzureCredential
```

## Local Development

```text
Developer Machine

        |

Azure CLI Login

        |

DefaultAzureCredential

        |

   Azure SDK

        |

  Azure Resources
```

## Azure Deployment

```text
Application

        |

System Assigned Managed Identity

        |

DefaultAzureCredential

        |

Azure Resources
```

The same application code works in both environments.

---

# Authentication Architecture

```text
Employee

      |

Login API

      |

Password Verification

      |

JWT Generation

      |

Access Token

      |

Protected APIs
```

---

# Authorization Architecture

The application uses Role-Based Access Control.

```text
User

      |

Role

      |

Permission

      |

Protected Endpoint
```

Current roles:

* Employee
* Admin

Example permissions:

* ticket:create
* ticket:view
* user:manage

---

# Azure Authorization

Azure authorization is separate from application authorization.

```text
Application

        |

Managed Identity

        |

Azure RBAC

        |

Azure Resource
```

Example roles:

* Storage Blob Data Reader
* Key Vault Secrets User
* Monitoring Reader

---

# Knowledge Base Architecture

```text
Employee

      |

Knowledge Endpoint

      |

Blob Storage Service

      |

Azure Blob Storage

      |

IT Documentation
```

Authentication:

```text
DefaultAzureCredential
```

No storage keys are stored.

---

# Security Monitoring

```text
   Request

      |

Audit Middleware

      |

Application Logging

      |

Azure Monitor

      |

Application Insights
```

Events logged include:

* Successful logins
* Failed logins
* API requests
* Authorization failures

---

# Future AI Architecture

The next development phase introduces an AI service layer.

```text
Employee

   |

Chat API

   |

Helpdesk Agent

      |

AI Service

    |

Azure OpenAI

      |

Knowledge Retrieval

      |

   Response
```

This separation allows AI providers to be replaced without changing the API layer.

---

# Deployment Architecture

```text
Developer

    |

GitHub Repository

      |

GitHub Actions (Future)

          |

Azure Application Hosting

        |

Managed Identity

      |

Azure Resources
```

---

# Design Principles

## Security First

* Identity-based authentication
* No embedded credentials
* Secure defaults

## Least Privilege

Only minimum Azure permissions are assigned.

Example:

```text
Storage Blob Data Reader
```

Avoid:

```text
Owner
Contributor
```

unless explicitly required.

## Separation of Concerns

Each application layer has a single responsibility.

* API
* Core
* Services
* Database
* Middleware

## Configuration Management

Environment-specific configuration is stored outside source control.

Secrets are retrieved using Azure Key Vault.

---

# Current Status

## Completed

* Repository foundation
* Configuration management
* Azure identity foundation
* User authentication
* JWT security
* Authorization model
* Ticket API
* Azure Blob Storage integration
* Azure Key Vault integration
* Azure RBAC design
* Least privilege review
* Audit logging
* Monitoring foundation

## Next Phase

* AI service layer
* Helpdesk agent
* Azure OpenAI integration
* Retrieval-Augmented Generation (RAG)
* ITSM automation
