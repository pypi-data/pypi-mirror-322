"""This module contains the abstract base class for all reader plugins."""

import abc
from pathlib import Path
from typing import Iterator

from tqdm.auto import tqdm

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record

# pylint: disable=I1101


class Reader(abc.ABC):
    """Abstract base class for all reader plugins.

    **BEWARE**: readers and writers are never to be instanced directly by the user but rather will
    be obtained by calling `get_instance()` on their specific Configuration-counterparts.

    Args:
        config (ReaderConfiguration): The configuration for the reader.
    """

    def __init__(self, config: ReaderConfiguration):
        """
        Parameters
        ----------
        config : ReaderConfiguration
            Configuration file for the reader. In concrete classes it will
            be a subclass of ReaderConfiguration.
        """
        self.config = config

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """

    @property
    @abc.abstractmethod
    def records(self) -> Iterator[Record]:
        """Subclasses **must** implement this abstract method and implement
        their reading logic here.

        Returns
        -------
        type: Iterator[Record]
            Generator which _should_ be one item per element.
        """


class FileReader(Reader):
    """Reader to read files from a path.

    It matches files in the path-tree against the pattern.
    """

    @abc.abstractmethod
    def read(self) -> Iterator[Record]:
        """Reads all files matching the pattern in the read_path."""

    @property
    def records(self) -> Iterator[Record]:
        """Generator for all files matching the pattern in the read_path."""
        yield from (
            Record(
                uuid=str(a),
                payload=a,
            )
            for a in tqdm(list(Path(self.config.read_path).rglob(self.config.pattern)))
        )
