import os
from neo4j import GraphDatabase, Driver
from dotenv import load_dotenv

load_dotenv()

COGNODB_URI = os.getenv("COGNODB_URI", "")
COGNODB_USER = os.getenv("COGNODB_USER", "cognodb")
COGNODB_PASSWORD = os.getenv("COGNODB_PASSWORD", "")

driver: Driver = None

def get_driver() -> Driver:
    global driver
    if driver is None:
        if not COGNODB_URI or not COGNODB_PASSWORD:
            raise RuntimeError("Database credentials not set in environment variables.")
        driver = GraphDatabase.driver(
            COGNODB_URI,
            auth=(COGNODB_USER, COGNODB_PASSWORD)
        )
    return driver

def close_driver():
    global driver
    if driver:
        driver.close()
        driver = None