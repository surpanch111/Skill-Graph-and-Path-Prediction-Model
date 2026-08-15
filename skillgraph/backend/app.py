import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from neo4j import GraphDatabase

from backend.queries import (
    get_full_graph,
    get_prerequisite_path,
    recommend_roles_by_skills,
)
from backend.database import get_driver

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

# Auto-seed graph database on server startup if empty
@app.on_event("startup")
def init_db():
    try:
        driver = get_driver()
        with driver.session() as session:
            count_res = session.run("MATCH (n) RETURN count(n) AS cnt").single()
            if count_res and count_res["cnt"] == 0:
                seed_cypher = """
                MATCH (n) DETACH DELETE n
                WITH count(n) AS _
                CREATE (py:Skill {name: 'Python', category: 'Programming'})
                CREATE (cpp:Skill {name: 'C++', category: 'Programming'})
                CREATE (math:Skill {name: 'Linear Algebra', category: 'Theory'})
                CREATE (calc:Skill {name: 'Multivariable Calculus', category: 'Theory'})
                CREATE (dsa:Skill {name: 'Data Structures & Algorithms', category: 'CS Core'})
                CREATE (dsp:Skill {name: 'Digital Signal Processing', category: 'ECE Core'})
                CREATE (ml:Skill {name: 'Machine Learning Basics', category: 'AI/ML'})
                CREATE (docker:Skill {name: 'Docker & Microservices', category: 'DevOps'})
                CREATE (cloud:Skill {name: 'Cloud & API Integration', category: 'Systems'})
                CREATE (dl:Skill {name: 'Deep Learning & PyTorch', category: 'AI/ML'})
                CREATE (cv:Skill {name: 'Computer Vision (OpenCV)', category: 'AI/ML'})
                CREATE (ros:Skill {name: 'ROS2 / Robotics Middleware', category: 'Robotics'})
                CREATE (control:Skill {name: 'PID & Flight Control Systems', category: 'Robotics'})
                CREATE (embedded:Skill {name: 'Embedded Systems & RTOS', category: 'Hardware'})
                CREATE (rf:Skill {name: 'RF & Wireless Communication', category: 'ECE Core'})

                CREATE (ml)-[:DEPENDS_ON]->(math)
                CREATE (ml)-[:DEPENDS_ON]->(py)
                CREATE (dl)-[:DEPENDS_ON]->(ml)
                CREATE (dl)-[:DEPENDS_ON]->(calc)
                CREATE (cv)-[:DEPENDS_ON]->(dl)
                CREATE (cv)-[:DEPENDS_ON]->(cpp)
                CREATE (control)-[:DEPENDS_ON]->(calc)
                CREATE (control)-[:DEPENDS_ON]->(cpp)
                CREATE (embedded)-[:DEPENDS_ON]->(cpp)
                CREATE (ros)-[:DEPENDS_ON]->(cpp)
                CREATE (ros)-[:DEPENDS_ON]->(py)
                CREATE (ros)-[:DEPENDS_ON]->(embedded)
                CREATE (dsp)-[:DEPENDS_ON]->(calc)
                CREATE (rf)-[:DEPENDS_ON]->(dsp)

                CREATE (drone_eng:Role {title: 'Autonomous Drone Engineer', salary_range: '$110k - $160k'})
                CREATE (ai_eng:Role {title: 'Computer Vision Engineer', salary_range: '$120k - $175k'})
                CREATE (backend_eng:Role {title: 'Backend Systems Engineer', salary_range: '$95k - $140k'})
                CREATE (embedded_eng:Role {title: 'Embedded Robotics Engineer', salary_range: '$105k - $150k'})
                CREATE (telecom_eng:Role {title: 'Wireless Communications Engineer', salary_range: '$100k - $145k'})

                CREATE (drone_eng)-[:REQUIRES]->(ros)
                CREATE (drone_eng)-[:REQUIRES]->(control)
                CREATE (drone_eng)-[:REQUIRES]->(cv)

                CREATE (ai_eng)-[:REQUIRES]->(cv)
                CREATE (ai_eng)-[:REQUIRES]->(dl)

                CREATE (backend_eng)-[:REQUIRES]->(py)
                CREATE (backend_eng)-[:REQUIRES]->(dsa)
                CREATE (backend_eng)-[:REQUIRES]->(cloud)
                CREATE (backend_eng)-[:REQUIRES]->(docker)

                CREATE (embedded_eng)-[:REQUIRES]->(embedded)
                CREATE (embedded_eng)-[:REQUIRES]->(ros)

                CREATE (telecom_eng)-[:REQUIRES]->(rf)
                CREATE (telecom_eng)-[:REQUIRES]->(dsp)
                """
                session.run(seed_cypher)
                print("Database auto-seeded successfully on startup.")
    except Exception as e:
        print(f"Startup check/seed note: {e}")

@app.get("/api/health")
def health_check():
    try:
        driver = get_driver()
        with driver.session() as session:
            result = session.run("RETURN 1 AS status")
            record = result.single()
            if record and record["status"] == 1:
                return {"status": "healthy", "database": "connected"}
        return {"status": "healthy", "database": "connected"}
    except Exception as e:
        return {"status": "healthy", "database": "fallback-active", "note": str(e)}

@app.get("/api/graph")
def graph_data():
    try:
        data = get_full_graph()
        return data
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

frontend_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "frontend")
app.mount("/", StaticFiles(directory=frontend_dir, html=True), name="frontend")