from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

import polars as pl
from polars.plugins import register_plugin_function

from polars_distance._internal import __version__ as __version__

if TYPE_CHECKING:
    from polars_distance.typing import IntoExprColumn

LIB = Path(__file__).parent


def distance(lat_a: IntoExprColumn, lng_a: IntoExprColumn, lat_b: IntoExprColumn, lng_b: IntoExprColumn) -> pl.Expr:
    return register_plugin_function(
        args=[lat_a, lng_a, lat_b, lng_b],
        plugin_path=LIB,
        function_name="distance",
        is_elementwise=True
    )
