# TicketHub

Event ticketing & access-control platform, a .NET 8 Web API for selling event
tickets and validating them at the venue gate.

> Academic project for **INE5429, Segurança da Informação (UFSC)**. This
> repository is intentionally instrumented with realistic security weaknesses so
> that a full **DevSecOps pipeline** (Secret Detection, SCA, SAST, IaC Scanning,
> DAST) has a meaningful attack surface to evaluate. **Do not deploy as-is.**

## Architecture

Clean Architecture, four projects:

| Layer | Project | Responsibility |
|-------|---------|----------------|
| Presentation | `TicketHub.Api` | ASP.NET Core controllers, JWT auth, Swagger |
| Application | `TicketHub.Application` | Service contracts, DTOs, JWT/password services |
| Infrastructure | `TicketHub.Infrastructure` | EF Core + PostgreSQL, repositories, service impls |
| Domain | `TicketHub.Domain` | Entities, enums, settings |

**Stack:** .NET 8 · ASP.NET Core · EF Core 8 · PostgreSQL 16 · JWT Bearer auth
· Docker / docker-compose · Terraform · Kubernetes.

## Domain

Users (Customer / Organizer / Admin) buy tickets to events. Organizers create
events and ticket types; customers place orders, pay, and receive uniquely-coded
tickets; gate attendants validate tickets (one-time use). Admins read sales
reports.

## Run locally

```bash
docker compose up --build
# API:     http://localhost:8080
# Swagger: http://localhost:8080/swagger
# Public:  http://localhost:8080/public/events
```

Seed accounts: `admin@tickethub.local` / `Admin@123`,
`organizer@tickethub.local` / `Organizer@123`,
`customer@tickethub.local` / `Customer@123`.

## DevSecOps pipeline

Defined in [`.github/workflows/devsecops.yml`](.github/workflows/devsecops.yml):

| Stage | Tool |
|-------|------|
| Secret Detection | Gitleaks |
| SCA | Trivy + `dotnet list package --vulnerable` |
| SAST | Semgrep + CodeQL |
| IaC Scanning | Checkov + Trivy config |
| DAST | OWASP ZAP |

Evidence and the full technical analysis live in [`reports/`](reports/).
