import string, random


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return plain_password == hashed_password


def get_random_string(length):
    characters = string.ascii_letters + string.digits
    return ''.join(random.choice(characters) for _ in range(length))
