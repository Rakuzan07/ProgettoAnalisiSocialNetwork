import json


class Artist:

    def __init__(self, id=None, name=None, genres=None, tags=None, related=None, image=None, row=None, popularity=None):
        super().__init__()
        self.name = name
        self.id = id
        self.genres = genres
        self.tags = tags
        self.related = related
        self.image = image
        self.url = "https://open.spotify.com/artist/" + self.id
        self.row = row
        self.popularity = popularity

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id
        self.url = "https://open.spotify.com/artist/" + id

    def get_genres(self) -> list:
        return self.genres

    def set_genres(self, genres: list):
        self.genres = genres

    def get_tags(self) -> list:
        return self.tags

    def set_tags(self, tags: list):
        self.tags = tags

    def get_related(self) -> list:
        return self.related

    def set_related(self, related: list):
        self.related = related

    def get_image(self) -> str:
        return self.image

    def set_image(self, image: str):
        self.image = image

    def set_row(self, row: int):
        self.row = row

    def get_row(self):
        return self.row

    def get_url(self):
        return self.url

    def get_as_JSON(self) -> json:
        x = {
            "_id": self.id,
            "name": self.name,
            "genres": self.genres,
            "tags": self.tags,
            "related": self.related,
            "image": self.image,
            "row": self.row
        }
        return json.dumps(x)

    def get_as_dict(self) -> dict:
        x = {
            "_id": self.id,
            "name": self.name,
            "genres": self.genres,
            "related": self.related,
            "image": self.image
        }
        return x

    def __str__(self):
        return self.name
