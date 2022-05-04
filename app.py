from crypt import methods
import os
import json
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from functools import wraps
from datetime import date
from models import setup_db, Actor, Movie
from urllib.request import urlopen
from auth import requires_auth, get_token_auth_header, AuthError




def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  CORS(app)

  @app.route('/', methods=["GET"])
  def index():
      return "<h2> Welcome to last project </h2>"

  # -- Actors Region ----- #
  @app.route('/actors', methods=['GET'])
  def get_actors():
      actors = Actor.query.all()

      if(len(actors) == 0):
          abort(404, "No actors to found !!")

      return jsonify({
          "success":True,
          "actors":[actor.format() for actor in actors]
      }),200


# --- POST NEW ACTORS Done--- #
  @app.route('/actors', methods=['POST'])
  @requires_auth('post:actors')
  def add_actor(jwt):
      body = request.json
      name = body.get('name')
      gender = body.get('gender')
      age = body.get('age')
      
      if any(arg is None for arg in [name, gender, age]) or '' in [name, gender,age]:
          abort(422, "name, gender and age are require")

      actor = Actor(name, gender, age)
      actor.insert()

      return jsonify({
        'success': True,
        'actor':[Actor.query.get(actor.id).format()]
      })

#--- UPDATE Actor Done ---# 
  @app.route('/actors/<int:actor_id>', methods=['PATCH'])
  @requires_auth("patch:actors")
  def update_actor(jwt, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          # if actor not exists 
          if actor is None:
              abort(404, "Not found actor")

          # figurout what's change or keeps old date 
          body = request.json
          name = body.get('name', None) 
          if name is not None:
              actor.name = json.dumps(body.get('name',actor.name))
          gender = body.get('gender', None)
          if gender is not None:
              actor.gender = json.dumps(body.get('gender',actor.gender))
          age = body.get('age', None)
          if age is not None:
              actor.age = json.dumps(body.get('age',actor.age))
        # Update actor 
          actor.update()
          return jsonify({
            "success": True,
            "actor":[Actor.query.get(actor_id).format()]
            })
      except Exception as exp:
          print(f'some error ocurred with patch {exp}')
          abort(400)

#---- DELETE ACTOR Done----# 
  @app.route('/actors/<int:actor_id>', methods=['DELETE'])
  @requires_auth("delete:actors")
  def delete_actor(jwt, actor_id):
      try:
          actor = Actor.query.filter(Actor.id == actor_id).one_or_none()
          if actor is None:
              abort(404)
          actor.delete()
          return jsonify({"success":True,"delete":actor_id}),200
      except Exception as exp:
          print(f'some error ocurred in delete {exp}')


### ----------- End Actors Region --------------###

### ----------- Movies Region --------------###
#--- Get movies Done---#
  @app.route('/movies', methods=['GET'])
  def get_movies():
      movies = Movie.query.all()
      return jsonify({
          "success": True,
          "movies":[movie.format() for movie in movies]
      })

# --- POST NEW Movie --- #
  @app.route('/movies', methods=['POST'])
  @requires_auth("post:movies")
  def add_movie(jwt):
      body = request.json
      title = body.get('title',None)
      #release = date.now().strftime("%d-%m-%y")
      release = body.get("release",None)

      movie = Movie(title, release)
      movie.insert()

      return jsonify({
          'success': True,
          'movie':[Movie.query.get(movie.id).format()]
      })

  #--- UPDATE Movie ---# 
  @app.route('/movies/<int:movie_id>', methods=['PATCH'])
  @requires_auth("patch:movies")
  def update_movie(jwt, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
          # if actor not exists 
          if movie is None:
              abort(400, '400 bad request')
          body = request.json
          #Check values befor update
          title = body.get('title',None)
          if title is not None:
              movie.title = json.dumps(body.get('title',movie.title))
          release = body.get('release',None)
          if release is not None:
              movie.release = json.dumps(body.get("release",movie.release))
        
        # Update movie when everythings work fine. 
          movie.update()
          return jsonify({
              "success": True,
              "movie":[Movie.query.get(movie_id).format()]
          })
      except Exception as exp:
          print(f'some error ocurred with patch {exp}')
          abort(400)


  #---- DELETE ACTOR ----# 
  @app.route('/movies/<int:movie_id>', methods=['DELETE'])
  @requires_auth("delete:movies")
  def delete_movie(jwt, movie_id):
      try:
          movie = Movie.query.filter(Movie.id == movie_id).one_or_none()
          if movie is None:
              abort(404)
          movie.delete()
          return jsonify({"success":True,"delete":movie_id}),200
      except Exception as exp:
          print(f'some error ocurred in delete {exp}')
          abort(422)

###-------  End Movie Region ------------###

###-------  Error Handler Region ------------###
  #Page not found
  @app.errorhandler(404)
  def not_found(error):
      return jsonify({
          'success':False,
          'error':404,
          'message':'not found'
      }),404

  #Unprocessable
  @app.errorhandler(422)
  def unprocessable(error):
      return jsonify({
          'success':False,
          'error':422,
          'message':'unprocessable'
      }),422

  #Interal server error
  @app.errorhandler(500)
  def internal_server_error(error):
      return jsonify({
          'success':False,
          'error':500,
          'message':'internal server error {}'.format(error)
      }),500

  #Method Not allowed
  @app.errorhandler(405)
  def method_not_allowed(error):
      return jsonify({
          'success':False,
          'error':405,
          'message':'Method not allowed {}'.format(error)
      }),405

  #Auth error
  @app.errorhandler(AuthError)
  def auth_err(error):
      return jsonify({
          'success':False,
          'error':error.status_code,
          'message':'unauthorized '.format(error.error)
      }),error.status_code
  
  return app


app = create_app()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)