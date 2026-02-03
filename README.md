# Diffy POC (Shadow Traffic + Response Comparison)

Esta POC levanta:
- Backend legacy (FastAPI)
- Backend candidate (FastAPI)
- Diffy (diffy/diffy)
- NGINX simulando un gateway (tipo DataPower) con mirroring a Diffy
- Un load generator
- Un reporter que imprime KPIs

## Requisitos
- Docker + Docker Compose

## Levantar la POC
```bash
docker compose up --build
