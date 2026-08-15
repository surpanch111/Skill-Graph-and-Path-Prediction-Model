import os
from neo4j import GraphDatabase, Driver
from dotenv import load_dotenv

load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI", "")
COGNODB_USER = os.getenv("COGNODB_USER", "cognodb")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD", "")

driver: Driver = None

def get_driver():
    global driver
    if driver is not None:
        return driver
    if not COGNODB_URI or not COGNODB_PASSWORD:
        return None
    try:
        driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USER, COGNODB_PASSWORD),
            connection_timeout=3.0,
            max_connection_lifetime=60
        )
        return driver
    except Exception:
        return None

def close_driver():
    global driver
    if driver:
        try:
            driver.close()
        except Exception:
            pass
        driver = None