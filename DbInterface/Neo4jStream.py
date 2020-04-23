from typing import AnyStr

from neo4j import GraphDatabase


class Neo4jStream:
    def __init__(self, address: AnyStr, username: AnyStr, password: AnyStr, encrypted: bool = False):
        self._address = address
        self._username = username
        self._password = password
        self._encrypted = encrypted
        self._session = None
        self._driver = None

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        """
        Connects to the neo4j database
        """
        self._driver = GraphDatabase.driver(self._address, auth=(self._username, self._password),
                                            encrypted=self._encrypted)
        self._session = self._driver.session()

    def close(self):
        """
        Closes the stream and releases resources
        """
        self._session.close()
        self._driver.close()

    def write(self, query: AnyStr) -> None:
        self._session.run(query)

    def read(self, query: AnyStr):
        return self._session.run(query)
