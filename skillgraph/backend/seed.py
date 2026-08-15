import os
from pathlib import Path
from dotenv import load_dotenv
from neo4j import GraphDatabase

root_dir = Path(__file__).resolve().parent.parent
env_path = root_dir / ".env"
load_dotenv(dotenv_path=env_path)

COGNODB_URI = os.getenv("COGNODB_URI", "")
COGNODB_USER = os.getenv("COGNODB_USER", "cognodb")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD", "")

EXPANDED_SEED_QUERY = """
MATCH (n) DETACH DELETE n
WITH count(n) AS _

// Base Programming & Math
CREATE (py:Skill {name: 'Python', category: 'Programming'})
CREATE (cpp:Skill {name: 'C++', category: 'Programming'})
CREATE (math:Skill {name: 'Linear Algebra', category: 'Theory'})
CREATE (calc:Skill {name: 'Multivariable Calculus', category: 'Theory'})
CREATE (dsa:Skill {name: 'Data Structures & Algorithms', category: 'CS Core'})

// Intermediate Skills
CREATE (dsp:Skill {name: 'Digital Signal Processing', category: 'ECE Core'})
CREATE (ml:Skill {name: 'Machine Learning Basics', category: 'AI/ML'})
CREATE (docker:Skill {name: 'Docker & Microservices', category: 'DevOps'})
CREATE (sql:Skill {name: 'SQL & Database Design', category: 'Data'})
CREATE (cloud:Skill {name: 'Cloud & API Integration', category: 'Systems'})

// Advanced Skills
CREATE (dl:Skill {name: 'Deep Learning & PyTorch', category: 'AI/ML'})
CREATE (cv:Skill {name: 'Computer Vision (OpenCV)', category: 'AI/ML'})
CREATE (ros:Skill {name: 'ROS2 / Robotics Middleware', category: 'Robotics'})
CREATE (control:Skill {name: 'PID & Flight Control Systems', category: 'Robotics'})
CREATE (embedded:Skill {name: 'Embedded Systems & RTOS', category: 'Hardware'})
CREATE (rf:Skill {name: 'RF & Wireless Communication', category: 'ECE Core'})

// Skill Prerequisite Dependencies (:DEPENDS_ON)
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

// Roles
CREATE (drone_eng:Role {title: 'Autonomous Drone Engineer', salary_range: '$110k - $160k'})
CREATE (ai_eng:Role {title: 'Computer Vision Engineer', salary_range: '$120k - $175k'})
CREATE (backend_eng:Role {title: 'Backend Systems Engineer', salary_range: '$95k - $140k'})
CREATE (embedded_eng:Role {title: 'Embedded Robotics Engineer', salary_range: '$105k - $150k'})
CREATE (telecom_eng:Role {title: 'Wireless Communications Engineer', salary_range: '$100k - $145k'})

// Role Requirements (:REQUIRES)
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

def seed_database():
    if not COGNODB_URI or not COGNODB_PASSWORD:
        print("Error: Missing credentials in .env")
        return
    driver = None
    try:
        driver = GraphDatabase.driver(COGNODB_URI, auth=(COGNODB_USER, COGNODB_PASSWORD))
        with driver.session() as session:
            session.run(EXPANDED_SEED_QUERY)
        print("SUCCESS: Expanded dataset loaded into CognoDB!")
    except Exception as e:
        print(f"Error seeding database: {e}")
    finally:
        if driver:
            driver.close()

if __name__ == "__main__":
    seed_database()