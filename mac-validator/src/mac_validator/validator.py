# src/mac_validator/validator.py
"""Валидация MAC-адресов."""

import re

_MAC_RE = re.compile(
    r"^"
    r"(?:"
    r"(?:[0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}"      # Формат: 00:1A:2B:3C:4D:5E (двоеточия)
    r"|"
    r"(?:[0-9A-Fa-f]{2}-){5}[0-9A-Fa-f]{2}"      # Формат: 00-1A-2B-3C-4D-5E (дефисы)
    r"|"
    r"(?:[0-9A-Fa-f]{4}\.){2}[0-9A-Fa-f]{4}"    # Формат: 001a.2b3c.4d5e (Cisco, точки)
    r")"
    r"\Z"
)

# Поддерживаемые стандарты разделителей: двоеточия (:), дефисы (-), точки (.).


def is_valid_mac(mac: str) -> bool:
    """Проверяет, является ли строка синтаксически корректным MAC-адресом.

    Args:
        mac: строка для проверки.

    Returns:
        True, если MAC-адрес похож на корректный, иначе False.

    Examples:
        >>> is_valid_mac("00:1A:2B:3C:4D:5E")
        True
        >>> is_valid_mac("not-a-mac-address")
        False
    """
    if not isinstance(mac, str):
        return False
    mac_clean = mac.strip(" ")
    if not mac_clean or len(mac_clean) not in (14, 17):  # 17 (для : и -), 14 (для .)
        return False
    return _MAC_RE.match(mac_clean) is not None