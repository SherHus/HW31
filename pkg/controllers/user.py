from fastapi import APIRouter

router = APIRouter()


@router.get("/users")
def get_users():
    return {"users": [{"name": "<NAME>", "email": "<EMAIL>"}]}


"""
router: 
{
    "GET /users":           get_users,
}
"""
