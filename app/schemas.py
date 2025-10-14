from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# --- User ---
class UserBase(BaseModel):
    """
    Base schema for a user, containing common user fields.
    """
    name: str
    email: str

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Inherits name and email fields from UserBase.
    """
    pass

class User(UserBase):
    """
    Schema for returning user data, including the user ID.
    """
    id: int
    class Config:
        from_attributes = True

# --- Account ---
class AccountBase(BaseModel):
    """
    Base schema for an account, containing the balance field.
    """
    balance: float = 0.0

class AccountCreate(AccountBase):
    """
    Schema for creating a new account.
    Includes user_id to associate the account with a user.
    """
    user_id: int

class Account(AccountBase):
    """
    Schema for returning account data, including account and user IDs.
    """
    id: int
    user_id: int
    class Config:
        from_attributes = True

class TransactionBase(BaseModel):
    """
    Base schema for a transaction, such as a deposit or withdrawal.
    Includes the transaction type and amount.
    """
    type: str  # e.g., 'deposit' or 'withdraw'
    amount: float

class TransactionCreate(BaseModel):
    """
    Schema for transferring funds between two accounts.
    Includes source and destination account IDs and the transfer amount.
    """
    from_account_id: int
    to_account_id: int
    amount: float

class Transaction(TransactionBase):
    """
    Schema for returning transaction data with database metadata.
    Includes transaction ID, associated account ID, and timestamp.
    """
    id: int
    account_id: int
    timestamp: datetime

    class Config:
        from_attributes = True

