r"""Contain the base class to implement an ingestor."""

from __future__ import annotations

__all__ = ["BaseIngestor", "is_ingestor_config", "setup_ingestor"]

import logging
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from coola.equality.comparators import BaseEqualityComparator
from coola.equality.handlers import EqualNanHandler, SameObjectHandler, SameTypeHandler
from coola.equality.testers import EqualityTester
from objectory import AbstractFactory
from objectory.utils import is_object_config

if TYPE_CHECKING:
    import polars as pl
    from coola.equality import EqualityConfig

logger = logging.getLogger(__name__)


class BaseIngestor(ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement a DataFrame ingestor.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import ParquetFileIngestor
    >>> ingestor = ParquetFileIngestor(path="/path/to/frame.parquet")
    >>> ingestor
    ParquetFileIngestor(source=/path/to/frame.parquet)
    >>> frame = ingestor.ingest()  # doctest: +SKIP

    ```
    """

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two ingestor objects are equal or not.

        Args:
            other: The other object to compare.
            equal_nan: Whether to compare NaN's as equal. If ``True``,
                NaN's in both objects will be considered equal.

        Returns:
            ``True`` if the two ingestors are equal, otherwise ``False``.

        Example usage:

        ```pycon

        >>> from grizz.ingestor import CsvIngestor
        >>> obj1 = CsvIngestor(path="/path/to/frame.csv")
        >>> obj2 = CsvIngestor(path="/path/to/frame.csv")
        >>> obj3 = CsvIngestor(path="/path/to/frame2.csv")
        >>> obj1.equal(obj2)
        True
        >>> obj1.equal(obj3)
        False

        ```
        """

    @abstractmethod
    def ingest(self) -> pl.DataFrame:
        r"""Ingest a DataFrame.

        Returns:
            The ingested DataFrame.

        Raises:
            DataFrameNotFoundError: if the DataFrame cannot be ingested.

        Example usage:

        ```pycon

        >>> from grizz.ingestor import ParquetFileIngestor
        >>> ingestor = ParquetFileIngestor(path="/path/to/frame.parquet")
        >>> frame = ingestor.ingest()  # doctest: +SKIP

        ```
        """


def is_ingestor_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseIngestor``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseIngestor`` object.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import is_ingestor_config
    >>> is_ingestor_config(
    ...     {"_target_": "grizz.ingestor.CsvIngestor", "path": "/path/to/data.csv"}
    ... )
    True

    ```
    """
    return is_object_config(config, BaseIngestor)


def setup_ingestor(
    ingestor: BaseIngestor | dict,
) -> BaseIngestor:
    r"""Set up an ingestor.

    The ingestor is instantiated from its configuration
    by using the ``BaseIngestor`` factory function.

    Args:
        ingestor: An ingestor or its configuration.

    Returns:
        An instantiated ingestor.

    Example usage:

    ```pycon

    >>> from grizz.ingestor import setup_ingestor
    >>> ingestor = setup_ingestor(
    ...     {"_target_": "grizz.ingestor.CsvIngestor", "path": "/path/to/data.csv"}
    ... )
    >>> ingestor
    CsvIngestor(path=/path/to/data.csv)

    ```
    """
    if isinstance(ingestor, dict):
        logger.info("Initializing an ingestor from its configuration... ")
        ingestor = BaseIngestor.factory(**ingestor)
    if not isinstance(ingestor, BaseIngestor):
        logger.warning(f"ingestor is not a `BaseIngestor` (received: {type(ingestor)})")
    return ingestor


class IngestorEqualityComparator(BaseEqualityComparator[BaseIngestor]):
    r"""Implement an equality comparator for ``BaseIngestor``
    objects."""

    def __init__(self) -> None:
        self._handler = SameObjectHandler()
        self._handler.chain(SameTypeHandler()).chain(EqualNanHandler())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def clone(self) -> IngestorEqualityComparator:
        return self.__class__()

    def equal(self, actual: BaseIngestor, expected: Any, config: EqualityConfig) -> bool:
        return self._handler.handle(actual, expected, config=config)


if not EqualityTester.has_comparator(BaseIngestor):  # pragma: no cover
    EqualityTester.add_comparator(BaseIngestor, IngestorEqualityComparator())
