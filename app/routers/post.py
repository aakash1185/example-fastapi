from fastapi import APIRouter, Body, FastAPI, Response, status, HTTPException, Depends
from sqlalchemy import func
import models, schemas, utils, oauth2
from sqlalchemy.orm import Session
from database import  get_db
from typing import List, Optional



router = APIRouter(
     prefix='/posts',
     tags =['Posts']
)

  
# @router.get("/")
# def root():
#     return { 'message': 'Keep Alive OK' }

# @router.get("/", response_model=List[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user),
              limit: int = 10, skip=0, search: Optional[str] = ""):
    # cursor.execute(""" Select * from posts """)
    # posts =cursor.fetchall()
    # posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip)
        .all()
    )
    # ===================================================================================================
    """"Changed in version 1.4:
    Renamed RowProxy to .Row. .Row is no longer a "proxy" object in that it contains the final form of data within it, and now acts mostly like a named tuple. Mapping-like functionality is moved to the .Row._mapping attribute, but will remain available in SQLAlchemy 1.x ... "
    So, in my understanding, we are not allowed to retrieve the jsonized data directly from the query anymore; the ._mapping method takes care of building the dict structure with "Post" and "votes" keys, and using map does this for each .Row element in the list; we then convert map to a list to be able to return it. """
    results = list(map(lambda x:x._mapping,results))
    # ===================================================================================================
    
    return results

@router.post("/", status_code=status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):   
        # cursor.execute("""INSERT INTO posts(title, content, published) values (%s, %s, %s)
        #     returning * """, (post.title, post.content, post.published))
        # new_post = cursor.fetchone()
        # conn.commit()
        new_post = models.Post(owner_id=current_user.id ,**post.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)

        return new_post


@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    #  cursor.execute("""select * from posts where id = %s""", (str(id)))
    #  post = cursor.fetchone()
    #  print(post)
    
    # post = db.query(models.Post).filter(models.Post.id == id).first()   
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(
        models.Post.id).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} not found ")
    # if post.owner_id != current_user.id:
    #     raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
    #                         detail= f"Not authorized to perform requested action")
    return post 


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db : Session = Depends(get_db), current_user : int = Depends(oauth2.get_current_user)):
    #deleting post
    # cursor.execute("""Delete from posts where id = %s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()


    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} not found ")
    
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Not authorized to perform requested action")
    post_query.delete(synchronize_session=False)
    db.commit()
    # return {"data" : post }

@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db : Session = Depends(get_db),current_user : int = Depends(oauth2.get_current_user)):
    # cursor.execute("""Update posts set title = %s, content = %s, published = %s where id = %s
    #                 returning * 
    #                 """, 
    #                (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail= f"post with id {id} not found ")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail= f"Not authorized to perform requested action")
    
    post_query.update(updated_post.dict(), synchronize_session=False)   
    db.commit()
    return post_query.first()
