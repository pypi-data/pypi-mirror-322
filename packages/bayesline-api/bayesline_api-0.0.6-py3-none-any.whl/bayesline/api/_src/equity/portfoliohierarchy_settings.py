from collections import Counter
from itertools import pairwise

import pandas as pd
from pydantic import BaseModel, Field, field_validator, model_validator

from bayesline.api._src.registry import SettingsMenu


class PortfolioHierarchySettings(BaseModel, frozen=True, extra="forbid"):
    """
    Specifies portfolio hierarchies with arbitrary groupings (e.g. manager, etc.).
    """

    groupings: dict[str, list[str]] = Field(default_factory=dict)
    portfolio_ids: list[str]
    benchmark_ids: list[str | None]

    @classmethod
    def from_pandas(
        cls: type["PortfolioHierarchySettings"],
        df: pd.DataFrame,
    ) -> "PortfolioHierarchySettings":
        """
        Creates a portfolio hierarchy from a dataframe.

        Must contain a column `portfolio_id` and optionally `benchmark_id`.
        Every other column is interpreted as a grouping. 0 groupings are allowed.
        Index is ignored.

        Parameters
        -----------
            df: pd.DataFrame: The dataframe to create the hierarchy from.

        Returns
        -------
        Pydantic object representing the hierarchy.
        """
        if "portfolio_id" not in df.columns:
            raise ValueError("portfolio_id column not found in the dataframe.")

        groupings = {
            col: df[col].tolist()
            for col in df.columns
            if col not in {"portfolio_id", "benchmark_id"}
        }
        portfolio_ids = df["portfolio_id"].tolist()

        if "benchmark_id" not in df.columns:
            benchmark_ids = [None] * len(portfolio_ids)
        else:
            benchmark_ids = df["benchmark_id"].tolist()

        return cls(
            groupings=groupings,
            portfolio_ids=portfolio_ids,
            benchmark_ids=benchmark_ids,
        )

    def to_pandas(self) -> pd.DataFrame:
        """
        Converts the hierarchy to a pandas dataframe.

        The last two columns are the portfolio and benchmark IDs.
        Every column before that is a grouping. 0 groupings are possible.

        Returns
        -------
        pd.DataFrame: The dataframe representation of the hierarchy.
        """
        df = pd.DataFrame(self.groupings)
        df["portfolio_id"] = self.portfolio_ids
        df["benchmark_id"] = self.benchmark_ids
        return df

    @field_validator("portfolio_ids")
    def _validate_portfolio_ids(
        cls: type["PortfolioHierarchySettings"], v: list[str]
    ) -> list[str]:
        if not v:
            raise ValueError("Portfolio IDs must be non-empty.")

        duplicates = [item for item, count in Counter(v).items() if count > 1]
        if duplicates:
            raise ValueError(
                "Portfolio IDs must be unique. "
                f"Found duplicates: {', '.join(duplicates)}"
            )

        if any(p is None or p.strip() == "" for p in v):
            raise ValueError("Portfolio IDs must be non-empty strings.")

        return v

    @field_validator("portfolio_ids")
    def _validate_benchmark_ids(
        cls: type["PortfolioHierarchySettings"], v: list[str]
    ) -> list[str]:
        if not v:
            raise ValueError("Benchmark IDs must be non-empty.")
        return v

    @field_validator("groupings")
    def _validate_groupings(
        cls: type["PortfolioHierarchySettings"], v: dict[str, list[str]]
    ) -> dict[str, list[str]]:
        if not all(len(v1) == len(v2) for v1, v2 in pairwise(v.values())):
            raise ValueError(f"Groupings must have the same length. {v}")

        groups_with_nulls = []
        for group, values in v.items():
            if any(e is None for e in values):
                groups_with_nulls.append(group)
        if groups_with_nulls:
            raise ValueError(
                f"Groupings must not contain null values. Found in: {groups_with_nulls}"
            )

        return v

    @model_validator(mode="after")
    def _validate_dimensions(self) -> "PortfolioHierarchySettings":
        if len(self.portfolio_ids) != len(self.benchmark_ids):
            raise ValueError(
                "Portfolio IDs and benchmark IDs must have the same length."
            )

        n = len(self.portfolio_ids)
        mismatches = [g for g in self.groupings.values() if len(g) != n]
        if len(mismatches) > 0:
            raise ValueError(
                "Portfolio IDs, benchmark IDs and groups must have the same length. "
                f"Found mismatches: {mismatches}"
            )
        return self


class PortfolioHierarchySettingsMenu(
    SettingsMenu[PortfolioHierarchySettings], frozen=True, extra="forbid"
):
    """
    Specifies the set of available portfolios that can be used to create hierarchies.
    """

    portfolio_ids: set[str] = Field(
        default_factory=set,
        description="Set of available portfolio IDs that can be used in hierarchies.",
    )

    def describe(self, settings: PortfolioHierarchySettings | None = None) -> str:
        if settings is None:
            return f"Available Portfolios: {sorted(self.portfolio_ids)}"
        else:
            df = settings.to_pandas()
            df["portfolio_id"] = df["portfolio_id"].map(
                lambda x: f"[{x}]" if x not in self.portfolio_ids else x
            )
            df["benchmark_id"] = df["benchmark_id"].map(
                lambda x: (
                    f"[{x}]" if x is not None and x not in self.portfolio_ids else x
                )
            )
            return f"""Missing portfolios are enclosed in brackets.
            
{df.to_string()}"""

    def validate_settings(self, settings: PortfolioHierarchySettings) -> None:
        available_portfolio_ids = set(self.portfolio_ids)
        portfolio_ids = set(settings.portfolio_ids)
        benchmark_ids = {b for b in settings.benchmark_ids if b is not None}

        if not portfolio_ids.issubset(available_portfolio_ids):
            raise ValueError(
                f"There are unknown portfolio ids. "
                f"Unknown: {portfolio_ids - available_portfolio_ids}"
            )

        if not benchmark_ids.issubset(available_portfolio_ids):
            raise ValueError(
                f"There are unknown benchmark ids. "
                f"Unknown: {benchmark_ids - available_portfolio_ids}"
            )
