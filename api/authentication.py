from django.contrib.auth.backends import BaseBackend
from api.settings import SECRET_KEY
from jwt import encode, decode
from jwt.exceptions import ExpiredSignatureError, InvalidSignatureError

from users.models import UserData


class TokenOps(BaseBackend):

    @classmethod
    def cook_token(cls, payload):
        token = encode(payload=payload, key=SECRET_KEY)
        return token

    def authenticate(self, request, token=None):
        try:
            payload = decode(jwt=token, key=SECRET_KEY, algorithms='HS256')
            _user = payload.get('username')
            user = UserData.objects.get(username=_user)
            if not user:
                pass
            else:
                return user.username
        except InvalidSignatureError:
            return False
        except ExpiredSignatureError:
            return False
