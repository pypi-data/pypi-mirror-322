import abc
from typing import Any

import numpy as np
import pandas as pd

from bayesline.api._src.types import DNFFilterExpressions


class DataFrameAccessor(abc.ABC):

    @property
    @abc.abstractmethod
    def columns(self) -> list[str]:
        pass

    @property
    @abc.abstractmethod
    def filters(self) -> dict[str, list[Any] | dict[str, Any]]:
        pass

    @property
    @abc.abstractmethod
    def schema(self) -> dict[str, np.dtype]:
        pass

    @abc.abstractmethod
    def get_data(
        self,
        columns: list[str] | None = None,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
    ) -> pd.DataFrame:
        pass


class AsyncDataFrameAccessor(abc.ABC):

    @property
    @abc.abstractmethod
    def columns(self) -> list[str]:
        pass

    @property
    @abc.abstractmethod
    def filters(self) -> dict[str, list[Any] | dict[str, Any]]:
        pass

    @property
    @abc.abstractmethod
    def schema(self) -> dict[str, np.dtype]:
        pass

    @abc.abstractmethod
    async def get_data(
        self,
        columns: list[str] | None = None,
        filters: DNFFilterExpressions | None = None,
        unique: bool = False,
    ) -> pd.DataFrame:
        pass
