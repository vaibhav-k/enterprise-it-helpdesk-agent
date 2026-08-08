# Enterprise IT Helpdesk Agent — Security Model

## Overview

The Enterprise IT Helpdesk Agent follows a layered security model designed for enterprise application development.

The current implementation uses:

* JWT-based user authentication
* Password hashing
* Role-based application authorization
* Azure Managed Identity
* Azure RBAC-ready resource access
* Azure Key Vault integration
* Azure Blob Storage integration
* Audit and security logging
* Least-privilege design

The application does **not** use Microsoft Entra ID for user authentication in the current development phase.

Azure identity is used for **application-to-Azure-resource authentication**, while application users are authenticated through the internal development user repository.

---

# Security Architecture

The application separates security into two major boundaries:

```text
                    User
                      |
                      v
              +---------------+
              | Authentication|
              |     Layer     |
              +-------+-------+
                      |
                    JWT
                      |
                      v
              +---------------+
              | Authorization |
              |     Layer     |
              +-------+-------+
                      |
                Role / Permission
                      |
                      v
              +---------------+
              | Application   |
              |     APIs      |
              +-------+-------+
                      |
                      v
              +---------------+
              | Azure Identity|
              |     Layer     |
              +-------+-------+
                      |
              DefaultAzureCredential
                      |
                      v
              +---------------+
              | Azure RBAC    |
              +-------+-------+
                      |
          +-----------+-----------+
          |                       |
          v                       v
     Blob Storage             Key Vault
```

---

# Authentication

## Current Authentication Model

Application users authenticate through the internal user repository.

Authentication flow:

```text
User
 |
 | username + password
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
JWT Access Token
    |
    v
Protected API
```

The application does not currently depend on Microsoft Entra ID for end-user authentication.

This keeps the current development environment simple while allowing the application security model to evolve later.

---

# Password Security

Passwords must never be stored in plaintext.

The application stores password hashes rather than original passwords.

```text
Password
   |
   v
Password Hashing
   |
   v
Password Hash
   |
   v
User Repository
```

During authentication:

```text
Submitted Password
        |
        v
Password Verification
        |
        v
Stored Password Hash
```

The application should never log:

* Passwords
* Password hashes
* Authentication secrets
* JWT signing secrets

---

# JWT Authentication

Protected APIs use JSON Web Tokens.

Authentication flow:

```text
POST /auth/login
        |
        v
Credential Validation
        |
        v
JWT Creation
        |
        v
Access Token
        |
        v
Authorization Header
        |
        v
Protected Endpoint
```

Clients send the token using:

```http
Authorization: Bearer <token>
```

JWT configuration is controlled through application settings.

Example:

```env
JWT_SECRET=local-development-secret
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=480
```

The JWT secret must never be committed to Git.

---

# JWT Claims

The application can use claims such as:

```json
{
  "sub": "employee",
  "role": "employee"
}
```

The `sub` claim identifies the authenticated user.

The `role` claim is used by the application authorization layer.

JWT claims must be treated as untrusted input until the token has been successfully:

1. Parsed
2. Cryptographically verified
3. Checked for expiration
4. Validated for required claims

---

# Authorization

Authentication answers:

```text
Who is the user?
```

Authorization answers:

```text
What is the user allowed to do?
```

The application uses role-based authorization.

Current conceptual model:

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
API Endpoint
```

---

# Application Roles

## Employee

Employees can perform normal helpdesk operations.

Example permissions:

```text
ticket:create
ticket:read
chat:use
knowledge:read
```

Employees should not be allowed to perform administrative operations.

---

## Admin

Administrators have additional operational permissions.

Example permissions:

```text
ticket:create
ticket:read
ticket:manage
user:read
user:manage
configuration:read
```

Administrative permissions should only be granted where required.

---

# Authorization Example

```text
Employee
   |
   +--> Create Ticket       ALLOW
   |
   +--> Read Knowledge      ALLOW
   |
   +--> Use Helpdesk Chat   ALLOW
   |
   +--> Manage Users        DENY
