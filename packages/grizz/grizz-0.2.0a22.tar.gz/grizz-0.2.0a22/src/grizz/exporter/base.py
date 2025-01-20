r"""Contain the base class to implement a DataFrame exporter."""

from __future__ import annotations

__all__ = ["BaseExporter", "is_exporter_config", "setup_exporter"]

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


class BaseExporter(ABC, metaclass=AbstractFactory):
    r"""Define the base class to implement a DataFrame exporter.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.exporter import ParquetExporter
    >>> exporter = ParquetExporter(path="/path/to/frame.parquet")
    >>> exporter
    ParquetExporter(path=/path/to/frame.parquet)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [1, 2, 3, 4, 5],
    ...         "col2": ["1", "2", "3", "4", "5"],
    ...         "col3": ["a", "b", "c", "d", "e"],
    ...     }
    ... )
    >>> exporter.export(frame)  # doctest: +SKIP

    ```
    """

    @abstractmethod
    def equal(self, other: Any, equal_nan: bool = False) -> bool:
        r"""Indicate if two exporter objects are equal or not.

        Args:
            other: The other object to compare.
            equal_nan: Whether to compare NaN's as equal. If ``True``,
                NaN's in both objects will be considered equal.

        Returns:
            ``True`` if the two exporters are equal, otherwise ``False``.

        Example usage:

        ```pycon

        >>> import numpy as np
        >>> from grizz.exporter import CsvExporter
        >>> obj1 = CsvExporter(path="/path/to/frame.csv")
        >>> obj2 = CsvExporter(path="/path/to/frame.csv")
        >>> obj3 = CsvExporter(path="/path/to/frame2.csv")
        >>> obj1.equal(obj2)
        True
        >>> obj1.equal(obj3)
        False

        ```
        """

    @abstractmethod
    def export(self, frame: pl.DataFrame) -> None:
        r"""Export a DataFrame.

        Args:
            frame: The DataFrame to export.

        Example usage:

        ```pycon

        >>> import polars as pl
        >>> from grizz.exporter import ParquetExporter
        >>> exporter = ParquetExporter(path="/path/to/frame.parquet")
        >>> frame = pl.DataFrame(
        ...     {
        ...         "col1": [1, 2, 3, 4, 5],
        ...         "col2": ["1", "2", "3", "4", "5"],
        ...         "col3": ["a", "b", "c", "d", "e"],
        ...     }
        ... )
        >>> exporter.export(frame)  # doctest: +SKIP

        ```
        """


def is_exporter_config(config: dict) -> bool:
    r"""Indicate if the input configuration is a configuration for a
    ``BaseExporter``.

    This function only checks if the value of the key  ``_target_``
    is valid. It does not check the other values. If ``_target_``
    indicates a function, the returned type hint is used to check
    the class.

    Args:
        config: The configuration to check.

    Returns:
        ``True`` if the input configuration is a configuration
            for a ``BaseExporter`` object.

    Example usage:

    ```pycon

    >>> from grizz.exporter import is_exporter_config
    >>> is_exporter_config(
    ...     {"_target_": "grizz.exporter.ParquetExporter", "path": "/path/to/data.parquet"}
    ... )
    True

    ```
    """
    return is_object_config(config, BaseExporter)


def setup_exporter(
    exporter: BaseExporter | dict,
) -> BaseExporter:
    r"""Set up an exporter.

    The exporter is instantiated from its configuration
    by using the ``BaseExporter`` factory function.

    Args:
        exporter: A exporter or its configuration.

    Returns:
        An instantiated exporter.

    Example usage:

    ```pycon

    >>> from grizz.exporter import setup_exporter
    >>> exporter = setup_exporter(
    ...     {"_target_": "grizz.exporter.ParquetExporter", "path": "/path/to/data.parquet"}
    ... )
    >>> exporter
    ParquetExporter(path=/path/to/data.parquet)

    ```
    """
    if isinstance(exporter, dict):
        logger.info("Initializing an exporter from its configuration... ")
        exporter = BaseExporter.factory(**exporter)
    if not isinstance(exporter, BaseExporter):
        logger.warning(f"exporter is not a `BaseExporter` (received: {type(exporter)})")
    return exporter


class ExporterEqualityComparator(BaseEqualityComparator[BaseExporter]):
    r"""Implement an equality comparator for ``BaseExporter``
    objects."""

    def __init__(self) -> None:
        self._handler = SameObjectHandler()
        self._handler.chain(SameTypeHandler()).chain(EqualNanHandler())

    def __eq__(self, other: object) -> bool:
        return isinstance(other, self.__class__)

    def clone(self) -> ExporterEqualityComparator:
        return self.__class__()

    def equal(self, actual: BaseExporter, expected: Any, config: EqualityConfig) -> bool:
        return self._handler.handle(actual, expected, config=config)


if not EqualityTester.has_comparator(BaseExporter):  # pragma: no cover
    EqualityTester.add_comparator(BaseExporter, ExporterEqualityComparator())
