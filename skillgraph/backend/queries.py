import os
from backend.database import get_driver

# Graph Dataset conforming to openCypher specifications
DATASET_NODES = [
    {"id": "1", "name": "Autonomous Drone Engineer", "label": "Role"},
    {"id": "2", "name": "Computer Vision Engineer", "label": "Role"},
    {"id": "3", "name": "Backend Systems Engineer", "label": "Role"},
    {"id": "4", "name": "Embedded Robotics Engineer", "label": "Role"},
    {"id": "5", "name": "Wireless Communications Engineer", "label": "Role"},
    {"id": "6", "name": "Python", "label": "Skill"},
    {"id": "7", "name": "C++", "label": "Skill"},
    {"id": "8", "name": "Linear Algebra", "label": "Skill"},
    {"id": "9", "name": "Multivariable Calculus", "label": "Skill"},
    {"id": "10", "name": "Data Structures & Algorithms", "label": "Skill"},
    {"id": "11", "name": "Machine Learning Basics", "label": "Skill"},
    {"id": "12", "name": "Deep Learning & PyTorch", "label": "Skill"},
    {"id": "13", "name": "Computer Vision (OpenCV)", "label": "Skill"},
    {"id": "14", "name": "ROS2 / Robotics Middleware", "label": "Skill"},
    {"id": "15", "name": "PID & Flight Control Systems", "label": "Skill"},
    {"id": "16", "name": "Embedded Systems & RTOS", "label": "Skill"},
    {"id": "17", "name": "Digital Signal Processing", "label": "Skill"},
    {"id": "18", "name": "RF & Wireless Communication", "label": "Skill"},
    {"id": "19", "name": "Cloud & API Integration", "label": "Skill"},
    {"id": "20", "name": "Docker & Microservices", "label": "Skill"}
]

DATASET_EDGES = [
    {"source": "1", "target": "14", "type": "REQUIRES"},
    {"source": "1", "target": "15", "type": "REQUIRES"},
    {"source": "1", "target": "13", "type": "REQUIRES"},
    {"source": "2", "target": "13", "type": "REQUIRES"},
    {"source": "2", "target": "12", "type": "REQUIRES"},
    {"source": "3", "target": "6", "type": "REQUIRES"},
    {"source": "3", "target": "10", "type": "REQUIRES"},
    {"source": "3", "target": "19", "type": "REQUIRES"},
    {"source": "3", "target": "20", "type": "REQUIRES"},
    {"source": "4", "target": "16", "type": "REQUIRES"},
    {"source": "4", "target": "14", "type": "REQUIRES"},
    {"source": "5", "target": "18", "type": "REQUIRES"},
    {"source": "5", "target": "17", "type": "REQUIRES"},
    {"source": "11", "target": "8", "type": "DEPENDS_ON"},
    {"source": "11", "target": "6", "type": "DEPENDS_ON"},
    {"source": "12", "target": "11", "type": "DEPENDS_ON"},
    {"source": "12", "target": "9", "type": "DEPENDS_ON"},
    {"source": "13", "target": "12", "type": "DEPENDS_ON"},
    {"source": "13", "target": "7", "type": "DEPENDS_ON"},
    {"source": "14", "target": "7", "type": "DEPENDS_ON"},
    {"source": "14", "target": "16", "type": "DEPENDS_ON"},
    {"source": "15", "target": "9", "type": "DEPENDS_ON"},
    {"source": "15", "target": "7", "type": "DEPENDS_ON"},
    {"source": "16", "target": "7", "type": "DEPENDS_ON"},
    {"source": "17", "target": "9", "type": "DEPENDS_ON"},
    {"source": "18", "target": "17", "type": "DEPENDS_ON"}
]

PATHS_DATA = {
    "Autonomous Drone Engineer": [
        {"direct_skill": "Computer Vision (OpenCV)", "learning_chain": ["Computer Vision (OpenCV)", "Deep Learning & PyTorch", "Machine Learning Basics", "Linear Algebra"], "depth": 4},
        {"direct_skill": "ROS2 / Robotics Middleware", "learning_chain": ["ROS2 / Robotics Middleware", "Embedded Systems & RTOS", "C++"], "depth": 3},
        {"direct_skill": "PID & Flight Control Systems", "learning_chain": ["PID & Flight Control Systems", "Multivariable Calculus"], "depth": 2}
    ],
    "Computer Vision Engineer": [
        {"direct_skill": "Computer Vision (OpenCV)", "learning_chain": ["Computer Vision (OpenCV)", "Deep Learning & PyTorch", "Machine Learning Basics", "Python"], "depth": 4},
        {"direct_skill": "Deep Learning & PyTorch", "learning_chain": ["Deep Learning & PyTorch", "Machine Learning Basics", "Linear Algebra"], "depth": 3}
    ],
    "Backend Systems Engineer": [
        {"direct_skill": "Cloud & API Integration", "learning_chain": ["Cloud & API Integration", "Docker & Microservices", "Python"], "depth": 3},
        {"direct_skill": "Data Structures & Algorithms", "learning_chain": ["Data Structures & Algorithms", "Python"], "depth": 2}
    ],
    "Embedded Robotics Engineer": [
        {"direct_skill": "ROS2 / Robotics Middleware", "learning_chain": ["ROS2 / Robotics Middleware", "Embedded Systems & RTOS", "C++"], "depth": 3},
        {"direct_skill": "Embedded Systems & RTOS", "learning_chain": ["Embedded Systems & RTOS", "C++"], "depth": 2}
    ],
    "Wireless Communications Engineer": [
        {"direct_skill": "RF & Wireless Communication", "learning_chain": ["RF & Wireless Communication", "Digital Signal Processing", "Multivariable Calculus"], "depth": 3}
    ]
}

