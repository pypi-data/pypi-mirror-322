from django.conf import settings


HASH_SECRET_KEY = getattr(settings, "HASH_SECRET_KEY", "cgDywMThqhuxBOEEnjhfgeFGxBJZJJLa6Xc3WpqKn")
TAMARA_EXTENSION_URL = getattr(settings, "TAMARA_EXTENSION_URL", None)
