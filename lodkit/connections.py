"""Docker/triple store connection classes."""

class AllegroConnection:
    """Doc."""

    def __init__(self):
        """Parameterize docker and Allegro server"""
        ...

    def _start_agraph_docker(self) -> docker.client.DockerClient:
        """Start a docker container running Allegrograph.

        The Allegrograph port is mapped to 8080 on the host.
        """
        client = docker.from_env()

        # this will pull the image initially, right?
        # so the image should probably be provided locally
        client.containers.run(
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

        return client

    def _get_agraph_server(self) -> AllegroGraphServer:
        """Create temporary Allegraph server and return a server object."""
        server = AllegroGraphServer(
            host="localhost",
            port=8080,
            user="temp",
            password="temp"
        )

        return server

    def _connect_to_agraph(self, server: AllegroGraphServer) -> RepositoryConnection:
        """Doc."""
        # get catalog
        catalog = server.openCatalog()
        # get temporary repo
        repo = catalog.getRepository("temp_repo", Repository.ACCESS)
        # get connection
        conn = repo.getConnection()

        return conn

    ##################################################

    @staticmethod
    def _stop_all_containers(client: docker.client.DockerClient):
        """Stop all container of a given docker client."""
        for cli in client.containers.list():
            logging.info(f"Stopping '{cli}'.")
            cli.stop()

    def __enter__(self):
        ...
        # run docker + agraph
        # connect to agraph
        # return connection

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_all_containers(client)
