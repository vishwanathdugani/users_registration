# login.py
import logging
from fastapi import Depends, APIRouter, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

from datetime import timedelta
from app.core import config
from app.core.security import verify_password, create_access_token
from app.crud.user import get_user_by_username
from app.schemas.token import Token
from app.db.sessions import get_db

router = APIRouter()
logger = logging.getLogger(__name__)


@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)) -> Token:
    logger.info(f"Attempting to log in user: {form_data.username}")

    user = get_user_by_username(db, username=form_data.username)
    if not user or not verify_password(form_data.password, user.hashed_password):
        logger.error(f"Failed to authenticate user: {form_data.username}")
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    if not user.verified:
        logger.warning(f"User {form_data.username} is not verified. Unable to log in.")
        return JSONResponse(status_code=400, content={"detail": "User not verified. Please verify your email."})

    access_token_expires = timedelta(minutes=config.settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)

    logger.info(f"User {form_data.username} successfully logged in.")
    return {"access_token": access_token, "token_type": "bearer"}
