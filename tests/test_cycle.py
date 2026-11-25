from betsy.main import DEFAULT_SCENARIO, build_system, run_cycle


def test_full_cycle_places_orders_for_short_items():
    bus, procurement = build_system(DEFAULT_SCENARIO)
    run_cycle(bus, horizon_days=3)

    ordered: dict[str, float] = {}
    for order in procurement.orders:
        for line in order.lines:
            ordered[line.sku] = ordered.get(line.sku, 0) + line.quantity

    # Flour stays above its reorder point (40 - 3*6 = 22 >= 20), so it is not ordered.
    assert set(ordered) == {"TOM", "MOZ", "OIL"}
    assert ordered["TOM"] == 29  # target 25 - projected (8 - 12)


def test_cheapest_supplier_is_used_first():
    bus, procurement = build_system(DEFAULT_SCENARIO)
    run_cycle(bus, horizon_days=3)
    metro = next(o for o in procurement.orders if o.supplier_id == "metro-wholesale")
    tom = next(line for line in metro.lines if line.sku == "TOM")
    assert tom.quantity == 12  # all of Metro's cheaper stock is taken first
