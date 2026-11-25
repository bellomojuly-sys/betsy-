"""Base class for all Betsy agents."""

from __future__ import annotations

import logging
from typing import Any

from betsy.core.bus import MessageBus
from betsy.core.messages import Message


class Agent:
    """An agent subscribes to topics on the bus and reacts to messages.

    Subclasses declare `subscriptions` and implement `handle`.
    """

    subscriptions: tuple[str, ...] = ()

    def __init__(self, name: str, bus: MessageBus) -> None:
        self.name = name
        self.bus = bus
        self.log = logging.getLogger(f"betsy.{name}")
        for topic in self.subscriptions:
            bus.subscribe(topic, name, self.handle)

    def send(self, topic: str, payload: dict[str, Any], recipient: str | None = None) -> None:
        self.bus.publish(
            Message(topic=topic, sender=self.name, payload=payload, recipient=recipient)
        )

    def handle(self, message: Message) -> None:  # pragma: no cover - abstract
        raise NotImplementedError
