import datetime as dt
from typing import Any, Literal

import pandas as pd

IdType = Literal[
    "bayesid",
    "ticker",
    "composite_figi",
    "cik",
    "cusip8",
    "cusip9",
    "isin",
    "sedol",
    "name",
]
DateLike = str | dt.date | dt.datetime | pd.Timestamp
DataFrameFormat = Literal["unstacked", "stacked"]
DNFFilterExpression = tuple[str, str, Any]
DNFFilterExpressions = list[DNFFilterExpression | list[DNFFilterExpression]]
