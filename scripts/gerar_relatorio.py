#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Gera o relatorio tecnico DevSecOps (TicketHub) em PDF, no padrao UFSC."""

import os
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import black, HexColor
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER, TA_LEFT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Preformatted,
    PageBreak, Table, TableStyle, Image,
)

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(BASE, "docs", "Relatorio_DevSecOps_Leonardo_Appio.pdf")
LOGO = os.path.join(BASE, "docs", "ufsc-logo.png")

COURSE = "INE5429 - Segurança da Informação"
AUTHOR = "Leonardo Lima Appio - 21101963"
REPO = "https://github.com/leoappio/tickethub"

styles = getSampleStyleSheet()
GREY = HexColor("#dddddd")
LIGHT = HexColor("#f4f4f4")

title_style = ParagraphStyle("TitleStyle", parent=styles["Title"],
    fontSize=17, spaceAfter=8, alignment=TA_CENTER, textColor=black)
sub_style = ParagraphStyle("SubStyle", parent=styles["Normal"],
    fontSize=11, alignment=TA_CENTER, spaceAfter=4, textColor=black)
h1 = ParagraphStyle("H1", parent=styles["Heading1"],
    fontSize=13, textColor=black, spaceBefore=14, spaceAfter=8)
h2 = ParagraphStyle("H2", parent=styles["Heading2"],
    fontSize=11, textColor=black, spaceBefore=10, spaceAfter=6)
body = ParagraphStyle("Body", parent=styles["BodyText"],
    fontSize=10.5, leading=14, alignment=TA_JUSTIFY, spaceAfter=6, textColor=black)
code_style = ParagraphStyle("Code", parent=styles["Code"],
    fontSize=8.0, leading=9.8, leftIndent=8, rightIndent=8,
    backColor=LIGHT, borderPadding=4, spaceBefore=4, spaceAfter=8, textColor=black)
cell = ParagraphStyle("Cell", parent=styles["Normal"],
    fontSize=8.5, leading=11, alignment=TA_LEFT, textColor=black)
cell_head = ParagraphStyle("CellHead", parent=cell,
    fontName="Helvetica-Bold", alignment=TA_CENTER)


def p(t):
    return Paragraph(t, body)


def code(t):
    return Preformatted(t, code_style)


def c(t):
    return Paragraph(t, cell)


def ch(t):
    return Paragraph(t, cell_head)


def make_table(rows, widths):
    t = Table(rows, colWidths=widths)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), GREY),
        ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
        ("FONTSIZE", (0, 0), (-1, -1), 8.5),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("ALIGN", (0, 0), (-1, 0), "CENTER"),
        ("GRID", (0, 0), (-1, -1), 0.4, black),
        ("LEFTPADDING", (0, 0), (-1, -1), 5),
        ("RIGHTPADDING", (0, 0), (-1, -1), 5),
        ("TOPPADDING", (0, 0), (-1, -1), 4),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 4),
    ]))
    return t


doc = SimpleDocTemplate(OUT, pagesize=A4,
    leftMargin=2 * cm, rightMargin=2 * cm, topMargin=1.6 * cm, bottomMargin=2 * cm,
    title="Relatorio DevSecOps - Leonardo Appio", author="Leonardo Lima Appio")

s = []

# ----------------------------------------------------------------- Cabecalho
logo = Image(LOGO, width=11 * cm, height=2.4 * cm)
logo.hAlign = "CENTER"
s += [logo, Spacer(1, 0.3 * cm)]
s.append(Paragraph("Universidade Federal de Santa Catarina", sub_style))
s.append(Paragraph(COURSE, sub_style))
s.append(Spacer(1, 0.4 * cm))
s.append(Paragraph("Implementação e Análise Crítica de um Pipeline DevSecOps", title_style))
s.append(Paragraph("Sistema avaliado: TicketHub, Plataforma de Venda e Validação de Ingressos (.NET 8)", sub_style))
s.append(Spacer(1, 0.15 * cm))
s.append(Paragraph(AUTHOR, sub_style))
s.append(Paragraph(f'Repositório: <font face="Courier">{REPO}</font>', sub_style))
s.append(Spacer(1, 0.5 * cm))

