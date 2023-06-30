from fastapi import FastAPI
import models
from database import engine
from routers import post, user, auth
from config import settings
from fastapi.middleware.cors import CORSMiddleware
 
origins = [ 
    "https://www.google.com"
    # "http://localhost",
    # "http://localhost:8080",
]

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"message": "Hello World"}