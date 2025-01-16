from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.db.db import engine, Base
from src.routes import users, projects



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


Base.metadata.create_all(bind=engine)



@app.get('/')
def home():
    return {'Hello': 'There'}

app.include_router(users.router)
app.include_router(projects.router)