# ----------------------------------------------------------------- Sumario
s.append(Paragraph("Sumário Executivo", h1))
s.append(p(
    "Este trabalho projeta, implementa e analisa criticamente um pipeline completo de "
    "<b>DevSecOps</b> aplicado ao <b>TicketHub</b>, um sistema de autoria própria "
    "(.NET 8 / ASP.NET Core / PostgreSQL) com interface web/API, banco de dados e "
    "infraestrutura como código (Docker, Terraform e Kubernetes). O pipeline roda em "
    "<b>GitHub Actions</b> e contempla as cinco análises exigidas, Secret Detection, "
    "SCA, SAST, IaC Scanning e DAST, com ferramentas de mercado. O sistema foi "
    "instrumentado com fraquezas realistas; cada falha de risco médio ou superior foi "
    "corrigida, com a redução comprovada por nova execução das ferramentas:"))

s.append(Spacer(1, 0.2 * cm))
s.append(make_table([
    [ch("Etapa"), ch("Ferramenta"), ch("Antes"), ch("Depois")],
    [c("Secret Detection"), c("Gitleaks"), c("10 segredos"), c("0 no HEAD")],
    [c("SCA"), c("Trivy / dotnet"), c("3 CVEs HIGH"), c("0")],
    [c("SAST"), c("Semgrep (+ CodeQL)"), c("9 (7 ERROR + 2 WARNING)"), c("1 (falso positivo)")],
    [c("IaC Scanning"), c("Trivy config / Checkov"), c("25 misconfigs"), c("4 (FP / risco aceito)")],
    [c("DAST"), c("OWASP ZAP"), c("1 High, 2 Medium, 7 Low"), c("mitigados")],
], [3.2 * cm, 3.6 * cm, 4.6 * cm, 3.6 * cm]))

# ----------------------------------------------------------------- Secao 1
s.append(PageBreak())
s.append(Paragraph("1. Descrição do Sistema e Ferramental", h1))

s.append(Paragraph("1.1 Contexto de uso", h2))
s.append(p(
    "O <b>TicketHub</b> é uma plataforma de bilheteria para eventos. Três perfis "
    "interagem com o sistema: <b>Organizer</b> (cria eventos e tipos de ingresso, "
    "publica eventos), <b>Customer</b> (pesquisa eventos, cria pedidos, paga e recebe "
    "ingressos com código único) e <b>Admin</b> (consulta relatórios e a base de "
    "usuários)."))
s.append(p(
    "A lógica de negócio é não-trivial: controle de capacidade e estoque por tipo de "
    "ingresso (impede <i>overselling</i>), máquina de estados de pedido "
    "(<font face=\"Courier\">Pending → Paid → Cancelled/Refunded</font>), emissão de "
    "ingressos com código único após pagamento e validação no portão (ingresso de uso "
    "único). Há autenticação JWT, autorização por papéis/políticas e registro de "
    "tentativas de login."))

s.append(Paragraph("1.2 Arquitetura e stack tecnológico", h2))
s.append(p("Arquitetura limpa (<i>Clean Architecture</i>) em quatro camadas, com o fluxo "
           "de dependências apontando sempre para o domínio:"))
s.append(code(
    "TicketHub.Api              (apresentacao)  Controllers, JWT, Swagger, pagina publica HTML\n"
    "  -> TicketHub.Application    (aplicacao)  Contratos de servico, DTOs, Token/PasswordService\n"
    "     -> TicketHub.Infrastructure (infra)   EF Core + Npgsql, repositorios, implementacoes\n"
    "        -> TicketHub.Domain     (dominio)  Entidades, enums, settings"))
