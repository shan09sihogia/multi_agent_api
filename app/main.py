from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import routes, external

app = FastAPI(
    title="Multi-Agent Backend",
    version="1.0.0",
    description="Backend for a multi-agent system using CrewAI and FastAPI, supporting client and dashboard queries, and external API interactions with MongoDB and Redis caching."
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(routes.router)
app.include_router(external.router, prefix="/external")


@app.get("/", summary="Root Health Check")
async def root():
    return {"message": "Multi-Agent Backend is running!"}