# Guia de entrega

## 1. Publicar no GitHub (repositório público) e disparar o pipeline

```bash
cd tickethub
gh repo create tickethub --public --source=. --remote=origin --push   # se tiver o gh CLI
# — ou manualmente —
git remote add origin https://github.com/<seu-usuario>/tickethub.git
git push -u origin main --tags
```

Ao dar `push`, o workflow `.github/workflows/devsecops.yml` executa as 5 etapas.
Acompanhe em **Actions**; os relatórios (SARIF/HTML) aparecem em
**Security → Code scanning** e em **Actions → (run) → Artifacts**.

> Lembre de editar o link do repositório no topo de `docs/RELATORIO.md` (e
> regenerar o PDF, passo 3) antes de enviar.

## 2. Evidência do DAST (OWASP ZAP)

O DAST precisa da aplicação rodando. Duas formas de obter a evidência:

**(a) No GitHub Actions (recomendado):** o job `DAST (OWASP ZAP)` sobe o stack e
escaneia automaticamente. Baixe o artefato `zap_scan` do run e use o HTML/PNG no
relatório.

**(b) Localmente (requer Docker):**
```bash
bash scripts/run-dast.sh        # gera reports/zap-report.html
```

## 3. Gerar o PDF final

Já existe `docs/RELATORIO.pdf`. Para regenerar após editar o `.md`:
```bash
python3 - <<'PY'
import markdown, re, pathlib
src = re.sub(r'^---\n.*?\n---\n','',pathlib.Path("docs/RELATORIO.md").read_text(),1,flags=re.S)
body = markdown.markdown(src, extensions=['tables','fenced_code','toc','sane_lists'])
pathlib.Path("docs/RELATORIO.html").write_text("<!doctype html><meta charset=utf-8>"+body)
PY
google-chrome --headless=new --print-to-pdf=docs/RELATORIO.pdf "file://$PWD/docs/RELATORIO.html"
```
Ou simplesmente abra `docs/RELATORIO.html` no navegador → **Imprimir → Salvar como PDF**.

## 4. Checklist de entrega (Moodle, PDF)

- [ ] Link do repositório público preenchido no relatório
- [ ] Seção 1 — Descrição do sistema e ferramental ✅
- [ ] Seção 2 — Evidências das 5 ferramentas (incluir print do ZAP do passo 2) ✅
- [ ] Seção 3 — Falsos positivos ✅
- [ ] Seção 4 — Correção das falhas reais (diffs) ✅
- [ ] PDF gerado e enviado **antes de 26/06 23:59**