s.append(make_table([
    [ch("Camada / aspecto"), ch("Tecnologia")],
    [c("Linguagem / runtime"), c("C# / .NET 8")],
    [c("Framework web"), c("ASP.NET Core 8 (Web API + página server-rendered)")],
    [c("ORM / banco"), c("Entity Framework Core 8 / PostgreSQL 16")],
    [c("Autenticação"), c("JWT Bearer (HMAC-SHA256) + autorização por papéis/políticas")],
    [c("Containerização"), c("Docker (multi-stage) + docker-compose")],
    [c("IaC"), c("Terraform (AWS) e Kubernetes")],
    [c("CI/CD"), c("GitHub Actions")],
], [4.6 * cm, 10.4 * cm]))

s.append(Paragraph("1.3 Plataforma de CI/CD e ferramental por análise", h2))
s.append(p(
    'O pipeline está em <font face="Courier">.github/workflows/devsecops.yml</font> e '
    "dispara em <i>push</i>/<i>pull_request</i>. Cada análise exigida foi mapeada a "
    "ferramentas consolidadas:"))
s.append(make_table([
    [ch("Análise"), ch("Ferramenta(s)"), ch("Por quê")],
    [c("Secret Detection"), c("Gitleaks"),
     c("Varre todo o histórico de commits (regex + entropia) buscando credenciais.")],
    [c("SCA"), c("Trivy + dotnet list --vulnerable"),
     c("Resolve o grafo de dependências NuGet (packages.lock.json) e cruza com bases de CVE.")],
    [c("SAST"), c("Semgrep + CodeQL"),
     c("Semgrep com packs p/csharp, p/security-audit, p/secrets e 5 regras customizadas; CodeQL para taint analysis profunda em C#.")],
    [c("IaC Scanning"), c("Checkov + Trivy config"),
     c("Cobrem Dockerfile, Terraform e Kubernetes com centenas de políticas de conformidade.")],
    [c("DAST"), c("OWASP ZAP"),
     c("Ataca a aplicação em execução (conteinerizada) buscando XSS, Injection, falhas de auth e cabeçalhos ausentes.")],
], [2.7 * cm, 4.3 * cm, 8.0 * cm]))
s.append(p(
    "Como as regras <i>community</i> do Semgrep para C# não cobrem alguns <i>sinks</i> "
    "específicos (ex.: <font face=\"Courier\">FromSqlRaw</font>, "
    "<font face=\"Courier\">MD5.Create()</font>), foram escritas 5 regras customizadas "
    "em <font face=\"Courier\">.semgrep/tickethub-rules.yml</font>, estendendo o SAST ao "
    "contexto do projeto."))

# ----------------------------------------------------------------- Secao 2
s.append(PageBreak())
s.append(Paragraph("2. Evidências de Execução", h1))
s.append(p(
    "Todas as ferramentas foram executadas sobre este repositório. Os artefatos brutos "
    "(JSON/SARIF/TXT) ficam em <font face=\"Courier\">reports/01-before-fixes/</font> "
    "(estado vulnerável) e <font face=\"Courier\">reports/02-after-fixes/</font> "
    "(pós-correção). Abaixo, os trechos mais relevantes."))

s.append(Paragraph("2.1 Secret Detection, Gitleaks", h2))
s.append(code(
    "$ gitleaks detect --source=. --report-format json --report-path reports/gitleaks.json\n"
    "INF  6 commits scanned.\n"
    "WRN  leaks found: 10"))
s.append(p("10 segredos detectados (6 generic-api-key, 2 stripe-access-token, "
           "2 aws-access-token) em <font face=\"Courier\">appsettings.json</font>, "
           "<font face=\"Courier\">.env</font> e "
           "<font face=\"Courier\">docker-compose.yml</font>. O arquivo "
           "<font face=\"Courier\">.env</font> foi adicionado e depois removido em "
           "commits distintos, o Gitleaks o encontra mesmo fora do HEAD, provando o "
           "valor da varredura sobre o histórico completo."))

s.append(Paragraph("2.2 SCA, Trivy", h2))
s.append(code(
    "$ trivy fs --scanners vuln --severity CRITICAL,HIGH,MEDIUM .\n"
    "src/TicketHub.Infrastructure/packages.lock.json (nuget)   Total: 3 (HIGH: 3)\n"
    "  Newtonsoft.Json                      12.0.1  CVE-2024-21907  -> 13.0.1\n"
    "  System.Text.Json                     8.0.4   CVE-2024-43485  -> 8.0.5\n"
    "  Microsoft.Extensions.Caching.Memory  8.0.0   CVE-2024-43483  -> 8.0.1"))
