import re
from base64 import b64encode
from Crypto.Hash import SHA256
from Crypto.Protocol.KDF import bcrypt
from Crypto.Random import get_random_bytes


def meets_requirements(pwd):
    # 8 chars, min 1 uppercase, min 1 lowercase, min 1 number or symbol
    pattern = r"^(?=.*[a-z])(?=.*[A-Z])((?=.*[@$!%*?&])|(?=.*\d))[A-Za-z\d@$!%*?&]{8,}$"
    return re.search(pattern, pwd)


def salt_and_hash(pwd):
    salt = get_random_bytes(16)
    pwd_b64 = b64encode(SHA256.new(pwd.encode()).digest())
    return bcrypt(pwd_b64, 12, salt).decode()

