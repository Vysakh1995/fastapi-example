from .. import schemas,models,utils
from fastapi import status,HTTPException,Depends,APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
from typing import List

router =APIRouter(prefix="/users",
                   tags = ['Users'])


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(post_user : schemas.UserCreate,db: Session = Depends(get_db)):
    # print(post_user.model_dump())
   
    post_user.password = utils.hash(post_user.password)

    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.publish))
    # conn.commit()
    # new_post = cursor.fetchone()
    new_user =  models.User(**post_user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user



@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id :int,db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()  
    if user == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"user with {id} not found")
    return user
    