s.append(p("Três CVEs HIGH: um em dependência direta (Newtonsoft.Json) e dois "
           "transitivos trazidos pelo EF Core 8.0.8. O próprio NuGet corrobora com o "
           "aviso <font face=\"Courier\">NU1903</font> em tempo de build."))

s.append(Paragraph("2.3 SAST, Semgrep", h2))
s.append(code(
    "$ semgrep scan --config=p/csharp --config=p/security-audit --config=p/secrets \\\n"
    "       --config=.semgrep/tickethub-rules.yml --exclude=reports --exclude=bin .\n"
    "Ran 78 rules on 53 files: 9 findings."))
s.append(make_table([
    [ch("Sev."), ch("Regra"), ch("Local")],
    [c("ERROR"), c("efcore-fromsqlraw-injection"), c("EventRepository.cs:30")],
    [c("ERROR"), c("weak-password-hash-md5-sha1"), c("PasswordService.cs:20")],
    [c("ERROR"), c("hardcoded-secret-in-source"), c("Program.cs:21, PasswordService.cs:16")],
    [c("ERROR"), c("raw-html-response-xss"), c("PublicController.cs:43")],
    [c("ERROR"), c("detected-aws/stripe-key"), c("appsettings.json:20,24")],
    [c("WARNING"), c("permissive-cors-any-origin"), c("Program.cs:56")],
    [c("WARNING"), c("stacktrace-disclosure"), c("Program.cs:88")],
], [2.0 * cm, 6.5 * cm, 6.5 * cm]))

s.append(Paragraph("2.4 IaC Scanning, Trivy config + Checkov", h2))
s.append(code(
    "$ trivy config --severity CRITICAL,HIGH,MEDIUM .\n"
    "Dockerfile   Failures: 1  (HIGH 1)                  -> DS-0002 sem USER nao-root\n"
    "k8s/deploy   Failures: 8  (HIGH 3, MEDIUM 5)        -> privileged, runAsRoot, sem limites\n"
    "terraform    Failures: 16 (CRIT 1, HIGH 11, MED 4)  -> SG 0.0.0.0/0, RDS publico, S3 publico"))
s.append(p("Checkov corrobora: 32 falhas em Terraform, 21 em Kubernetes, 2 em Dockerfile "
           "e 3 de segredo em IaC. Exemplos de IDs: "
           "<font face=\"Courier\">CKV_AWS_24</font> (SSH aberto), "
           "<font face=\"Courier\">CKV_AWS_20</font> (S3 público), "
           "<font face=\"Courier\">CKV_K8S_16</font> (container privilegiado)."))

s.append(Paragraph("2.5 DAST, OWASP ZAP", h2))
s.append(p(
    "A etapa DAST sobe o stack completo (<font face=\"Courier\">docker compose up</font>) "
    "e executa o OWASP ZAP em <b>varredura ativa</b> alimentada pela especificação "
    "OpenAPI/Swagger da aplicação (<font face=\"Courier\">zap-api-scan.py</font>), "
    "exercitando todos os endpoints, sem isso o spider só veria a raiz 404. Contra a "
    "versão vulnerável (tag <font face=\"Courier\">v0-vulnerable-baseline</font>) o ZAP "
    "reportou <b>1 alerta High, 2 Medium e 7 Low</b>:"))
s.append(code(
    "$ zap-api-scan.py -t http://localhost:8080/swagger/v1/swagger.json -f openapi\n"
    "[High]    SQL Injection                          /api/events/search?q='   (param q, 500 error-based)\n"
    "[Medium]  Content Security Policy (CSP) Not Set   /public/events?search=\n"
    "[Medium]  Missing Anti-clickjacking Header        /public/events?search=\n"
    "[Low]     X-Content-Type-Options Header Missing   /api/admin/users\n"
    "[Low]     Cross-Origin-Resource-Policy Missing    /api/admin/users\n"
    "[Info]    User Controllable HTML (Potential XSS)  /public/events?search=ZAP\n"
    "WARN-NEW: 8     PASS: 113"))
