"""General testing LODKit utils."""

from collections.abc import Callable, Iterator
import os
from pathlib import Path
import re
from tempfile import NamedTemporaryFile, _TemporaryFileWrapper
from typing import Any
from typing import Protocol

import pytest

from rdflib import Graph


_formats: tuple[str, ...] = ("ttl", "n3", "xml", "json-ld")


class _TempSerializerCallback(Protocol):
    def __call__(
        self, graph: Graph, formats: tuple[str, ...] = _formats
    ) -> Iterator[_TemporaryFileWrapper]:
        """Callback Protocol for Tempserializer callables."""
        ...


def serialize_temp_graphs(
    graph: Graph, formats: tuple[str, ...] = _formats
) -> Iterator[_TemporaryFileWrapper]:
    """Serialize a graph to temporary files for every given format."""
    for _format in formats:
        temp_file = NamedTemporaryFile(suffix=f".{_format}")

        with open(temp_file.name, "w") as f:
            f.write(graph.serialize(format=_format))

        yield temp_file


def parametrize_serializations_from_graph(
    graph: Graph,
    param: str,
    temp_serializer: _TempSerializerCallback = serialize_temp_graphs,
) -> pytest.MarkDecorator:
    """Constructor for a pytest.Markdecorator.

    Serializes a graph to temporary file objects based on temp_serializer;
    temporary file objects are bound to param.
    """
    paramter_values = [
        pytest.param(temp_file, id=temp_file.name)
        for temp_file in temp_serializer(graph)
    ]

    parametrizer = pytest.mark.parametrize(param, paramter_values)
    return parametrizer


def parametrize_paths_from_glob(
    *directories: str | os.PathLike,
    param: str,
    glob_pattern: str = "*",
    recursive: bool = False,
    parameter_callback: Callable[[Path], Any] = lambda x: x,
) -> pytest.MarkDecorator:
    """Constructor for a pytest.Markdecorator.

    Binds the result of a glob against a directory to param.
    """
    _glob_callable = Path.rglob if recursive else Path.glob

    def _parameter_values():
        for directory in directories:
            _directory: Path = Path(directory)

            if not _directory.is_dir():
                raise Exception(f"'{directory}' is not a directory.")

            yield from (
                pytest.param(parameter_callback(glob), id=glob.name)
                for glob in _glob_callable(directory, glob_pattern)
            )

    parametrizer = pytest.mark.parametrize(param, list(_parameter_values()))
    return parametrizer


def parametrize_graphs_from_glob(
    *directories: str | os.PathLike,
    param: str,
    glob_pattern: str = "*",
    recursive: bool = False,
    parameter_callback: Callable[[Path], Any] = lambda x: Graph().parse(x),
) -> pytest.MarkDecorator:
    """Constructor for a pytest.Markdecorator.

    Parses the result of a glob into Graph instances and binds to param.
    """
    return parametrize_paths_from_glob(
        *directories,
        param=param,
        glob_pattern=glob_pattern,
        recursive=recursive,
        parameter_callback=parameter_callback,
    )


def _get_tests_import_path_from_path(path: str | os.PathLike) -> tuple[str, Path]:
    _path = Path(path)
    _split = re.split(r"/|\.", str(_path))
    _index = _split.index("tests")

    import_path = ".".join(_split[_index:-1])
    return import_path, _path


def parametrize_import_paths_from_glob(
    *directories: str | os.PathLike,
    param: str,
    glob_pattern: str = "*",
    recursive: bool = False,
    parameter_callback: Callable[[Path], Any] = _get_tests_import_path_from_path,
) -> pytest.MarkDecorator:
    """"""
    return parametrize_paths_from_glob(
        *directories,
        param=param,
        glob_pattern=glob_pattern,
        recursive=recursive,
        parameter_callback=parameter_callback,
    )
