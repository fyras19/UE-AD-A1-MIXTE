# REST API
from flask import Flask, render_template, request, jsonify, make_response
import requests
import json
from werkzeug.exceptions import NotFound

# CALLING gRPC requests
#import grpc
#from concurrent import futures
#import booking_pb2
#import booking_pb2_grpc
#import movie_pb2
#import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
   users = json.load(jsf)["users"]



#GET Methods
@app.route("/movies", methods=['GET'])
def get_movies():
   body = """
   {
   get_all_movies {
      id
      title
      rating
   }
   }
   """
   response = requests.post(f"http://{HOST}:3001/graphql",json={'query': body})
   return make_response(response.json(), response.status_code)

@app.route("/movies/<title>", methods=['GET'])
def get_movie_wtitle(title):
   body = """
   {
   movie_with_title(_title: 
   """
   body += '"'+title+'"'
   body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
   response = requests.post(f"http://{HOST}:3001/graphql",json={'query': body})
   return make_response(response.json(), response.status_code)

@app.route("/movie_id/<id>", methods=['GET'])
def get_movie_wid(id):
   body = """
   {
   movie_with_id(_id: 
   """
   body += '"' + id + '"'
   body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
   response = requests.post(f"http://{HOST}:3001/graphql",json={'query': body})
   return make_response(response.json(), response.status_code)

#POST Methods
@app.route("/movie_id/<id>", methods=['POST'])
def add_movie(id):
   req = request.get_json()
   title,rating,director = req['title'],req['rating'],req['director']
   body = """mutation
   {
   add_movie(_id: 
   """
   body += '"'+id+'",'
   body += '_title:"'+title+'",'
   body += '_rating:"'+str(rating)+'",'
   body += '_director:"'+director+'"'
   body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
   response = requests.post(f"http://{HOST}:3001/graphql",json={'query': body})
   return make_response(response.json(), response.status_code)

@app.route("/movie_id/<id>/<rate>", methods=['POST'])
def update_movie_rate(id,rate):
   body = """mutation
   {
   update_movie_rate(_id: 
   """
   body += '"'+id+'",'
   body += '_rate:"'+rate+'"'
   body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
   response = requests.post(f"http://{HOST}:3001/graphql",json={'query': body})
   return make_response(response.json(), response.status_code)

@app.route("/movie_id/<id>", methods=['DELETE'])
def del_movie(id):
   body = """mutation
   {
   delete_movie(_id: 
   """
   body += '"'+id+'"'
   body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
   response = requests.post(f"http://{HOST}:3001/graphql",json={'query': body})
   return make_response(response.json(), response.status_code)




if __name__ == "__main__":
   print("Server running in port %s"%(PORT))
   app.run(host=HOST, port=PORT)


