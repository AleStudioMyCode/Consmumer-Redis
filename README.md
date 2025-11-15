# Redis Python Client — API Async (FastAPI)

API assíncrona em FastAPI que encapsula operações Redis (cliente `redis.asyncio`) e expõe endpoints REST para `set`, `get`, `delete`, `exists`, `ttl` e `publish`. Projetada para ser usada como um serviço centralizado que outros sistemas consultam via HTTP.

> Estrutura do projeto (padrão obrigatório — não altere):
>
> ```
> redis_python_client/
> ├── src/
> │   ├── __init__.py
> │   ├── main.py
> │   ├── api/
> │   │   ├── __init__.py
> │   │   └── redis_routes.py
> │   ├── service/
> │   │   ├── __init__.py
> │   │ └── redis_service.py
> │   ├── core/
> │   │   ├── __init__.py
> │   │   └── dependencies.py
> │   └── redis_client/
> │       ├── __init__.py
> │       ├── async_client.py
> │       ├── config.py
> │       ├── exceptions.py
> │       └── utils.py
> ├── tests/
> │   ├── __init__.py
> │   ├── test_redis_service_async.py
> │   └── test_api_async.py
> ├── requirements.txt
> ├── requirements-dev.txt
> ├── Dockerfile
> ├── docker-compose.yml
> └── pytest.ini
> ```

---

## Funcionalidades

- Cliente Redis assíncrono (`AsyncRedisClient`) com: `set`, `get`, `delete`, `exists`, `ttl`, `publish`.
- FastAPI expondo endpoints REST para todas as operações.
- Startup/shutdown que inicializa e fecha o cliente Redis (`app.state.redis_client`).
- Testes usando `pytest` + `pytest-asyncio` e `fakeredis` (com wrapper `AsyncFakeRedis`).
- Dockerfile e docker-compose para rodar API + Redis localmente.

---

## Endpoints

Base URL padrão (local): `http://127.0.0.1:8000`

- `POST /redis/set`  
  Body JSON: `{ "key": "<key>", "value": "<value>", "ex": <seconds_optional> }`  
  Resposta: `{ "message": "OK" }` (ou `"FAIL"`)

- `GET /redis/get/{key}`  
  Resposta: `{ "value": "<value_or_null>" }`

- `DELETE /redis/delete/{key}`  
  Resposta: `{ "deleted": <int> }`

- `GET /redis/exists/{key}`  
  Resposta: `{ "exists": true|false }`

- `GET /redis/ttl/{key}`  
  Resposta: `{ "ttl": <int_seconds> }`

- `POST /redis/publish`  
  Body JSON: `{ "channel": "<ch>", "message": "<msg>" }`  
  Resposta: `{ "subscribers": <int> }`

> Docs automáticos: `http://127.0.0.1:8000/docs`

---

## Como rodar localmente (desenvolvimento)

1. Entre na raiz do projeto (onde está a pasta `src/`)

```bash
cd path/to/redis_python_client
```

2. Crie e ative virtualenv

```bash
Windows (PowerShell):
  python -m venv .venv
  .\.venv\Scripts\Activate

Linux/macOS:
  python -m venv .venv
  source .venv/bin/activate
```
3. Instale dependências
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

4. Subir Redis (opcional para desenvolvimento; necessário para integração)
```bash
docker-compose up -d
```

5. Rodar a API (Execute a partir da pasta src/:)

```bash
cd src
uvicorn main:app --reload --port 8000
```
Abra: http://127.0.0.1:8000/docs

Rodar testes


```bash
Na raiz do projeto (onde está pytest.ini):

pytest -v
```
Observações importantes sobre os testes:

Os testes usam fakeredis e um wrapper AsyncFakeRedis para simular o cliente assíncrono.

A fixture de teste executa await app.router.startup() para garantir app.state.redis_client esteja inicializado durante os testes.

Docker

Build e run (na raiz):

```bash
docker-compose up --build
```


API disponível em http://localhost:8000, Redis em localhost:6379.


Arquivos relevantes (resumo)

- src/main.py — inicializa FastAPI, inclui rotas e conecta o Redis no evento startup.

- src/api/redis_routes.py — define endpoints e usa dependência get_redis_client.

- src/service/redis_service.py — functions que chamam AsyncRedisClient.

- src/core/dependencies.py — fornece get_redis_client via Depends.

- src/redis_client/async_client.py — implementação do cliente Redis (async).

- tests/test_api_async.py — testes de integração com AsyncClient/ASGITransport + AsyncFakeRedis.

- pytest.ini — configura pytest (asyncio_mode, pythonpath=src etc).
