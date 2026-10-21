from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional

app = FastAPI() # ' app ' is the instance 

#class to create post
class Post(BaseModel):
    title : str
    content : str
    pubished  : bool = True #defaults to true 
    rating : Optional[int] = None

#this is a path or route 
@app.get("/")
def root():
    return {"message": "you are on the root url "}



@app.get("/posts")
def get_posts():
    return {"data ": " this is a post"}



@app.post("/createposts")
def create_posts(new_post : Post):
     
    print(new_post.rating)    
    print(new_post.dict())    
    return {"data" : new_post.dict() }
#string title , string content 

   