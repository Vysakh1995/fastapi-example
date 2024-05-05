from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from. config import settings


SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)


sessionLocal = sessionmaker(autocommit = False,autoflush=False,bind = engine)
Base = declarative_base()


def get_db():
    db = sessionLocal()
    try:
        yield db
    finally:
        db.close()


#not used after sqlalchemy
while(True):
    try:
        conn = psycopg2.connect(host = 'localhost',dbname='fastapi',user='postgres',password = 'password',cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("DB conn successful")
        break
    except Exception as err :
        print("Failed to connect")
        print("Error :",err)
        time.sleep(2)
