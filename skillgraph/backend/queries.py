from backend.database import get_driver

def execute_read_query(query: str, params: dict = None):
    driver = get_driver()
    with driver.session() as session:
        result = session.run(query, params or {})
        return [record.data() for record in result]

def get_full_graph():
    query = """
    MATCH (n)
    OPTIONAL MATCH (n)-[r]->(m)
    RETURN 
        id(n) AS src_id, 
        labels(n)[0] AS src_label, 
        coalesce(n.name, n.title) AS src_name,
        type(r) AS rel_type,
        id(m) AS tgt_id,
        labels(m)[0] AS tgt_label,
        coalesce(m.name, m.title) AS tgt_name
    """
    records = execute_read_query(query)
    
    nodes_dict = {}
    edges = []
    
    for row in records:
        src_id = str(row["src_id"])
        if src_id not in nodes_dict and row["src_name"]:
            nodes_dict[src_id] = {
                "id": src_id,
                "name": row["src_name"],
                "label": row["src_label"]
            }
        
        if row["tgt_id"] is not None and row["tgt_name"]:
            tgt_id = str(row["tgt_id"])
            if tgt_id not in nodes_dict:
                nodes_dict[tgt_id] = {
                    "id": tgt_id,
                    "name": row["tgt_name"],
                    "label": row["tgt_label"]
                }
            edges.append({
                "source": src_id,
                "target": tgt_id,
                "type": row["rel_type"]
            })
            
    return {"nodes": list(nodes_dict.values()), "edges": edges}

def get_prerequisite_path(role_title: str):
    query = """
    MATCH path = (r:Role {title: $role_title})-[:REQUIRES]->(s1:Skill)-[:DEPENDS_ON*1..4]->(s2:Skill)
    RETURN s1.name AS direct_skill,
           [n IN nodes(path) WHERE n:Skill | n.name] AS learning_chain,
           length(path) AS depth
    ORDER BY depth DESC
    """
    return execute_read_query(query, {"role_title": role_title})

def recommend_roles_by_skills(user_skills: list):
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
    return execute_read_query(query, {"skills": user_skills})