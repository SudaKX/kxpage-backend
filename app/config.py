

import hashlib

MYSQL_HOST = "127.0.0.1"
MYSQL_PORT = 3306
MYSQL_AUTH = "root:password"

IMAGE_STORE = "./images"

ADMIN_TOKEN = "kxpage_password"

def get_admin_hash() -> str:
    h = hashlib.sha512()
    h.update(ADMIN_TOKEN.encode())
    return h.hexdigest()

ADMIN_HASH = get_admin_hash()
