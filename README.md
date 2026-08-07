# Azure Identity & Security Weekend Practice Roadmap

## Objective

The objective of this weekend practice is to gain practical experience implementing enterprise identity and security patterns on Microsoft Azure.

By the end of this sprint, you should understand and implement:

- Azure Managed Identities
- User and application authentication patterns
- Azure authorization models
- Microsoft Entra ID application permissions
- RBAC-based access control
- Least privilege security design

The goal is to build a small secure Azure application that follows enterprise identity best practices.

---

# Weekend Project

## Project: Secure Azure Application Identity Lab

Build a small backend application deployed on Azure that:

- Authenticates users using Microsoft Entra ID
- Uses Managed Identity to access Azure resources
- Uses RBAC for authorization
- Follows least privilege principles

---

# Target Architecture

```
             User

              |

              |

      Microsoft Entra ID

              |

              |

      Backend Application

              |

    ----------------------

    |                    |

Managed Identity    User Context

    |                    |

    |                    |

Azure Resources       Microsoft APIs

    |

    |

Storage / Key Vault

```

---

# Day 1 — Identity & Authentication Foundation

## Morning Session (3-4 Hours)

## 1. Azure Identity Fundamentals

### Learn

- Microsoft Entra ID concepts
- Users
- Applications
- Service principals
- Managed identities
- Access tokens


### Practice

Create:

- Azure Resource Group
- Storage Account
- Key Vault
- App Service / Container App


### Outcome

Understand:

```
Identity
|
Authentication
|
Authorization
```

---

# 2. Managed Identity Practice

## Learn

Types:

### System Assigned Identity

- Created with Azure resource
- Lifecycle tied to resource


### User Assigned Identity

- Independent Azure resource
- Can be shared


---

## Hands-on

Tasks:

1. Enable Managed Identity on Azure resource

2. Verify identity appears in Entra ID

3. Assign RBAC permissions


Example:

```
Container App

        |

Managed Identity

        |

Storage Blob Data Reader

        |

Storage Account

```

---

## Skills Practiced

✅ Workload identity  
✅ Passwordless authentication  
✅ Azure resource access  

---

# Afternoon Session (3-4 Hours)

# 3. Authentication Patterns

## Pattern 1 — User Authentication


Implement:

```

User

|

Microsoft Entra Login

|

Application

|

JWT Token

```


Learn:

- OAuth 2.0
- OpenID Connect
- Access tokens
- ID tokens


Practice:

- Register application
- Configure redirect URL
- Login using Entra ID


---

## Pattern 2 — Application Authentication


Implement:

```

Backend Service

    |

Client Credential Flow

    |

Microsoft API

```


Learn:

- Service principals
- Application permissions
- Client credentials flow


Practice:

- Create app registration
- Add API permission
- Request token


---

# Day 1 Deliverables

By end of Day 1:

✅ Azure environment created  
✅ Managed Identity configured  
✅ Application registered in Entra ID  
✅ User authentication working  
✅ Service-to-service authentication understood  


---

# Day 2 — Authorization & Security Design

## Morning Session (3-4 Hours)

# 4. Authorization Models

## Learn RBAC

Understand:

```

Who?

Can do what?

Where?

```

Example:

```

Application Identity

        |

Storage Blob Reader Role

        |

Storage Account

```

---

## Practice RBAC

Tasks:

Create permissions:

### Storage

```
Storage Blob Data Reader
```

### Key Vault

```
Key Vault Secrets User
```

### Container

```
Reader
```

---

Test:

Allowed:

```
Read document
```

Denied:

```
Delete resource
```

---

# 5. Microsoft Entra API Permissions

Practice:

Configure Microsoft Graph access.


Examples:

Read user profile:

```
User.Read.All
```


Read groups:

```
Group.Read.All
```


Understand:

- Delegated permissions
- Application permissions
- Admin consent


---

# Afternoon Session (3-4 Hours)

# 6. Least Privilege Design

## Goal

Reduce unnecessary permissions.


Review:

Current:

```

Application

Permissions:

Owner
Full Directory Access

```

Improve:

```

Application

Permissions:

User.Read.All

Storage Reader

Key Vault Reader

```


---

## Security Review Exercise

For each permission:

Ask:

### Why does the application need this?

### What happens if compromised?

### Can access be reduced?


---

# 7. Build Final Secure Application


Final implementation:

```

User

|

Entra Authentication

|

Backend API

|

Managed Identity

|

Azure Resources

```


Security controls:

- No stored secrets
- RBAC enabled
- Minimal permissions
- Audit logging enabled


---

# Day 2 Deliverables

By end of Day 2:

✅ RBAC configured  
✅ API permissions configured  
✅ Least privilege review completed  
✅ Secure application architecture documented  
✅ Identity flow understood  


---

# Weekend Schedule Summary

| Time | Activity |
|-|-|
| Saturday Morning | Azure Identity fundamentals |
| Saturday Morning | Managed Identity |
| Saturday Afternoon | OAuth authentication |
| Saturday Afternoon | Service principals |
| Sunday Morning | RBAC authorization |
| Sunday Morning | Microsoft Graph permissions |
| Sunday Afternoon | Least privilege design |
| Sunday Afternoon | Security review |


---

# Skills Checklist

## Managed Identity

- [ ] Enable system assigned identity
- [ ] Create user assigned identity
- [ ] Assign RBAC permissions
- [ ] Access Azure resources without secrets


## Authentication

- [ ] Register Entra application
- [ ] Implement OAuth login
- [ ] Understand access tokens
- [ ] Implement service authentication


## Authorization

- [ ] Configure Azure RBAC
- [ ] Assign roles
- [ ] Understand delegated permissions
- [ ] Understand application permissions


## Least Privilege

- [ ] Review permissions
- [ ] Remove excessive access
- [ ] Create minimal role assignments
- [ ] Document security decisions


---

# Final Outcome

After this weekend sprint, you will have practical experience designing secure Azure workloads using:

```

Microsoft Entra ID

    +

Managed Identity

    +

Authentication Patterns

    +

Authorization Models

    +

Least Privilege Security

```

These skills form the foundation for building secure enterprise applications and AI agents on Azure.
