"""
Main entry point for LiteBank API.
Initializes database, creates tables, and registers routers.
"""

from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from .routers import users, accounts, transactions
from .database import engine
from . import models

# Initialize FastAPI app
app = FastAPI(title="LiteBank API 🏦")

# Register API routers
app.include_router(users.router)
app.include_router(accounts.router)
app.include_router(transactions.router)

@app.get("/")
def root():
    return RedirectResponse(url="/docs")
