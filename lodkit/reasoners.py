"""Reasoners (inference plugins) for lodkit.Graph.."""

import logging

from collections.abc import MutableMapping
from typing import Protocol, runtime_checkable

import docker
import reasonable

from rdflib import Graph
from owlrl import DeductiveClosure, RDFS_OWLRL_Semantics, RDFS_Semantics

from franz.openrdf.sail.allegrographserver import AllegroGraphServer, Repository
from franz.openrdf.repository.repositoryconnection import RepositoryConnection


@runtime_checkable
class Reasoner(Protocol):
    """Protocol class for lodkit.Graph reasoners."""

    def inference(self, graph: Graph) -> Graph:
        """Logic for inferencing on an rdflib.Graph intance."""
        ...


class OWLRLReasoner(Reasoner):
    """Reasoner plugin for the Python owlrl inference engine.

    The combined RDFS_OWLRL_Semantics closure type is used.
    See https://owl-rl.readthedocs.io/en/latest/CombinedClosure.html.
    """

    _closure_type = RDFS_OWLRL_Semantics

    def inference(self, graph: Graph) -> Graph:
        """Perform inferencing on a graph."""
        DeductiveClosure(self._closure_type).expand(graph)

        return graph


class RDFSReasoner(OWLRLReasoner):
    """Reasoner plugin for the Python owlrl inference engine.

    The RDFS closure type is used.
    See https://owl-rl.readthedocs.io/en/latest/RDFSClosure.html.
    """

    _closure_type = RDFS_Semantics


class ReasonableReasoner(Reasoner):
    """ Reasoner plugin using the reasonable engine.

    OWL-RL and RFDS entailments are supported.
    See https://github.com/gtfierro/reasonable.
    """

    def inference(self, graph: Graph) -> Graph:
        """Perform inferencing on a graph."""
        reasoner = reasonable.PyReasoner()
        reasoner.from_graph(graph)

        entailment = iter(reasoner.reason())

        for triple in entailment:
            graph.add(triple)

        return graph




class AllegroReasoner(Reasoner):
    """InferencePlugin for the AllegroGraph inference engine."""

    _agraph_rule:str = "all"

    @staticmethod
    def _stop_all_containers(client: docker.client.DockerClient):
        """Stop all container of a given docker client."""
        for cli in client.containers.list():
            logging.info(f"Stopping '{cli}'.")
            cli.stop()

    @staticmethod
    def _start_agraph_docker() -> docker.client.DockerClient:
        """Start a docker container running Allegrograph.

        The Allegrograph port is mapped to 8080 on the host.
        """
        client = docker.from_env()

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

    @staticmethod
    def _get_agraph_server() -> AllegroGraphServer:
        """Create temporary Allegraph server and return a server object."""
        server = AllegroGraphServer(
            host="localhost",
            port=8080,
            user="temp",
            password="temp"
        )

        return server

    @staticmethod
    def _connect_to_agraph(server: AllegroGraphServer) -> RepositoryConnection:
        """Doc."""
        # get catalog
        catalog = server.openCatalog()
        # get temporary repo
        repo = catalog.getRepository("temp_repo", Repository.ACCESS)
        # get connection
        conn = repo.getConnection()

        return conn

    def _agraph_add_data(self, graph, connection: RepositoryConnection):
        ...

    # def inference(self, graph: Graph) -> Graph:
    #     """Perform inferencing on a graph."""
    #     try:
    #         # run docker + agraph
    #         client = self._start_agraph_docker()
    #         agraph_server = self._get_agraph_server()
    #         # connect to agraph
    #         connection = self._connect_to_agraph(agraph_server)
    #         # add data to agraph
    #         ...
    #         # do the inferencing
    #         connection.materializeEntailed(_whith=self._agraph_rule)
    #         # get entailed data
    #         ...
    #         # generate graph from entailed
    #         ...

    #     finally:
    #         self._stop_all_containers(client)

    #     # return entailed graph
    #     return graph

    def inference(self, graph):
        """Perform inferencing on a graph."""

        with AllegroConnection as connection:

            # add data
            for triple in graph.triples():
                connection.addTriple(triple)

            # inference
            connection.materializeEntailed(_with=self._agraph_rule)

            # get the data
            for triple in connection.getStatements(): #?
                graph.add(triple)

        return graph


reasoners: MutableMapping[str, Reasoner] = {
    "owlrl": OWLRLReasoner(),
    "rdfs": RDFSReasoner(),
    "reasonable": ReasonableReasoner()
}
