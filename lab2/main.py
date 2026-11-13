import os
import requests
from ip_validator import (
    find_ipv4_on_webpage,
    is_valid_ipv4,
    process_file,
)


def handle_manual_input() -> None:
    user_ip = input("Введите IPv4-адрес для проверки: ").strip()
    if is_valid_ipv4(user_ip):
        print(f"Адрес {user_ip} корректный.")
    else:
        print(f"Адрес {user_ip} некорректный.")


def handle_file_search() -> None:
    in_prompt = "Входной файл (Enter для input_data.txt): "
    input_path = input(in_prompt).strip() or "input_data.txt"

    if not os.path.exists(input_path):
        print(f"Файл '{input_path}' не найден.")
        return

    out_prompt = "Выходной файл (Enter для output_ips.txt): "
    output_path = input(out_prompt).strip() or "output_ips.txt"

    found_ips = process_file(input_path, output_path)
    print(f"Найдено адресов: {len(found_ips)}")
    if found_ips:
        print("Найденные IPv4:", ", ".join(found_ips))
    print(f"Результат записан в файл: {output_path}")


def handle_url_search() -> None:
    url = input("Введите URL страницы: ").strip()
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    try:
        found_ips = find_ipv4_on_webpage(url)
    except requests.RequestException as err:
        print(f"Ошибка при запросе к странице: {err}")
        return

    print(f"Найдено адресов на странице: {len(found_ips)}")
    if found_ips:
        for ip in found_ips:
            print(" -", ip)

        choice = input("Сохранить результат в файл? (y/n): ").strip().lower()
        if choice == "y":
            out_path = (
                input("Имя файла (Enter для web_ips.txt): ").strip()
                or "web_ips.txt"
            )
            with open(out_path, "w", encoding="utf-8") as outfile:
                outfile.write("\n".join(found_ips) + "\n")
            print(f"Сохранено в {out_path}")


def main() -> None:
    while True:
        print("\n--- Проверка и поиск IPv4-адресов ---")
        print("1. Проверить IPv4-адрес вручную")
        print("2. Найти IPv4-адреса в файле (с записью в файл)")
        print("3. Найти IPv4-адреса на веб-странице по URL")
        print("0. Выход")

        choice = input("Выберите пункт меню: ").strip()

        if choice == "1":
            handle_manual_input()
        elif choice == "2":
            handle_file_search()
        elif choice == "3":
            handle_url_search()
        elif choice == "0":
            print("Завершение работы.")
            break
        else:
            print("Неверный пункт меню, попробуйте снова.")


if __name__ == "__main__":
    main()