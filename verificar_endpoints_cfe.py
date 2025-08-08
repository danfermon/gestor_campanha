import requests
import csv

# Lista de endpoints CFe
endpoints = {
    "ac": "https://api.infosimples.com/consultas/docs/sefaz/ac/cfe",
    "al": "https://api.infosimples.com/consultas/docs/sefaz/al/cfe",
    "ap": "https://api.infosimples.com/consultas/docs/sefaz/ap/cfe",
    "am": "https://api.infosimples.com/consultas/docs/sefaz/am/cfe",
    "ba": "https://api.infosimples.com/consultas/docs/sefaz/ba/cfe",
    "ce": "https://api.infosimples.com/consultas/docs/sefaz/ce/cfe",
    "df": "https://api.infosimples.com/consultas/docs/sefaz/df/cfe",
    "es": "https://api.infosimples.com/consultas/docs/sefaz/es/cfe",
    "go": "https://api.infosimples.com/consultas/docs/sefaz/go/cfe",
    "ma": "https://api.infosimples.com/consultas/docs/sefaz/ma/cfe",
    "mt": "https://api.infosimples.com/consultas/docs/sefaz/mt/cfe",
    "ms": "https://api.infosimples.com/consultas/docs/sefaz/ms/cfe",
    "mg": "https://api.infosimples.com/consultas/docs/sefaz/mg/cfe",
    "pa": "https://api.infosimples.com/consultas/docs/sefaz/pa/cfe",
    "pb": "https://api.infosimples.com/consultas/docs/sefaz/pb/cfe",
    "pr": "https://api.infosimples.com/consultas/docs/sefaz/pr/cfe",
    "pe": "https://api.infosimples.com/consultas/docs/sefaz/pe/cfe",
    "pi": "https://api.infosimples.com/consultas/docs/sefaz/pi/cfe",
    "rj": "https://api.infosimples.com/consultas/docs/sefaz/rj/cfe",
    "rn": "https://api.infosimples.com/consultas/docs/sefaz/rn/cfe",
    "rs": "https://api.infosimples.com/consultas/docs/sefaz/rs/cfe",
    "ro": "https://api.infosimples.com/consultas/docs/sefaz/ro/cfe",
    "rr": "https://api.infosimples.com/consultas/docs/sefaz/rr/cfe",
    "sc": "https://api.infosimples.com/consultas/docs/sefaz/sc/cfe",
    "sp": "https://api.infosimples.com/consultas/docs/sefaz/sp/cfe",
    "se": "https://api.infosimples.com/consultas/docs/sefaz/se/cfe",
    "to": "https://api.infosimples.com/consultas/docs/sefaz/to/cfe"
}

# Arquivo de saída
output_file = "status_endpoints_cfe.csv"

# Timeout em segundos
timeout = 8

# Headers (adicione seu token se necessário)
headers = {
    "Authorization": "gw0qcYijpRgnmpRCp6GM9oSUVYh2iRdA3PjxtBhu"
}

# Coleta dos resultados
results = []
for uf, url in endpoints.items():
    print(f"🔍 Testando {uf.upper()} -> {url}")
    try:
        r = requests.get(url, headers=headers, timeout=timeout)
        status = r.status_code
        content_type = r.headers.get("Content-Type", "")
        sample = r.text[:200].replace("\n", " ").replace("\r", " ")
    except requests.RequestException as e:
        status = "ERR"
        content_type = ""
        sample = str(e)[:200]

    results.append({
        "uf": uf.upper(),
        "url": url,
        "status": status,
        "content_type": content_type,
        "sample": sample
    })

# Salva em CSV
with open(output_file, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["uf", "url", "status", "content_type", "sample"])
    writer.writeheader()
    for row in results:
        writer.writerow(row)

print(f"\n✅ Verificação concluída! Resultado salvo em: {output_file}")
