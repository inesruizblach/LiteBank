from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from typing import Optional
from enum import Enum

# --- User Schemas---
class UserBase(BaseModel):
    """
    Base schema for a user, containing common user fields.
    """
    name: str
    email: EmailStr

class UserCreate(UserBase):
    """
    Schema for creating a new user.
    Inherits name and email fields from UserBase.
    """
    password: str = Field(..., min_length=6)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class User(UserBase):
    """
    Schema for returning user data, including the user ID.
    """
    id: int

    class Config:
        orm_mode = True

# --- Account Schemas---
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
    user_id: Optional[int] = None  # Will be filled from JWT in router

class Account(AccountBase):
    """
    Schema for returning account data, including account and user IDs.
    """
    id: int
    user_id: int

    class Config:
        orm_mode = True

# --- Transaction Schemas---

class TransactionType(str, Enum):
    DEPOSIT = "deposit"
    WITHDRAW = "withdraw"

class TransactionBase(BaseModel):
    """
    Base schema for a transaction, such as a deposit or withdrawal.
    Includes the transaction type and amount.
    """
    type: TransactionType
    amount: float = Field(..., gt=0)

class TransactionCreate(TransactionBase):
    """
    Schema for creating a new transaction.
    Includes the associated account ID.
    """
    account_id: int

class Transaction(TransactionBase):
    """
    Schema for returning transaction data with database metadata.
    Includes transaction ID, associated account ID, and created_at.
    """
    id: int
    account_id: int
    created_at: datetime

    class Config:
        orm_mode = True

# --- Transfer Schema---

class TransferCreate(BaseModel):
    """
    Schema for transferring funds between two accounts.
    Includes source and destination account IDs and the transfer amount.
    """
    from_account_id: int
    to_account_id: int
    amount: float = Field(..., gt=0)

class TransferResponse(BaseModel):
    """ Schema for transfer response details. """
    message: str
    from_account_balance: float
    to_account_balance: float