```

```text
Admin
   |
   +--> Create Ticket       ALLOW
   |
   +--> Manage Tickets      ALLOW
   |
   +--> Manage Users        ALLOW
```

Authorization must be enforced by the backend.

The application must not rely on frontend controls for security.

---

# FastAPI Dependency Security

Protected endpoints should use FastAPI dependencies for authentication and authorization.

Conceptually:

```text
Request
   |
   v
Authentication Dependency
   |
   v
Current User
   |
   v
Authorization Dependency
   |
   v
Endpoint
```

This keeps security checks centralized and reusable.

FastAPI dependency injection should use `Annotated` type hints for security dependencies.

---

# Azure Identity

The application uses:

```text
DefaultAzureCredential
```

for Azure SDK authentication.

This provides a consistent credential mechanism across development and Azure-hosted environments.

---

# Local Azure Authentication

During local development:

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

Developers can authenticate with:

```powershell
az login
```

and verify the active account with:

```powershell
az account show
```

---

# Azure Hosting Authentication

In Azure, the application should use a managed identity.

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

This removes the need to store Azure client secrets or storage access keys in application configuration.

---

# Managed Identity Security

Managed identity is used for application-to-Azure authentication.

The application should not store:

* Azure client secrets
* Storage account keys
* Azure service principal passwords
* Long-lived Azure access tokens

Instead:

```text
Application
    |
    v
Managed Identity
    |
    v
Microsoft Entra-backed Azure Identity
    |
    v
Azure RBAC
    |
    v
Resource
```

---

# Azure Blob Storage Security

The knowledge base uses Azure Blob Storage.

Access flow:

```text
Helpdesk Agent
      |
      v
Storage Service
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
Blob Storage
```

The application should use a read-only role when the agent only needs to retrieve knowledge documents.

Recommended role:

```text
Storage Blob Data Reader
```

Avoid broad roles such as:

```text
Owner
Contributor
Storage Account Contributor
```

unless a specific application requirement justifies them.

---

# Azure Key Vault Security

Key Vault is used for protected application secrets and configuration.

Access flow:

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
Key Vault
```

For applications that only need to retrieve secrets, use the smallest appropriate permission.

Recommended role:

```text
Key Vault Secrets User
```

The application should not grant secret-management permissions unless secret creation or administration is actually required.

---

# Secret Management

Sensitive values must remain outside source control.

Examples:

```text
JWT_SECRET
API_KEYS
CONNECTION_STRINGS
SERVICE_CREDENTIALS
```

Local development uses:

```text
.env
```

The `.env` file must not be committed.

The repository should contain:

```text
.env.example
```

with safe placeholder values.

---

# Least Privilege

Least privilege is a core security principle.

Every permission should answer three questions:

## 1. Why is the permission required?

Example:

```text
Storage Blob Data Reader

Reason:
The helpdesk agent needs to read IT knowledge documents.
```

## 2. What is the impact if compromised?

Example:

```text
Impact:
An attacker could potentially read knowledge-base documents.
```

## 3. Can the permission be reduced?

Example:

```text
Before:

Storage Blob Data Contributor

After:

Storage Blob Data Reader
```

---

# Permission Review

Every new permission should be documented.

Recommended review table:

| Component      | Permission               | Purpose                  | Access Level |
| -------------- | ------------------------ | ------------------------ | ------------ |
| Helpdesk Agent | Storage Blob Data Reader | Read knowledge documents | Read         |
| Helpdesk Agent | Key Vault Secrets User   | Read required secrets    | Read         |
| Employee       | ticket:create            | Create tickets           | Application  |
| Employee       | ticket:read              | View permitted tickets   | Application  |
| Admin          | user:manage              | Manage users             | Application  |

Permissions should be reviewed whenever a new Azure service or application capability is introduced.

---

# Defense in Depth

The application uses multiple security layers.

