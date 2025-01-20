r"""Contain ``polars.DataFrame`` transformers to impute missing values
with simple strategies."""

from __future__ import annotations

__all__ = ["SimpleImputerTransformer"]

import logging
from typing import TYPE_CHECKING, Any

import polars as pl

from grizz.transformer.columns import BaseInNOutNTransformer
from grizz.utils.imports import check_sklearn, is_sklearn_available
from grizz.utils.null import propagate_nulls

if is_sklearn_available():  # pragma: no cover
    from sklearn.impute import SimpleImputer

if TYPE_CHECKING:
    from collections.abc import Sequence

logger = logging.getLogger(__name__)


class SimpleImputerTransformer(BaseInNOutNTransformer):
    r"""Implement a transformer to impute missing values with simple
    strategies.

    Args:
        columns: The columns to scale. ``None`` means all the
            columns.
        prefix: The column name prefix for the output columns.
        suffix: The column name suffix for the output columns.
        exclude_columns: The columns to exclude from the input
            ``columns``. If any column is not found, it will be ignored
            during the filtering process.
        exist_policy: The policy on how to handle existing columns.
            The following options are available: ``'ignore'``,
            ``'warn'``, and ``'raise'``. If ``'raise'``, an exception
            is raised if at least one column already exist.
            If ``'warn'``, a warning is raised if at least one column
            already exist and the existing columns are overwritten.
            If ``'ignore'``, the existing columns are overwritten and
            no warning message appears.
        missing_policy: The policy on how to handle missing columns.
            The following options are available: ``'ignore'``,
            ``'warn'``, and ``'raise'``. If ``'raise'``, an exception
            is raised if at least one column is missing.
            If ``'warn'``, a warning is raised if at least one column
            is missing and the missing columns are ignored.
            If ``'ignore'``, the missing columns are ignored and
            no warning message appears.
        propagate_nulls: If set to ``True``, the ``None`` values are
            propagated after the transformation. If ``False``, the
            ``None`` values are replaced by NaNs.
        **kwargs: Additional arguments passed to
            ``sklearn.impute.SimpleImputer``.

    Example usage:

    ```pycon

    >>> import polars as pl
    >>> from grizz.transformer import SimpleImputer
    >>> transformer = SimpleImputer(columns=["col1", "col3"], prefix="", suffix="_out")
    >>> transformer
    SimpleImputerTransformer(columns=('col1', 'col3'), exclude_columns=(), exist_policy='raise', missing_policy='raise', prefix='', suffix='_out', propagate_nulls=True)
    >>> frame = pl.DataFrame(
    ...     {
    ...         "col1": [0, 1, None, 3, 4, 5],
    ...         "col2": ["0", "1", "2", "3", "4", "5"],
    ...         "col3": [float("nan"), 10, 20, 30, 40, None],
    ...         "col4": ["a", "b", "c", "d", "e", "f"],
    ...     }
    ... )
    >>> frame
    shape: (6, 4)
    ┌──────┬──────┬──────┬──────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 │
    │ ---  ┆ ---  ┆ ---  ┆ ---  │
    │ i64  ┆ str  ┆ f64  ┆ str  │
    ╞══════╪══════╪══════╪══════╡
    │ 0    ┆ 0    ┆ NaN  ┆ a    │
    │ 1    ┆ 1    ┆ 10.0 ┆ b    │
    │ null ┆ 2    ┆ 20.0 ┆ c    │
    │ 3    ┆ 3    ┆ 30.0 ┆ d    │
    │ 4    ┆ 4    ┆ 40.0 ┆ e    │
    │ 5    ┆ 5    ┆ null ┆ f    │
    └──────┴──────┴──────┴──────┘
    >>> out = transformer.fit_transform(frame)
    >>> out
    shape: (6, 6)
    ┌──────┬──────┬──────┬──────┬──────────┬──────────┐
    │ col1 ┆ col2 ┆ col3 ┆ col4 ┆ col1_out ┆ col3_out │
    │ ---  ┆ ---  ┆ ---  ┆ ---  ┆ ---      ┆ ---      │
    │ i64  ┆ str  ┆ f64  ┆ str  ┆ f64      ┆ f64      │
    ╞══════╪══════╪══════╪══════╪══════════╪══════════╡
    │ 0    ┆ 0    ┆ NaN  ┆ a    ┆ 0.0      ┆ 25.0     │
    │ 1    ┆ 1    ┆ 10.0 ┆ b    ┆ 1.0      ┆ 10.0     │
    │ null ┆ 2    ┆ 20.0 ┆ c    ┆ null     ┆ 20.0     │
    │ 3    ┆ 3    ┆ 30.0 ┆ d    ┆ 3.0      ┆ 30.0     │
    │ 4    ┆ 4    ┆ 40.0 ┆ e    ┆ 4.0      ┆ 40.0     │
    │ 5    ┆ 5    ┆ null ┆ f    ┆ 5.0      ┆ null     │
    └──────┴──────┴──────┴──────┴──────────┴──────────┘

    ```
    """

    def __init__(
        self,
        columns: Sequence[str] | None,
        prefix: str,
        suffix: str,
        exclude_columns: Sequence[str] = (),
        exist_policy: str = "raise",
        missing_policy: str = "raise",
        propagate_nulls: bool = True,
        **kwargs: Any,
    ) -> None:
        super().__init__(
            columns=columns,
            prefix=prefix,
            suffix=suffix,
            exclude_columns=exclude_columns,
            exist_policy=exist_policy,
            missing_policy=missing_policy,
        )
        self._propagate_nulls = propagate_nulls

        check_sklearn()
        self._imputer = SimpleImputer(**kwargs)
        self._kwargs = kwargs

    def get_args(self) -> dict:
        return super().get_args() | {"propagate_nulls": self._propagate_nulls} | self._kwargs

    def _fit(self, frame: pl.DataFrame) -> None:
        logger.info(
            f"Fitting the imputation parameters of {len(self.find_columns(frame)):,} columns..."
        )
        columns = self.find_common_columns(frame)
        self._imputer.fit(frame.select(columns).to_numpy())

    def _transform(self, frame: pl.DataFrame) -> pl.DataFrame:
        logger.info(
            f"Imputing the missing values of {len(self.find_columns(frame)):,} columns | "
            f"prefix={self._prefix!r} | suffix={self._suffix!r}"
        )
        columns = self.find_common_columns(frame)
        data = frame.select(columns)
        x = self._imputer.transform(data.to_numpy())
        out = pl.from_numpy(x, schema=data.columns)
        if self._propagate_nulls:
            out = propagate_nulls(out, data)
        return out
