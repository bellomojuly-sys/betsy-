"""Coordinates sourcing: requests quotes, compares them, places orders."""

from __future__ import annotations

from collections import defaultdict

from betsy.agents import topics
from betsy.core import Agent, Message, MessageBus
from betsy.models import Offer, OrderLine, PurchaseOrder


class ProcurementAgent(Agent):
    subscriptions = (topics.PROCUREMENT_REQUEST, topics.QUOTE)

    def __init__(self, name: str, bus: MessageBus, expected_suppliers: int) -> None:
        super().__init__(name, bus)
        self.expected_suppliers = expected_suppliers
        self._needs: dict[str, float] = {}
        self._quotes: list[dict] = []
        self.orders: list[PurchaseOrder] = []

    def handle(self, message: Message) -> None:
        if message.topic == topics.PROCUREMENT_REQUEST:
            self._needs = dict(message.payload["needs"])
            self._quotes = []
            self.send(topics.RFQ, {"needs": self._needs})
        elif message.topic == topics.QUOTE:
            self._quotes.append(message.payload)
            if len(self._quotes) >= self.expected_suppliers:
                self._decide()

    def _decide(self) -> None:
        # TODO: multi-criteria selection / negotiation (lead time, quality, sustainability...)
        offers = [
            Offer(q["supplier_id"], o["sku"], o["unit_price"], o["available_qty"])
            for q in self._quotes
            for o in q["offers"]
        ]
        by_supplier: dict[str, list[OrderLine]] = defaultdict(list)
        for sku, qty in self._needs.items():
            remaining = qty
            for offer in sorted((o for o in offers if o.sku == sku), key=lambda o: o.unit_price):
                if remaining <= 0:
                    break
                take = min(remaining, offer.available_qty)
                if take > 0:
                    by_supplier[offer.supplier_id].append(OrderLine(sku, take, offer.unit_price))
                    remaining -= take
            if remaining > 0:
                self.log.warning("could not fully source %s (missing %.2f)", sku, remaining)

        for supplier_id, lines in by_supplier.items():
            order = PurchaseOrder(supplier_id=supplier_id, lines=lines)
            self.orders.append(order)
            self.send(
                topics.ORDER_PLACED,
                {
                    "supplier_id": supplier_id,
                    "lines": [(line.sku, line.quantity, line.unit_price) for line in lines],
                    "total": round(order.total, 2),
                },
            )
