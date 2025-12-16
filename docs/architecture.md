# System Architecture — Self‑Healing CI/CD (Level 2)

## High-Level Flow

```mermaid
flowchart LR
    Dev[Developer Commit] --> CI[CI Pipeline]

    CI -->|Build & Test| Deploy[Deploy Latest]
    Deploy --> Health[/health/intelligent/]

    Health -->|degraded=true OR decision_ready=false| Rollback[Auto Rollback Guard]
    Rollback --> Stable[Deploy Stable Image]

    Health -->|degraded=false AND decision_ready=true| Promote[Promote Image]
    Promote --> Stable

    Stable --> Runtime[Production Runtime]
```

---

## Component Responsibilities

### CI Pipeline
- Builds and deploys `latest`
- Acts as **Decision Gate**
- Fail‑Closed by default

---

### Intelligent Health Endpoint
- Single source of truth
- Returns semantic health signals
- Defined by **Health Contract v1**

---

### Auto Rollback Guard
- Enforces deterministic decisions
- Blocks unsafe deployments
- Guarantees idempotent rollback

---

### Image Strategy
- `latest` → evaluation candidate
- `stable` → proven production artifact

Promotion happens **only** after positive health confirmation.
```

---

## 🔹 ASCII Diagram ( README / Review )

```text
Developer
   |
   v
 CI Pipeline
   |
   v
 Deploy (latest)
   |
   v
 /health/intelligent
   |              |
   | bad health   | good health
   v              v
 Rollback      Promote
   |              |
 stable <---------
   |
   v
 Production
```