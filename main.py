from fastapi import FastAPI, Request
from app.api.routers import user
from app.api.routers import track
from app.api.routers import tokens
from app.api.routers import friendship
from app.api.routers import shared_track
from app.api.routers import feed
from fastapi.middleware.cors import CORSMiddleware
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI()

Instrumentator().instrument(app).expose(app)

app.add_middleware(
    CORSMiddleware,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(friendship.router)
app.include_router(user.router)
app.include_router(tokens.router)
app.include_router(track.router)
app.include_router(shared_track.router)
app.include_router(feed.router)
app.include_router(user.profile_router)
