import re
import requests


# Октет IPv4: числа от 0 до 255 без ведущих нулей (кроме самого 0)
OCTET_PATTERN = r"(?:25[0-5]|2[0-4]\d|1\d\d|[1-9]\d|\d)"

# Регулярное выражение для поиска корректных IPv4 в произвольном тексте.
# Просмотры вперед/назад отсекают адреса с 5 октетами и числа больше 255.
IPV4_REGEX = re.compile(
    rf"(?<![\d.])(?:{OCTET_PATTERN}\.){{3}}{OCTET_PATTERN}(?![\d.])"
)


def is_valid_ipv4(value: str) -> bool:
    """Проверяет, является ли строка корректным IPv4-адресом."""
    return bool(IPV4_REGEX.fullmatch(value.strip()))


def find_ipv4_in_text(text: str) -> list[str]:
    """Ищет все корректные IPv4-адреса в переданном тексте."""
    return IPV4_REGEX.findall(text)


def process_file(input_path: str, output_path: str) -> list[str]:
    """Читает входной файл, находит IPv4 и сохраняет их в выходной файл."""
    with open(input_path, "r", encoding="utf-8") as infile:
        content = infile.read()

    found_ips = find_ipv4_in_text(content)

    with open(output_path, "w", encoding="utf-8") as outfile:
        if found_ips:
            outfile.write("\n".join(found_ips) + "\n")
        else:
            outfile.write("Корректные IPv4-адреса не найдены.\n")

    return found_ips


def find_ipv4_on_webpage(url: str, timeout: int = 10) -> list[str]:
    """Загружает HTML-страницу по URL и возвращает найденные IPv4-адреса."""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }
    response = requests.get(url, headers=headers, timeout=timeout)
    response.raise_for_status()
    return find_ipv4_in_text(response.text)