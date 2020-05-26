import requests


api_url = "https://sv443.net/jokeapi/v2/joke/"


def get_random(genre="Any", ):
    resp = requests.get(api_url + genre)
    joke = resp.json()
    try:
        if joke["type"] == "twopart":
            return "\n".join([joke["setup"], joke["delivery"]])
        else:
            return joke["joke"]
    except KeyError:
        return f"Unable to get genre {genre.lower()}!"
