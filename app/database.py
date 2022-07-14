from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import settings

import psycopg2
from psycopg2.extras import RealDictCursor   # This is for returning the column names
import time


# Format of connection string we need to pass to SQLalchemmy
# 'postgresql://<username>:<password>@<ip-address/hostname>/<database-name>'
SQLALCHEMY_DATABASE_URL = f'postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}'


# The engine is what connects to the postgres database
engine = create_engine(SQLALCHEMY_DATABASE_URL)  # If you  are using sqlite, you have to pass a 2nd parameter here (look fastapi doc)

# When you want to talk to a database youhave to make of a session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define Base class
Base = declarative_base()

# Dependency, this function gets a connection/ session to our database and finally closes it
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# We don't use this anymore since we are using sqlalchemy 
# But I will keep here for documentation purposes
# while True:
#     try:
#         conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
#                                 password='', cursor_factory=RealDictCursor)
#         cursor = conn.cursor()
#         print('Database connection was successful!')
#         break
#     except Exception as error:
#         print('Connecting to database failed')
#         print('Error: ', error)
#         time.sleep(2)