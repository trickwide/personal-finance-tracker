import re
from repositories.user_repository import default_user_repository


class UserService:
    def __init__(self, user_repository=default_user_repository):
        self.user_repository = user_repository

    def is_username_valid(self, username):
        if len(username) < 5:
            return False, "Username is too short. Minimum length is 5 characters"

        if not re.match("^[a-zA-Z0-9_]*$", username):
            return False, "Username can only contain letters, numbers and underscores"

        if username.isdigit():
            return False, "Username cannot be a number"

        return True, None

    def is_password_valid(self, password):
        if len(password) < 8:
            return False, "Password must be at least 8 characters long."

        if not any(c.isupper() for c in password):
            return False, "Password must contain at least one uppercase letter."

        if not any(c.isdigit() for c in password):
            return False, "Password must contain at least one number."

        if not bool(re.search(r"[!@#$%^&*(),.?\":{}|<>]", password)):
            return False, "Password must contain at least one special character (e.g., !@#$%^&*)."

        return True, None

    def validate_user_credentials(self, username, password):
        return self.user_repository.validate_user_credentials(username, password)

    def register_user(self, username, password):
        self.user_repository.register_user(username, password)

    def get_user_id_by_username(self, username):
        return self.user_repository.get_user_id_by_username(username)

    def delete_user(self, user_id):
        self.user_repository.delete_user(user_id)


default_user_service = UserService(default_user_repository)
