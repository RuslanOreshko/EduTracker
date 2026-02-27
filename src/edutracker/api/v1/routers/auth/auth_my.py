from fastapi import Depends, APIRouter
from edutracker.api.deps.auth import get_current_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.get("/me")
def me(user = Depends(get_current_user)):
    return {
        "user_id": user.id,
        "email": user.email,
        "role": user.role,
    }