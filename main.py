from fastapi import FastAPI
from app.api.routers import user
from app.api.routers import track
from app.api.routers import friendship
from app.api.routers import shared_track
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(friendship.router)
app.include_router(user.router)
app.include_router(track.router)
app.include_router(shared_track.router)
app.include_router(user.profile_router)
