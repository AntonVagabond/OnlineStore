import bcrypt


def hash_password(password: str) -> bytes:
    """Хеширование пароля при регистрации."""
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)
