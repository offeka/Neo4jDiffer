import asyncio
from concurrent import futures
from contextlib import asynccontextmanager
from typing import AnyStr

from neo4j import GraphDatabase

LOOP = asyncio.get_running_loop()


class Neo4jStreamAsync:
    def __init__(self, address: AnyStr, username: AnyStr, password: AnyStr, encrypted: bool = False,
                 max_workers: int = 30):
        """
        Neo4j async interface as a stream
        :param address: the db address
        :param username: the db username
        :param password: the db password
        :param encrypted: whether encrypt the neo4j connection. must be false with neo4j 4.0
        :param max_workers: the max workers in the thread pool for running the queries
        """
        self._address = address
        self._username = username
        self._password = password
        self._encrypted = encrypted
        self._executor = futures.ThreadPoolExecutor(max_workers=max_workers)
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._address, auth=(self._username, self._password),
                                            encrypted=self._encrypted)

    @asynccontextmanager
    async def __session(self):
        session = None
        try:
            def connect():
                return self._driver.session()

            session = await LOOP.run_in_executor(self._executor, connect)
        finally:
            def disconnect():
                session.close()

            if session:
                await LOOP.run_in_executor(self._executor, disconnect)

    def close(self):
        self._driver.close()

    async def write_async(self, query):
        """
        Writes data to neo4j
        :param query:
        :return:
        """

        with await self.__session as session:
            def run():
                return session.run(query)

            await LOOP.run_in_executor(self._executor, run)

    async def read_async(self, query):
        """
        Reads results from neo4j lazily and returns them as an iterator
        :param query: the query to run
        :return: the results iterator
        """
        with await self.__session as session:
            def run():
                return session.run(query).records()

            query_results = await LOOP.run_in_executor(self._executor, run)
        for result in query_results:
            yield result
