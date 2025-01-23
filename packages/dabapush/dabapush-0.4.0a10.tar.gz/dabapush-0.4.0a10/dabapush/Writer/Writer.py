"""Writer base class for writing records to a destination.

The Writer class is an abstract base class for writing records to a destination.
It provides a write method to consume a queue of records and a persist method to
write the records to the destination.
"""

import abc
from pathlib import Path
from typing import Iterator, List

import ujson
from loguru import logger as log

from ..Configuration.WriterConfiguration import WriterConfiguration
from ..Record import Record


class Writer:
    """Abstract base class for all writer plugins."""

    def __init__(self, config: WriterConfiguration):
        """Initializes the Writer with the given configuration.

        Args:
           config (WriterConfiguration): The configuration for the writer.
        """
        super().__init__()

        self.config = config
        self.buffer: List[Record] = []
        self.back_log: List[Record] = []
        # initialize file log
        if not Path(".dabapush/").exists():
            Path(".dabapush/").mkdir()

        self.log_path = Path(f".dabapush/{config.name}.jsonl")
        if self.log_path.exists():
            log.debug(
                f"Found log file for {self.config.name} at {self.log_path}. Loading..."
            )
            with self.log_path.open("rt", encoding="utf8") as f:
                self.back_log = [
                    Record(**ujson.loads(_))  # pylint: disable=I1101
                    for _ in f.readlines()
                ]
        else:
            self.log_path.touch()
        self.log_file = self.log_path.open(  # pylint: disable=R1732
            "a", encoding="utf8"
        )

    def __del__(self):
        """Ensures the buffer is flushed before the object is destroyed."""
        self._trigger_persist()
        self.log_file.close()

    def write(self, queue: Iterator[Record]) -> None:
        """Consumes items from the provided queue.

        Args:
            queue (Iterator[Record]): Items to be consumed.
        """
        for item in queue:
            if item in self.back_log:
                continue
            self.buffer.append(item)
            if len(self.buffer) >= self.config.chunk_size:
                self._trigger_persist()

    def _trigger_persist(self):
        self.persist()
        log.debug(f"Persisted {len(self.buffer)} records. Setting to done.")
        for record in self.buffer:
            log.debug(f"Setting record {record.uuid} as done.")
            record.done()
            self.log(record)
            self.log_file.flush()
        self.buffer = []

    @abc.abstractmethod
    def persist(self) -> None:
        """Abstract method to persist the records to the destination."""

    @property
    def name(self):
        """Gets the name of the writer.

        Returns:
            str: The name of the writer.
        """
        return self.config.name

    @property
    def id(self):
        """Gets the ID of the writer.

        Returns:
            str: The ID of the writer.
        """
        return self.config.id

    def log(self, record: Record):
        """Log the record to the persistent record log file."""
        ujson.dump(record.to_log(), self.log_file)  # pylint: disable=I1101
        self.log_file.write("\n")

        log.debug(f"Done with {record.uuid}")
