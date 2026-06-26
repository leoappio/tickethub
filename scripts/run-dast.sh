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

echo "==> Running OWASP ZAP full scan (active) against http://localhost:8080"
# Uses host networking so ZAP can reach the API published on localhost:8080.
docker run --rm --network host \
  -v "$PWD/reports:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-full-scan.py -t http://localhost:8080 \
    -r zap-report.html -J zap-report.json -w zap-report.md \
    -I || true

echo "==> Tearing down the stack"
docker compose down -v
echo "Done. DAST report: reports/zap-report.html"
