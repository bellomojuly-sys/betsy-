# betsy-
Multi-agent procurement system for restaurants (Fontys MA-AAI personal project)

## Project layout

```
src/betsy/
  core/        message envelope, pub/sub bus, base Agent class
  agents/      Forecast, Inventory, Procurement, Supplier agents + bus topics
  models/      domain model (Ingredient, StockLevel, Supplier, Offer, PurchaseOrder)
  data.py      scenario loader (JSON)
  main.py      CLI: runs one procurement cycle
data/          sample scenarios
docs/          architecture notes
tests/         pytest suite
```

See [docs/architecture.md](docs/architecture.md) for the agent design.

## Getting started

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

betsy                                  # run one cycle on data/sample_scenario.json
betsy --scenario path/to/file.json --horizon 5

pytest
ruff check .
```