```text
Layer 1
User Authentication
       |
       v
Layer 2
JWT Validation
       |
       v
Layer 3
Application Authorization
       |
       v
Layer 4
Azure Identity
       |
       v
Layer 5
Azure RBAC
       |
       v
Layer 6
Azure Resource
```

A successful authentication should never automatically imply unrestricted resource access.

---

# AI Service Security

The AI Helpdesk Agent uses a provider abstraction.

Current architecture:

```text
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

The AI service must not bypass application authorization.

Before processing protected information, the request should already have passed:

```text
JWT Validation
       |
       v
User Authorization
       |
       v
Agent Processing
```

Future Azure OpenAI integration should use identity-based authentication where supported rather than embedding service credentials in source code.

---

# Logging and Auditing

Security-relevant events should be logged without exposing sensitive information.

Recommended events include:

* Authentication attempts
* Successful authentication
* Failed authentication
* Authorization failures
* Protected resource access
* Configuration access
* Azure service failures
* Application errors

Do not log:

* Passwords
* Password hashes
* JWT secrets
* Access tokens
* Azure credentials
* Key Vault secret values

---

# Error Handling

Security-sensitive errors should avoid exposing internal implementation details.

Avoid returning:

```text
Database connection failed because...
```

or:

```text
Invalid password hash for user...
```

Prefer controlled responses such as:

```text
Invalid credentials
```

or:

```text
Access denied
```

Detailed diagnostic information should remain in secure server-side logs.

---

# Security Boundaries

## User Boundary

The user interacts with:

```text
HTTP API
```

The user should only receive data authorized for their role and identity.

---

## Application Boundary

The application is responsible for:

* Authentication
* JWT validation
* Authorization
* Input validation
* Business rules
* Security logging

---

## Azure Boundary

Azure is responsible for:

* Managed identity authentication
* RBAC enforcement
* Resource-level access control
* Key Vault access control
* Storage authorization

---

# Current Security Status

| Security Area                     | Status     |
| --------------------------------- | ---------- |
| Password hashing                  | Completed  |
| JWT authentication                | Completed  |
| Protected API routes              | Completed  |
| Role-based authorization          | Completed  |
| Azure `DefaultAzureCredential`    | Completed  |
| Blob Storage identity access      | Completed  |
| Key Vault identity access         | Completed  |
| Least-privilege model             | Documented |
| Azure RBAC deployment             | Planned    |
| Production identity hardening     | Planned    |
| Azure OpenAI identity integration | Next       |
| Security testing                  | Ongoing    |

---

# Security Checklist

Before merging security-related changes:

* [ ] No secrets committed
* [ ] No passwords logged
* [ ] JWT validation is enforced
* [ ] Protected endpoints require authentication
* [ ] Authorization is enforced server-side
* [ ] Azure SDK clients use identity-based authentication
* [ ] Azure permissions follow least privilege
* [ ] Key Vault access is restricted
* [ ] Storage access is restricted
* [ ] Security events are auditable
* [ ] Documentation reflects the current security model
* [ ] Tests pass
* [ ] Ruff passes
* [ ] Mypy passes

---

# Security Development Rules

Always:

1. Prefer identity-based authentication.
2. Never hardcode secrets.
3. Never commit `.env`.
4. Use the smallest required Azure RBAC role.
5. Validate JWTs before accessing protected resources.
6. Enforce authorization on the backend.
7. Avoid exposing sensitive information in errors.
8. Avoid logging credentials and tokens.
9. Document every new permission.
10. Review security implications before adding new Azure integrations.

---

# Future Security Enhancements

Future production hardening should include:

* Azure RBAC deployment automation
* Centralized audit logging
* Application Insights monitoring
* Security alerting
* Token rotation strategy
* Stronger production secret management
* Automated dependency scanning
* Static type checking
* Static security analysis
* Automated security tests
* Azure OpenAI identity-based authentication
* Production identity-provider integration

The security architecture should evolve together with the application rather than being added after functionality is complete.
