import asyncio
from concurrent import futures
from contextlib import asynccontextmanager
from typing import AnyStr

from neo4j import GraphDatabase


class Neo4jStreamAsync:
    def __init__(self, address: AnyStr, username: AnyStr, password: AnyStr, loop, encrypted: bool = False,
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
        self._loop = loop
        self._driver = None

    def connect(self):
        self._driver = GraphDatabase.driver(self._address, auth=(self._username, self._password),
                                            encrypted=self._encrypted)

    def close(self):
        self._driver.close()

    async def __aenter__(self):
        self.connect()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.close()

    async def read_async(self, query: AnyStr):
        """
        Reads results from the database in an async manner
        :param query: the query to run
        :return: the results
        """
        return await self._loop.run_in_executor(self._executor, self.__run, query)

    async def write_async(self, query: AnyStr):
        """
        Writes to a neo4j database in an async manner
        :param query: the query to write
        """
        await self._loop.run_in_executor(self._executor, self.__run, query)

    def __run(self, query: AnyStr):
        with self._driver.session() as session:
            result = session.run(query)
        return result.records()

    async def get_session(self):
        def get(driver):
            return driver.session()

        return await self._loop.run_in_executor(self._executor, get, self._driver)

    @asynccontextmanager
    async def transaction(self):
        with await self.get_session() as session:
            transaction = None
            try:
                transaction = Neo4jAsyncTransaction(session, self._loop, self._executor)
                await transaction.begin_transaction()
                yield transaction
            finally:
                if transaction:
                    await transaction.commit()


class Neo4jAsyncTransaction:
    def __init__(self, session, loop, executor):
        self._session = session
        self._loop = loop
        self._executor = executor
        self._transaction = None

    async def run(self, query):
        def run_blocking(transaction, data):
            transaction.run(data)

        await self._loop.run_in_executor(self._executor, run_blocking, self._transaction, query)

    async def commit(self):
        def commit_blocking(transaction):
            transaction.commit()

        await self._loop.run_in_executor(self._executor, commit_blocking, self._transaction)

    async def begin_transaction(self):
        def begin_blocking(session):
            return session.begin_transaction()

        self._transaction = await self._loop.run_in_executor(self._executor, begin_blocking, self._session)
