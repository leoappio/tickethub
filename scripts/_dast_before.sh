#!/usr/bin/env bash
# Runs OWASP ZAP against the VULNERABLE baseline (tag v0-vulnerable-baseline)
# in an isolated git worktree, so ZAP actually finds the planted issues.
set -uo pipefail
MAIN=/home/lenovo/UFSC/Seguranca/tickethub
WT=/home/lenovo/UFSC/Seguranca/tickethub-vuln-dast   # under $HOME: snap docker can only see $HOME
OUT="$MAIN/reports/01-before-fixes"
mkdir -p "$OUT"

cd "$MAIN"
git worktree remove --force "$WT" 2>/dev/null || true
rm -rf "$WT"
git worktree add --detach "$WT" v0-vulnerable-baseline

cd "$WT"
echo "==> docker compose up --build (vulnerable baseline)"
docker compose -p tickethubvuln up -d --build

echo "==> waiting for API health"
for i in $(seq 1 60); do
  curl -sf http://localhost:8080/health >/dev/null 2>&1 && { echo "API up"; break; }
  sleep 3
done
curl -s "http://localhost:8080/public/events?search=test" -o /dev/null -w "public page: HTTP %{http_code}\n" || true
curl -s "http://localhost:8080/swagger/v1/swagger.json" -o /dev/null -w "swagger: HTTP %{http_code}\n" || true

echo "==> ZAP API scan (active) seeded by the OpenAPI/Swagger definition"
docker run --rm --network host -v "$OUT:/zap/wrk:rw" \
  ghcr.io/zaproxy/zaproxy:stable \
  zap-api-scan.py -t http://localhost:8080/swagger/v1/swagger.json -f openapi \
    -r zap-before.html -J zap-before.json -w zap-before.md -I
echo "ZAP exit: $?"

echo "==> teardown"
docker compose -p tickethubvuln down -v
cd "$MAIN"
git worktree remove --force "$WT" 2>/dev/null || true
echo "DONE_DAST_BEFORE"
ls -la "$OUT"/zap-before.* 2>/dev/null
