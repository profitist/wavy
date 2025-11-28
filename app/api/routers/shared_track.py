from fastapi import APIRouter, Depends


router = APIRouter(
    prefix="/shared_track",
    tags=["Shared Track"],
)
