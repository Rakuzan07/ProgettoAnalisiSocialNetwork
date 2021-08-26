import pylast
import spotipy
from SpotiGraph.crawler.artist import *
from pymongo import MongoClient
from spotipy.oauth2 import SpotifyClientCredentials

# credentials


client = MongoClient("mongodb://localhost:27017/")
db = client["spotigraph"]
db_artists = db['artists']
db_tags = db['tags']

LAST_KEY = "5f52c83a8ed0440af21be4b5514262ae"
LAST_SECRET = "b9f3f2c9d1a855c6dd0508be9208f5e4"
SPOTIFY_KEY = "8dceec3b5bec4d618979142ee304feb9"
SPOTIFY_SECRET = "8f9afd96f99d49b38946b18ea05bd8d6"
# initialization of api
last = pylast.LastFMNetwork(api_key=LAST_KEY, api_secret=LAST_SECRET)
client_credentials_manager = SpotifyClientCredentials(SPOTIFY_KEY, SPOTIFY_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
spotify.trace = False


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
