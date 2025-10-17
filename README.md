# LiteBank API 🏦

**LiteBank** is a modern, lightweight banking API built with **FastAPI** and **SQLAlchemy** — designed to handle user accounts, transactions, and secure financial operations with JWT authentication.

---

## 🌐 Live Deployment

LiteBank is now live and hosted on **Render** 🚀  
🔗 **Live API:** [https://litebank.onrender.com](https://litebank.onrender.com)  
🩺 **Health Check:** [https://litebank.onrender.com/healthz](https://litebank.onrender.com/healthz)  
📘 **Interactive Docs:** [https://litebank.onrender.com/docs](https://litebank.onrender.com/docs)

Deployed automatically via **GitHub Actions → Render** CI/CD pipeline.

## Features

* 👤 Create and manage user profiles
* 💰 Deposit and withdraw funds
* 🔄 Transfer money between accounts
* 🧾 View transaction history
* 🔐 JWT-based authentication
* 🐳 Dockerized for easy deployment

---

## Tech Stack

| Category         | Technology          |
| ---------------- | ------------------- |
| Language         | Python 3.11         |
| Framework        | FastAPI             |
| ORM              | SQLAlchemy          |
| Auth             | FastAPI-JWT-Auth    |
| Database         | PostgreSQL / SQLite |
| Server           | Uvicorn             |
| Migrations       | Alembic             |
| Containerization | Docker              |
| Deployment       | Render (via GitHub Actions) |

---

## Getting Started (Local)

1. **Clone the repo**

```bash
git clone https://github.com/inesruizblach/LiteBank.git
cd LiteBank
```

2. **Set up env**

Option A: Create a virtual environment
```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```
Option B: Create a conda environment
```bash
conda create -n litebank python=3.11
conda activate litebank
```

3. **Install dependencies**

```bash
pip install -r requirements.txt
```

4. **Run the API locally**

```bash
uvicorn app.main:app --reload
```

5. Visit:
* API Root → [http://127.0.0.1:8000](http://127.0.0.1:8000)
* Interactive Docs → [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Example Endpoints

### 👥 Users

1. **List users**
```bash
GET /users/
```

2. **Create new users**
```bash
POST /users/
```

### 🔑 Authentication
3. **Login to get JWT token**
```bash
POST /login
```

### 💵 Accounts (JWT required) 

4. **Create and list accounts**
```bash
POST /accounts/
GET /accounts/
```

### 💸 Transactions Endpoints (JWT required) 

5. Perform deposits, withdrawals, or transfers:
```bash
POST /transactions/
POST /transactions/transfer/
GET /transactions/
```

---

## Local Run Test Cases - Example API calls

### 👥 Users

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

### 🔑 Authentication
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

### 💵 Accounts (JWT required) 

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

### 💸 Transactions Endpoints (JWT required) 

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
LiteBank/
│── app/
│   ├── main.py              # FastAPI entrypoint
│   ├── models.py            # SQLAlchemy models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud.py              # Business logic and DB ops
│   ├── database.py          # Database configuration
│   ├── config.py            # App/JWT settings
│   └── routers/
│       ├── users.py
│       ├── accounts.py
│       └── transactions.py
│
├── alembic/                 # Database migrations
│   └── versions/
│
├── .github/
│   └── workflows/
│       └── deploy.yml       # CI/CD pipeline for Render deployment
│
├── Dockerfile               # Docker build configuration
├── docker-compose.yml       # Local dev environment
├── requirements.txt         # Python dependencies
└── README.md

```

---

## 🧰 Development Tools

| Command                         | Description           |
| ------------------------------- | --------------------- |
| `uvicorn app.main:app --reload` | Run API locally       |
| `alembic upgrade head`          | Run DB migrations     |
| `pytest`                        | Run test suite        |
| `docker compose up --build`     | Start app with Docker |

---

## 🌍 Deployment

LiteBank is automatically deployed to Render using a GitHub Actions workflow (.github/workflows/deploy.yml), which:
1. Installs dependencies
2. Runs Alembic migrations on the Render PostgreSQL database
3. Triggers a new Render deploy

🔗 Production URL: https://litebank.onrender.com

---

## 📜 License

This project is open-source and available under the **MIT License**.

---

Developed by [Inés Ruiz Blach](https://github.com/inesruizblach)