import os
import re
from dotenv import load_dotenv
from sqlalchemy import Column, String, Integer, Date, create_engine 
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


# Access variables in env file
load_dotenv()

# Database setup 
db_name = os.getenv('DB_name')
db_user = os.getenv('DB_user')
db_pass = os.getenv('DB_pass')
db_host = os.getenv('DB_host')
db_port = os.getenv('DB_port')

# Try to solve database path between heroku and sqlachemy.
database_path = os.getenv('DATABASE_URL')
if database_path and database_path.startswith("postgresql://"):
    database_path = database_path.replace("postgresql://","postgres://",1)

print(database_path)
# use path for local work.
#database_path = "postgresql://{}:{}@{}:{}/{}".format(
#    db_user, db_pass, db_host, db_port, db_name)

# initial DB 
db = SQLAlchemy()


# Setup and config database path and creat tables if exists 
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    # avoid leak connection
    db.init_app(app) 
    #db.drop_all() #comment this line after first run and delpoyment
    db.create_all()

# Actors table
class Actor(db.Model):
    __tablename__ = 'actors'
    id = Column(Integer, primary_key= True)
    name = Column(String)
    gender = Column(String)
    age = Column(Integer)

    def __init__(self, name, gender, age):
        self.name = name
        self.gender = gender 
        self.age = age 


    #---- CUPD functions ---# 
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()
        
    # show details  data
    def format(self):
        return{
            'id':self.id,
            'name':self.name,
            'gender':self.gender,
            'age':self.age
        }
    

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key = True)
    title = Column(String)
    release = Column(db.DateTime(), default=datetime.utcnow) 

    def __init__(self, title, release):
        self.title = title
        self.release = release

    #---- CUPD functions ---# 
    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return{
            'id':self.id,
            'title':self.title,
            'release':self.release
        }