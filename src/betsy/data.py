"""Load scenario data (stock, usage, suppliers) from JSON."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from betsy.models import Ingredient, StockLevel, Supplier


@dataclass
class Scenario:
    ingredients: dict[str, Ingredient]
    stock: dict[str, StockLevel]
    avg_daily_usage: dict[str, float]
    suppliers: list[tuple[Supplier, dict[str, dict[str, float]]]]


def load_scenario(path: str | Path) -> Scenario:
    raw = json.loads(Path(path).read_text())
    ingredients = {i["sku"]: Ingredient(**i) for i in raw["ingredients"]}
    stock = {s["sku"]: StockLevel(**s) for s in raw["stock"]}
    suppliers = [
        (Supplier(**{k: v for k, v in s.items() if k != "catalog"}), s["catalog"])
        for s in raw["suppliers"]
    ]
    return Scenario(ingredients, stock, raw["avg_daily_usage"], suppliers)
