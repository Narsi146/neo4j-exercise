import os
import pytest
from dotenv import load_dotenv

import sys

# ---- Append your local path for python directory ----
sys.path.append(r"./python")

from data.driver import Neo4jDriver

# Below are the pytest fixtures, that are used by various tests.


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
