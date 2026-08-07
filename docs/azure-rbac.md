# Azure RBAC Security Model


## Overview

Azure RBAC controls what the Helpdesk Agent can access inside Azure.

The application uses:

```text

Application

    |

Managed Identity

    |

Azure RBAC

    |

Azure Resources

```

No Azure credentials are stored.


# Managed Identity


Production identity:

```text

Enterprise IT Helpdesk Agent

    |

System Assigned Managed Identity

    |

Microsoft Entra Identity Platform

```

# Resource Permission Model


## Azure Blob Storage


Purpose:
```
Store IT knowledge documents.
```

Required Role:

```
Storage Blob Data Reader
```


Access:

```text
Read documents

Search knowledge base

Retrieve files
```


Not Allowed:

```text
Delete documents

Modify documents

Manage storage account
```

---

## Azure Key Vault


Purpose:

```text
Secure secret storage.
```

Required Role:

```text
Key Vault Secrets User
```

Access:

```text
Read required secrets
```

Not Allowed:

```text
Create secrets

Delete secrets

Manage Key Vault
```

---

## Application Insights


Purpose:

```text
Application monitoring.
```

Required Role:

```text
Monitoring Reader
```

Access:

```text
View logs

View metrics
```

# RBAC Assignment Model


```text

Managed Identity

    |

Role Assignment

    |

Specific Resource Scope
```

Example:


```text

Helpdesk Agent Identity

    |

Storage Blob Data Reader

    |

Knowledge Base Container
```


# RBAC Rules


Always:

- Assign roles at minimum required scope
- Prefer read-only roles
- Review permissions regularly
- Remove unused permissions


Avoid:

```text
Owner

Contributor

Global Administrator
```

unless specifically required.