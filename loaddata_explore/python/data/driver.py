import os
from dotenv import load_dotenv
from neo4j import GraphDatabase


class Neo4jDriver:
    """
    Returns Neo4j driver instance, initiate with following args:
    uri : URL for Neo4j
    user, pwd : username and password

    The following methods can be used with the Class instance:

    close() : closes the driver

    verify_driver() : verifies connectivity to driver

    query(query, parameters, db) : returns running a query run
    against Neo4j.
        query : is the query to run against database
        parameters : pass various parameters for examples data rows
        db : database name

    """

    def __init__(self, uri, user, pwd):
        self.__driver = None
        try:
            self.__driver = GraphDatabase.driver(uri=uri, auth=(user, pwd))
        except Exception as e:
            print("Failed to create Driver:", e)

    def close(self):
        if self.__driver is not None:
            self.__driver.close()

    def verify_driver(self):
        if self.__driver is not None:
            self.__driver.verify_connectivity()
            return "Success"

    def query(self, query, parameters=None, db=None):
        assert self.__driver is not None, "Driver not initialized!"
        session = None
        response = None
        try:
            session = (
                self.__driver.session(database=db)
                if db is not None
                else self.__driver.session()
            )
            response = list(session.run(query, parameters))
        except Exception as e:
            print("Query failed:", e)
        finally:
            if session is not None:
                session.close()
        return response


if __name__ == "__main__":
    """Test connectivity in isolation"""
    load_dotenv()
    conn = Neo4jDriver(
        os.environ.get("NEO4J_URI"),
        os.environ.get("NEO4J_USERNAME"),
        os.environ.get("NEO4J_PASSWORD"),
    )
    assert conn.verify_driver() is not None, "Failed"
    conn.close()
