# tests/test_validator.py
import pytest

from mac_validator import is_valid_mac


# ---------- Тесты через фикстуры из conftest.py ----------
def test_all_valid_fixture_macs(valid_macs):
    for mac in valid_macs:
        assert is_valid_mac(mac) is True, f"должен быть валидным: {mac!r}"


def test_all_invalid_fixture_macs(invalid_macs):
    for mac in invalid_macs:
        assert is_valid_mac(mac) is False, f"должен быть невалидным: {mac!r}"