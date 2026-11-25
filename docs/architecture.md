# Architecture

Betsy is a set of autonomous agents that communicate only through messages on a
publish/subscribe bus (`betsy.core.MessageBus`). No agent calls another directly,
so agents can be replaced (rule-based → ML → LLM) or distributed independently.

## Agents

| Agent              | Listens to                  | Publishes             | Responsibility                               |
|--------------------|-----------------------------|-----------------------|----------------------------------------------|
| `ForecastAgent`    | `cycle.start`               | `forecast.ready`      | Predict ingredient usage over the horizon    |
| `InventoryAgent`   | `forecast.ready`            | `procurement.request` | Compare projected stock to reorder points    |
| `ProcurementAgent` | `procurement.request`, `quote` | `rfq`, `order.placed` | Request quotes, select offers, place orders |
| `SupplierAgent` ×N | `rfq`                       | `quote` (direct)      | Represent one supplier and its catalog       |

## One procurement cycle

```
system ──cycle.start──▶ Forecast ──forecast.ready──▶ Inventory ──procurement.request──▶ Procurement
                                                                                          │ rfq (broadcast)
                                                                         ┌────────────────┴───────────┐
                                                                    Supplier A                   Supplier B
                                                                         └──quote──▶ Procurement ◀──quote┘
                                                                                          │
                                                                                   order.placed
```

## Extension points (TODO)

- **Forecasting**: replace the naive daily average with a model (seasonality, reservations, weather, events).
- **Supplier selection / negotiation**: multi-criteria scoring (price, lead time, quality, sustainability),
  minimum order values, counter-offers.
- **LLM agents**: e.g. parse supplier emails/price lists, explain decisions to the chef.
- **Bus**: async or networked transport (asyncio, Redis, MQTT) behind the same interface.
- **Persistence**: store stock, orders and message history.
