from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg2
from psycopg2.extras import RealDictCursor

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

def find_post_id(id):
    for p in my_posts:
        if p["id"] == id:
            return p

    return None


def find_post_index(id:int):
    for i , p in enumerate(my_posts):
        if p["id"] == id:
            return i
    return None

#this is a path or route 
@app.get("/")
def root():
    return {"message": "you are on the root url "}




####
@app.get("/posts")
def get_posts():
    cursor.execute("select * from posts ")
    posts =  cursor.fetchall()
   
    return {"data ": posts}
####

@app.get("/posts/latest")
def latest_post(res : Response):
    post = my_posts[len(my_posts)-1]

    if len(my_posts) == 0:
        res.status_code = status.HTTP_404_NOT_FOUND

    return {"latest post" : post}


@app.get("/posts/{id}")
def get_post(id : int, res : Response):
    
    post = find_post_id (id)

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} was not found")

    return {"detils" : post }




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
    index = find_post_index(id)

    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} does not exist")
    my_posts.pop(index) #deletion is happening here

    return Response(status_code=status.HTTP_204_NO_CONTENT)




@app.put("/posts/{id}" , status_code=status.HTTP_201_CREATED)
def update_post(id:int, post: Post):###taken 
    
    index = find_post_index(id)
    
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail= f"post with id {id} does not exist")

    post_dict = post.dict()###using here
    post_dict['id'] = id
    my_posts[index] = post_dict

    return {"data" : post_dict }

   