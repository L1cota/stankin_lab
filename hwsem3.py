import re

def extract_log_records(content: str, pattern : str = r"\d{4}-\d{2}-\d{2}\s+(?P<time>\d{2}:\d{2}:\d{2})\s+(?P<level>[A-Z]+)\s+(?P<message>.*)$"):
    """Выделяет строки лога по уровню (ERROR/WARN) и наличию IP-адреса.
    :param content:
    :param pattern:
    :return:"""
    errors_list = []
    ip_list = []

    ip_pattern = r"\d+\.\d+\.\d+\.\d+"

    text_lines = content.splitlines()
    for line in text_lines:
        match = re.search(pattern, line)
        if match:
            time_str = match.group("time")
            level_str = match.group("level")
            message_str = match.group("message")
            formatted_line  = f"{time_str} {level_str} {message_str}"
            if level_str in ("ERROR", "WARN"):
                errors_list.append(formatted_line)
            ip_matches = list(re.finditer(ip_pattern, message_str))
            if ip_matches:
                ip_list.append(formatted_line)

    return errors_list, ip_list

try:
    with open("log.txt", "r") as f:
        log_content = f.read()

    errors, ips = extract_log_records(log_content)
    print("Errors and Warnings:")
    for error in errors:
        print(error)
    print("\nLines with IP addresses:")
    for ip_line in ips:
        print(ip_line)
except FileNotFoundError:
    print("Файл log.txt не найден.")
except TypeError:
    print("Ошибка: передан неверный тип данных.")
except Exception as e:
    print(f"Произошла ошибка: {e}")