from __future__ import annotations

from datetime import datetime
from os import PathLike
from typing import final

__all__ = [
    "File",
    "InvalidNzbError",
    "Meta",
    "Nzb",
    "Segment",
    "parse",
    "parse_file",
]

def parse(nzb: str) -> Nzb:
    """
    Parse the given string into an [`Nzb`].

    Returns
    -------
    Nzb
        Object representing the parsed Nzb file.

    Raises
    ------
    InvalidNzbError
        Raised if the Nzb is invalid.

    """

def parse_file(nzb: str | PathLike[str]) -> Nzb:
    """
    Parse the given file into an [`Nzb`].
    Note that this will read the entire file into memory.

    Parameters
    ----------
    nzb : str | PathLike[str]
        Path to the Nzb file.

    Returns
    -------
    Nzb
        Object representing the parsed Nzb file.

    Raises
    ------
    InvalidNzbError
        Raised if:
        - the contents of the file are not valid UTF-8.
        - the Nzb is invalid.

    """
@final
class InvalidNzbError(Exception):
    """Raised when the Nzb is invalid."""

@final
class Meta:
    """Optional creator-definable metadata for the contents of the Nzb."""

    title: str | None
    """Title."""

    passwords: tuple[str, ...]
    """Password(s)."""

    tags: tuple[str, ...]
    """Tag(s)."""

    category: str | None
    """Category."""

@final
class Segment:
    """One part segment of a file."""

    size: int
    """Size of the segment."""
    number: int
    """Number of the segment."""
    message_id: str
    """Message ID of the segment."""

@final
class File:
    """Represents a complete file, consisting of segments that make up a file."""

    poster: str
    """The poster of the file."""

    datetime: datetime
    """The date and time when the file was posted, in UTC."""

    subject: str
    """The subject of the file."""

    groups: tuple[str, ...]
    """Groups that reference the file."""

    segments: tuple[Segment, ...]
    """Segments that make up the file."""

    @property
    def size(self) -> int:
        """Size of the file calculated from the sum of segment sizes."""

    @property
    def name(self) -> str | None:
        """
        Complete name of the file with it's extension extracted from the subject.
        May return `None` if it fails to extract the name. if it fails to extract the name.
        """

    @property
    def stem(self) -> str | None:
        """
        Base name of the file without it's extension extracted from the [`File.name`][nzb._models.File.name].
        May return `None` if it fails to extract the stem.
        """

    @property
    def extension(self) -> str | None:
        """
        Extension of the file extracted from the [`File.name`][nzb._models.File.name].
        May return `None` if it fails to extract the extension.
        """

    def is_par2(self) -> bool:
        """
        Return `True` if the file is a `.par2` file, `False` otherwise.
        """

    def is_rar(self) -> bool:
        """
        Return `True` if the file is a `.rar` file, `False` otherwise.
        """

    def is_obfuscated(self) -> bool:
        """
        Return `True` if the file is obfuscated, `False` otherwise.
        """

@final
class Nzb:
    """Represents a complete Nzb file."""

    meta: Meta
    """Optional creator-definable metadata for the contents of the Nzb."""

    files: tuple[File, ...]
    """File objects representing the files included in the Nzb."""

    @property
    def file(self) -> File:
        """
        The main content file (episode, movie, etc) in the Nzb.
        This is determined by finding the largest file in the Nzb
        and may not always be accurate.
        """

    @property
    def size(self) -> int:
        """Total size of all the files in the Nzb."""

    @property
    def filenames(self) -> tuple[str, ...]:
        """
        Tuple of unique file names across all the files in the Nzb.
        May return an empty tuple if it fails to extract the name for every file.
        """

    @property
    def posters(self) -> tuple[str, ...]:
        """
        Tuple of unique posters across all the files in the Nzb.
        """

    @property
    def groups(self) -> tuple[str, ...]:
        """
        Tuple of unique groups across all the files in the Nzb.
        """

    @property
    def par2_size(self) -> int:
        """
        Total size of all the `.par2` files.
        """

    @property
    def par2_percentage(self) -> float:
        """
        Percentage of the size of all the `.par2` files relative to the total size.
        """

    def has_rar(self) -> bool:
        """
        Return `True` if any file in the Nzb is a `.rar` file, `False` otherwise.
        """

    def is_rar(self) -> bool:
        """
        Return `True` if all files in the Nzb are `.rar` files, `False` otherwise.
        """

    def is_obfuscated(self) -> bool:
        """
        Return `True` if any file in the Nzb is obfuscated, `False` otherwise.
        """

    def has_par2(self) -> bool:
        """
        Return `True` if there's at least one `.par2` file in the Nzb, `False` otherwise.
        """
