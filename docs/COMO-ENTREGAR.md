# Guia de entrega

## 1. Publicar no GitHub (repositório público) e disparar o pipeline

```bash
cd tickethub
gh repo create tickethub --public --source=. --remote=origin --push   # se tiver o gh CLI
# ou manualmente
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

O PDF oficial (padrão UFSC, com logo/cabeçalho) é
`docs/Relatorio_DevSecOps_Leonardo_Appio.pdf`, gerado por reportlab:
```bash
python3 scripts/gerar_relatorio.py
```
> Confira a constante `COURSE` no topo de `scripts/gerar_relatorio.py`, está como
> `"INE5429 - Segurança da Informação"`; ajuste o código da disciplina se necessário.

## 4. Checklist de entrega (Moodle, PDF)

- [ ] Link do repositório público preenchido no relatório
- [ ] Seção 1, Descrição do sistema e ferramental ✅
- [ ] Seção 2, Evidências das 5 ferramentas (incluir print do ZAP do passo 2) ✅
- [ ] Seção 3, Falsos positivos ✅
- [ ] Seção 4, Correção das falhas reais (diffs) ✅
- [ ] PDF gerado e enviado **antes de 26/06 23:59**
