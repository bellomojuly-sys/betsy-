"""Represents one supplier and answers requests for quotation."""

from __future__ import annotations

from betsy.agents import topics
from betsy.core import Agent, Message, MessageBus
from betsy.models import Supplier


class SupplierAgent(Agent):
    subscriptions = (topics.RFQ,)

    def __init__(
        self, name: str, bus: MessageBus, supplier: Supplier, catalog: dict[str, dict[str, float]]
    ) -> None:
        super().__init__(name, bus)
        self.supplier = supplier
        self.catalog = catalog  # sku -> {"unit_price": ..., "available_qty": ...}

    def handle(self, message: Message) -> None:
        needs: dict[str, float] = message.payload["needs"]
        offers = [
            {
                "sku": sku,
                "unit_price": self.catalog[sku]["unit_price"],
                "available_qty": min(qty, self.catalog[sku]["available_qty"]),
            }
            for sku, qty in needs.items()
            if sku in self.catalog
        ]
        self.send(
            topics.QUOTE,
            {
                "supplier_id": self.supplier.id,
                "lead_time_days": self.supplier.lead_time_days,
                "offers": offers,
            },
            recipient=message.sender,
        )
