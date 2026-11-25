"""Run one procurement cycle on a scenario file."""

from __future__ import annotations

import argparse
import logging
import os
from pathlib import Path

from betsy.agents import ForecastAgent, InventoryAgent, ProcurementAgent, SupplierAgent, topics
from betsy.core import Message, MessageBus
from betsy.data import load_scenario

DEFAULT_SCENARIO = Path(__file__).resolve().parents[2] / "data" / "sample_scenario.json"


def build_system(scenario_path: str | Path) -> tuple[MessageBus, ProcurementAgent]:
    scenario = load_scenario(scenario_path)
    bus = MessageBus()
    ForecastAgent("forecast", bus, scenario.avg_daily_usage)
    InventoryAgent("inventory", bus, scenario.stock)
    for supplier, catalog in scenario.suppliers:
        SupplierAgent(f"supplier:{supplier.id}", bus, supplier, catalog)
    procurement = ProcurementAgent("procurement", bus, expected_suppliers=len(scenario.suppliers))
    return bus, procurement


def run_cycle(bus: MessageBus, horizon_days: int = 3) -> None:
    bus.publish(
        Message(topic=topics.CYCLE_START, sender="system", payload={"horizon_days": horizon_days})
    )
    bus.run_until_idle()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--scenario", default=str(DEFAULT_SCENARIO))
    parser.add_argument("--horizon", type=int, default=3, help="planning horizon in days")
    args = parser.parse_args()

    logging.basicConfig(
        level=os.getenv("BETSY_LOG_LEVEL", "INFO"), format="%(levelname)s %(name)s: %(message)s"
    )
    bus, procurement = build_system(args.scenario)
    run_cycle(bus, args.horizon)

    for msg in bus.history:
        print(f"[{msg.topic:<20}] {msg.sender:<22} -> {msg.recipient or '*'}")
    print()
    for order in procurement.orders:
        print(f"Order to {order.supplier_id}: EUR {order.total:.2f}")
        for line in order.lines:
            print(f"  - {line.sku}: {line.quantity} @ {line.unit_price}")


if __name__ == "__main__":
    main()
