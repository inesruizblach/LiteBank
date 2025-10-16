from fastapi import APIRouter, Depends, HTTPException
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session
from .. import schemas, crud, database
from fastapi_jwt_auth.exceptions import AuthJWTException

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/signup", response_model=schemas.UserResponse)
def signup(user: schemas.UserCreate, db: Session = Depends(database.SessionLocal)) -> schemas.UserResponse:
    """Register a new user account.

    Args:
        user (schemas.UserCreate): User registration data.
        db (Session): SQLAlchemy database session dependency.

    Raises:
        HTTPException: If the email is already registered.

    Returns:
        schemas.UserResponse: The newly created user data.
    """
    existing = db.query(crud.models.User).filter(crud.models.User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.create_user(db, user)


@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(database.SessionLocal),
    Authorize: AuthJWT = Depends()) -> dict[str, str]:
    """Authenticate a user and return a JWT access token.

    Args:
        user (schemas.UserLogin): User login credentials.
        db (Session): SQLAlchemy database session dependency.
        Authorize (AuthJWT): JWT authorization dependency.

    Raises:
        HTTPException: If authentication fails.

    Returns:
        dict[str, str]: Access token and token type.
    """
    db_user = crud.authenticate_user(db, user.email, user.password)
    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = Authorize.create_access_token(subject=db_user.id)
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/me", response_model=schemas.UserResponse)
def get_me(Authorize: AuthJWT = Depends(), db: Session = Depends(database.SessionLocal)) -> schemas.UserResponse:
    """Retrieve the currently authenticated user's details.

    Args:
        Authorize (AuthJWT): JWT authorization dependency.
        db (Session): SQLAlchemy database session dependency.

    Returns:
        schemas.UserResponse: The authenticated user's data.
    """
    Authorize.jwt_required()
    current_user_id = Authorize.get_jwt_subject()
    user = db.query(crud.models.User).filter(crud.models.User.id == current_user_id).first()
    return user


class Settings(schemas.BaseModel):
    """JWT configuration settings."""
    authjwt_secret_key: str = "supersecretkey123"


@AuthJWT.load_config
def get_config() -> Settings:
    """Provide JWT configuration to FastAPI-JWT-Auth.

    Returns:
        Settings: JWT configuration object.
    """
    return Settings()
