# server/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routes import api
from db.database import init_db

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:4200"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# initialize database on startup
@app.on_event("startup")
async def startup_event():
    init_db()

app.include_router(api.router)

@app.get("/")
async def root():
    return {"message": "AI Sales Bot Backend"}
