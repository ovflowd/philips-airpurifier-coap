"""AC3737 mode readback while humidifying, against the device statuses from #356."""

from unittest.mock import MagicMock

import pytest

from custom_components.philips_airpurifier_coap.const import PhilipsApi
from custom_components.philips_airpurifier_coap.philips import PhilipsAC3737

MEASURED = {
    "auto": {"D03102": 1, "D03105": 100, "D03106": 0, "D0310A": 4, "D0310C": 0, "D0310D": 5},
    "sleep": {"D03102": 1, "D03105": 0, "D03106": 2, "D0310A": 4, "D0310C": 17, "D0310D": 5},
    "speed_1": {"D03102": 1, "D03105": 0, "D03106": 2, "D0310A": 4, "D0310C": 1, "D0310D": 1},
    "speed_2": {"D03102": 1, "D03105": 100, "D03106": 0, "D0310A": 4, "D0310C": 2, "D0310D": 2},
    "turbo": {"D03102": 1, "D03105": 0, "D03106": 2, "D0310A": 4, "D0310C": 18, "D0310D": 4},
}


def _make_fan(status: dict) -> PhilipsAC3737:
    fan = PhilipsAC3737.__new__(PhilipsAC3737)
    fan.coordinator = MagicMock(status=status)
    fan._collect_available_preset_modes()
    fan._collect_available_speeds()
    return fan


@pytest.mark.parametrize(
    ("mode", "percentage"),
    [("auto", None), ("sleep", 25), ("speed_1", 50), ("speed_2", 75), ("turbo", 100)],
)
def test_mode_reads_back_while_humidifying(mode: str, percentage: int | None) -> None:
    fan = _make_fan(MEASURED[mode])

    assert fan.preset_mode == mode
    assert fan.percentage == percentage


def test_mode_patterns_leave_the_humidification_flag_alone() -> None:
    patterns = [*PhilipsAC3737.AVAILABLE_PRESET_MODES.values(), *PhilipsAC3737.AVAILABLE_SPEEDS.values()]

    assert all(PhilipsApi.NEW2_MODE_A not in pattern for pattern in patterns)
