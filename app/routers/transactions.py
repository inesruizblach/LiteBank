"""
API routes for transaction operations (deposit, withdraw, transfer).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi_jwt_auth import AuthJWT
from .. import crud, schemas, database, models

router = APIRouter(
    prefix="/transactions",
    tags=["transactions"],
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

@router.get("/", response_model=list[schemas.Transaction])
def read_transactions(db: Session = Depends(get_db), Authorize: AuthJWT = Depends()):
    """
    Retrieve all transactions belonging to the authenticated user.
    Args:
        db (Session): Database session (injected).
        Authorize (AuthJWT): JWT authorization dependency.
    Returns:
        list[schemas.Transaction]: List of transactions.
    """
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    return crud.get_transactions(db, user_id=int(current_user_id))

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db),
                       Authorize: AuthJWT = Depends()):
    """
    Create a transaction (deposit or withdraw).

    Args:
        transaction (schemas.TransactionCreate): Transaction details.
        db (Session): Database session (injected).
        Authorize (AuthJWT): JWT authorization dependency.

    Returns:
        schemas.Transaction: The created transaction.

    Raises:
        HTTPException: If withdrawal fails or type is invalid.
    """
    Authorize.jwt_required()
    current_user_id = int(Authorize.get_jwt_subject())

    # Verify the account belongs to this user
    account = db.query(models.Account).filter(models.Account.id == transaction.account_id).first()
    if not account or account.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized access to this account")

    try:
        return crud.create_transaction(db=db, transaction=transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transfer/", response_model=schemas.TransferResponse)
def transfer_funds(
    transfer: schemas.TransferCreate,
    db: Session = Depends(get_db),
    Authorize: AuthJWT = Depends()
):
    """
    Transfer funds between two accounts owned by the authenticated user

    Args:
        transfer (schemas.TransferCreate): JSON body with from_account_id, to_account_id, and amount.
        db (Session): Database session (injected).
        Authorize (AuthJWT): JWT authorization dependency.

    Returns:
        dict: Transfer confirmation message and balances.

    Raises:
        HTTPException: If insufficient funds or accounts are invalid.
    """
    Authorize.jwt_required()
    current_user_id = int(Authorize.get_jwt_subject())

    source = db.query(models.Account).filter(models.Account.id == transfer.from_account_id).first()
    target = db.query(models.Account).filter(models.Account.id == transfer.to_account_id).first()

    if not source or not target:
        raise HTTPException(status_code=404, detail="One or both accounts not found")

    if source.user_id != current_user_id or target.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Unauthorized transfer")

    if source.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Withdraw from source account
    source.balance -= transfer.amount
    # Deposit into target account
    target.balance += transfer.amount
    db.commit()

    return {
        "message": f"Transferred {transfer.amount} from account {transfer.from_account_id} to {transfer.to_account_id}.",
        "from_account_balance": source.balance,
        "to_account_balance": target.balance,
    }

