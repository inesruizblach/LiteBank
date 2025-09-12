# LiteBank API 🏦

**LiteBank API is a lightweight banking API I built with FastAPI and SQLAlchemy to manage accounts, transactions, and financial tracking.**

---

## Features

* Create user accounts
* Deposit and withdraw funds
* Transfer money between accounts
* View transaction history
* JWT-based authentication (planned for future)

---

## Tech Stack

* **Python 3.11+**
* **FastAPI** – API framework
* **SQLAlchemy** – ORM for database interactions
* **SQLite/PostgreSQL** – database
* **Uvicorn** – ASGI server
* **Pytest** – for unit testing (optional)

---

## Getting Started

### Option 1: Using pip

1. Clone the repo:

```bash
git clone https://github.com/inesruizblach/LiteBank.git
cd LiteBank
```

2. Create a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate   # macOS/Linux
venv\Scripts\activate      # Windows
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
uvicorn app.main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the endpoints.

### Option 2: Using conda

1. Clone the repo:

```bash
git clone https://github.com/inesruizblach/LiteBank.git
cd LiteBank
```

2. Create a conda environment:

```bash
conda create -n litebank python=3.11
conda activate litebank
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. Run the API:

```bash
uvicorn app.main:app --reload
```

Visit [http://127.0.0.1:8000](http://127.0.0.1:8000) and [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) to explore the endpoints.

---

## Quick Start Test Cases

If no accounts or transactions exist yet, you can test the API as follows:

### 1. Check accounts (empty)

```bash
curl -X GET "http://127.0.0.1:8000/accounts/" -H "accept: application/json"
```

Expected response:

```json
[]
```

### 2. Create two new users and accounts

```bash
curl -X POST "http://127.0.0.1:8000/accounts/" \
-H "Content-Type: application/json" \
-d '{"user_id":1,"balance":0}'
```

```bash
curl -X POST "http://127.0.0.1:8000/accounts/" \
-H "Content-Type: application/json" \
-d '{"user_id":2,"balance":50}'
```

Expected responses:

```json
{"id":1,"user_id":1,"balance":0}
```

```json
{"balance":50.0,"id":2,"user_id":2}
```

### 3. Check transactions (empty)

```bash
curl -X GET "http://127.0.0.1:8000/transactions/" -H "accept: application/json"
```

Expected response:

```json
[]
```

### 4. Deposit funds

```bash
curl -X POST "http://127.0.0.1:8000/transactions/" \
-H "Content-Type: application/json" \
-d '{"account_id":1,"type":"deposit","amount":100}'
```

Expected response:

```json
{"id":1,"account_id":1,"type":"deposit","amount":100,"timestamp":"2025-09-12T00:00:00"}
```

### 5. Transfer funds (once you have two accounts)

```bash
curl -X POST "http://127.0.0.1:8000/transactions/transfer/" \
-H "Content-Type: application/json" \
-d '{"from_account_id":1,"to_account_id":2,"amount":50}'
```

Expected response:

```json
{
  "message": "Transferred 50 from account 1 to 2.",
  "from_account_balance": 50,
  "to_account_balance": 50
}
```

---

## Project Structure

```
litebank-api/
│── app/
│   ├── main.py          # Entry point
│   ├── models.py        # Database models
│   ├── schemas.py       # Request/response models
│   ├── database.py      # DB connection setup
│   ├── crud.py          # DB operations
│   └── routers/
│       ├── accounts.py
│       └── transactions.py
├── requirements.txt
└── README.md
```
