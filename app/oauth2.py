from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from . import schemas, database, models
from sqlalchemy.orm import Session
from .config import settings

oauth_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECRET_KEY = settings.secret_key
JWT_EXPIRES_IN = settings.access_token_expires_in
ALGORITHM = settings.algorithm


def create_access_token(data: dict):
    to_encode = data.copy()
    expires = datetime.now() + timedelta(minutes=JWT_EXPIRES_IN)
    to_encode.update({'exp': expires})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


def verify_access_token(token: str, credential_exception: HTTPException):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id = payload.get('user_id')

        if not id:
            raise credential_exception
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    return token_data


def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                                         detail='Could not validate credentials', headers={"WWW-Authenticate": "Bearer"})

    decoded = verify_access_token(token, credential_exception)
    user = db.query(models.User).filter(models.User.id == decoded.id).first()
    return user