s.append(make_table([
    [ch("Alerta ZAP"), ch("Endpoint"), ch("Fraqueza correspondente")],
    [c("SQL Injection (High)"), c("/api/events/search?q="), c("FromSqlRaw com interpolação; payload <font face=\"Courier\">q='</font> gera HTTP 500")],
    [c("User Controllable HTML / Potential XSS"), c("/public/events?search="), c("eco da entrada refletido sem encoding")],
    [c("CSP / Anti-clickjacking / nosniff ausentes"), c("global"), c("sem CSP, X-Frame-Options, X-Content-Type-Options")],
    [c("X-Content-Type-Options Missing (em rota admin)"), c("/api/admin/users"), c("rota respondeu 200 sem autenticação (BAC)")],
    [c("Server Error response (info disclosure)"), c("/api/events/search"), c("erro 500 detalhado a partir da injeção")],
], [5.6 * cm, 4.0 * cm, 5.4 * cm]))
s.append(p(
    "O <b>SQL Injection</b> foi confirmado dinamicamente: o payload "
    "<font face=\"Courier\">q='</font> provoca HTTP 500 (injeção <i>error-based</i>) no "
    "buscador que usa <font face=\"Courier\">FromSqlRaw</font>. O endpoint "
    "<font face=\"Courier\">/api/admin/users</font> respondeu 200 sem autenticação "
    "(Broken Access Control). Após as correções (parametrização, encoding, "
    "<font face=\"Courier\">[Authorize]</font> e middleware de cabeçalhos) uma nova "
    "varredura não reproduz esses alertas. O relatório HTML completo está em "
    "<font face=\"Courier\">reports/01-before-fixes/zap-before.html</font> e é gerado "
    "automaticamente pelo job <font face=\"Courier\">dast</font> no GitHub Actions."))

# ----------------------------------------------------------------- Secao 3
s.append(PageBreak())
s.append(Paragraph("3. Análise de Falsos Positivos e Alertas Irrelevantes", h1))
s.append(p("Distinguir ruído de risco real é central em DevSecOps. Abaixo, alertas que "
           "<b>não</b> representam risco no contexto do TicketHub e a justificativa "
           "técnica para ignorá-los/aceitá-los."))

