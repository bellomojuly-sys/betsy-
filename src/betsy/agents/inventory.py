"""Tracks stock and turns forecasts into replenishment needs."""

from __future__ import annotations

from betsy.agents import topics
from betsy.core import Agent, Message, MessageBus
from betsy.models import StockLevel


class InventoryAgent(Agent):
    subscriptions = (topics.FORECAST_READY,)

    def __init__(self, name: str, bus: MessageBus, stock: dict[str, StockLevel]) -> None:
        super().__init__(name, bus)
        self.stock = stock

    def handle(self, message: Message) -> None:
        usage: dict[str, float] = message.payload["usage"]
        needs: dict[str, float] = {}
        for sku, level in self.stock.items():
            projected = level.on_hand - usage.get(sku, 0.0)
            if projected < level.reorder_point:
                needs[sku] = round(level.target_level - projected, 3)
        self.log.info("needs: %s", needs)
        if needs:
            self.send(topics.PROCUREMENT_REQUEST, {"needs": needs})
