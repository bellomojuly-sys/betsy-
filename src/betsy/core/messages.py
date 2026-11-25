"""Message envelope exchanged between agents."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime
from typing import Any


@dataclass(frozen=True)
class Message:
    topic: str
    sender: str
    payload: dict[str, Any] = field(default_factory=dict)
    recipient: str | None = None  # None = broadcast to topic subscribers
    id: str = field(default_factory=lambda: uuid.uuid4().hex)
    timestamp: datetime = field(default_factory=lambda: datetime.now(UTC))
