"""
API routes for transaction operations (deposit, withdraw, transfer).
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
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
def read_transactions(db: Session = Depends(get_db)):
    """
    Retrieve all transactions.
    """
    return db.query(crud.models.Transaction).all()

@router.post("/", response_model=schemas.Transaction)
def create_transaction(transaction: schemas.TransactionCreate, db: Session = Depends(get_db)):
    """
    Create a transaction (deposit or withdraw).

    Args:
        transaction (schemas.TransactionCreate): Transaction details.
        db (Session): Database session (injected).

    Returns:
        schemas.Transaction: The created transaction.

    Raises:
        HTTPException: If withdrawal fails or type is invalid.
    """
    try:
        return crud.create_transaction(db=db, transaction=transaction)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/transfer/")
def transfer_funds(
    transfer: schemas.TransactionCreate,
    db: Session = Depends(get_db),
):
    """
    Transfer funds from one account to another.

    Args:
        transfer (schemas.TransferCreate): JSON body with from_account_id, to_account_id, and amount.
        db (Session): Database session (injected).

    Returns:
        dict: Transfer confirmation message and balances.

    Raises:
        HTTPException: If insufficient funds or accounts are invalid.
    """
    source = db.query(models.Account).filter(models.Account.id == transfer.from_account_id).first()
    target = db.query(models.Account).filter(models.Account.id == transfer.to_account_id).first()

    if not source or not target:
        raise HTTPException(status_code=404, detail="One or both accounts not found")

    if source.balance < transfer.amount:
        raise HTTPException(status_code=400, detail="Insufficient funds")

    # Withdraw from source
    source.balance -= transfer.amount
    # Deposit into target
    target.balance += transfer.amount

    db.commit()

    return {
        "message": f"Transferred {transfer.amount} from account {transfer.from_account_id} to {transfer.to_account_id}.",
        "from_account_balance": source.balance,
        "to_account_balance": target.balance,
    }

