"""Domain model shared by all agents."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import date


@dataclass(frozen=True)
class Ingredient:
    sku: str
    name: str
    unit: str  # e.g. "kg", "l", "pcs"
    perishable: bool = False


@dataclass
class StockLevel:
    sku: str
    on_hand: float
    reorder_point: float
    target_level: float


@dataclass(frozen=True)
class Supplier:
    id: str
    name: str
    lead_time_days: int
    min_order_value: float = 0.0


@dataclass(frozen=True)
class Offer:
    supplier_id: str
    sku: str
    unit_price: float
    available_qty: float


@dataclass(frozen=True)
class OrderLine:
    sku: str
    quantity: float
    unit_price: float

    @property
    def total(self) -> float:
        return self.quantity * self.unit_price


@dataclass
class PurchaseOrder:
    supplier_id: str
    lines: list[OrderLine] = field(default_factory=list)
    delivery_date: date | None = None

    @property
    def total(self) -> float:
        return sum(line.total for line in self.lines)
