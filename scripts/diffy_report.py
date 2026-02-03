import argparse
import json
import requests
import sys

def safe_get(d, *keys):
    cur = d
    for k in keys:
        if isinstance(cur, dict) and k in cur:
            cur = cur[k]
        else:
            return None
    return cur

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--host", default="localhost")
    ap.add_argument("--admin-port", type=int, default=8881)
    args = ap.parse_args()

    base = f"http://{args.host}:{args.admin_port}"

    # API conocida de Diffy (v1)
    # - listar endpoints: /api/1/endpoints
    # - stats: /api/1/endpoints/:endpoint/stats  (reportado por la comunidad) :contentReference[oaicite:4]{index=4}
    endpoints_url = f"{base}/api/1/endpoints"

    print(f"Diffy admin base: {base}")

    try:
        endpoints_resp = requests.get(endpoints_url, timeout=5)
        endpoints_resp.raise_for_status()
        endpoints = endpoints_resp.json()
    except Exception as e:
        print("ERROR: no pude obtener la lista de endpoints.")
        print(f"Intenté: {endpoints_url}")
        print(f"Detalle: {e}")
        print("\nTip: abre la UI en http://localhost:8888 para ver que Diffy esté recibiendo tráfico.")
        sys.exit(2)

    if not endpoints:
        print("No hay endpoints aún. Genera tráfico y vuelve a ejecutar.")
        sys.exit(0)

    print("\n=== DIFFY KPI REPORT ===")
    for ep in endpoints:
        stats_url = f"{base}/api/1/endpoints/{ep}/stats"
        try:
            s = requests.get(stats_url, timeout=5)
            s.raise_for_status()
            data = s.json()
        except Exception as e:
            print(f"\nEndpoint: {ep}")
            print(f"  ERROR obteniendo stats: {e}")
            continue

        # Intentos de extraer campos comunes
        # (si no existen, mostramos el JSON)
        total = safe_get(data, "summary", "count") or safe_get(data, "count")
        same = safe_get(data, "summary", "same") or safe_get(data, "same")
        diff = safe_get(data, "summary", "diff") or safe_get(data, "diff")

        print(f"\nEndpoint: {ep}")
        if total is not None and (same is not None or diff is not None):
            same = same or 0
            diff = diff or 0
            match_rate = (same / total * 100) if total else 0
            print(f"  total={total} same={same} diff={diff} match_rate={match_rate:.2f}%")
        else:
            print("  (No pude mapear campos estándar; imprimo JSON crudo)")
            print(json.dumps(data, indent=2)[:4000])

    print("\nUI: http://localhost:8888")
    print("Entrada cliente (NGINX): http://localhost:8080/success")

if __name__ == "__main__":
    main()
