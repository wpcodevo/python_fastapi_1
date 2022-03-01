from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import schemas, models, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(tags=['Auth'])


@router.post('/login', response_model=schemas.Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(
        models.User.email == form_data.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid email or password')
    if not utils.verify_password(form_data.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='Invalid email or password')

    # Create Access Token
    access_token = oauth2.create_access_token({'user_id': user.id})

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
