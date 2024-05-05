import json
from sqlalchemy import func
from .. import schemas,models,oauth2
from fastapi import Response,status,HTTPException,Depends,APIRouter
from .. database import get_db
from sqlalchemy.orm import Session
from typing import List,Optional
import pandas as pd


router =APIRouter(prefix="/posts",
                  tags = ['Posts'])

# def find_post(id):
#     for i in my_post:
#         if(i["id"] == id):
#             return i
        
# def get_id(id):
#     for ind , p  in enumerate(my_post):
#         if p["id"] == id:
#             return ind
            

# @router.get("/")
@router.get("/",response_model=List[schemas.PostOut])
async def get_posts(db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
                    limit :int =10,skip: int=0,search : Optional[str] = ''):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(limit)
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post,models.User.email,func.count(models.Vote.post_id).label("votes")).join(models.User,models.Post.owner_id == models.User.id,isouter=True).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id,models.User.email).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(results)
    
    
    response1 = [i[0].__dict__ for i in results]
    response2 =[i[1] for i in results]
    response3 =[i[2] for i in results]
    df = pd.DataFrame(response1)
    df.drop(['_sa_instance_state'],inplace=True,axis=1)
    df["user_id"] = response2
    df["votes"] = response3
    return df.to_dict(orient='records')
    # return results

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_post(post_create : schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # print(current_user.email)
    print(current_user.id)
    # cursor.execute(""" INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",(post.title,post.content,post.publish))
    # conn.commit()
    # new_post = cursor.fetchone()
    new_post =  models.Post(owner_id=current_user.id, **post_create.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

# @app.get("/posts/latest") 
# def getLatestPost():
#     return {"data":my_post[-1]}


@router.get("/{id}",response_model=List[schemas.PostOut])
def get_post(id : int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts where id = %s """,(str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    results = db.query(models.Post,models.User.email,func.count(models.Vote.post_id).label("votes")).join(models.User,models.Post.owner_id == models.User.id,isouter=True).join(models.Vote,models.Post.id == models.Vote.post_id,isouter=True).group_by(models.Post.id,models.User.email).filter(models.Post.id == id).first()
    if results == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with {id} not found")
    response1 =[ results[0].__dict__]
    response2 =[results[1]] 
    response3 =[results[2] ]
    df = pd.DataFrame(response1,)
    df.drop(['_sa_instance_state'],inplace=True,axis=1)
    df["user_id"] = response2
    df["votes"] = response3
    
    print(df)
   
    return df.to_dict(orient='records')


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delte_post(id : int,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE  FROM posts where id = %s RETURNING * """,(str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with {id} not found")
    if(post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"not allowed to delete {id} ")


    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post_update : schemas.PostCreate,db: Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s where id = %s RETURNING *""",(post.title,post.content,str(post.publish),str(id)))
    # post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail= f"post with {id} not found") 

    if(post.owner_id != current_user.id):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail= f"not allowed to update {id} ")
    
    post_query.update(post_update.model_dump(),synchronize_session=False)
    db.commit()
    return post_query.first()