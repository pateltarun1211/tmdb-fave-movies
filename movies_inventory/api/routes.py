from flask import Blueprint, request, jsonify, render_template, url_for, current_app, redirect, request
import requests
import os
from movies_inventory.helpers import token_required
from movies_inventory.forms import MovieSearchForm
from movies_inventory.models import db, SaveMovie, movie_schema, movies_schema, Movie
from datetime import datetime


api = Blueprint('api', __name__, url_prefix='/api')

@api.route('/movies', methods = ['POST'])
@token_required
def save_movie(token):
    title = request.form.get('title')
    tmdb_id = request.form.get('tmdb_id')
    overview = request.form.get('overview')
    poster = request.form.get('poster')

    
    movie = SaveMovie(title, tmdb_id, overview, poster, user_token=token)
    
    db.session.add(movie)
    db.session.commit()
    
    return redirect(url_for("site.profile"))

@api.route('/movies', methods = ['GET'])
@token_required
def saved_movies(token):
    movies = SaveMovie.query.filter_by(user_token=token).all()
    response = movies_schema.dump(movies)
    return response

@api.route('/movies/<id>', methods = ['GET'])
@token_required
def get_saved_movie(token, id):
    movie = SaveMovie.query.get(id)
    response = movie_schema.dump(movie)
    return jsonify(response)

@api.route('movies/<id>', methods = ['POST', 'PUT'])
@token_required
def update_movie(token, id):
    movie = SaveMovie.query.get(id)
    movie.title = request.json['title']
    movie.tmdb_id = request.json['tmdb_id']
    movie.overview = request.json['overview']
    movie.poster = request.json['poster']
    db.session.commit()
    response = movie_schema.dump(movie)
    return jsonify(response)

@api.route('/movies/delete', methods = ['POST'])
@token_required
def delete_movie(token):
    tmdb_id = request.form.get('tmdb_id')
    movie = SaveMovie.query.filter_by(tmdb_id = tmdb_id).first()
    db.session.delete(movie)
    db.session.commit()
    return redirect(url_for("site.profile"))


# ----------- TMDB API calls -------------
API_KEY = os.environ.get('API_KEY')
BASEURL = "https://api.themoviedb.org/3"

def get_popular():
    data = requests.get(f"{BASEURL}/movie/popular?api_key={API_KEY}").json()
    if data['results']:
        popular_data = process_results(data['results'])
        
    return popular_data

def get_nowplaying():
    data = requests.get(f"{BASEURL}/movie/now_playing?api_key={API_KEY}").json()
    if data['results']:
        nowplaying_data = process_results(data['results'])
    return nowplaying_data

def get_upcoming():
    data = requests.get(f"{BASEURL}/movie/upcoming?api_key={API_KEY}").json()
    if data['results']:
        upcoming_data = process_results(data['results'])
    return upcoming_data


def search_movie(query):
    data = requests.get(f"{BASEURL}/search/movie?api_key={API_KEY}&language=en-US&query={query}&page=1&include_adult=false").json()
    if data['results']:
        search_data = process_results(data['results'])
    return search_data

def get_movie(id):
    data = requests.get(f"{BASEURL}/movie/{id}?api_key={API_KEY}&language=en-US").json()
    if data:
        movie_data = process_results(data)
    return movie_data
    
def process_results(movie_list):
    movie_results = []
    for movie_item in movie_list:
        id = movie_item.get('id')
        title = movie_item.get('original_title')
        overview = movie_item.get('overview')
        poster = movie_item.get('poster_path')
        
        if poster:
            movie_object = Movie(id, title, overview, poster)
            movie_results.append(movie_object)
        
    return movie_results

