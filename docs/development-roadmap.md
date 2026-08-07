# Enterprise IT Helpdesk Agent — Weekend Development Roadmap

## Objective

The objective of this weekend project is to build the security foundation of an enterprise AI Helpdesk Agent running on Microsoft Azure.

The focus areas are:

- Managed Identities
- Authentication Patterns
- Authorization Models
- Least Privilege Design

By the end of this sprint, the application should:

- Authenticate users using Microsoft Entra ID
- Run securely using Azure Managed Identity
- Access Azure resources without storing secrets
- Implement RBAC authorization
- Follow least privilege security principles
- Maintain an auditable identity and permission model


---

# Project Goal

## Build a Secure Enterprise Helpdesk Agent Backend

The application will simulate an internal IT support assistant.

Capabilities:

- Employee authentication
- User profile lookup
- Knowledge base access
- Ticket creation
- Secure Azure resource access


---

# Target Architecture

```
                Employee

                   |

                   |

          Microsoft Entra ID

                   |

                   |

          Helpdesk Web/API App

                   |

    --------------------------------

    |                              |

User Authentication          Managed Identity

    |                              |

    |                              |

Microsoft Graph              Azure Resources

                                   |

                     ------------------------

                     |                      |

                Key Vault              Storage

```


---

# Weekend Plan Overview

| Day | Focus |
|---|---|
| Saturday | Identity, Authentication, Managed Identity |
| Sunday | Authorization, RBAC, Least Privilege, Security Review |


---

# Day 1 — Identity & Authentication Foundation

## Goal

Create the application identity foundation and enable secure authentication.

Duration:

6-8 hours


---

# 1. Azure Environment Setup

## Learn

Azure identity building blocks:

- Microsoft Entra ID
- Users
- Groups
- Applications
- Service Principals
- Managed Identities


## Create Azure Resources

Create:

```

Resource Group

    |

Azure Container App

    |

Storage Account

    |

Azure Key Vault

    |

Application Insights

```


## Deliverable

Azure environment ready for application deployment.


---

# 2. Microsoft Entra Application Registration


## Objective

Register the Helpdesk Agent application.


Create:

```

Enterprise-IT-Helpdesk-Agent

    |

Application Object

    |

Service Principal

```


Configure:

- Application name
- Redirect URLs
- Authentication settings
- API permissions


---

# Skills Practiced

✅ Application registration  
✅ Service principals  
✅ Identity lifecycle  


---

# 3. Implement User Authentication


## Authentication Flow


```

Employee

|

Microsoft Entra Login

|

Access Token

|

Helpdesk API

```


Implement:

- OAuth 2.0
- OpenID Connect
- JWT validation


Users should be able to:

- Login
- Receive identity token
- Access protected APIs


---

# Skills Practiced

✅ User authentication  
✅ OAuth flows  
✅ Token validation  
✅ Identity claims  


---

# 4. Configure Managed Identity


## Objective

Allow the application to access Azure resources without secrets.


Enable:

```

Azure Container App

    |

System Assigned Managed Identity

    |

Microsoft Entra ID

```


Practice:

- Enable managed identity
- Verify identity creation
- Assign Azure roles


Example:

```

Helpdesk Agent Identity

    |

Storage Blob Data Reader

    |

Knowledge Base Storage

```


---

# Skills Practiced

✅ Workload identity  
✅ Passwordless authentication  
✅ Azure resource authentication  


---

# Day 1 Deliverables


By end of Saturday:

```

✓ Azure resources created

✓ Entra application registered

✓ User login working

✓ Managed Identity enabled

✓ Application identity documented

```


---

# Day 2 — Authorization & Least Privilege Design

## Goal

Secure the application by controlling what the agent can access.


Duration:

6-8 hours


---

# 5. Authorization Model Implementation


## Learn

Authentication:

```

Who are you?

```


Authorization:

```

What are you allowed to do?

```


---

# Implement Azure RBAC


Assign roles to Managed Identity.


Example:


```

Helpdesk Agent Identity

      |

      |

Storage Blob Data Reader

      |

      |

Knowledge Base Storage

```


---

## Required Roles


### Storage

```

Storage Blob Data Reader

```


Purpose:

Read IT documentation.


---

### Key Vault

```

Key Vault Secrets User

```


Purpose:

Read required configuration.


---

### Application Insights

```

Monitoring Reader

```


Purpose:

View application telemetry.


---

# Skills Practiced

✅ Azure RBAC  
✅ Role assignments  
✅ Resource-level authorization  


---

# 6. Microsoft Graph Authorization


## Objective

Allow the agent to access employee information securely.


Example:


User asks:

```

Who is my manager?

```


Flow:

```

Helpdesk Agent

   |

Managed Identity

   |

Microsoft Graph

   |

Employee Information

```


---

## Permissions Practice


Start with minimum permissions:


User profile:

```

User.Read.All

```


Groups:

```

Group.Read.All

```


Avoid:

```

Directory.ReadWrite.All

```


unless specifically required.


---

# Skills Practiced

✅ API permissions  
✅ Delegated permissions  
✅ Application permissions  
✅ Admin consent  


---

# 7. Least Privilege Security Review


## Objective

Review every permission.


For each permission answer:


### Why does the agent need it?

Example:

```

User.Read.All

Reason:

Required to retrieve employee information.

```


---

### What happens if compromised?

Example:

```

Storage Reader

Impact:

Knowledge documents exposed.

Mitigation:

Read-only access.

```


---

### Can permission be reduced?

Example:


Before:

```

Contributor

```


After:

```

Storage Blob Data Reader

```


---

# Skills Practiced

✅ Security analysis  
✅ Permission reduction  
✅ Risk assessment  


---

# 8. Final Secure Architecture


Final design:

```
                User

                 |

                 |

         Microsoft Entra ID

                 |

                 |

        Helpdesk Agent API

                 |

      -------------------------

      |                       |

User Identity            Managed Identity

      |                       |

      |                       |

Microsoft Graph        Azure Resources

                          |

                -----------------

                |               |

           Storage         Key Vault
```

---

# Day 2 Deliverables


By end of Sunday:


```

✓ RBAC configured

✓ Graph permissions configured

✓ Managed identity access verified

✓ Least privilege review completed

✓ Security model documented

✓ Identity architecture completed

```


---

# Final Skills Checklist


## Managed Identities

- [ ] Enable system assigned identity
- [ ] Understand user assigned identity
- [ ] Authenticate Azure resources without secrets
- [ ] Assign RBAC permissions


---

## Authentication Patterns

- [ ] Implement Entra user login
- [ ] Understand OAuth 2.0
- [ ] Validate JWT tokens
- [ ] Understand service authentication


---

## Authorization Models

- [ ] Configure Azure RBAC
- [ ] Assign resource permissions
- [ ] Configure Graph API permissions
- [ ] Understand delegated vs application permissions


---

## Least Privilege Design

- [ ] Review permissions
- [ ] Remove unnecessary roles
- [ ] Document access decisions
- [ ] Apply security boundaries


---

# Final Weekend Outcome


At the end of this project, the Enterprise IT Helpdesk Agent will have:


```

Microsoft Entra Authentication

        +

Azure Managed Identity

        +

RBAC Authorization

        +

Microsoft Graph Integration

        +

Least Privilege Security Model

        +

Auditable Enterprise Identity Design

```


These foundations prepare the project for the next stages:

- Azure OpenAI integration
- RAG knowledge base
- AI agent workflows
- ITSM automation
- Production deployment
