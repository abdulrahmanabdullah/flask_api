# Flask api with authentcation 
The Project API models a company that is responsible for creating movies and managing/assigning actors to those movies. This api is responsible for checking permissions and handling CRUD for an Actor and Movie model/
 ## Getting started
 **Install Dependencies**
 **python3**
 Follow instructions to install the latest version of python for your platform in the [python docs](https://www.python.org/downloads/)

 **virtual env**
 We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [simple way](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)

 **PIP Dependencies**
 Once you have your virtual environment setup and running, install dependencies by naviging to the root directory of this project and running:
 ```pip install -r requirements.txt```

 This will install all of the required packages we selected within the requirements.txt file.

### What we used:
- Flask  is a lightweight backend microservices framework.
- SQLALchemy is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 
- Flask-Cors
- jose.
---
### Running the server
You can run app with two ways, with env mode or export flask variables in your terminal 
First way:
```source env/bin/activate```
Make sure your installed virtual env.
The second way:

`export FLASK_APP=app.py`
`export FLASK_ENV=development`
`flask run`


--- 
API Ref
---
**Error handler**
- 400:Bad Request
- 400: Permissions were not included in the JWT.
- 401: Authorization header is expected.
- 401: Token expired.
- 403: Permission denied.
- 404: Resource Not Found.

**Endpoints**
`Get /actors` to get all actors in db
`Get /movies` to get all movies in db
`Post /actors` to post new actors, here you need JWT authentcation.
`Post /movies` post new movie with credationls
`patch /actors/actor_id` to update actor's data with id in database
`patch /movies/movie_id` same here with actors
`delete /actors/actor_id`
`delete /movies/movie_id`

### example:
```curl http://localhost:8080/actors```
 
response:
```json
{
    "actor": [
        {
            "age": 34,
            "gender": "Male",
            "id": 1,
            "name": "First actor"
        }
    ],
    "success": true
}
```
### example for delete:
```curl -X DELETE http://localhost:8080/movies/1```
response:

```json
{
    "delete": 1,
    "success": true
}
```
### Live Demo
[here](https://capstone-project-xy.herokuapp.com/) 

**developement by Abdulrahman**