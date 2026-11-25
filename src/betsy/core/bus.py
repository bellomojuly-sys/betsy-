"""Minimal synchronous in-memory publish/subscribe bus.

Swap for an async or networked implementation later without changing agents.
"""

from __future__ import annotations

from collections import defaultdict, deque
from collections.abc import Callable

from betsy.core.messages import Message

Handler = Callable[[Message], None]


class MessageBus:
    def __init__(self) -> None:
        self._subscribers: dict[str, list[tuple[str, Handler]]] = defaultdict(list)
        self._queue: deque[Message] = deque()
        self.history: list[Message] = []

    def subscribe(self, topic: str, agent_name: str, handler: Handler) -> None:
        self._subscribers[topic].append((agent_name, handler))

    def publish(self, message: Message) -> None:
        self._queue.append(message)

    def run_until_idle(self, max_steps: int = 1000) -> int:
        """Deliver queued messages until the queue is empty. Returns messages delivered."""
        steps = 0
        while self._queue and steps < max_steps:
            message = self._queue.popleft()
            self.history.append(message)
            for name, handler in self._subscribers.get(message.topic, []):
                if message.recipient is None or message.recipient == name:
                    handler(message)
            steps += 1
        return steps
