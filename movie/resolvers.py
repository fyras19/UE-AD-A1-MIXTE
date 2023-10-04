import json


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie


def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors
    
def add_movie(_,info,_title,_rating,_director,_id):

    with open('{}/data/movies.json'.format("."), "r") as rfile:
        data = json.load(rfile)
    movie = {"title" : _title, "rating":_rating, "director":_director, "id":_id,"actors":[]}
    data["movies"].append(movie)
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(data, wfile)    
    return movie

def get_all_movies(_,info):
    with open('{}/data/movies.json'.format("."), "r") as file:
        data = json.load(file)
    return data["movies"]


def delete_movie(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        data = json.load(rfile)
        movies = data['movies']
        new_movies = {"movies": []}
        for movie in movies:
            if movie["id"] != _id:
                new_movies["movies"].append(movie)
            else:
                movie_to_delete = movie
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(new_movies, wfile)
    return movie_to_delete


def movie_with_title(_, info, _title):
    with open("{}/data/movies.json".format("."), "r") as file:
        movies = json.load(file)["movies"]
        for movie in movies:
            if movie["title"] == _title:
                return movie