for titulo, texto in [
    ("3.1 Trivy AWS-0104 (CRITICAL), “egress irrestrito”",
     "Após o hardening, o security group mantém uma regra de egresso: HTTPS (443) para "
     "<font face=\"Courier\">0.0.0.0/0</font>. O Trivy classifica qualquer "
     "<font face=\"Courier\">0.0.0.0/0</font> de saída como crítico, mas tráfego HTTPS "
     "de saída para a internet é requisito legítimo (gateway de pagamento, APIs). "
     "<b>Risco aceito</b>, mitigado por limitar porta (443) e protocolo (TCP)."),
    ("3.2 Trivy AWS-0132 (HIGH), “bucket sem chave KMS gerenciada pelo cliente”",
     "O bucket já usa criptografia em repouso (<font face=\"Courier\">sse_algorithm = "
     "aws:kms</font>). O alerta exige uma CMK (customer-managed key); para os ativos do "
     "TicketHub a chave gerenciada pela AWS atende à política de dados. "
     "<b>Alerta irrelevante</b> ao contexto."),
    ("3.3 Trivy KSV-0125 (MEDIUM), “imagem de registry não confiável”",
     "A regra marca <font face=\"Courier\">ghcr.io/...</font> como untrusted por não "
     "constar de uma allowlist padrão. O GitHub Container Registry é o registro oficial "
     "do projeto. <b>Falso positivo.</b>"),
    ("3.4 Semgrep raw-html-response-xss após a correção (FP residual)",
     "A regra customizada dispara sobre o padrão “resposta text/html montada "
     "manualmente”. Após a correção (codificação com <font face=\"Courier\">HtmlEncoder"
     "</font>), o XSS deixou de existir, mas o padrão sintático permanece, logo a regra "
     "continua acusando o arquivo. É um <b>falso positivo pós-remediação</b>: a "
     "heurística prioriza recall. Em produção, suprimir-se-ia com "
     "<font face=\"Courier\">// nosemgrep</font> justificado."),
    ("3.5 Segredos detectados dentro dos relatórios do próprio scanner",
     "A primeira execução acusou segredos em "
     "<font face=\"Courier\">reports/gitleaks.json</font> e em "
     "<font face=\"Courier\">bin/Release/.../appsettings.json</font> (cópia de build). "
     "São artefatos de varredura e de compilação, não código-fonte. Corrigiu-se a "
     "configuração para excluir <font face=\"Courier\">reports/</font>, "
     "<font face=\"Courier\">bin/</font> e <font face=\"Courier\">obj/</font>, ruído "
     "clássico por escopo de varredura mal delimitado."),
    ("3.6 Checkov de hardening incremental (CKV_AWS_226, CKV_AWS_353, RDS IAM Auth)",
     "Alertas remanescentes (auto-upgrade de minor, performance insights, autenticação "
     "IAM no RDS) são boas práticas operacionais, não vulnerabilidades exploráveis. "
     "Classificados como backlog de melhoria, ilustram que “falha de política” ≠ "
     "“vulnerabilidade”."),
]:
    s.append(Paragraph(titulo, h2))
    s.append(p(texto))

# ----------------------------------------------------------------- Secao 4
s.append(PageBreak())
s.append(Paragraph("4. Identificação e Correção de Falhas Reais", h1))
s.append(p("As falhas abaixo são de risco médio ou superior, reais e exploráveis. Para "
           "cada uma: a fraqueza, o impacto e a correção (com diff). Os commits de "
           "correção estão entre as tags <font face=\"Courier\">v0-vulnerable-baseline"
           "</font> e <font face=\"Courier\">v1-remediated</font>."))

s.append(Paragraph("4.1 SQL Injection no buscador público, CWE-89 (Crítico)", h2))
s.append(p("<b>Detecção:</b> Semgrep e ZAP. <b>Impacto:</b> o termo de busca era "
           "interpolado em SQL bruto via <font face=\"Courier\">FromSqlRaw</font>. No "
           "endpoint não autenticado <font face=\"Courier\">/public/events?search=</font>, "
           "um atacante exfiltra a base inteira, incluindo hashes de senha."))
s.append(code(
    '- var sql = $@"... WHERE \"Name\" ILIKE \'%{term}%\' OR \"Venue\" ILIKE \'%{term}%\'";\n'
    "- return await _db.Events.FromSqlRaw(sql).ToListAsync();\n"
    '+ var pattern = $"%{term}%";\n'
    "+ return await _db.Events.Where(e => e.IsPublished &&\n"
    "+     (EF.Functions.ILike(e.Name, pattern) || EF.Functions.ILike(e.Venue, pattern)))\n"
    "+     .AsNoTracking().ToListAsync();"))
s.append(p("A consulta passa a usar LINQ parametrizado: o termo viaja como valor de "
           "parâmetro, nunca como texto SQL."))

s.append(Paragraph("4.2 Cross-Site Scripting na página pública, CWE-79 (Alto)", h2))
s.append(p("<b>Detecção:</b> Semgrep e ZAP. <b>Impacto:</b> "
           "<font face=\"Courier\">PublicController</font> concatenava a busca e os "
           "campos do evento em HTML (text/html) sem codificação, XSS refletido e "
           "armazenado. Permite roubo de sessão e ações em nome do usuário."))
s.append(code(
    "+ var enc = HtmlEncoder.Default;\n"
    '- sb.Append("<p>Results for: ").Append(search);\n'
    '+ sb.Append("<p>Results for: ").Append(enc.Encode(search));\n'
    "- .Append(e.Name) ... .Append(e.Description)\n"
    "+ .Append(enc.Encode(e.Name)) ... .Append(enc.Encode(e.Description))"))

