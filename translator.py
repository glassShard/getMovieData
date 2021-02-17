import json
from pprint import pprint

with open('netflix-movies.json', 'r', encoding='utf-8') as films:
    movies = json.load(films)['movies']

for movie in movies:
    movie['actor'] = movie.pop('actors')

pprint(movies[0])



# with open(f'netflix-movies.json', 'w', encoding='utf-8') as f:
#     json.dump(data, f, ensure_ascii=False, indent=4)
