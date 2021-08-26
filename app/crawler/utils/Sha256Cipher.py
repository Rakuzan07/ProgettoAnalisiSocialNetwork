import hashlib


class SHA256Cipher(object):

    def __init__(self, value : str):
        self.value = value
        self.encrypted = None

    def encrypt(self):
      self.encrypted = hashlib.sha256(self.value.encode('utf-8')).hexdigest()

    def get_encrypted_value(self):
        return self.encrypted

    def __eq__(self, other):
        return self.value==other

