#
# #establishes the connection logic, engine, and session management to communicate with that database

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


#'<>://user : password@ip/database'
SQLALCHEMY_DATABASE_URL = 'postgresql+psycopg2://postgres:bruse12345@localhost/fastapi'

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

##

#will call this fun everytime we get a req on our api endpoint
#this is a working function
def get_db():
    db  = SessionLocal()
    try:
        yield db
    finally:
        db.close()