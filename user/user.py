# REST API
import json

# CALLING gRPC requests
import grpc
import requests
from flask import Flask, request, jsonify, make_response

import booking_pb2
import booking_pb2_grpc

# import movie_pb2
# import movie_pb2_grpc

# CALLING GraphQL requests
# todo to complete

app = Flask(__name__)

PORT = 3004
HOST = '0.0.0.0'

with open('{}/data/users.json'.format("."), "r") as jsf:
    users = json.load(jsf)["users"]


@app.route("/users", methods=['GET'])
def get_json():
    return make_response(jsonify({"users": users}), 200)


@app.route("/users/<userid>", methods=['GET'])
def get_user_byid(userid):
    for user in users:
        if str(user["id"]) == str(userid):
            return make_response(jsonify(user), 200)
    return make_response(jsonify({"error": "User ID not found"}), 400)


# GET Methods
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
    response = requests.post(f"http://{HOST}:3001/graphql", json={'query': body})
    return make_response(jsonify({"movies": response.json()["data"]["get_all_movies"]}), response.status_code)


@app.route("/movies/<title>", methods=['GET'])
def get_movie_wtitle(title):
    body = """
   {
   movie_with_title(_title: 
   """
    body += '"' + title + '"'
    body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
    response = requests.post(f"http://{HOST}:3001/graphql", json={'query': body})
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
    response = requests.post(f"http://{HOST}:3001/graphql", json={'query': body})
    return make_response(response.json(), response.status_code)


# POST Methods
@app.route("/movie_id/<id>", methods=['POST'])
def add_movie(id):
    req = request.get_json()
    title, rating, director = req['title'], req['rating'], req['director']
    body = """mutation
   {
   add_movie(_id: 
   """
    body += '"' + id + '",'
    body += '_title:"' + title + '",'
    body += '_rating:"' + str(rating) + '",'
    body += '_director:"' + director + '"'
    body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
    response = requests.post(f"http://{HOST}:3001/graphql", json={'query': body})
    return make_response(response.json(), response.status_code)


@app.route("/movie_id/<id>/<rate>", methods=['POST'])
def update_movie_rate(id, rate):
    body = """mutation
   {
   update_movie_rate(_id: 
   """
    body += '"' + id + '",'
    body += '_rate:"' + rate + '"'
    body += """
   ){
      id
      title
      rating
      director
   }
   }
   """
    response = requests.post(f"http://{HOST}:3001/graphql", json={'query': body})
    return make_response(response.json(), response.status_code)


@app.route("/movie_id/<id>", methods=['DELETE'])
def del_movie(id):
    body = """mutation
   {
   delete_movie(_id: 
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
    response = requests.post(f"http://{HOST}:3001/graphql", json={'query': body})
    return make_response(response.json(), response.status_code)


@app.route("/bookings/<userid>", methods=['GET'])
def get_booking_for_user(userid):
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        user_id = booking_pb2.UsedID(userid=userid)
        bookings_by_user = stub.GetBookingsByUserID(user_id)
        if bookings_by_user.userid != "":
            dates = []
            for dateSlot in bookings_by_user.dates:
                dates.append({"date": dateSlot.date, "movies": []})
                for movie in dateSlot.movies:
                    dates[-1]["movies"].append(movie)
            return make_response(jsonify({"userid": userid, "dates": dates}), 200)
        return make_response(jsonify({"error": "user not found"}), 400)


@app.route("/<userid>/movies", methods=['GET'])
def get_movies_for_user(userid):
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        user_id = booking_pb2.UsedID(userid=userid)
        bookings_by_user = stub.GetBookingsByUserID(user_id)
        movie_ids = set()
        if bookings_by_user.userid != "":
            for dateSlot in bookings_by_user.dates:
                for movie in dateSlot.movies:
                    movie_ids.add(movie)
            movies = []
            for movie_id in movie_ids:
                movie_request = get_movie_wid(movie_id)
                if movie_request.status_code == 200:
                    movies.append(movie_request.get_json()["data"]["movie_with_id"])
            return make_response(jsonify({"movies": movies}), 200)
    return make_response(jsonify({"error": "No bookings found for this user"}), 400)


@app.route("/bookings/<userid>", methods=['POST'])
def add_booking_by_user(userid):
    req = request.get_json()
    date, movie_id = req["date"], req["movie"]
    with grpc.insecure_channel('localhost:3003') as channel:
        stub = booking_pb2_grpc.BookingStub(channel)
        user_booking = booking_pb2.UserBooking(userid=userid, date=date, movieid=movie_id)
        booking_info = stub.AddBooking(user_booking)
        dates = []
        for date in booking_info.dates:
            dates.append(date)
        response = {"userid": userid, "dates": dates}
        return make_response(jsonify(response), 200)
    return make_response(jsonify({"error": "Could not add booking for user"}), 400)


if __name__ == "__main__":
    print("Server running in port %s" % PORT)
    app.run(host=HOST, port=PORT)
