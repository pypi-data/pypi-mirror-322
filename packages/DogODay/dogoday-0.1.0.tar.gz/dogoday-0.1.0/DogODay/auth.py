from requests.auth import AuthBase

class DogAPIAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers['x-api-key'] = f'{self.token}'
        return r