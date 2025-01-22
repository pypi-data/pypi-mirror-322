import abc
import datetime as dt
from collections import defaultdict
from typing import Literal

import pandas as pd

from bayesline.api._src.dataframe import AsyncDataFrameAccessor, DataFrameAccessor
from bayesline.api._src.equity.byod_settings import ByodSettings, ByodSettingsMenu
from bayesline.api._src.equity.exposure_settings import (
    ExposureSettings,
    ExposureSettingsMenu,
)
from bayesline.api._src.equity.modelconstruction_settings import (
    ModelConstructionSettings,
    ModelConstructionSettingsMenu,
)
from bayesline.api._src.equity.portfoliohierarchy_settings import (
    PortfolioHierarchySettings,
    PortfolioHierarchySettingsMenu,
)
from bayesline.api._src.equity.report_settings import ReportSettings, ReportSettingsMenu
from bayesline.api._src.equity.riskmodels_settings import (
    FactorRiskModelSettings,
    FactorRiskModelSettingsMenu,
)
from bayesline.api._src.equity.universe_settings import (
    UniverseSettings,
    UniverseSettingsMenu,
)
from bayesline.api._src.registry import AsyncRegistryBasedApi, RegistryBasedApi
from bayesline.api._src.types import DataFrameFormat, DateLike, IdType

FactorType = Literal["Market", "Style", "Industry", "Region"]


class AssetUniverseApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> UniverseSettings:
        """
        Returns
        -------
        The settings used to create this universe.
        """
        ...

    @property
    @abc.abstractmethod
    def id_types(self) -> list[IdType]:
        """
        Returns
        -------
        supported id types for this universe.
        """
        ...

    @abc.abstractmethod
    def coverage(self, id_type: IdType | None = None) -> list[str]:
        """
        Parameters
        ----------
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`

        Raises
        ------
        ValueError
            If the given id type is not supported.

        Returns
        -------
        list of all asset ids this universe covers, in given id type.
        """
        ...

    @abc.abstractmethod
    def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        """
        Parameters
        ----------
        range_only: bool, default=False
            If True, returns the first and last date only.
        trade_only: bool, default=False
            If True, filter down the dats to trade dates only.

        Returns
        -------
        list of all dates this universe covers.
        """

    @abc.abstractmethod
    def counts(
        self,
        dates: bool = True,
        industry_level: int = 0,
        region_level: int = 0,
        universe_type: Literal["estimation", "coverage", "both"] = "both",
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        dates: bool, optional
            If True, groups by dates
        industry_level: int, optional
            The level of industry aggregation to group by.
            0 means no industry aggregation, 1 means level 1, etc.
            Values greater than the max level are treated as the max level.
        region_level: int, optional
            The level of region aggregation to group by.
            0 means no region aggregation, 1 means level 1, etc.
            Values greater than the max level are treated as the max level.
        universe_type: Literal["estimation", "coverage", "both"], optional
            The type of universe to calculate the counts for.
        id_type: IdType, optional
            The id type to calculate the daily stats for, e.g. `ticker`,
            which is relevant as the coverage may differ by id type.
            The given id type must be supported, i.e. in `id_types`.

        Returns
        -------
        pd.DataFrame
            Universe counts.
            If grouped by dates then the count will be given.
            If not grouped by dates then the mean/min/max across
            all dates will be given.
        """
        ...

    @abc.abstractmethod
    def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`, or the default
            ID type of the universe if `None`.
        filter_mode: Literal[all, mapped, unmapped]
            if `mapped` will only consider assets that could be mapped.
            if `unmapped` will only consider assets that could not be mapped.
        mode: Literal[all, daily-counts, latest-name]
            if `all`, returns all dated mappings
            if `daily-counts`, returns the daily counts of mapped assets
            if `input-asset-counts`, returns the total counts of input assets
            if `latest-name`, returns the latest name of mapped assets

        Returns
        -------
        pd.DataFrame
            If mode is `all`, a DataFrame with `date`, `input_asset_id`,
            `input_asset_id_type`, `output_asset_id`, `output_asset_id_type` and,
            `name` columns.
            It contains contains the original input ID space and the mapped ids.
            The mapped IDs will be `None` if for the given date and input ID the
            asset cannot be mapped.
            If mode is `daily-counts`, a DataFrame with `date`, `asset_id` and `count`
            columns.
            If mode is `input-asset-counts`, a DataFrame with `input_asset_id` and `count`
            columns.
            If mode is `latest-name`, a DataFrame with `asset_id` and `name` columns.
        """
        ...

    @abc.abstractmethod
    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        df_format: DataFrameFormat = "unstacked",
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        start: DateLike, optional
            The start date of the universe to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported, i.e. in `id_types`.
        df_format: DataFrameFormat, optional
            The output format of the returned DataFrame.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range.
        """
        ...


class AsyncAssetUniverseApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> UniverseSettings:
        """
        Returns
        -------
        The settings used to create this universe.
        """
        ...

    @property
    @abc.abstractmethod
    def id_types(self) -> list[IdType]:
        """
        Returns
        -------
        supported id types for this universe.
        """
        ...

    @abc.abstractmethod
    async def coverage(self, id_type: IdType | None = None) -> list[str]:
        """
        Parameters
        ----------
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`

        Raises
        ------
        ValueError
            If the given id type is not supported.

        Returns
        -------
        list of all asset ids this universe covers, in given id type.
        """
        ...

    @abc.abstractmethod
    async def dates(
        self, *, range_only: bool = False, trade_only: bool = False
    ) -> list[dt.date]:
        """
        Parameters
        ----------
        range_only: bool, default=False
            If True, returns the first and last date only.
        trade_only: bool, default=False
            If True, filter down the dats to trade dates only.

        Returns
        -------
        list of all dates this universe covers.
        """

    @abc.abstractmethod
    async def counts(
        self,
        dates: bool = True,
        industry_level: int = 0,
        region_level: int = 0,
        universe_type: Literal["estimation", "coverage", "both"] = "both",
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        dates: bool, optional
            If True, groups by dates
        industry_level: int, optional
            The level of industry aggregation to group by.
            0 means no industry aggregation, 1 means level 1, etc.
            Values greater than the max level are treated as the max level.
        region_level: int, optional
            The level of region aggregation to group by.
            0 means no region aggregation, 1 means level 1, etc.
            Values greater than the max level are treated as the max level.
        universe_type: Literal["estimation", "coverage", "both"], optional
            The type of universe to calculate the counts for.
        id_type: IdType, optional
            The id type to calculate the daily stats for, e.g. `ticker`,
            which is relevant as the coverage may differ by id type.
            The given id type must be supported, i.e. in `id_types`.

        Returns
        -------
        pd.DataFrame
            Universe counts.
            If grouped by dates then the count will be given.
            If not grouped by dates then the mean/min/max across
            all dates will be given.
        """
        ...

    @abc.abstractmethod
    async def input_id_mapping(
        self,
        *,
        id_type: IdType | None = None,
        filter_mode: Literal["all", "mapped", "unmapped"] = "all",
        mode: Literal[
            "all", "daily-counts", "input-asset-counts", "latest-name"
        ] = "all",
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`, or the default
            ID type of the universe if `None`.
        filter_mode: Literal[all, mapped, unmapped]
            if `mapped` will only consider assets that could be mapped.
            if `unmapped` will only consider assets that could not be mapped.
        mode: Literal[all, daily-counts, latest-name]
            if `all`, returns all dated mappings
            if `daily-counts`, returns the daily counts of mapped assets
            if `input-asset-counts`, returns the total counts of input assets
            if `latest-name`, returns the latest name of mapped assets

        Returns
        -------
        pd.DataFrame
            If mode is `all`, a DataFrame with `date`, `input_asset_id`,
            `input_asset_id_type`, `output_asset_id`, `output_asset_id_type` and,
            `name` columns.
            It contains contains the original input ID space and the mapped ids.
            The mapped IDs will be `None` if for the given date and input ID the
            asset cannot be mapped.
            If mode is `daily-counts`, a DataFrame with `date` and `count`
            columns.
            If mode is `asset-counts`, a DataFrame with `input_asset_id` and `count`
            columns.
            If mode is `latest-name`, a DataFrame with `asset_id` and `name` columns.
        """
        ...

    @abc.abstractmethod
    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
        df_format: DataFrameFormat = "unstacked",
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        start: DateLike, optional
            The start date of the universe to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported, i.e. in `id_types`.
        df_format: DataFrameFormat, optional
            The output format of the returned DataFrame.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range.
        """
        ...


class AssetExposureApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ExposureSettings:
        """
        Returns
        -------
        The settings used to create these exposures.
        """
        ...

    @abc.abstractmethod
    def dates(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        """
        Parameters
        ----------
        universe: str | int | UniverseSettings | AssetUniverseApi
            The universe to use for the exposure calculation.
        range_only: bool, optional
            If True, returns the first and last date only.

        Returns
        -------
        list of all covered dates.
        """

    @abc.abstractmethod
    def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        universe: str | int | UniverseSettings | AssetUniverseApi
            The universe to use for the exposure calculation.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        by: str, optional
            The aggregation, either by date or by asset

        Returns
        -------
        pd.DataFrame
            A dataframe with date index and multi column index where the first
            level is the style name and the second level is the substyle name.
            The values are the counts of the underlying data before it was imputed.
        """

    @abc.abstractmethod
    def get(
        self,
        universe: str | int | UniverseSettings | AssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        universe: str | int | UniverseSettings | AssetUniverseApi
            The universe to use for the exposure calculation.
        start: DateLike, optional
            The start date of the universe to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range with a multi-index where the date
            is the first level and the asset id is the second level.
            The columns are the individual styles.
        """
        ...


class AsyncAssetExposureApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ExposureSettings:
        """
        Returns
        -------
        The settings used to create these exposures.
        """
        ...

    @abc.abstractmethod
    async def dates(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        range_only: bool = False,
    ) -> list[dt.date]:
        """
        Parameters
        ----------
        universe: str | int | UniverseSettings | AssetUniverseApi
            The universe to use for the exposure calculation.
        range_only: bool, optional
            If True, returns the first and last date only.

        Returns
        -------
        list of all covered dates.
        """

    @abc.abstractmethod
    async def coverage_stats(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        id_type: IdType | None = None,
        by: Literal["date", "asset"] = "date",
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        universe: str | int | UniverseSettings | AssetUniverseApi
            The universe to use for the exposure calculation.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.
        by: str, optional
            The aggregation, either by date or by asset

        Returns
        -------
        pd.DataFrame
            A dataframe with date index and multi column index where the first
            level is the style name and the second level is the substyle name.
            The values are the counts of the underlying data before it was imputed.
        """

    @abc.abstractmethod
    async def get(
        self,
        universe: str | int | UniverseSettings | AsyncAssetUniverseApi,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        universe: str | int | UniverseSettings | AssetUniverseApi
            The universe to use for the exposure calculation.
        start: DateLike, optional
            The start date of the universe to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range with a multi-index where the date
            is the first level and the asset id is the second level.
            The columns are the individual styles.
        """
        ...


class ByodApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ByodSettings:
        """
        Returns
        -------
        The settings used to create this byod.
        """
        ...

    @abc.abstractmethod
    def is_uploaded(self) -> bool:
        """
        Returns
        -------
        True if the byod data has been uploaded, False else.
        """
        ...

    @abc.abstractmethod
    def get_raw(self) -> pd.DataFrame:
        """
        Returns
        -------
        The raw uploaded dataframe.
        """
        ...

    @abc.abstractmethod
    def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the processed byod data.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range with a multi-index where the date
            is the first level and the asset id is the second level.
            The columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    def upload(self, df: pd.DataFrame, overwrite: bool = False) -> None:
        """
        Uploads the given byod data if it validates against the settings.

        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame to upload.
        overwrite: bool, optional
            If True, overwrites any existing data
            If False, throws an error if data already exists.
        """
        ...


class AsyncByodApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ByodSettings:
        """
        Returns
        -------
        The settings used to create this byod.
        """
        ...

    @abc.abstractmethod
    async def is_uploaded(self) -> bool:
        """
        Returns
        -------
        True if the byod data has been uploaded, False else.
        """
        ...

    @abc.abstractmethod
    async def get_raw(self) -> pd.DataFrame:
        """
        Returns
        -------
        The raw uploaded dataframe.
        """
        ...

    @abc.abstractmethod
    async def get(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the processed byod data.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range with a multi-index where the date
            is the first level and the asset id is the second level.
            The columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    async def upload(self, df: pd.DataFrame, overwrite: bool = False) -> None:
        """
        Uploads the given byod data if it validates against the settings.

        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame to upload.
        overwrite: bool, optional
            If True, overwrites any existing data
            If False, throws an error if data already exists.
        """
        ...


class FactorRiskModelApi(abc.ABC):

    @abc.abstractmethod
    def dates(self) -> list[dt.date]:
        """
        Returns
        -------
        All dates covered by this risk model.
        """
        pass

    @abc.abstractmethod
    def factors(self, *which: FactorType) -> list[str]:
        """
        Parameters
        ----------
        which: FactorType
            The factor types to return, e.g. `Market`, `Style`, `Industry`, `Region`.
            By default returns all factors.

        Returns
        -------
        list of all factors for the given factor types.
        """
        ...

    @abc.abstractmethod
    def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the risk model exposures for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range with a multi-index where the date
            is the first level and the asset id is the second level.
            The columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the risk model universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the universe inclusion.
        """
        ...

    @abc.abstractmethod
    def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the risk model estimation universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date and the
            columns are the asset id. The values are the estimation universe inclusion.
        """
        ...

    @abc.abstractmethod
    def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the market caps for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset market caps.
        """
        ...

    @abc.abstractmethod
    def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the asset returns for this risk model on the next day.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset returns.
        """
        ...

    @abc.abstractmethod
    def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        estimation_universe: bool, optional
            If True, returns the market stats for the estimation universe.
        industries: bool, optional
            If True, groups the market by industries.
        regions: bool, optional
            If True, groups the market by regions.

        Returns
        -------
        pd.DataFrame
            Descriptive daily stats for this risk model.
        """
        ...

    @abc.abstractmethod
    def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        freq: str, optional
            The frequency of the return aggregation, e.g. `D` for daily.
            Defaults to daily (i.e. unaggregated)
        cumulative: bool, optional
            If True, returns the cumulative returns.
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pd.DataFrame
            The factor returns for the given date range.
        """
        ...

    @abc.abstractmethod
    def fcov(
        self,
        start: DateLike | int | None = -1,
        end: DateLike | None = None,
        dates: list[DateLike] | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        start: DateLike | int, optional
            The start date of the covariance matrix calculation.
            If an integer is given, it is treated as an offset against the `dates` list.
        end: DateLike, optional
            The end date of the covariance matrix calculation.
            If an integer is given, it is treated as an offset against the `dates` list.
        dates: list[DateLike], optional
            The discrete set of dates to calculate the covariance matrix for.
            If given, `start` and `end` are ignored.
            The given dates must exist in `dates`.

        Raises
        ------
        ValueError
            If dates are given but some do not exist in the risk model.

        Returns
        -------
        pd.DataFrame
            A time series of covariance matrices for all dates between given range.
            The index is a multi-index with the date as the first level and the
            factor name as the second level.
        """
        ...

    @abc.abstractmethod
    def t_stats(self) -> pd.DataFrame: ...

    @abc.abstractmethod
    def p_values(self) -> pd.DataFrame: ...

    @abc.abstractmethod
    def r2(self) -> pd.Series: ...

    @abc.abstractmethod
    def sigma2(self) -> pd.Series: ...

    @abc.abstractmethod
    def style_correlation(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pd.DataFrame
            The style correlation matrix for the given date range.
        """
        ...

    @abc.abstractmethod
    def industry_exposures(
        self, start: DateLike | None = None, end: DateLike | None = None
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pd.DataFrame
            The average style exposures grouped by industry.
        """
        ...


class AsyncFactorRiskModelApi(abc.ABC):

    @abc.abstractmethod
    async def dates(self) -> list[dt.date]:
        """
        Returns
        -------
        All dates covered by this risk model.
        """
        pass

    @abc.abstractmethod
    async def factors(self, *which: FactorType) -> list[str]:
        """
        Parameters
        ----------
        which: FactorType
            The factor types to return, e.g. `Market`, `Style`, `Industry`, `Region`.
            By default returns all factors.

        Returns
        -------
        list of all factors for the given factor types.
        """
        ...

    @abc.abstractmethod
    async def exposures(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the risk model exposures for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the universe to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range with a multi-index where the date
            is the first level and the asset id is the second level.
            The columns are the individual styles.
        """
        ...

    @abc.abstractmethod
    async def universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the risk model universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the universe inclusion.
        """
        ...

    @abc.abstractmethod
    async def estimation_universe(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the risk model estimation universe for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date and the
            columns are the asset id. The values are the estimation universe inclusion.
        """
        ...

    @abc.abstractmethod
    async def market_caps(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the market caps for this risk model.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset market caps.
        """
        ...

    @abc.abstractmethod
    async def future_asset_returns(
        self,
        *,
        start: DateLike | None = None,
        end: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the asset returns for this risk model on the next day.

        Parameters
        ----------
        start: DateLike, optional
            The start date of the data to return, inclusive.
        end: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: IdType, optional
            The id type to return asset ids in, e.g. `ticker`.
            The given id type must be supported by the linked universe.

        Raises
        ------
        ValueError
            If the given id type is not supported or date range is invalid.

        Returns
        -------
        pd.DataFrame
            The data for the given date range where the index is the date
            and the columns are the asset id. The values are the asset returns.
        """
        ...

    @abc.abstractmethod
    async def market_stats(
        self,
        estimation_universe: bool = False,
        industries: bool = False,
        regions: bool = False,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        estimation_universe: bool, optional
            If True, returns the market stats for the estimation universe.
        industries: bool, optional
            If True, groups the market by industries.
        regions: bool, optional
            If True, groups the market by regions.

        Returns
        -------
        pd.DataFrame
            Descriptive daily stats for this risk model.
        """
        ...

    @abc.abstractmethod
    async def fret(
        self,
        *,
        freq: str | None = None,
        cumulative: bool = False,
        start: DateLike | None = None,
        end: DateLike | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        freq: str, optional
            The frequency of the return aggregation, e.g. `D` for daily.
            Defaults to daily (i.e. unaggregated)
        cumulative: bool, optional
            If True, returns the cumulative returns.
        start: DateLike, optional
        end: DateLike, optional

        Returns
        -------
        pd.DataFrame
            The factor returns for the given date range.
        """
        ...

    @abc.abstractmethod
    async def t_stats(self) -> pd.DataFrame: ...

    @abc.abstractmethod
    async def p_values(self) -> pd.DataFrame: ...

    @abc.abstractmethod
    async def r2(self) -> pd.Series: ...

    @abc.abstractmethod
    async def sigma2(self) -> pd.Series: ...


class ModelConstructionEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ModelConstructionSettings:
        """
        Returns
        -------
        The modelconstruction settings.
        """
        ...


class AsyncModelConstructionEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ModelConstructionSettings:
        """
        Returns
        -------
        The modelconstruction settings.
        """
        ...


class FactorRiskEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> FactorRiskModelSettings:
        """
        Returns
        -------
        The settings used to create these risk model.
        """
        ...

    @abc.abstractmethod
    def get(self) -> FactorRiskModelApi:
        """

        Returns
        -------
        A built `FactorRiskModelApi` instance for given settings.
        """


class AsyncFactorRiskEngineApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> FactorRiskModelSettings:
        """
        Returns
        -------
        The settings used to create these risk model.
        """
        ...

    @abc.abstractmethod
    async def get(self) -> AsyncFactorRiskModelApi:
        """

        Returns
        -------
        A built `FactorRiskModelApi` instance for given settings.
        """


class PortfolioReportApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ReportSettings:
        """
        Returns
        -------
        The settings used to create this report.
        """
        ...

    @abc.abstractmethod
    def dates(self) -> list[dt.date]: ...

    @abc.abstractmethod
    def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
        add_totals_columns: bool = False,
        serverside: bool = False,
    ) -> pd.DataFrame | DataFrameAccessor: ...


class AsyncPortfolioReportApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> ReportSettings:
        """
        Returns
        -------
        The settings used to create this report.
        """
        ...

    @abc.abstractmethod
    async def dates(self) -> list[dt.date]: ...

    @abc.abstractmethod
    async def get_report(
        self,
        order: dict[str, list[str]],
        *,
        date: DateLike | None = None,
        date_start: DateLike | None = None,
        date_end: DateLike | None = None,
        subtotals: list[str] | None = None,
        serverside: bool = False,
        add_totals_columns: bool = False,
    ) -> pd.DataFrame | AsyncDataFrameAccessor: ...


class BayeslineFactorRiskModelsApi(
    RegistryBasedApi[
        FactorRiskModelSettings, FactorRiskModelSettingsMenu, FactorRiskEngineApi
    ]
): ...


class AsyncBayeslineFactorRiskModelsApi(
    AsyncRegistryBasedApi[
        FactorRiskModelSettings, FactorRiskModelSettingsMenu, AsyncFactorRiskEngineApi
    ]
): ...


class BayeslineModelConstructionApi(
    RegistryBasedApi[
        ModelConstructionSettings,
        ModelConstructionSettingsMenu,
        ModelConstructionEngineApi,
    ],
): ...


class AsyncBayeslineModelConstructionApi(
    AsyncRegistryBasedApi[
        ModelConstructionSettings,
        ModelConstructionSettingsMenu,
        AsyncModelConstructionEngineApi,
    ],
): ...


class BayeslineEquityUniverseApi(
    RegistryBasedApi[UniverseSettings, UniverseSettingsMenu, AssetUniverseApi],
): ...


class AsyncBayeslineEquityUniverseApi(
    AsyncRegistryBasedApi[
        UniverseSettings, UniverseSettingsMenu, AsyncAssetUniverseApi
    ],
): ...


class BayeslineEquityExposureApi(
    RegistryBasedApi[ExposureSettings, ExposureSettingsMenu, AssetExposureApi],
): ...


class AsyncBayeslineEquityExposureApi(
    AsyncRegistryBasedApi[
        ExposureSettings, ExposureSettingsMenu, AsyncAssetExposureApi
    ],
): ...


class BayeslinePortfolioReportApi(
    RegistryBasedApi[ReportSettings, ReportSettingsMenu, PortfolioReportApi],
):

    @abc.abstractmethod
    def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
        dates: list[DateLike] | tuple[DateLike, DateLike] | None = None,
    ) -> PortfolioReportApi: ...


class AsyncBayeslinePortfolioReportApi(
    AsyncRegistryBasedApi[ReportSettings, ReportSettingsMenu, AsyncPortfolioReportApi],
):

    @abc.abstractmethod
    async def load(
        self,
        ref_or_settings: str | int | ReportSettings,
        *,
        hierarchy_ref_or_settings: str | int | PortfolioHierarchySettings | None = None,
        dates: list[DateLike] | tuple[DateLike, DateLike] | None = None,
    ) -> AsyncPortfolioReportApi: ...


class InferAssetIdException(Exception):
    def __init__(self, id_types: list[IdType], id_cols: list[str]):
        self.id_types = id_types
        self.id_cols = id_cols


class BayeslineEquityByodApi(
    RegistryBasedApi[ByodSettings, ByodSettingsMenu, ByodApi],
):

    @abc.abstractmethod
    def load(
        self, ref_or_settings: str | int | ByodSettings, *, name: str | None = None
    ) -> ByodApi: ...

    def portfolios(self) -> dict[str, list[str]]:
        """
        Returns
        -------
        A mapping of byod name to the portfolios that are uploaded
        under this name.
        Note that the portfolio names are not necessarily unique
        and the unique key is formed using the byod name and portfolio name.
        """
        all_settings = self.settings.get_all()
        result = defaultdict(list)
        for name, settings in all_settings.items():
            for portfolio in settings.portfolios:
                result[name].append(portfolio)
        return result

    def styles(self) -> dict[str, dict[str, list[str]]]:
        """
        Returns
        -------
        A mapping of byod name to the style/substyle definitions that
        are uploaded under this name.
        Note that substyle names are not necessarily unique
        and the unique key is formed using the byod name and substyle name.
        """
        return {
            name: settings.styles for name, settings in self.settings.get_all().items()
        }

    def generate_settings(
        self,
        df: pd.DataFrame,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        """
        Infers settings from the given DataFrame, should they be unambiguous.

        To provide hard overrides and skip inference for a given setting use
        the optional parameters.

        Either `portfolios` or `styles` (or both) must be provided.

        The dataframe needs to be given in long format and can contain multiple
        exposure sub-styles and portfolios, as outlined below.
        Date/asset combinations must be unique.

        .. code-block:: csv

            date,asset_id,substyle_1,substyle_2,portfolio_1,portfolio_2
            2020-01-01,A,0.1,0.2,0.3,0.4
            2020-01-01,B,0.1,,0.5,0.6
            2020-01-01,C,,0.3,0.6,0.7

        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame to infer settings from.
        styles: dict[str, list[str]], optional
            The style hierarchy to use for the byod.
            Each sub-style must be assigned to a style.
            Existing styles can be used, unknown style
            values will be treated as new styles.
        portfolios: list[str], optional
            The columns that contain portfolio values.
        date_col: str, optional
            The column name of the date column.
        asset_id_col: str, optional
            The column name of the asset id column.
        asset_id_type: IdType, optional
            The type of the asset id column.
        extra_cols: list[str], optional
            Extra columns to be retained in the dataframe.
            Defaults to all extra columns in the DataFrame.
        description: str, optional
        start_date: DateLike, optional
            The start date of the data to choose for the data which can be after
            the first date in the dataset.
        end_date: DateLike, optional
            The end date of the data to choose for the data which can be before
            the last date in the dataset.

        Returns
        -------
        The inferred settings.
        """
        menu = self.settings.available_settings()
        return self._generate_settings(
            df,
            menu,
            styles=styles,
            portfolios=portfolios,
            date_col=date_col,
            asset_id_col=asset_id_col,
            asset_id_type=asset_id_type,
            extra_cols=extra_cols,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )

    @staticmethod
    def _generate_settings(
        df: pd.DataFrame,
        menu: ByodSettingsMenu,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        columns = df.columns
        portfolios = portfolios or []
        styles = styles or {}

        asset_id_cols = [
            col for col in columns if pd.api.types.is_string_dtype(df[col])
        ]
        date_cols = [
            col for col in columns if pd.api.types.is_datetime64_any_dtype(df[col])
        ]
        numerical_cols = [
            col for col in columns if pd.api.types.is_numeric_dtype(df[col])
        ]

        errors = []
        if asset_id_col and asset_id_col not in asset_id_cols:
            errors.append(f"asset_id_col {asset_id_col} is not a str column in df")

        if not asset_id_cols:
            errors.append("No asset id candidate (str) columns found in df")

        if asset_id_type and asset_id_type not in menu.id_types:
            errors.append(
                f"asset_id_type {asset_id_type} is not in the supported id_types"
            )

        if date_col and date_col not in date_cols:
            errors.append(f"date_col {date_col} is not a date(time) column in df")

        if not date_col and len(date_cols) > 1:
            errors.append("Multiple date columns found, please specify date_col")

        if not date_cols:
            errors.append("No date(time) columns found in df")

        if asset_id_type and asset_id_col:
            id_col = asset_id_col
            id_type = asset_id_type
        else:
            raise InferAssetIdException(
                id_types=[asset_id_type] if asset_id_type else menu.id_types,
                id_cols=[asset_id_col] if asset_id_col else asset_id_cols,
            )

        if id_type is None:
            errors.append("No matching id type found")

        missing_portfolios = set(portfolios) - set(columns) if portfolios else set()
        if missing_portfolios:
            errors.append(
                f"Portfolios contain columns not in df: {', '.join(missing_portfolios)}"
            )

        missing_extra_cols = set(extra_cols) - set(columns) if extra_cols else set()
        if missing_extra_cols:
            errors.append(
                f"Extra cols contain columns not in df: {', '.join(missing_extra_cols)}"
            )

        substyles = [st for sts in styles.values() for st in sts]
        missing_substyles = set(substyles) - set(columns)
        if missing_substyles:
            errors.append(
                f"Styles contain columns not in df: {', '.join(missing_substyles)}"
            )

        if date_cols:
            date_col = date_col or date_cols[0]
            null_dates = df[date_col].isna().sum()
            null_assets = df[asset_id_col].isna().sum()
            if null_dates:
                errors.append(f"There are {null_dates} null values in {date_col}")
            if null_assets:
                errors.append(f"There are {null_assets} null values in {id_col}")

            dupe_date_assets = len(df) != len(
                df.drop_duplicates(subset=[date_col, id_col])
            )
            if dupe_date_assets:
                errors.append(
                    f"There are {dupe_date_assets} duplicate date-asset_id pairs"
                )

        if errors:
            raise ValueError("\n".join(errors))

        min_date = pd.to_datetime(df[date_col].min())  # type: ignore
        start_date = pd.to_datetime(min_date if not start_date else start_date)
        if start_date < min_date:
            raise ValueError(f"start_date {start_date} is before the earliest date")

        max_date = pd.to_datetime(df[date_col].max())  # type: ignore
        end_date = pd.to_datetime(max_date if not end_date else end_date)
        if end_date > max_date:
            raise ValueError(f"end_date {end_date} is after the latest date")

        illegal_portfolios = set(portfolios) - set(numerical_cols)
        if illegal_portfolios:
            raise ValueError(
                f"Portfolios contain non-numeric columns: {', '.join(illegal_portfolios)}"
            )

        illegal_substyles = set(substyles) - set(numerical_cols)
        if illegal_substyles:
            raise ValueError(
                f"Styles contain non-numeric columns: {', '.join(illegal_substyles)}"
            )

        if extra_cols is None:
            existing = (
                [date_col, id_col]
                + portfolios
                + [e for sts in styles.values() for e in sts]
            )
            extra_cols = [col for col in columns if col not in existing]

        return ByodSettings(
            description=description,
            extra_cols=extra_cols,
            date_col=date_col,
            asset_id_col=id_col,
            asset_id_type=id_type,
            styles={k: list(v) for k, v in styles.items()} if styles else {},
            portfolios=list(portfolios) if portfolios else [],
            start_date=start_date,
            end_date=end_date,
        )


class AsyncBayeslineEquityByodApi(
    AsyncRegistryBasedApi[ByodSettings, ByodSettingsMenu, AsyncByodApi],
):
    @abc.abstractmethod
    async def load(
        self, ref_or_settings: str | int | ByodSettings, *, name: str | None = None
    ) -> AsyncByodApi: ...

    async def portfolios(self) -> dict[str, list[str]]:
        """
        Returns
        -------
        A mapping of byod name to the portfolios that are uploaded
        under this name.
        Note that the portfolio names are not necessarily unique
        and the unique key is formed using the byod name and portfolio name.
        """
        all_settings = await self.settings.get_all()
        result = defaultdict(list)
        for name, settings in all_settings.items():
            for portfolio in settings.portfolios:
                result[name].append(portfolio)
        return result

    async def styles(self) -> dict[str, dict[str, list[str]]]:
        """
        Returns
        -------
        A mapping of byod name to the style/substyle definitions that
        are uploaded under this name.
        Note that substyle names are not necessarily unique
        and the unique key is formed using the byod name and substyle name.
        """
        return {
            name: settings.styles
            for name, settings in (await self.settings.get_all()).items()
        }

    @abc.abstractmethod
    async def generate_settings(
        self,
        df: pd.DataFrame,
        *,
        styles: dict[str, list[str]] | None = None,
        portfolios: list[str] | None = None,
        date_col: str | None = None,
        asset_id_col: str | None = None,
        asset_id_type: IdType | None = None,
        extra_cols: list[str] | None = None,
        description: str | None = None,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
    ) -> ByodSettings:
        """
        Infers settings from the given DataFrame, should they be unambiguous.

        To provide hard overrides and skip inference for a given setting use
        the optional parameters.

        Either `portfolios` or `styles` (or both) must be provided.

        The dataframe needs to be given in long format and can contain multiple
        exposure sub-styles and portfolios, as outlined below.
        Date/asset combinations must be unique.

        .. code-block:: csv

            date,asset_id,substyle_1,substyle_2,portfolio_1,portfolio_2
            2020-01-01,A,0.1,0.2,0.3,0.4
            2020-01-01,B,0.1,,0.5,0.6
            2020-01-01,C,,0.3,0.6,0.7

        Parameters
        ----------
        df: pd.DataFrame
            The DataFrame to infer settings from.
        styles: dict[str, list[str]], optional
            The style hierarchy to use for the byod.
            Each sub-style must be assigned to a style.
            Existing styles can be used, unknown style
            values will be treated as new styles.
        portfolios: list[str], optional
            The columns that contain portfolio values.
        date_col: str, optional
            The column name of the date column.
        asset_id_col: str, optional
            The column name of the asset id column.
        asset_id_type: IdType, optional
            The type of the asset id column.
        extra_cols: list[str], optional
            Extra columns to be retained in the dataframe.
            Defaults to all extra columns in the DataFrame.
        description: str, optional
        start_date: DateLike, optional
            The start date of the data to choose for the data which can be after
            the first date in the dataset.
        end_date: DateLike, optional
            The end date of the data to choose for the data which can be before
            the last date in the dataset.

        Returns
        -------
        The inferred settings.
        """
        menu = await self.settings.available_settings()
        return BayeslineEquityByodApi._generate_settings(
            df,
            menu,
            styles=styles,
            portfolios=portfolios,
            date_col=date_col,
            asset_id_col=asset_id_col,
            asset_id_type=asset_id_type,
            extra_cols=extra_cols,
            description=description,
            start_date=start_date,
            end_date=end_date,
        )


class PortfolioHierarchyApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> PortfolioHierarchySettings:
        """
        Returns
        -------
        The settings used to create this hierarchy.
        """
        ...

    @abc.abstractmethod
    def get_id_types(self) -> dict[str, list[IdType]]:
        """
        Returns
        -------
        dict[str, list[IdType]]:
            The available ID types that at least a portion of assets can be mapped
            to for each portfolio.
            If a portfolio has a benchmark then the available id types are those
            that are available for both the portfolio and the benchmark.
        """

    @abc.abstractmethod
    def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        """
        Parameters
        ----------
        collapse: bool, optional
            If True, will calculate aggregations `any` and `all`, indicating
            of for a given date, any (or all) portfolios have holdings.

        Returns
        -------
        A dict of portfolio-id to dates for which this hierarchy can be produced.
        For a given portfolio and date, the hierarchy can be produced if
        the portfolio has holdings for that date. If a benchmark is given then
        this benchmark also must have holdings for the given date.
        """

    @abc.abstractmethod
    def get(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame: ...


class AsyncPortfolioHierarchyApi(abc.ABC):

    @property
    @abc.abstractmethod
    def settings(self) -> PortfolioHierarchySettings:
        """
        Returns
        -------
        The settings used to create this hierarchy.
        """
        ...

    @abc.abstractmethod
    async def get_id_types(self) -> dict[str, list[IdType]]:
        """
        Returns
        -------
        dict[str, list[IdType]]:
            The available ID types that at least a portion of assets can be mapped
            to for each portfolio.
            If a portfolio has a benchmark then the available id types are those
            that are available for both the portfolio and the benchmark.
        """

    @abc.abstractmethod
    async def get_dates(self, *, collapse: bool = False) -> dict[str, list[dt.date]]:
        """
        Parameters
        ----------
        collapse: bool, optional
            If True, will calculate aggregations `any` and `all`, indicating
            of for a given date, any (or all) portfolios have holdings.

        Returns
        -------
        A dict of portfolio-id to dates for which this hierarchy can be produced.
        For a given portfolio and date, the hierarchy can be produced if
        the portfolio has holdings for that date. If a benchmark is given then
        this benchmark also must have holdings for the given date.
        """

    @abc.abstractmethod
    async def get(
        self,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: IdType | None = None,
    ) -> pd.DataFrame: ...


class BayeslinePortfolioHierarchyApi(
    RegistryBasedApi[
        PortfolioHierarchySettings,
        PortfolioHierarchySettingsMenu,
        PortfolioHierarchyApi,
    ]
): ...


class AsyncBayeslinePortfolioHierarchyApi(
    AsyncRegistryBasedApi[
        PortfolioHierarchySettings,
        PortfolioHierarchySettingsMenu,
        AsyncPortfolioHierarchyApi,
    ]
): ...


class BayeslineEquityPortfolioApi(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    def get_id_types(self) -> dict[str, list[IdType]]:
        """
        Returns
        -------
        dict[str, list[IdType]]:
            The available ID types that at least a portion of assets can be mapped
            to for each portfolio.
        """

    @abc.abstractmethod
    def get_coverage(
        self,
        names: str | list[str] | None = None,
        by: Literal["date", "asset"] = "date",
        stats: list[str] | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        names: str | list[str], optional
            The names of the portfolios.
        by: str, optional
            The coverage aggregation, either by date or by asset.
        stats: list[str], optional
            list of 'min', 'max', 'mean', collapses `by` into these stats.

        Returns
        -------
        pd.DataFrame:
            The coverage count for each id type.
            If no portfolio name is given all portfolios will be calculated.
            The index columns are `portfolio_group` and `portolio` will be the first
            two levels of the index unless `names` is a `str` (ie. single portfolio).
            If `stats` given, collapses the `by` index to the given aggregations.
        """

    @abc.abstractmethod
    def get_portfolio_names(self) -> list[str]: ...

    @abc.abstractmethod
    def get_portfolio_groups(self) -> dict[str, list[str]]: ...

    @abc.abstractmethod
    def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]: ...

    @abc.abstractmethod
    def get_portfolio(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: str | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the portfolios for the given names between given start and end dates.

        Parameters
        ----------
        names: list[str] | str
            The list of portfolio names.
        start_date: DateLike, optional
            The start date of the data to return, inclusive.
        end_date: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: str, optional
            id type to return the portfolio holdings in.

        Returns
        -------
        pd.DataFrame:
            A dataframe with columns `portfolio_group`, `portfolio`, `date`,
            `input_asset_id`, `input_asset_id_type`, `asset_id`, `asset_id_type` and
            `value`.

            If no `id_type` is given then the input ID space will be used unmapped. In
            this case the columns `asset_id`, `asset_id_type` will not be returned.
        """


class AsyncBayeslineEquityPortfolioApi(abc.ABC):

    @property
    @abc.abstractmethod
    def name(self) -> str: ...

    @abc.abstractmethod
    async def get_id_types(self) -> dict[str, list[IdType]]:
        """
        Returns
        -------
        dict[str, list[IdType]]:
            The available ID types that at least a portion of assets can be mapped
            to for each portfolio.
        """

    @abc.abstractmethod
    async def get_coverage(
        self,
        names: str | list[str] | None = None,
        by: Literal["date", "asset"] = "date",
        stats: list[str] | None = None,
    ) -> pd.DataFrame:
        """
        Parameters
        ----------
        names: str | list[str], optional
            The names of the portfolios.
        by: str, optional
            The coverage aggregation, either by date or by asset.
        stats: list[str], optional
            list of 'min', 'max', 'mean', collapses `by` into these stats.

        Returns
        -------
        pd.DataFrame:
            The dated coverage count for each id type.
            If no portfolio name is given all portfolios will be calculated.
            The index columns are `portfolio_group` and `portolio` will be the first
            two levels of the index unless `names` is a `str` (ie. single portfolio).
            If `stats` given, collapses the `by` index to the given aggregations.
        """

    @abc.abstractmethod
    async def get_portfolio_names(self) -> list[str]: ...

    @abc.abstractmethod
    async def get_portfolio_groups(self) -> dict[str, list[str]]: ...

    @abc.abstractmethod
    async def get_dates(
        self, names: list[str] | str | None = None, *, collapse: bool = False
    ) -> dict[str, list[dt.date]]: ...

    @abc.abstractmethod
    async def get_portfolio(
        self,
        names: list[str] | str,
        start_date: DateLike | None = None,
        end_date: DateLike | None = None,
        id_type: str | None = None,
    ) -> pd.DataFrame:
        """
        Obtains the portfolios for the given names between given start and end dates.

        Parameters
        ----------
        names: list[str] | str
            The list of portfolio names.
        start_date: DateLike, optional
            The start date of the data to return, inclusive.
        end_date: DateLike, optional
            The end date of the data to return, inclusive.
        id_type: str, optional
            id type to return the portfolio holdings in.

        Returns
        -------
        pd.DataFrame:
            A dataframe with columns `portfolio_group`, `portfolio`, `date`,
            `input_asset_id`, `input_asset_id_type`, `asset_id`, `asset_id_type` and
            `value`.

            If no `id_type` is given then the input ID space will be used unmapped. In
            this case the columns `asset_id`, `asset_id_type` will not be returned.
        """


class BayeslineEquityApi(abc.ABC):

    @property
    @abc.abstractmethod
    def universes(self) -> BayeslineEquityUniverseApi: ...

    @property
    @abc.abstractmethod
    def exposures(self) -> BayeslineEquityExposureApi: ...

    @property
    @abc.abstractmethod
    def modelconstruction(self) -> BayeslineModelConstructionApi: ...

    @property
    @abc.abstractmethod
    def riskmodels(self) -> BayeslineFactorRiskModelsApi: ...

    @property
    @abc.abstractmethod
    def portfoliohierarchy(self) -> BayeslinePortfolioHierarchyApi: ...

    @property
    @abc.abstractmethod
    def portfolioreport(self) -> BayeslinePortfolioReportApi: ...

    @property
    @abc.abstractmethod
    def byod(self) -> BayeslineEquityByodApi: ...

    @property
    @abc.abstractmethod
    def portfolios(self) -> BayeslineEquityPortfolioApi: ...


class AsyncBayeslineEquityApi(abc.ABC):

    @property
    @abc.abstractmethod
    def universes(self) -> AsyncBayeslineEquityUniverseApi: ...

    @property
    @abc.abstractmethod
    def exposures(self) -> AsyncBayeslineEquityExposureApi: ...

    @property
    @abc.abstractmethod
    def modelconstruction(self) -> AsyncBayeslineModelConstructionApi: ...

    @property
    @abc.abstractmethod
    def riskmodels(self) -> AsyncBayeslineFactorRiskModelsApi: ...

    @property
    @abc.abstractmethod
    def portfoliohierarchy(self) -> AsyncBayeslinePortfolioHierarchyApi: ...

    @property
    @abc.abstractmethod
    def portfolioreport(self) -> AsyncBayeslinePortfolioReportApi: ...

    @property
    @abc.abstractmethod
    def byod(self) -> AsyncBayeslineEquityByodApi: ...

    @property
    @abc.abstractmethod
    def portfolios(self) -> AsyncBayeslineEquityPortfolioApi: ...
