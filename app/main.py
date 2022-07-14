
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from app.database import engine
from app.routers import post, user, auth, vote
from app.config import settings

# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

origins = ["*"]  # We allow every single domain

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # The domains we allow
    allow_credentials=True,
    allow_methods=["*"],  # The HTTP methods we allow
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

@app.get("/")  # set the path of the url
async def root():
    return {"message": "Hello World"}

 



