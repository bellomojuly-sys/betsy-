"""Forecasts ingredient usage for the next planning horizon."""

from __future__ import annotations

from betsy.agents import topics
from betsy.core import Agent, Message, MessageBus


class ForecastAgent(Agent):
    subscriptions = (topics.CYCLE_START,)

    def __init__(self, name: str, bus: MessageBus, avg_daily_usage: dict[str, float]) -> None:
        super().__init__(name, bus)
        self.avg_daily_usage = avg_daily_usage

    def handle(self, message: Message) -> None:
        horizon = int(message.payload.get("horizon_days", 3))
        # TODO: replace naive average with a real model (seasonality, reservations, events...)
        forecast = {sku: rate * horizon for sku, rate in self.avg_daily_usage.items()}
        self.send(topics.FORECAST_READY, {"horizon_days": horizon, "usage": forecast})
