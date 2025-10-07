from fastapi import FastAPI
from . import models, database
from .routes import users

models.Base.metadata.create_all(bind=database.engine)



app = FastAPI(title="FastAPI Testing Template")
app.include_router(users.router)

@app.get("/")
def home():
    return {"message": "Welcome to the API!"}
