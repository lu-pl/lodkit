"""Docker/triple store connection classes."""

class AllegroConnection:
    """Doc."""

    def __init__(self):
        ...

    @staticmethod
    def _stop_all_containers(client: docker.client.DockerClient):
        """Stop all container of a given docker client."""
        for cli in client.containers.list():
            logging.info(f"Stopping '{cli}'.")
            cli.stop()

    def __enter__(self):
        ...

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._stop_all_containers(client)
