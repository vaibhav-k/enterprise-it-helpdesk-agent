# Enterprise IT Helpdesk Agent

A secure enterprise IT helpdesk backend built using Python FastAPI and Azure cloud security patterns.

The project demonstrates how to build an enterprise-ready IT support platform with:

- Secure application authentication
- Role-based access control
- Azure Managed Identity
- Azure RBAC ready architecture
- Secure Azure resource access
- Future AI agent integration


# Project Vision

The goal is to build an internal IT Helpdesk Agent capable of:

- Creating IT support tickets
- Managing employee requests
- Accessing enterprise knowledge resources
- Integrating with Azure services securely
- Supporting future AI-powered workflows


# Technology Stack

## Backend

- Python 3.12
- FastAPI
- Pydantic Settings


## Security

- JWT authentication
- Password hashing
- Role-based authorization
- Azure Managed Identity
- Azure RBAC


## Azure Services

Planned integrations:

- Azure Blob Storage
- Azure Key Vault
- Azure Application Insights
- Azure AI services


# Current Development Status

| Feature | Status |
|---|---|
| Repository structure | Completed |
| Python environment setup | Completed |
| Configuration management | Completed |
| Azure Managed Identity foundation | Completed |
| User authentication | Completed |
| Ticket management | Completed |
| Azure Storage integration | Completed |
| Key Vault integration | Completed |
| AI Helpdesk Agent | Planned |


## Identity Foundation

The application currently uses an internal user repository
for development.

Future production authentication options:

- Enterprise Identity Provider
- Azure SQL user database
- External identity services


## Authentication Flow


```text
User

 |

Login API

    |

Password Verification

    |

JWT Token

    |

Protected API Access
```


## Ticket Workflow


```text
Employee

    |

JWT Authentication

    |

Ticket API

    |

Ticket Created

    |

Helpdesk Queue
```


## Knowledge Base


The Helpdesk Agent connects to Azure Blob Storage for IT documentation.


Flow:

```text

Helpdesk API

        |

Storage Service

        |

Managed Identity

        |

Azure Blob Storage

        |

Knowledge Documents

```


## Secure Configuration


Application secrets are retrieved through:

```text

FastAPI

    |

Key Vault Service

        |

Managed Identity

        |

Azure Key Vault

```


## Authorization Model


The application uses RBAC:

```text

User

 |

Role

 |

Permission

    |

Endpoint Access

```

Example:


- Employee

- ticket:create

- Create Ticket

- Admin

- user:manage

- User Management


# Architecture Overview


Current architecture:


```

User

|

FastAPI Helpdesk API

|

Application Security Layer

|

Azure Identity Layer

|

Azure Resources

```


# Azure Identity Architecture


The application uses Azure SDK authentication through:

```

DefaultAzureCredential

```


The same application code supports both environments.


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


## Azure Deployment


```

Azure Application

    |

Managed Identity

    |

Azure RBAC

    |

Azure Resources

```


Benefits:

- No Azure secrets stored in code
- No connection strings required
- Same code works locally and in Azure
- Supports enterprise security practices


# Repository Structure


```

enterprise-it-helpdesk-agent/

├── app/
│
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── models/
│   └── services/
│
├── docs/
│
├── requirements.txt
├── pyproject.toml
└── README.md

````


# Local Development


## Create Virtual Environment


Windows:

```powershell
python -m venv .venv
````

Activate:

```powershell
.venv\Scripts\activate
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

Create environment file:

```powershell
copy .env.example .env
```

Run application:

```powershell
uvicorn app.main:app --reload
```

API documentation:

```
http://localhost:8000/docs
```

# Azure Development

Login using Azure CLI:

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

to automatically discover available Azure authentication.

# Security Principles

The project follows:

## Least Privilege

Only required permissions should be assigned to application components.

## No Secrets in Code

Avoid:

* Passwords
* API keys
* Connection strings

## Managed Identity

Azure resources are accessed using:

```
Application Identity

        |

Managed Identity

        |

Azure RBAC

        |

Azure Resource
```

# Development Roadmap

## Phase 1 — Security Foundation

Completed:

* Project setup
* Configuration management
* Azure identity foundation

## Phase 2 — Application Security

Next:

* User management
* JWT authentication
* Role authorization

## Phase 3 — Azure Integration

Planned:

* Blob Storage knowledge base
* Key Vault secrets
* Application monitoring

## Phase 4 — AI Agent

Planned:

* RAG knowledge retrieval
* AI troubleshooting workflows
* IT automation

# Contribution

Development follows small Git commits:

Example:

```
feat: add azure managed identity credential foundation
```

Each milestone updates:

* Source code
* Documentation
* Security model


---

After saving:

Run:

```powershell
git add README.md

git commit -m "docs: update readme with project architecture and development status"
```