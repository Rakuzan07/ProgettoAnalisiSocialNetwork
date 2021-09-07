import json


class User_Info:

    def __init__(self, id=None, name=None, image=None):
        super().__init__()
        self.name = name
        self.id = id
        self.image = image

    def get_name(self) -> str:
        return self.name

    def set_name(self, name: str):
        self.name = name

    def get_id(self) -> str:
        return self.id

    def set_id(self, id: str):
        self.id = id
        self.url = "https://open.spotify.com/artist/" + id

    def get_image(self) -> str:
        return self.image

    def set_image(self, image: str):
        self.image = image

    def get_as_JSON(self) -> json:
        x = {
            "_id": self.id,
            "name": self.name,
            "image": self.image
        }
        return json.dumps(x)

    def get_as_dict(self) -> dict:
        x = {
            "_id": self.id,
            "name": self.name,
            "image": self.image
        }
        return x

    def __str__(self):
        return self.name
