# users.py
import logging
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.sessions import get_db
from app.crud.user import get_user_by_username, create_user, update_user_verification
from app.schemas.userschema import UserCreate, UserSchema, VerifyUserRequest

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/users", response_model=UserSchema)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)) -> UserSchema:
    logger.info(f"Creating new user: {user.username}")

    db_user = get_user_by_username(db, username=user.username)
    if db_user:
        logger.warning(f"Username already registered: {user.username}")
        raise HTTPException(status_code=400, detail="Username already registered")

    user_creation = create_user(db=db, user=user)
    logger.info("User created successfully")
    return user_creation


@router.post("/verify-user")
def verify_user(request: VerifyUserRequest, db: Session = Depends(get_db)):
    logger.info(f"Verifying user: {request.email}")

    user = get_user_by_username(db, username=request.email)
    if not user:
        logger.error(f"User not found: {request.email}")
        raise HTTPException(status_code=404, detail="User not found")

    update_user_verification(db, user, verified=True)
    logger.info(f"User verified: {request.email}")
    return {"message": f"User {request.email} has been verified"}
