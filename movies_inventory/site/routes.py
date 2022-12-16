from flask import Blueprint, render_template, redirect, request, url_for
from flask_login import login_required
from movies_inventory.helpers import token_required
from movies_inventory.forms import MovieSearchForm
from movies_inventory.api.routes import get_nowplaying, get_popular, get_upcoming, search_movie, saved_movies, BASEURL, API_KEY
import requests
import time

site = Blueprint('site', __name__, template_folder='site_templates')

@site.route('/', methods=['GET', 'POST'])
def home():
    popular_movies = get_popular()
    upcoming_movies = get_upcoming()
    now_playing = get_nowplaying()
    if request.method == 'POST':
        query = request.form.get('query')
        if query == "":
            return render_template('invalidsearch.html')
        else:
            search = search_movie(query)
        
        return render_template('searchresults.html', results = search)
    return render_template('index.html', popular = popular_movies, upcoming = upcoming_movies, nowplaying = now_playing)

@site.route('/profile')
@login_required
def profile():
    getmovies = saved_movies()
    if request.method == 'POST':
        query = request.form.get('query')
        if query == "":
            return render_template('invalidsearch.html')
        else:
            search = search_movie(query)
        
        return render_template('searchresults.html', results = search)
    
    return render_template('favoritemovies.html', movies = getmovies)
    

@site.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == 'POST':
        query = request.form.get('query')
        results = search_movie(query)
    return render_template('searchresults.html', results = results)

@site.route('/about')
def about():
    if request.method == 'POST':
        query = request.form.get('query')
        if query == "":
            return render_template('invalidsearch.html')
        else:
            search = search_movie(query)
        
        return render_template('searchresults.html', results = search)
    return render_template('about.html')