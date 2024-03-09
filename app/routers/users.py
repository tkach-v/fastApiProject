from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/", summary="")
def get_users():
    pass
