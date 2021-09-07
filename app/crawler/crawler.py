import base64

import pylast
import pymongo
import spotipy
from app.crawler.beans.artist import *
from app.crawler.beans.user_info import *
from spotipy.oauth2 import SpotifyClientCredentials
from app.crawler.utils.Sha256Cipher import SHA256Cipher
from spotipy.oauth2 import SpotifyOAuth
import requests

# credentials


client = pymongo.MongoClient(
    "mongodb+srv://lolloborag:ProgettoSN@Cluster0.vtzyc.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
db = client["database"]
db_artists = db['artists']
db_tags = db['tags']
db_users = db['users']

LAST_KEY = "5f52c83a8ed0440af21be4b5514262ae"
LAST_SECRET = "b9f3f2c9d1a855c6dd0508be9208f5e4"
SPOTIFY_KEY = "7dfcff2789584927a64d6685f9f0d614"
SPOTIFY_SECRET = "62d6f5da88564005971ba8b2897de968"
# initialization of api
last = pylast.LastFMNetwork(api_key=LAST_KEY, api_secret=LAST_SECRET)
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_KEY, SPOTIFY_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
spotify.trace = False
scope = ['user-follow-modify', 'user-follow-read']
sp_oauth = SpotifyOAuth(scope=scope, client_id=SPOTIFY_KEY, client_secret=SPOTIFY_SECRET,
                        redirect_uri='http://localhost:8000/authenticate')


# inizializzo sp
#token_info = sp_oauth.get_access_token(code="", check_cache=False)
#access_token = token_info["access_token"]
#sp = spotipy.Spotify(access_token)


def api_get_artist_by_name(name: str) -> Artist:
    id = api_get_id(name)
    return api_get_artist_by_id(id)


def api_get_related(id: str) -> list:
    data = spotify.artist_related_artists(id)
    related = []
    for i in range(len(data["artists"])):
        related.append(data["artists"][i]["id"])
    return related


def api_get_id(name: str) -> str:
    data = spotify.search(q=name, limit=10, type='artist')
    index = 0
    max_pop = 0
    for i in range(len(data['artists']['items'])):
        if data['artists']['items'][i]['popularity'] > max_pop:
            max_pop = data['artists']['items'][i]['popularity']
            index = i
    return data['artists']['items'][index]['id']


def get_recently_played(token, limit: int = None):
    if limit is None:
        limit = 10
    spo = spotipy.Spotify(auth=token)
    results = spo.current_user_recently_played(limit)
    data = []
    for i in range(len(results['items'])):
        artists = []
        for j in range(len(results['items'][i]['track']['artists'])):
            artists.append({'id': results['items'][i]['track']['artists'][j]['id'],
                            'name': results['items'][i]['track']['artists'][j]['name']})
        track = {
            'id': results['items'][i]['track']['id'],
            'name': results['items'][i]['track']['name'],
            'artists': artists
        }
        data.append(track)
    return data


def db_get_artist_by_id(id: str):
    a = db_artists.find_one({"_id": id})
    if a is not None:
        retVal = Artist(a["_id"], a["name"], a["genres"], a["tags"], a["related"], a["image"], a['row'])
        return retVal
    else:
        return None


def db_insert_artist(artist_id: str):
    art = api_get_artist_by_id(artist_id).get_as_dict()
    db_artists.update_one({'_id': art['_id']}, {'$setOnInsert': art}, upsert=True)



def db_get_tag_by_artist_names(names: list) -> list:
    filters = []
    for name in names:
        filters.append({'name': name})
    rec = db_artists.find({'$or': filters}, {'tags': 1, '_id': 0})
    tags = []
    for record in rec:
        tags.append(record['tags'])
    return tags


def get_tag_column(tag: str) -> int:
    return db_tags.find_one({'_id': tag})['column']


def get_artist_by_id(id: str) -> Artist:
    art = db_get_artist_by_id(id)
    if art is None:
        art = api_get_artist_by_id(id)
        db_insert_artist(id)
    return art


def get_artist_by_name(name: str) -> Artist:
    id = api_get_id(name)
    return get_artist_by_id(id)


def get_all_artists_as_dict() -> dict:
    art = list(db_artists.find().sort('row', 1))
    retVal = {}
    for x in art:
        retVal[x["_id"]] = {"_id": x["_id"],
                            "name": x["name"],
                            "genres": x["genres"],
                            "related": x["related"],
                            "tags": x["tags"],
                            "image": x['image'],
                            "url": "https://open.spotify.com/artist/" + x["_id"],
                            "row": x["row"]}
    return {'artists': retVal, 'count': len(art)}


def get_tags(id: str) -> list:
    artist = get_artist_by_id(id)
    return artist.get_tags()


def get_all_tags() -> dict:
    data = list(db_tags.find({}))
    ret_val = {}
    count = len(data)
    for i in data:
        ret_val[i['_id']] = {'_id': i['_id'], 'column': i['column']}
    return {'tags': ret_val, 'count': count}


def get_artists_by_row() -> dict:
    data = db_artists.find({})
    ret_val = {}
    for x in data:
        ret_val[x['row']] = {"_id": x["_id"],
                             "name": x["name"],
                             "genres": x["genres"],
                             "related": x["related"],
                             "tags": x["tags"],
                             "image": x['image'],
                             "url": "https://open.spotify.com/artist/" + x["_id"],
                             "row": x["row"]}
    return ret_val



def user_exist(username: str, password: str) -> bool:
    sha_pass = SHA256Cipher(password)
    sha_pass.encrypt()
    data = db_users.find_one({'username': username, 'password': sha_pass.get_encrypted_value()})
    if data is None:
        return False
    return True


def get_artist_followed(token):
    access_token = refresh_token(token)['access_token']
    sp = spotipy.Spotify(access_token)
    results = sp.current_user_followed_artists()
    artists = []
    for art in results['artists']['items']:
        artist = Artist(id=art['id'], name=art['name'], genres=art['genres'], popularity=art['popularity'],
                        image=art['images'][len(art['images']) - 1]['url'])
        artists.append(artist)
    return artists


def db_user(user_id):
    return db_users.find_one({'id': user_id})


def get_users_followed(token):
    access_token = refresh_token(token)['access_token']
    sp = spotipy.Spotify(access_token)
    query = db_users.find({}, {'id': 1, '_id': False})
    ids = []
    for e in query:
        ids.append(e['id'])

    results = sp.current_user_following_users(ids)

    i = 0
    while i < len(results):
        if not results[i]:
            results.pop(i)
            ids.pop(i)
        else:
            i += 1

    return ids


def store_user(token):
    access_token = refresh_token(token)['access_token']
    sp = spotipy.Spotify(access_token)
    user = sp.current_user()
    if len(user['images']) > 0:
        image = user['images'][0]['url']
    else:
        image = None

    user_followed = get_users_followed(token)
    artists_followed = get_artist_followed(token)
    for artist in artists_followed:
        db_insert_artist(artist.id)
    art_id = []
    for artist in artists_followed:
        art_id.append(artist.id)
    user = {
        'name': user['display_name'],
        'id': user['id'],
        'image': image,
        'users_followed': user_followed,
        'artists_followed': art_id
    }
    db_users.update_one({'id': user['id']}, {'$set': user}, upsert=True)


def get_user_info(token):
    access_token = refresh_token(token)['access_token']
    sp = spotipy.Spotify(access_token)
    return sp.current_user()


def get_artists_followed_by_user(user_id):
    result = db_users.find_one({'id': user_id}, {'artists_followed': 1, '_id': 0})
    return result['artists_followed']


def get_all_artists_followed_by_all_users():
    result = db_users.find({}, {'artists_followed': 1, '_id': 0, 'genres': 1, 'image': 1, 'name': 1, 'tags': 1, 'id': 1})
    ret_val = {}
    for user in result:
        art = []
        artist_followed = user['artists_followed']
        artists = db_artists.find({'_id': {'$in': artist_followed}})
        for e in artists:
            art.append(Artist(id=e['_id'], genres=e['genres'], name=e['name'], related=e['related'], image=e['image']))
        ret_val[user['id']] = art

    return ret_val


def get_all_users_followed_by_all_users():
    result = db_users.find({}, {'users_followed': 1, 'id': 1, '_id': 0})
    return result

def users_connectivity():
    result = db_users.find({}, {'users_followed': 1, '_id': 0, 'id': 1, 'image': 1, 'name': 1})
    ret_val = {}
    for user in result:
        users = []
        users_followed = user['users_followed']
        #end = db_artists.find({'_id': {'$in': artist_followed}})

        for end_user in result:
            for index in range(len(users_followed)):
                if users_followed[index]==end_user['id']:
                    users.append(User_Info(id=end_user['id'], name=end_user['name'], image=end_user['image']))
        ret_val[user['name']] = users
    return ret_val

def user_info():
    result = db_users.find({}, {'users_followed': 1, '_id': 0, 'id': 1, 'image': 1, 'name': 1})
    return result

def get_artist_inf_from_db(id: str):
    result = db_artists.find_one({'_id': id})
    artist = Artist(id=result['_id'], name=result['name'], genres=result['genres'], related=result['related'],
                    image=result['image'])


def get_token(code):
    """
    Method that must be used only the first time during the login
    :param code: Code provided during authorize operation
    :return: json containing access_token, refresh_token
    """
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    payload = {
        "redirect_uri": 'http://localhost:8000/authenticate',
        "code": code,
        "grant_type": "authorization_code",
    }
    s = SPOTIFY_KEY + ":" + SPOTIFY_SECRET
    ascii = s.encode('ascii')
    base64_bytes = base64.b64encode(ascii)
    auth_header = base64_bytes.decode('ascii')
    headers = {"Authorization": "Basic %s" % auth_header}

    response = requests.post(
        OAUTH_TOKEN_URL,
        data=payload,
        headers=headers
    )

    return response.json()


def refresh_token(code):
    """
        Method that must be used every time you use the spotipy api
        :param code: refresh token provided during the get_token operations
        :return: json containing access_token, refresh_token
    """
    OAUTH_TOKEN_URL = "https://accounts.spotify.com/api/token"
    payload = {
        "redirect_uri": 'http://localhost:8000/authenticate',
        "refresh_token": code,
        "grant_type": "refresh_token",
    }
    s = SPOTIFY_KEY + ":" + SPOTIFY_SECRET
    ascii = s.encode('ascii')
    base64_bytes = base64.b64encode(ascii)
    auth_header = base64_bytes.decode('ascii')
    headers = {"Authorization": "Basic %s" % auth_header}

    response = requests.post(
        OAUTH_TOKEN_URL,
        data=payload,
        headers=headers
    )

    return response.json()


def api_get_artist_by_id(id: str) -> Artist:
    data = spotify.artist(id)
    related = api_get_related(id)
    try:
        img = data['images'][2]['url']
    except IndexError:
        try:
            img = data['images'][1]['url']
        except IndexError:
            try:
                img = data['images'][0]['url']
            except IndexError:
                img = None
    return Artist(id=data["id"], name=data["name"], genres=data["genres"], related=related, image=img)



#get_all_artists_followed_by_all_users()
print(user_info())