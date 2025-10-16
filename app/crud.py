"""
Database CRUD operations for Users, Accounts, and Transactions.
"""

from passlib.context import CryptContext
from sqlalchemy.orm import Session
from . import models, schemas

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_password_hash(password: str):
    """Hash a plaintext password."""
    return pwd_context.hash(password[:72])

def verify_password(plain_password, hashed_password):
    """Verify a plaintext password against a hashed password."""
    return pwd_context.verify(plain_password, hashed_password)


def create_user(db: Session, user: schemas.UserCreate):
    """
    Create and persist a new user.

    Args:
        db (Session): Database session.
        user (schemas.UserCreate): Pydantic model with user details.

    Returns:
        models.User: The created user instance.
    """
    hashed_pw = get_password_hash(user.password)
    db_user = models.User(name=user.name, email=user.email, password_hash=hashed_pw)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str):
    """
    Authenticate a user by email and password.

    Args:
        db (Session): Database session.
        email (str): User's email.
        password (str): User's password.

    Returns:
        models.User | None: The authenticated user or None if authentication fails.
    """
    user = db.query(models.User).filter(models.User.email == email).first()
    if not user:
        return None
    if not verify_password(password, user.password_hash):
        return None
    return user

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


def get_accounts(db: Session,  user_id: int | None = None):
    """
    Retrieve all accounts or filter by user.

    Args:
        db (Session): Database session.
        user_id (int | None): Optional user ID to filter accounts.

    Returns:
        list[models.Account]: List of accounts.
    """
    query = db.query(models.Account)
    if user_id:
        query = query.filter(models.Account.user_id == user_id)
    return query.all()


def create_transaction(db: Session, transaction: schemas.TransactionCreate):
    """
    Create a transaction (deposit or withdraw) and update the account balance.

    Args:
        db (Session): Database session.
        transaction (schemas.TransactionCreate): Transaction details.

    Raises:
        ValueError: 
            If account not found.
            If withdrawal amount exceeds balance or transaction type is invalid.

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
    if not account:
        raise ValueError("Account not found")

    if transaction.type == schemas.TransactionType.DEPOSIT:
        account.balance += transaction.amount
    elif transaction.type == schemas.TransactionType.WITHDRAW:
        if account.balance >= transaction.amount:
            account.balance -= transaction.amount
        else:
            raise ValueError("Insufficient funds")
    else:
        raise ValueError("Invalid transaction type")

    db.commit()
    db.refresh(db_transaction)
    return db_transaction

def get_transactions(db: Session, user_id: int | None = None):
    """
    Retrieve all transactions or only those belonging to a user's accounts.

    Args:
        db (Session): Database session.
        user_id (int | None): Optional user ID filter.

    Returns:
        list[models.Transaction]: List of transactions.
    """
    query = db.query(models.Transaction)
    if user_id:
        query = (
            query.join(models.Account)
            .filter(models.Account.user_id == user_id)
        )
    return query.all()

