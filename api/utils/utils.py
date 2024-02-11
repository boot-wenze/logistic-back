"""Utils module"""

import hashlib
import pytz


def set_timezone():
    """Timezone"""
    return pytz.timezone("Africa/Kinshasa")


def hash_password(password: str = None) -> str:
    """Hashing system"""
    return hashlib.md5(str(password).encode()).hexdigest()


def host():
    "Host"
    # return "http://localhost:8000/api/media/"
    return "https://c0117f177fefb3c297af1ae370655a18.serveo.net/api/media/"
