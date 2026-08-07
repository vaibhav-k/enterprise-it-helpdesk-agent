# Least Privilege Security Review

## Purpose

This document records why each permission exists and the associated risk.

# Permission Review

## Storage Blob Data Reader


Purpose:
```text
Read IT knowledge documents
```
Required because:
```text
Agent needs documentation access for troubleshooting responses
```

Risk if compromised:

```text
Knowledge documents could be exposed
```

Mitigation:

```text
Read-only access
No write permissions
```

---

## Key Vault Secrets User


Purpose:

```text
Retrieve application configuration secrets
```

Required because:

```text
Application requires secure configuration access
```

Risk if compromised:

```text
Approved secrets may be exposed
```

Mitigation:

```text
Only required secrets are stored
Access is audited
```

---

## Monitoring Reader


Purpose:

```text
View application telemetry
```

Risk:

```text
Monitoring information exposed
```

Mitigation:

```text
Read-only monitoring access
```

# Permission Reduction Review


Before:

```text
Contributor
```

Risk:

```text
Can modify Azure resources
```

After:

```text
Storage Blob Data Reader
```

Benefit:

```text
Only required read access remains
```

# Security Checklist


## Identity

- [x] Managed Identity planned
- [x] No application secrets stored
- [ ] Production identity enabled


## Authorization

- [x] Application RBAC implemented
- [x] Azure RBAC model documented
- [ ] Roles assigned in Azure


## Least Privilege

- [x] Permissions reviewed
- [x] Excessive permissions avoided
- [ ] Production access review completed