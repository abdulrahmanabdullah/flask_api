import os
import unittest 
import json
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
import app
from app import create_app 
from models import Actor, Movie, setup_db 

load_dotenv()
assistant_jwt = "Bearer {}".format(os.getenv("ASSISTENT_JWT"))
direct_jwt = "Bearer {}".format(os.getenv("DIRCT_JWT"))
prod_jwt = "Bearer {}".format(os.getenv("PROD_JWT"))


class ConnectionTest(unittest.TestCase):
   # setup database path and config.
   def setUp(self):
       self.app = create_app()
       app.testing = True
       self.client = self.app.test_client 
       self.datebase_path = os.getenv("SQLAlchemy_DATABASE_URL")
       setup_db(self.app, self.datebase_path)
       with self.app.app_context():
           self.db = SQLAlchemy()
           self.db.init_app(self.app)
           self.db.create_all()
   #test get actors
   def test_get_actors(self):
       res = self.client().get('/actors')
       result = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertEqual(result['success'],True)
       self.assertTrue(result['actors'])

   #detele actors test 
   def test_delete_actors(self):
       res = self.client().delete('/actors/12',
          headers={'Authorization':(assistant_jwt)})
       result = json.loads(res.data)
       actor = Actor.query.filter(Actor.id == 12).one_or_none()
       self.assertEqual(res.status_code,200)
       self.assertEqual(result['success'],True)
       self.assertTrue(result['delete'])
       self.assertEqual(actor,None)

   # Create new actor test
   def test_post_actor(self):
       self.new_actor = {
          "name":"Actor for test",
          "gender":"Male",
          "age":35
          }
       res = self.client().post('/actors', json=self.new_actor, headers={'Authorization':(direct_jwt)})
       result = json.loads(res.data)
       self.assertTrue(result['success'])
       self.assertTrue(len(result['actor']) == 1)

    #Update actor test
   def test_update_actor(self):
       self.new_actor = {
          "name":"Actor update from test",
          "gender":"Male",
          "age":35
          }
       res = self.client().patch('/actors/7', json=self.new_actor, headers={'Authorization':(prod_jwt)})
       result = json.loads(res.data)
       self.assertTrue(result['success'])
       self.assertTrue(len(result['actor']) == 1)

   #Test throw 422 when add actor not allowed 
   def test_422_post_actor(self):
       res = self.client().post('/actors', json={"name":None},
            headers={'Authorization':(direct_jwt)})
       self.assertEqual(res.status_code,422)

   #Movies Test 
   def test_get_movies(self):
       res = self.client().get('/movies')
       result = json.loads(res.data)
       self.assertEqual(res.status_code,200)
       self.assertEqual(result['success'],True)
       self.assertTrue(result['movies'])
    
   #update movie
   def test_post_movies(self):
       self.new_movie = {
          "title":"Movie for test"
          }
       res = self.client().post('/movies', json=self.new_movie, headers={'Authorization':(direct_jwt)})
       result = json.loads(res.data)
       self.assertTrue(result['success'])
       self.assertTrue(len(result['movie']) == 1)

   #Delete movie
   def test_delete_movies(self):
       res = self.client().delete('/movies/3', headers={'Authorization':(assistant_jwt)})
       result = json.loads(res.data)
       movie = Movie.query.filter(Movie.id == 3).one_or_none()
       self.assertEqual(res.status_code,200)
       self.assertEqual(result['success'],True)
       self.assertTrue(result['delete'])
       self.assertEqual(movie,None)


   #Update movie test
   def test_update_movie(self):
       self.new_movie = {
          "title":"Movie update from test"
          }
       res = self.client().patch('/movies/7', json=self.new_movie, headers={'Authorization':(prod_jwt)})
       result = json.loads(res.data)
       self.assertTrue(result['success'])
       self.assertTrue(len(result['movie']) == 1)


   #test movie bad request
   def test_404_movie(self):
       res = self.client().patch('/movies/40', json={"ttle":None}, headers={'Authorization':(prod_jwt)})
       self.assertEqual(res.status_code ,400)

   #test movie bad request
   def test_422_movie(self):
       res = self.client().delete('/movies/40', json={"ttle":None}, headers={'Authorization':(prod_jwt)})
       self.assertEqual(res.status_code ,422)
if __name__ == '__main__':
    unittest.main()