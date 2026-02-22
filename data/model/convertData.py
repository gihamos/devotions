from .databaseModels import User
def to_user_model(data: dict) -> User:
    data["_id"] = str(data["_id"])
    return User(**data)
