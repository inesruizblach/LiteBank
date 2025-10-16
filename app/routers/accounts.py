"""
API routes for account operations.
"""

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from .. import crud, schemas, database, models

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
def create_account(account: schemas.AccountCreate, db: Session = Depends(get_db),
                   Authorize: AuthJWT = Depends()):
    """
    Create a new account for the authenticated user.

    Args:
        account (schemas.AccountCreate): Account creation details.
        db (Session): Database session (injected).

    Returns:
        schemas.Account: The created account.
    """
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()

    # Force ownership
    account.user_id = current_user_id

    return crud.create_account(db=db, account=account)


@router.get("/", response_model=list[schemas.Account])
def read_accounts(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Retrieve all accounts belonging to the authenticated user.

    Args:
        db (Session): Database session (injected).

    Returns:
        list[schemas.Account]: List of accounts.
    """
    Authorize.jwt_required()
    current_user_id = int(Authorize.get_jwt_subject())
    return crud.get_accounts(db, user_id=current_user_id)
