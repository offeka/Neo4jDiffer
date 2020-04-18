from neo4j import GraphDatabase


class Neo4jWriter:
    def __init__(self, address, username, password):
        self._address = address
        self._username = username
        self._password = password

    def __enter__(self):
        self._driver = GraphDatabase.driver(self._address, auth=(self._username, self._password))
        self._session = self._driver.session()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._session.close()
        self._driver.close()
