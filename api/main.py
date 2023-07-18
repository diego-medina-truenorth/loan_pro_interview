from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.routes.endpoints import router as endpoints_router

from app.database import Base, engine

app = FastAPI()

Base.metadata.create_all(bind=engine)


# Configure CORS
origins = [
    "http://localhost:3000",  # Add your frontend's URL here
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the router with endpoints
app.include_router(endpoints_router)

# Serve the frontend as static files
app.mount("/", StaticFiles(directory="web/build", html=True))
