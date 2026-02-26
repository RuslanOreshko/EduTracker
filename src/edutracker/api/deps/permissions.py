from fastapi import Depends
from edutracker.api.deps.auth import get_current_user
from edutracker.application.common.exceptions import ForbiddenError

def required_roles(*allowed_roles: str):
    def dependency(user = Depends(get_current_user)):
        if user.role not in allowed_roles:
            raise ForbiddenError(f"Role '{user.role}' not allowed")
        return user
    return dependency