from fastapi import  Depends, FastAPI, Response, status, HTTPException, APIRouter
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import get_db
from typing import List, Optional

router = APIRouter(prefix='/posts',
                   tags=['Posts'])  # Tags is a list

# @router.get("/", response_model=List[schemas.Post])  # when we retrieve data we usually use get
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()

    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()
    print(posts)

    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post) # change the status code to 201
async def create_posts(post: schemas.PostCreate, db: Session=Depends(get_db),
                       current_user: int = Depends(oauth2.get_current_user)): # Call now new post, and reference pydantic model, Fastapi will now validate the data types before passing them in
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """,
    #                 (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id=current_user.id, **post.dict()) # ** Unpacks the dictionary
    db.add(new_post)
    db.commit()  # Similar to conn.commit()
    db.refresh(new_post) # new_post is a SQLalchemy model so we need to convert to dict for the response

    return new_post



@router.get("/{id}", response_model=schemas.PostOut) #{id} represents/is a path parameter whis is always a string
def get_post(id: int, db: Session=Depends(get_db), current_user:int = Depends(oauth2.get_current_user)):  #by declaring it to be int here we don't have to convert further down

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))  # Need to pass id as str in SQL
    # post = cursor.fetchone()


    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.id == id).first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} was not found") # detail is what we want to print as an error

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session=Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):
    # Deleting a post

    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")


    post_query.delete(synchronize_session=False)
    db.commit()


    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session=Depends(get_db),
                current_user:int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
    #                   (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with id: {id} does not exist")

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, 
                            detail="Not authorized to perform requested action")

    post_query.update(updated_post.dict(), synchronize_session=False)

    db.commit()


    return post_query.first()