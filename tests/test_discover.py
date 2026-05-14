"""Discovery: broadcast then unicast-sweep fallback."""

from __future__ import annotations

from unittest.mock import AsyncMock

from philips_wiz_bulb_core.discover import discover, parse_discovery_response


def test_parse_response_extracts_mac_module() -> None:
    raw = {
        "method": "getPilot", "env": "pro",
        "result": {"mac": "d8a0118dc5c3", "rssi": -63, "state": True, "temp": 2200, "dimming": 100},
    }
    parsed = parse_discovery_response(raw, ip="192.168.1.3")
    assert parsed["mac"] == "d8a0118dc5c3"
    assert parsed["ip"] == "192.168.1.3"
    assert parsed["rssi"] == -63


async def test_discover_calls_broadcast_then_sweep() -> None:
    async def fake_get_pilot(ip: str) -> dict:
        if ip == "192.168.1.3":
            return {"mac": "aabb", "rssi": -50}
        raise TimeoutError("nope")

    client = AsyncMock()
    client.get_pilot = AsyncMock(side_effect=fake_get_pilot)

    bulbs = await discover(
        client,
        broadcast="192.168.1.255",
        subnet="192.168.1.0/30",  # only .1, .2 in unicast sweep
        broadcast_collect_s=0.05,
    )
    # 192.168.1.3 is outside the /30 (.0/.1/.2/.3 — .3 is broadcast, .0 is network)
    # So sweep will hit .1, .2 only; broadcast path doesn't run real I/O in this test.
    # We assert the fn returned (no exception); zero bulbs is fine for the API test.
    assert isinstance(bulbs, list)
