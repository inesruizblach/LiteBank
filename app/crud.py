"""
Database CRUD operations for Users, Accounts, and Transactions.
"""

from sqlalchemy.orm import Session
from . import models, schemas


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create and persist a new user.

    Args:
        db (Session): Database session.
        user (schemas.UserCreate): Pydantic model with user details.

    Returns:
        models.User: The created user instance.
    """
    db_user = models.User(name=user.name, email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_users(db: Session, skip: int = 0, limit: int = 10):
    """
    Retrieve a list of users with pagination.

    Args:
        db (Session): Database session.
        skip (int): Number of records to skip.
        limit (int): Maximum number of records to return.

    Returns:
        list[models.User]: List of users.
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def create_account(db: Session, account: schemas.AccountCreate):
    """
    Create a new account for a given user.

    Args:
        db (Session): Database session.
        account (schemas.AccountCreate): Account creation schema.

    Returns:
        models.Account: The created account instance.
    """
    db_account = models.Account(user_id=account.user_id, balance=account.balance)
    db.add(db_account)
    db.commit()
    db.refresh(db_account)
    return db_account


def get_accounts(db: Session):
    """
    Retrieve all accounts.

    Args:
        db (Session): Database session.

    Returns:
        list[models.Account]: List of accounts.
    """
    return db.query(models.Account).all()


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    """
    Create a transaction (deposit or withdraw) and update the account balance.

    Args:
        db (Session): Database session.
        transaction (schemas.TransactionCreate): Transaction details.

    Raises:
        ValueError: If withdrawal amount exceeds balance or transaction type is invalid.

    Returns:
        models.Transaction: The created transaction instance.
    """
    db_transaction = models.Transaction(
        account_id=transaction.account_id,
        type=transaction.type,
        amount=transaction.amount
    )
    db.add(db_transaction)

    account = db.query(models.Account).filter(models.Account.id == transaction.account_id).first()

    if transaction.type == "deposit":
        account.balance += transaction.amount
    elif transaction.type == "withdraw":
        if account.balance >= transaction.amount:
            account.balance -= transaction.amount
        else:
            raise ValueError("Insufficient funds")
    else:
        raise ValueError("Invalid transaction type")

    db.commit()
    db.refresh(db_transaction)
    return db_transaction
