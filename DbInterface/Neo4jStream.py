from typing import AnyStr

from neo4j import GraphDatabase


class Neo4jStream:
    def __init__(self, address: AnyStr, username: AnyStr, password: AnyStr, encrypted: bool = False):
        """
        A neo4j interface as a stream
        :param address: the db address
        :param username: the db username
        :param password: the db password
        :param encrypted: whether encrypt the neo4j connection. must be false with neo4j 4.0
        """
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
        """
        Executes a query in neo4j database. Use this function only for creating data not for reading
        :param query: the query to run
        """
        self._session.run(query)

    def read(self, query: AnyStr):
        """
        Reads data from neo4j. use this function only for retrieving data from neo4j
        :param query: the query to run
        :return: the query result from neo4j
        """
        return self._session.run(query)
