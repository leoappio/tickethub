#!/usr/bin/env bash
# DAST stage: boots the full stack (API + PostgreSQL) and runs an OWASP ZAP
# scan against the running application, writing an HTML/JSON report to ./reports.
#
# Requires: Docker + docker compose.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p reports

echo "==> Building and starting the stack"
docker compose up -d --build

echo "==> Waiting for the API health endpoint"
for i in $(seq 1 40); do
  if curl -sf http://localhost:8080/health >/dev/null 2>&1; then echo "API is up"; break; fi
  sleep 3
done

echo "==> Running OWASP ZAP API scan (active, OpenAPI-seeded) against the running app"
# Seeding ZAP with the Swagger/OpenAPI definition makes it exercise every endpoint;
# a plain spider would only see the 404 root. Host networking lets ZAP reach :8080.
docker run --rm --network host \
  -v "$PWD/reports:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t http://localhost:8080/swagger/v1/swagger.json -f openapi \
    -r zap-report.html -J zap-report.json -w zap-report.md \
    -I || true

echo "==> Tearing down the stack"
docker compose down -v
echo "Done. DAST report: reports/zap-report.html"