s.append(Paragraph("4.3 Broken Access Control em /api/admin/users, CWE-862 + CWE-200 (Crítico)", h2))
s.append(p("<b>Detecção:</b> ZAP e revisão manual. <b>Impacto:</b> o endpoint não tinha "
           "<font face=\"Courier\">[Authorize]</font> e ainda retornava o "
           "<font face=\"Courier\">PasswordHash</font> de todos os usuários. Qualquer "
           "anônimo lia a base de credenciais."))
s.append(code(
    '+ [Authorize(Roles = "Admin")]\n'
    "  [HttpGet(\"users\")] public async Task<IActionResult> Users() {\n"
    "    var users = await _db.Users.AsNoTracking()\n"
    "-       .Select(u => new { u.Id, u.Email, u.FullName, Role, u.PasswordHash, u.CreatedAt })\n"
    "+       .Select(u => new { u.Id, u.Email, u.FullName, Role, u.CreatedAt })"))

s.append(Paragraph("4.4 Armazenamento de senha com MD5, CWE-916 (Alto)", h2))
s.append(p("<b>Detecção:</b> Semgrep. <b>Impacto:</b> senhas eram "
           "<font face=\"Courier\">MD5(password + pepper)</font>, rápido e sem salt por "
           "usuário, vulnerável a rainbow tables e brute force em GPU."))
s.append(code(
    "- using var md5 = MD5.Create();\n"
    "- return Convert.ToHexString(md5.ComputeHash(Encoding.UTF8.GetBytes(password + Pepper)));\n"
    "+ var salt = RandomNumberGenerator.GetBytes(16);\n"
    "+ var subkey = Rfc2898DeriveBytes.Pbkdf2(password, salt, 210_000, HashAlgorithmName.SHA256, 32);\n"
    '+ return $"pbkdf2$210000${Convert.ToBase64String(salt)}${Convert.ToBase64String(subkey)}";'))
s.append(p("Migrou-se para PBKDF2-HMAC-SHA256, 210.000 iterações (diretriz OWASP 2023), "
           "salt aleatório de 128 bits por usuário e comparação em tempo constante."))

s.append(Paragraph("4.5 Segredos hardcoded (código e configuração), CWE-798 (Crítico)", h2))
s.append(p("<b>Detecção:</b> Gitleaks, Semgrep, Checkov. <b>Impacto:</b> "
           "<font face=\"Courier\">appsettings.json</font>, "
           "<font face=\"Courier\">.env</font> e "
           "<font face=\"Courier\">docker-compose.yml</font> continham senha do Postgres, "
           "chave JWT e chaves Stripe/AWS/SendGrid; havia ainda uma chave JWT de fallback "
           "e um pepper embutidos no código."))
s.append(code(
    '- Key = "S3cr3t-JWT-Sign1ng-K3y-tickethub-2026-fallback"   // fallback no Program.cs\n'
    "+ if (string.IsNullOrWhiteSpace(jwt.Key) || jwt.Key.Length < 32)\n"
    '+     throw new InvalidOperationException("Jwt:Key deve vir de variável/secret store.");'))
s.append(p("Todos os segredos passam por variáveis de ambiente / secret store, com "
           "<font face=\"Courier\">.env.example</font> documentando o contrato. "
           "<b>Importante:</b> o Gitleaks confirma que os 10 segredos continuam no "
           "histórico git. A correção real exige <b>(1) rotacionar</b> imediatamente "
           "todas as chaves expostas (devem ser consideradas comprometidas) e "
           "<b>(2) reescrever o histórico</b> com "
           "<font face=\"Courier\">git filter-repo</font>/BFG. Apagar só do último commit "
           "dá falsa sensação de segurança."))

