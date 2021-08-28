import pylast
import pymongo
import spotipy
from app.crawler.beans.artist import *
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyClientCredentials
from app.crawler.utils.Sha256Cipher import SHA256Cipher
import logging
from spotipy.oauth2 import SpotifyOAuth
from bottle import route, run, request

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
token_info = sp_oauth.get_access_token("")
access_token = token_info["access_token"]
sp = spotipy.Spotify(access_token)


def api_get_artist_by_id(id: str) -> Artist:
    data = spotify.artist(id)
    related = api_get_related(id)
    tag = last.get_artist(data["name"]).get_top_tags() + data["genres"]
    tags = []
    for i in tag:
        tags.append(str(i[0]))
    for i in data['genres']:
        tags.append(i)
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
    return Artist(id=data["id"], name=data["name"], genres=data["genres"], tags=tags, related=related,
                  image=img, row=-1)


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


def db_insert_artist(artist_id: str, limit: int = None):
    number_of_artists = db_artists.count_documents({})
    number_of_tags = db_tags.count_documents({})
    if limit is not None:
        to_insert = [artist_id]
        inserted = 0
        retVal = {}
        while len(to_insert) > 0 and inserted < limit:
            actual = to_insert.pop(0)
            dic = api_get_artist_by_id(actual).get_as_dict()
            dic['row'] = number_of_artists
            if db_artists.update_one({'_id': dic['_id']}, {'$setOnInsert': dic}, upsert=True).upserted_id is not None:
                number_of_artists += 1
                retVal[dic["_id"]] = dic
                for tag in dic['tags']:
                    if db_tags.update_one({'_id': tag},
                                          {'$setOnInsert': {'_id': tag, 'column': number_of_tags}},
                                          upsert=True).upserted_id is not None:
                        number_of_tags += 1
            inserted += 1
            for x in dic["related"]:
                to_insert.append(x)
        return retVal
    else:
        art = api_get_artist_by_id(artist_id).get_as_dict()
        if db_artists.update_one({'_id': art['_id']}, {'$setOnInsert': art}, upsert=True).upserted_id is not None:
            number_of_artists += 1
            for tag in art['tags']:
                if db_tags.update_one({'_id': tag},
                                      {'$setOnInsert': {'_id': tag, 'column': number_of_tags}},
                                      upsert=True).upserted_id is not None:
                    number_of_tags += 1
            return art
        else:
            return None


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


def get_row(id: str) -> int:
    data = db_artists.find_one({'_id': id})
    return data['row']


def user_exist(username: str, password: str) -> bool:
    sha_pass = SHA256Cipher(password)
    sha_pass.encrypt()
    data = db_users.find_one({'username': username, 'password': sha_pass.get_encrypted_value()})
    if data is None:
        return False
    return True


def get_artist_followed():
    build_token()
    results = sp.current_user_followed_artists()
    artists = []
    for art in results['artists']['items']:
        artist = Artist(id=art['id'], name=art['name'], genres=art['genres'], popularity=art['popularity'],
                        image=art['images'][len(art['images']) - 1]['url'])
        artists.append(artist)
    return artists


def get_users_followed():
    build_token()
    query = db_users.find({}, {'id': 1, '_id': False})
    ids = []
    for e in query:
        print(ids.append(e['id']))

    results = sp.current_user_following_users(ids)

    i = 0
    for e in results:
        if not e:
            results.pop(i)
            ids.pop(i)
        else:
            i += 1

    return ids


def build_token():
    access_token = ""

    token_info = sp_oauth.get_cached_token()

    if token_info:
        print("Found cached token!")
        access_token = token_info['access_token']
    else:
        url = request.url
        code = sp_oauth.parse_response_code(url)
        if code != url:
            print("Found Spotify auth code in Request URL! Trying to get valid access token...")
            token_info = sp_oauth.get_access_token(code)
            access_token = token_info['access_token']

    if access_token:
        print("Access token available! Trying to get user information...")
        sp = spotipy.Spotify(access_token)
        results = sp.current_user()
        return results


def store_user():
    user = build_token()
    if len(user['images']) > 0:
        image = user['images'][0]['url']
    else:
        image = None

    user_followed = get_users_followed()
    artists_followed = get_artist_followed()
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
    db_users.update_one({'id': user['id']}, {'$set': user})


def get_artists_followed_by_user(user_id):
    result = db_users.find_one({'id': user_id}, {'artists_followed': 1, '_id': 0})
    return result['artists_followed']


def get_all_artists_follwoed_by_all_users():
    result = db_users.find({}, {'artists_followed': 1, 'id': 1, '_id': 0})
    return result

