"""Docker/triple store connection classes."""

import logging
import requests
import time

import docker

from franz.openrdf.sail.allegrographserver import AllegroGraphServer, Repository
from franz.openrdf.repository.repositoryconnection import RepositoryConnection


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(logging.StreamHandler())


class AllegroConnection:
    """Connection abstraction for Allegrograph.

    Starts a docker image of Allegrograph and connects to the server.
    """

    def __init__(self, *, host_port=8080):
        """Parameterize docker and Allegro server."""
        # self.host_port = host_port
        ...

    def _start_agraph_docker(self) -> docker.models.containers.Container:
        """Start a docker container running Allegrograph.

        The Allegrograph port is mapped to 8080 on the host.
        """
        client = docker.from_env()

        container = client.containers.run(
            "franzinc/agraph:v7.1.0",
            shm_size="1G",
            ports={'10035/tcp': 8080},
            environment={
                "AGRAPH_SUPER_USER": "temp",
                "AGRAPH_SUPER_PASSWORD": "temp"
            },
            detach=True,
            remove=True
        )

        return container

    def _get_agraph_server(self) -> AllegroGraphServer:
        """Get an Allegraph server object."""
        server = AllegroGraphServer(
            host="localhost",
            port=8080,
            user="temp",
            password="temp"
        )

        return server

    def _connect_to_agraph(self, server: AllegroGraphServer) -> RepositoryConnection:
        """Connect to an Allegrograph server and return a connection object."""
        # get catalog
        catalog = server.openCatalog()
        # get temporary repo
        repo = catalog.getRepository("temp_repo", Repository.ACCESS)
        # get connection
        conn = repo.getConnection()

        return conn

    @staticmethod
    def _wait_for_server(sever: AllegroGraphServer):

        logger.info("Waiting for server...")

        while True:
            try:
                response = requests.get("http://127.0.0.1:8080/")
                if response.status_code == 200:
                    logger.info("Server is up and running!")
                    break
            except requests.exceptions.RequestException:
                pass

            time.sleep(0.1)

    def __enter__(self):
        """On entering context: run docker and connect to Agraph."""
        try:
            # run docker + agraph server
            self._container = self._start_agraph_docker()
            server = self._get_agraph_server()

            # wait for the server
            self._wait_for_server(server)

            # connect to agraph server + return connection
            connection = self._connect_to_agraph(server)

        except Exception as e:
            self._container.kill()
            raise e

        return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        """On exiting context: Stop the container."""
        self._container.kill()