s.append(Paragraph("4.6 Dependências vulneráveis, SCA (Alto)", h2))
s.append(p("<b>Detecção:</b> Trivy / dotnet. <b>Correção:</b> "
           "<font face=\"Courier\">Newtonsoft.Json 12.0.1 → 13.0.3</font> e EF "
           "Core/Npgsql <font face=\"Courier\">8.0.8 → 8.0.11</font> (traz "
           "System.Text.Json 8.0.5 e Microsoft.Extensions.Caching.Memory 8.0.1 "
           "corrigidos). Nova varredura: <b>0 CVEs</b>."))

s.append(Paragraph("4.7 Erros, CORS e cabeçalhos inseguros, CWE-16/942/209 (Médio)", h2))
s.append(code(
    "- app.UseDeveloperExceptionPage();                 // stack trace em producao\n"
    "+ if (env.IsDevelopment()) app.UseDeveloperExceptionPage();\n"
    '+ else { app.UseExceptionHandler("/error"); app.UseHsts(); }\n'
    "- p.AllowAnyOrigin()                                // CORS para qualquer origem\n"
    "+ p.WithOrigins(allowedOrigins)\n"
    "+ // + middleware de headers: CSP, X-Frame-Options=DENY, nosniff, Referrer-Policy"))

s.append(Paragraph("4.8 Infraestrutura como Código, IaC (Crítico/Alto)", h2))
s.append(make_table([
    [ch("Recurso"), ch("Antes"), ch("Depois")],
    [c("Dockerfile"), c("roda como root"), c("USER 10001 não-privilegiado + HEALTHCHECK")],
    [c("Security Group"), c("0.0.0.0/0 em 22/5432/8080; egress total"),
     c("ingresso restrito a var.admin_cidr; egress só 443")],
    [c("RDS"), c("público, sem criptografia, sem backup"),
     c("privado, storage_encrypted, deletion_protection, backup 14d, senha no Secrets Manager")],
    [c("S3"), c("ACL public-read, sem criptografia"),
     c("block public access total, SSE-KMS, versionamento, logging")],
    [c("EC2"), c("IMDSv1, IP público, disco sem cripto"),
     c("IMDSv2 obrigatório, sem IP público, root volume criptografado")],
    [c("Kubernetes"), c("privileged: true, runAsUser: 0, sem limites"),
     c("runAsNonRoot, drop ALL caps, readOnlyRootFilesystem, limites, probes, Secret")],
], [2.6 * cm, 5.6 * cm, 6.8 * cm]))
s.append(p("Resultado pós-correção (Trivy config): <b>25 → 4</b> misconfigs, e as 4 "
           "restantes são os falsos positivos/riscos aceitos discutidos na Seção 3."))

# ----------------------------------------------------------------- Secao 5
s.append(Paragraph("5. Conclusão", h1))
s.append(p("O pipeline cobre integralmente as cinco análises exigidas, integradas ao "
           "GitHub Actions e executadas sobre código de autoria própria com superfície "
           "de ataque real. Mais relevante que a contagem de alertas foi o processo de "
           "triagem: separar os falsos positivos/riscos aceitos das falhas reais, "
           "corrigi-las e comprovar a redução com nova execução das ferramentas "
           "(SAST 9→1, SCA 3→0, IaC 25→4). O caso dos segredos no histórico ilustra um "
           "princípio central de DevSecOps: a ferramenta aponta o sintoma, mas a correção "
           "segura exige entender o ciclo de vida completo do dado, aqui, rotacionar e "
           "expurgar, não apenas apagar."))

s.append(Spacer(1, 0.3 * cm))
s.append(Paragraph("Apêndice, Reprodução", h2))
s.append(code(
    "# Análises estáticas (Secret, SCA, SAST, IaC):\n"
    "bash scripts/run-all-scans.sh        # gera reports/\n"
    "# DAST (requer Docker):\n"
    "bash scripts/run-dast.sh             # sobe o stack + OWASP ZAP -> reports/zap-report.html\n"
    "# Build e execução local:\n"
    "cp .env.example .env && docker compose up --build   # http://localhost:8080/swagger\n\n"
    "# Tags:  v0-vulnerable-baseline (antes)   |   v1-remediated (depois)"))

doc.build(s)
print("OK ->", OUT)
