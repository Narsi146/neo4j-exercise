import os
import pytest
from dotenv import load_dotenv

import sys

# Append your local path for python directory
sys.path.append(r"D:\Narsi\jobs\neo4j\experiment\loaddata_explore\python")

from data.driver import Neo4jDriver


@pytest.fixture(scope="session", autouse=True)
def load_env():
    load_dotenv()


@pytest.fixture
def conn():
    conn = Neo4jDriver(
        os.environ.get("NEO4J_URI"),
        os.environ.get("NEO4J_USERNAME"),
        os.environ.get("NEO4J_PASSWORD"),
    )
    return conn
