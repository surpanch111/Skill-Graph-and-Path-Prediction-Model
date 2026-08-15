import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from backend.database import get_driver
from backend.queries import (
    get_full_graph,
    get_prerequisite_path,
    recommend_roles_by_skills,
)

app = FastAPI(title="SkillGraph API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class MatchRequest(BaseModel):
    skills: List[str]

@app.get("/api/health")
def health_check():
    try:
        driver = get_driver()
        with driver.session() as session:
            result = session.run("RETURN 1 AS status")
            record = result.single()
            if record and record["status"] == 1:
                return {"status": "healthy", "database": "connected"}
        return {"status": "degraded", "database": "connected"}
    except Exception as e:
        # Fallback to 200 with offline status so the UI gracefully handles degraded state
        return {"status": "offline", "database": "unreachable", "error": str(e)}

@app.get("/api/graph")
def graph_data():
    try:
        return get_full_graph()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/path/{role_title}")
def role_path(role_title: str):
    try:
        return get_prerequisite_path(role_title)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/match")
def match_roles(body: MatchRequest):
    try:
        return recommend_roles_by_skills(body.skills)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Mount static frontend
frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")