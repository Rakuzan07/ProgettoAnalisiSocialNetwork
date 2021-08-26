
def __init__(self, username: str, password: str):
    super().__init__()
    self.username = username
    self.password = password
    self.followed = []
    self.artist_followed = []

