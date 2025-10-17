# ClickSeguro - ZAP Pipeline

Projeto para demonstrar testes de segurança automatizados com **OWASP ZAP GitHub Actions**:
- Escaneia `http://localhost:8080`
- Gera relatórios (HTML/JSON/MD)
- Falha automaticamente se houver **High** ou **Critical**
- Publica os relatórios como **artefatos** do workflow

## Requisitos locais
- Node.js 18+
- Docker (para executar o ZAP localmente, opcional)

## Rodando localmente
1) Instale dependências:
```bash
cd app

npm install
```

2) Inicie a aplicação:
```bash
npm start

# acessa http://localhost:8080
```

3) (Opcional) Rode o ZAP via Docker e gere relatórios em `./zap-reports`:
```bash
mkdir zap-reports

docker run --rm -v "%cd%\zap-reports":/zap/wrk/:rw ghcr.io/zaproxy/zaproxy:stable zap-full-scan.py -t http://host.docker.internal:8080 -r zap-report.html -J zap-report.json -w zap-report.md -I
```

## Como o CI funciona
- O workflow `ci-zap.yml`:
  - Sobe a app em `localhost:8080`
  - Executa ZAP (Docker) gerando `zap-report.html`, `zap-report.json` e `zap-report.md`
  - Roda `scripts/parse_zap_report.py` e **falha** em High/Critical
  - Publica tudo como artefato `zap-reports`

## Vulnerabilidade proposital
- O endpoint `POST /login` reflete `username`/`password` **sem validação ou escape**.
- O ZAP costuma sinalizar entradas refletidas (p. ex., potenciais XSS) e endpoints sem proteção.

## Observações
- Este projeto é **didático** e não deve ser usado em produção.
