from fastapi import FastAPI, Response, status, HTTPException, Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor 
from  sqlalchemy.orm import session
from . import models
from .database import engine, get_db


models.Base.metadata.create_all(bind = engine) #should create a table in postgres

app = FastAPI() # ' app ' is the instance 



#class/pydantic model for a post
#schmea for our post
class Post(BaseModel):
    
    title : str
    content : str
    published  : bool = True #defaults to true 

    
try:
    conn = psycopg2.connect(host = 'localhost' , database = 'fastapi' , user = 'postgres' , password= 'bruse12345'
                            , cursor_factory=RealDictCursor)

    cursor = conn.cursor()
    print(" - - - - - - - - - - -----sucessfully connected to database---- -  - - - - - - - - - - ")

except Exception as e:
    print("oops!!!!connection failed!!!!!")
    print("error:", e)



#db as of now in memory 
# my_posts = [
#     {"title" : "title of post 1", "content": "content of post 1", "id": 1}, 
#         {"title" : "favorite foods", "content": "I like pizza", "id": 2}
# ]




def find_post_index(id:int):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None

#this is a path or route 
@app.get("/")
def root():
    return {"message": "you are on the root url "}

@app.get("/sqlalchemy")
def test_posts(db: session = Depends(get_db)):
    return {"status" : "success"}



@app.get("/posts")
def get_posts():
    cursor.execute("select * from posts ")
    posts =  cursor.fetchall()
   
    return {"data ": posts}


@app.get("/posts/latest")
def latest_post(res : Response):
    cursor.execute("select * from posts ORDER BY created_at DESC LIMIT 1")
    post  = cursor.fetchone()

    if not post:
        res.status_code = status.HTTP_404_NOT_FOUND
        return {"data" : "no post available"}

    return {"latest post" : post}


@app.get("/posts/{id}")
def get_post(id : int, res : Response):
    
    cursor.execute(f"select * from posts WHERE id = {id}")
        
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} was not found")
    
    return {"data" : post}



@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post : Post): #based on the schema provided
    cursor.execute("""insert into posts (title , content, published) values (%s,%s,%s) RETURNING * ; """,
                   (post.title,
                    post.content,
                    post.published ))

    new_post = cursor.fetchone()

    conn.commit() #this actually push the changes into my database 
    
    return {"data" : new_post}


@app.delete("/posts/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete(id: int):
    cursor.execute(f"DELETE FROM posts WHERE id = {id} returning * ")
    deleted_post = cursor.fetchone()
    conn.commit() #commit everytime we make changes in the db

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {id} was not found ")



@app.put("/posts/{id}" , status_code=status.HTTP_201_CREATED)
def update_post(id:int, post: Post):###taken 

    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """, 
                   (post.title, 
                    post.content, post.published , id))

    updated_post = cursor.fetchone()
    conn.commit()
    
    if updated_post == None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND , details = "post with id: {id} was not found")

    return { "data " : updated_post}
