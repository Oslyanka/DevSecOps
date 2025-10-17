#!/usr/bin/env python3
import json
import sys
from collections import Counter, defaultdict

def main(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    alerts = []
    for site in data.get("site", []):
        alerts.extend(site.get("alerts", []))

    total = len(alerts)
    by_risk = Counter(a.get("riskdesc", "Unknown").split(' ')[0] for a in alerts)
    by_name = Counter(a.get("name", "Unknown") for a in alerts)

    print("==== OWASP ZAP - Resumo ====")
    print(f"Total de alertas: {total}")

    normalize = defaultdict(int)
    for k, v in by_risk.items():
        key = k.strip().capitalize()
        normalize[key] += v

    for sev in ["Informational", "Low", "Medium", "High", "Critical"]:
        if normalize.get(sev, 0):
            print(f"- {sev}: {normalize[sev]}")

    print("\nTop vulnerabilidades:")
    for name, count in by_name.most_common(10):
        print(f"- {name}: {count}")

    high_count = normalize.get("High", 0)
    critical_count = normalize.get("Critical", 0)
    if high_count > 0 or critical_count > 0:
        print(f"\n❌ Falha: Encontrados High={high_count}, Critical={critical_count}")
        sys.exit(2)
    else:
        print("\n✅ Sucesso: Nenhum High/Critical encontrado.")
        sys.exit(0)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: parse_zap_report.py <caminho_json>")
        sys.exit(1)
    main(sys.argv[1])