ROLE_REQUIREMENTS = {
    "Autonomous Drone Engineer": (["ROS2 / Robotics Middleware", "PID & Flight Control Systems", "Computer Vision (OpenCV)"], "$110k - $160k"),
    "Computer Vision Engineer": (["Computer Vision (OpenCV)", "Deep Learning & PyTorch"], "$120k - $175k"),
    "Backend Systems Engineer": (["Python", "Data Structures & Algorithms", "Cloud & API Integration", "Docker & Microservices"], "$95k - $140k"),
    "Embedded Robotics Engineer": (["Embedded Systems & RTOS", "ROS2 / Robotics Middleware"], "$105k - $150k"),
    "Wireless Communications Engineer": (["RF & Wireless Communication", "Digital Signal Processing"], "$100k - $145k")
}

def get_full_graph():
    driver = get_driver()
    if driver:
        try:
            with driver.session() as session:
                query = """
                MATCH (n)
                OPTIONAL MATCH (n)-[r]->(m)
                RETURN id(n) AS src_id, labels(n)[0] AS src_label, coalesce(n.name, n.title) AS src_name,
                       type(r) AS rel_type, id(m) AS tgt_id, labels(m)[0] AS tgt_label, coalesce(m.name, m.title) AS tgt_name
                """
                records = [record.data() for record in session.run(query)]
                if records and len(records) > 0 and records[0]["src_name"]:
                    nodes_dict = {}
                    edges = []
                    for row in records:
                        s_id = str(row["src_id"])
                        if s_id not in nodes_dict and row["src_name"]:
                            nodes_dict[s_id] = {"id": s_id, "name": row["src_name"], "label": row["src_label"]}
                        if row["tgt_id"] is not None and row["tgt_name"]:
                            t_id = str(row["tgt_id"])
                            if t_id not in nodes_dict:
                                nodes_dict[t_id] = {"id": t_id, "name": row["tgt_name"], "label": row["tgt_label"]}
                            edges.append({"source": s_id, "target": t_id, "type": row["rel_type"]})
                    return {"nodes": list(nodes_dict.values()), "edges": edges}
        except Exception:
            pass
    return {"nodes": [dict(n) for n in DATASET_NODES], "edges": [dict(e) for e in DATASET_EDGES]}

def get_prerequisite_path(role_title: str):
    driver = get_driver()
    if driver:
        try:
            with driver.session() as session:
                query = """
                MATCH path = (r:Role {title: $role_title})-[:REQUIRES]->(s1:Skill)-[:DEPENDS_ON*1..4]->(s2:Skill)
                RETURN s1.name AS direct_skill,
                       [n IN nodes(path) WHERE n:Skill | n.name] AS learning_chain,
                       length(path) AS depth
                ORDER BY depth DESC
                """
                res = [record.data() for record in session.run(query, {"role_title": role_title})]
                if res:
                    return res
        except Exception:
            pass
    return PATHS_DATA.get(role_title, [])

def recommend_roles_by_skills(user_skills: list):
    driver = get_driver()
    if driver:
        try:
            with driver.session() as session:
                query = """
                UNWIND $skills AS my_skill
                MATCH (s:Skill {name: my_skill})<-[:REQUIRES]-(r:Role)
                WITH r, count(DISTINCT s) AS matched_skills
                MATCH (r)-[:REQUIRES]->(total_req:Skill)
                WITH r, matched_skills, count(DISTINCT total_req) AS total_skills
                RETURN r.title AS role,
                       r.salary_range AS salary,
                       matched_skills,
                       total_skills,
                       round((toFloat(matched_skills) / total_skills) * 100) AS match_percentage
                ORDER BY match_percentage DESC
                """
                res = [record.data() for record in session.run(query, {"skills": user_skills})]
                if res:
                    return res
        except Exception:
            pass

    results = []
    for role, (reqs, salary) in ROLE_REQUIREMENTS.items():
        matched = len(set(user_skills).intersection(set(reqs)))
        if matched > 0:
            results.append({
                "role": role,
                "salary": salary,
                "matched_skills": matched,
                "total_skills": len(reqs),
                "match_percentage": round((matched / len(reqs)) * 100)
            })
    return sorted(results, key=lambda x: x["match_percentage"], reverse=True)