# Enterprise IT Helpdesk Agent Architecture


## Overview

The Enterprise IT Helpdesk Agent is designed as a secure backend service that can evolve into an AI-powered enterprise support platform.

The current implementation focuses on:

- Secure application foundation
- Configuration management
- Azure identity integration
- Future Azure resource access


# High-Level Architecture


```

+----------------------+
|       Employee       |
+----------+-----------+
|
|
v
+----------------------+
|   FastAPI Backend    |
|                      |
| - API Layer          |
| - Business Logic     |
| - Security Layer     |
+----------+-----------+
|
|
v
+----------------------+
| Application Identity |
|                      |
| DefaultAzureCredential|
+----------+-----------+
|
|
v
+----------------------+
|   Azure Resources    |
|                      |
| Storage              |
| Key Vault            |
| Monitoring           |
+----------------------+

```


# Application Components


## API Layer

Location:

```

app/api/

```


Responsibilities:

- Expose REST endpoints
- Handle HTTP requests
- Validate input
- Return API responses


Current APIs:

- Health endpoint
- Authentication endpoint
- Ticket endpoint


---

## Core Layer

Location:

```

app/core/

```


Responsibilities:

- Application configuration
- Security utilities
- Azure identity handling


Components:


### Configuration

File:

```

config.py

```


Purpose:

- Load environment settings
- Centralize application configuration


### Azure Identity

File:

```

azure_identity.py

```


Purpose:

Provide Azure authentication using:


```

DefaultAzureCredential

```


---

# Azure Identity Architecture


The application does not store Azure credentials.


## Local Development Flow


```

Developer

    |

Azure CLI Login

    |

DefaultAzureCredential

    |

Azure SDK

    |

Azure Resource

```


## Azure Hosting Flow


```

Azure Application

        |

System Assigned Managed Identity

        |

Azure RBAC

    |

Azure Resource

```


The same application code supports both scenarios.


# Security Boundaries


## Application Boundary


The FastAPI application is responsible for:

- User authentication
- Request validation
- Authorization checks


## Azure Boundary


Azure manages:

- Resource authentication
- Identity validation
- Permission enforcement


# Future Azure Integration Architecture


Planned:


```

             FastAPI Agent

                  |

      ----------------------------

      |                          |

      v                          v

Azure Blob Storage              Azure Key Vault

Knowledge Base                 Secrets

                  |

                  v

          AI Agent Layer

                  |

                  v

          User Assistance

```


# Deployment Architecture


Future production deployment:


```

Developer

    |

GitHub Repository

    |

Azure Deployment Pipeline

            |

Azure Application Hosting

            |

Managed Identity Enabled

        |

Azure Services

```


# Knowledge Base Architecture


```text

User

 |

Helpdesk Agent

        |

Knowledge Service

        |

Azure Blob Storage

        |

IT Documentation

```

The application accesses documents using:

```text
DefaultAzureCredential
```

No storage keys are stored.


# Design Principles


## Security First

All Azure communication should use identity-based authentication.


## Least Privilege

Applications receive only required permissions.


Example:


Required:

```

Storage Blob Data Reader

```


Avoid:

```

Owner
Contributor

```


## Configuration Separation

Application configuration is separated from source code.


Environment-specific values are stored outside the repository.


# Current Status


Completed:

- Repository structure
- Configuration layer
- Azure identity foundation


In Progress:

- User authentication
- Authorization model


Planned:

- Azure Storage integration
- Key Vault integration
- AI agent workflows

---

After saving:

```powershell
git add docs/architecture.md

git commit -m "docs: add application architecture documentation"

git push origin main
```
