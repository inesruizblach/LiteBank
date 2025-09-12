"""
API routes for account operations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from .. import crud, schemas, database

router = APIRouter(
    prefix="/accounts",
    tags=["accounts"],
)


def get_db():
    """
    Provide a database session dependency.
    """
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=schemas.Account)
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db)):
    """
    Create a new account.

    Args:
        account (schemas.AccountCreate): Account creation details.
        db (Session): Database session (injected).

    Returns:
        schemas.Account: The created account.
    """
    return crud.create_account(db=db, account=account)


@router.get("/", response_model=list[schemas.Account])
def read_accounts(db: Session = Depends(get_db)):
    """
    Retrieve all accounts.

    Args:
        db (Session): Database session (injected).

    Returns:
        list[schemas.Account]: List of accounts.
    """
    return crud.get_accounts(db)
