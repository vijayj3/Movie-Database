
from movie import MovieAPI

example = "which are the movies Tom Cruise acted in 2000"

movieapi = MovieAPI(example)

print movieapi.parser()