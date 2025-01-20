r"""Contain DataFrame ingestors."""

from __future__ import annotations

__all__ = [
    "BaseIngestor",
    "CacheIngestor",
    "ClickHouseArrowIngestor",
    "CsvIngestor",
    "Ingestor",
    "JoinIngestor",
    "ParquetFileIngestor",
    "ParquetIngestor",
    "TransformIngestor",
    "is_ingestor_config",
    "setup_ingestor",
]

from grizz.ingestor.base import BaseIngestor, is_ingestor_config, setup_ingestor
from grizz.ingestor.cache import CacheIngestor
from grizz.ingestor.clickhouse import ClickHouseArrowIngestor
from grizz.ingestor.csv import CsvIngestor
from grizz.ingestor.join import JoinIngestor
from grizz.ingestor.parquet import ParquetFileIngestor, ParquetIngestor
from grizz.ingestor.transform import TransformIngestor
from grizz.ingestor.vanilla import Ingestor
