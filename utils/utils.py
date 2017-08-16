from django.conf import settings
from itsdangerous import URLSafeTimedSerializer, BadTimeSignature, SignatureExpired


def encode_URLSafeTimedToken(obj, salt=None):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    encoded = s.dumps(obj, salt=salt)
    return encoded


def decode_URLSafeTimedToken(encoded, max_age=None, salt=None):
    s = URLSafeTimedSerializer(settings.SECRET_KEY)
    decoded = s.loads(encoded, max_age=max_age, salt=salt)
    return decoded


def send_email(to_user="to", ):
    from_user = settings.DEFAULT_FROM_EMAIL
