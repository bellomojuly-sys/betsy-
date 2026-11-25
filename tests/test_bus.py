from betsy.core import Message, MessageBus


def test_broadcast_and_direct_delivery():
    bus = MessageBus()
    received: dict[str, list[str]] = {"a": [], "b": []}
    bus.subscribe("t", "a", lambda m: received["a"].append(m.id))
    bus.subscribe("t", "b", lambda m: received["b"].append(m.id))

    bus.publish(Message(topic="t", sender="x"))
    bus.publish(Message(topic="t", sender="x", recipient="b"))
    assert bus.run_until_idle() == 2

    assert len(received["a"]) == 1
    assert len(received["b"]) == 2
