# LiteBank API 🏦

**LiteBank API is a lightweight banking API I built with FastAPI and SQLAlchemy to manage accounts, transactions, and financial tracking.**

---

## Features

* Create user accounts
* Deposit and withdraw funds
* Transfer money between accounts
* View transaction history
* JWT-based authentication

---

## Tech Stack

* **Python 3.11+**
* **FastAPI** – API framework
* **SQLAlchemy** – ORM for database interactions
* **SQLite/PostgreSQL** – database
* **Uvicorn** – ASGI server
* **FastAPI-JWT-Auth** – for authentication
* **Pytest** – for unit testing

---

## Getting Started

1. **Clone the repo**

```bash
git clone https://github.com/inesruizblach/LiteBank.git
cd LiteBank
```

2. **Set up env**

Option 1: Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
Option 2: Create a conda environment
```bash
conda create -n litebank python=3.11
conda activate litebank
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the API**

```bash
uvicorn app.main:app --reload
```

5. Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the endpoints.

---

## Quick Start Test Cases

### User Endpoints

1. **List users**
```bash
curl -X GET "http://127.0.0.1:8000/users/"
```

2. **Create new users**
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
-H "Content-Type: application/json" \
-d '{"name":"User1","email":"user1@example.com","password":"password123"}'
```

```bash
curl -X POST "http://127.0.0.1:8000/users/" \
-H "Content-Type: application/json" \
-d '{"name":"User2","email":"user2@example.com","password":"password123"}'
```

Expected response:
```bash
{"id":1,"name":"User1","email":"user1@example.com"}
```

3. **Login to get JWT token**
```bash
curl -X POST "http://127.0.0.1:8000/login" \
-H "Content-Type: application/json" \
-d '{"email":"user1@example.com","password":"password123"}'
```

Response:
```bash
{
  "access_token": "your_jwt_token",
  "token_type": "bearer"
}
```

### Accounts Endpoints (JWT required) 

4. **Create accounts**
```bash
curl -X POST "http://127.0.0.1:8000/accounts/" \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"balance":100}'
```

```bash
curl -X POST "http://127.0.0.1:8000/accounts/" \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"balance":50}'
```

Expected response:
```bash
{"id":1,"user_id":1,"balance":0}
```

5. **List accounts**
```bash
curl -X GET "http://127.0.0.1:8000/accounts/" \
-H "Authorization: Bearer your_jwt_token"
```

Expected response (empty if no accounts yet):
```bash
[]
```

### Transactions Endpoints (JWT required) 

6. **Deposit funds**
```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"account_id":1,"type":"deposit","amount":100}'
```

Expected response:
```bash
{"id":1,"account_id":1,"type":"deposit","amount":100,"created_at":"2025-10-16T12:00:00"}
```

7. **Withdraw funds**
```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"account_id":1,"type":"withdraw","amount":50}'
```

8. **Transfer funds**
```bash
curl -X POST "http://127.0.0.1:8000/transactions/transfer/" \
-H "Authorization: Bearer your_jwt_token" \
-H "Content-Type: application/json" \
-d '{"from_account_id":1,"to_account_id":2,"amount":30}'
```

Expected response:
```bash
{
  "message": "Transferred 50 from account 1 to 2.",
  "from_account_balance": 50,
  "to_account_balance": 50
}
```

9. **List transactions**
```bash
curl -X GET "http://127.0.0.1:8000/transactions/" \
-H "Authorization: Bearer your_jwt_token"
```

---

## Authentication Flow

1. Signup → Create user with /users/.
2. Login → Obtain JWT from /auth/login.
3. Access Protected Routes → Include header:
```Authorization: Bearer <access_token>```

---

## Project Structure

```
litebank-api/
│── app/
│   ├── main.py              # Entry point
│   ├── models.py            # Database models
│   ├── schemas.py           # Request/response models
│   ├── database.py          # DB connection setup
│   ├── crud.py              # DB operations
│   ├── config.py            # JWT and app config
│   └── routers/
│       ├── users.py
│       ├── accounts.py
│       └── transactions.py
│
├── alembic/                 # Database migrations
│   └── versions/
│
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
│
├── requirements.txt
└── README.md

```
