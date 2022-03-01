from typing import List
from sqlalchemy import func
from app import oauth2
from .. import schemas, models
from sqlalchemy.orm import Session
from fastapi import Depends, HTTPException, status, APIRouter, Response
from ..database import get_db

router = APIRouter(
    prefix='/posts',
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), limit: int = 10, page: int = 1, search: str | None = ''):
    skip = (page - 1) * limit

    posts = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).outerjoin(
        models.Vote, models.Post.id == models.Vote.post_id).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts


@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    new_post = models.Post(**post.dict(), owner_id=current_user.id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = post_query.first()

    if not updated_post:
        raise HTTPException(status_code=status.HTTP_200_OK,
                            detail=f'No post with this id: {id} found')
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    post_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return updated_post


@router.get('/{id}', response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label('votes')).outerjoin(
        models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"No post with this id: {id} found")
    return post


@router.delete('/{id}')
def delete_post(id: int, db: Session = Depends(get_db), current_user=Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'No post with this id: {id} found')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail='You are not allowed to perform this action')
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
