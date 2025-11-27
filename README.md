*

A simple mock banking API built with **FastAPI**. This project lets you create accounts, add transactions, and manage balances. It’s designed for personal use, testing, or demonstrating API integration in your web apps.

This backend is intended to work alongside a finance tracker frontend, but it’s fully functional on its own.

---

## Tech Stack

* **Python 3.11**
* **FastAPI** for API framework
* **SQLAlchemy** with **PostgreSQL** (Numeric(18,2) for balances)
* **Pydantic** for request validation and schema
* **Redis** for optional rate limiting (via `fastapi-limiter`)
* **Uvicorn + Gunicorn** for production deployment
* **Docker** for local PostgreSQL and Redis setup

---

## Features

* Create and manage accounts (checking/savings)
* Add and list transactions with categories and timestamps
* Accurate balance calculations using `Decimal`
* Optional rate-limiting per API key (via Redis)
* Separate **master API key** and **public API keys** for secure access

---

## Setup & Local Development

1. Clone the repository:

```bash
git clone https://github.com/yourusername/your-repo.git
cd your-repo
```

2. Create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Configure environment variables:

```bash
cp .env.example .env
nano .env
```

Fill in `DATABASE_URL`, `REDIS_URL`, and `MASTER_API_KEY`. For local testing, you can use Docker:

```bash
# PostgreSQL
docker run --name mockbank-postgres -e POSTGRES_USER=dbuser -e POSTGRES_PASSWORD=dbpassword -e POSTGRES_DB=mockbank -p 5432:5432 -d postgres:15

# Redis
docker run --name mockbank-redis -p 6379:6379 -d redis:7
```

5. Run the API locally:

```bash
# activate .venv first
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Visit `http://127.0.0.1:8000/docs` to explore the API using Swagger UI.

---

## API Usage Examples

**Create a public API key** (requires `MASTER_API_KEY`):

```bash
curl -X POST "http://127.0.0.1:8000/accounts/keys" \
-H "x-api-key: $MASTER_API_KEY" \
-H "Content-Type: application/json" \
-d '{"name":"public-test-key"}'
```

**Create an account**:

```bash
curl -X POST "http://127.0.0.1:8000/accounts" \
-H "x-api-key: $PUBLIC_API_KEY" \
-H "Content-Type: application/json" \
-d '{"name":"Alice","type":"checking","balance":100.00}'
```

**List accounts**:

```bash
curl -X GET "http://127.0.0.1:8000/accounts" -H "x-api-key: $PUBLIC_API_KEY"
```

**Get account details**:

```bash
curl -X GET "http://127.0.0.1:8000/accounts/1" -H "x-api-key: $PUBLIC_API_KEY"
```

**Add a transaction**:

```bash
curl -X POST "http://127.0.0.1:8000/transactions" \
-H "x-api-key: $PUBLIC_API_KEY" \
-H "Content-Type: application/json" \
-d '{"account_id":1,"amount":-25.50,"category":"groceries","description":"supermarket"}'
```

**List transactions**:

```bash
curl -X GET "http://127.0.0.1:8000/transactions?account_id=1&limit=50" \
-H "x-api-key: $PUBLIC_API_KEY"
```

---

## Deployment

**Using Gunicorn + Uvicorn (production-ready)**

1. Create a `start.sh`:

```bash
#!/bin/bash
gunicorn app.main:app -w ${GUNICORN_WORKERS:-4} -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

2. Make it executable and run:

```bash
chmod +x start.sh
./start.sh
```

**Optional VPS deployment** (Ubuntu example):

* Use Docker for Postgres and Redis.
* Configure Nginx as a reverse proxy and enable HTTPS via Certbot.
* Use `systemd` to keep the service running.

---

## Notes

* **Numeric balances** use `Decimal` for precision — no floating-point errors.
* **Concurrency**: simultaneous transactions on the same account may cause race conditions in this mock API. For production banking apps, row-level locking is required.
* **Rate limiting** is optional; Redis is required for `fastapi-limiter`.

---

## License

This project is open-source for learning and portfolio purposes. Feel free to fork or adapt for personal projects.


