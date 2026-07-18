import bcrypt

from models import User


def hash_password(password):
    return bcrypt.hashpw(
        password.encode(),
        bcrypt.gensalt()
    ).decode()


def verify_password(password, hashed_password):
    return bcrypt.checkpw(
        password.encode(),
        hashed_password.encode()
    )


def create_user(db, username, password, full_name):

    existing = db.query(User).filter(
        User.username == username
    ).first()

    if existing:
        return False

    user = User(
        username=username,
        password=hash_password(password),
        full_name=full_name,
    )

    db.add(user)
    db.commit()

    return True


def authenticate(db, username, password):

    user = db.query(User).filter(
        User.username == username
    ).first()

    if not user:
        return None

    if verify_password(password, user.password):
        return user

    return None