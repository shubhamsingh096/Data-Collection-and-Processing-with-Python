import json
import requests_with_caching                                         ##you can also use "import requests" here 

def get_movies_from_tastedive(movie_name):
    baseurl = "https://tastedive.com/api/similar"
    param_d = {}
    param_d["q"] = movie_name
    param_d["type"] = "movies"
    param_d["limit"] = "5"
    resp = requests_with_caching.get(baseurl, params= param_d)              ## you can also request data using "requests.get((baseurl, params= param_d))"
    info_movie = resp.json()
    return info_movie

def extract_movie_titles(movie_title):
    name_lst = [ x["Name"] for x in movie_title['Similar']['Results'] ]
    return name_lst

def get_related_titles(title_lst):
    rel_movie = []
    for x in title_lst:
        rel_movie.extend( extract_movie_titles(get_movies_from_tastedive(x)))
    rel_movie = list(dict.fromkeys(rel_movie))
    return rel_movie

def get_movie_data(movie_name):
    baseurl = "http://www.omdbapi.com/"
    param_d = {}
    param_d["t"] = movie_name
    param_d["r"] = "json"
    resp = requests_with_caching.get(baseurl, params= param_d)
    info_movie = resp.json()
    return info_movie

def get_movie_rating(info):
    rating_value = 0
    for x in info['Ratings']:
        if x['Source'] == 'Rotten Tomatoes':
            rating_value = int(x['Value'][:2])
    return rating_value

def get_sorted_recommendations(movie_list):
    rel_movie = get_related_titles(movie_list)
    new_dict = {}
    for i in rel_movie:
        new_dict[i] = get_movie_rating(get_movie_data(i))
    return [i[0] for i in sorted(new_dict.items(), key=lambda item: (item[1], item[0]), reverse=True)]
