#!/usr/bin/env bash
# Reproduces the static stages of the DevSecOps pipeline locally and writes
# evidence into ./reports. Mirrors .github/workflows/devsecops.yml.
#
# Requires: gitleaks, trivy, semgrep, checkov, dotnet on PATH.
set -uo pipefail
cd "$(dirname "$0")/.."
mkdir -p reports

echo "==> [1/5] Secret Detection — Gitleaks (full git history)"
gitleaks detect --source=. --report-format json --report-path reports/gitleaks.json --no-banner

echo "==> [2/5] SCA — Trivy (NuGet dependency vulnerabilities)"
trivy fs --scanners vuln --severity CRITICAL,HIGH,MEDIUM --format json -o reports/trivy-sca.json .
trivy fs --scanners vuln --severity CRITICAL,HIGH,MEDIUM .            | tee reports/trivy-sca.txt
dotnet list TicketHub.sln package --vulnerable --include-transitive  | tee reports/dotnet-vuln.txt || true

echo "==> [3/5] SAST — Semgrep (registry packs + custom C# rules)"
semgrep scan \
  --config=p/csharp --config=p/security-audit --config=p/secrets \
  --config=.semgrep/tickethub-rules.yml \
  --exclude=reports --exclude=bin --exclude=obj --exclude='*.sarif' \
  --sarif --output reports/semgrep.sarif --json-output=reports/semgrep.json .

echo "==> [4/5] IaC — Checkov + Trivy config"
checkov -d . --framework dockerfile,terraform,kubernetes,secrets \
  --skip-path bin --skip-path obj --skip-path reports --skip-path .git \
  --compact -o cli -o sarif --output-file-path reports/checkov_cli.txt,reports/checkov.sarif || true
trivy config --severity CRITICAL,HIGH,MEDIUM --format json -o reports/trivy-iac.json .
trivy config --severity CRITICAL,HIGH,MEDIUM . | tee reports/trivy-iac.txt

echo "==> [5/5] DAST — see scripts/run-dast.sh (requires Docker + running app)"
echo "Done. Evidence written to ./reports"
