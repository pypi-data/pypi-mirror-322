"""NDJSON Writer plug-in for dabapush"""

# pylint: disable=R,I1101
from typing import Iterator

import ujson

from ..Configuration.ReaderConfiguration import ReaderConfiguration
from ..Record import Record
from ..utils import flatten
from .Reader import FileReader



class JSONReader(FileReader):
    """Reader to read ready to read directories containing multiple json files.
    It matches files in the path-tree against the pattern and reads the
    content of each file as JSON.

    Attributes
    ----------
    config: DirectoryJSONReaderConfiguration
        The configuration file used for reading
    """

    def __init__(self, config: "JSONReaderConfiguration") -> None:
        super().__init__(config)
        self.config = config

    def read(self) -> Iterator[Record]:
        """reads multiple JSON files and emits them."""

        for file_record in self.records:
            with file_record.payload.open("rt", encoding="utf8") as json_file:
                parsed = ujson.load(json_file)
                record = Record(
                    uuid=f"{str(file_record.uuid)}",
                    payload=(
                        parsed
                        if not self.config.flatten_dicts
                        else flatten(parsed)
                    ),
                    source=file_record,
                )
                if record not in self.back_log:
                    yield record


class JSONReaderConfiguration(ReaderConfiguration):
    """Read directory containing JSON files.

    Attributes
    ----------
    flatten_dicts: bool
        whether to flatten those nested dicts

    """

    yaml_tag = "!dabapush:JSONReaderConfiguration"
    """internal tag for pyYAML
    """

    def __init__(
        self,
        name,
        id=None,  # pylint: disable=W0622
        read_path: str = ".",
        pattern: str = "*.json",
        flatten_dicts=True,
    ) -> None:
        """
        Parameters
        ----------
        name: str
            target pipeline name
        id : UUID
            ID of the instance (default value = None, is set by super class)
        read_path: str
            path to directory to read
        pattern: str
            filename pattern to match files in `read_path` against
        flatten_dicts: bool
            whether nested dictionaries are flattend (for details see `dabapush.utils.flatten`)

        """
        super().__init__(name, id=id, read_path=read_path, pattern=pattern)
        self.flatten_dicts = flatten_dicts

    def get_instance(self) -> JSONReader:  # pylint: disable=W0221
        """Get a configured instance of NDJSONReader

        Returns
        -------
        type: JSONReader
            Configured JSONReader instance
        """
        return JSONReader(self)
