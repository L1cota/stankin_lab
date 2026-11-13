import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from ip_validator import (
    find_ipv4_in_text,
    find_ipv4_on_webpage,
    is_valid_ipv4,
    process_file,
)


class TestIPv4Validator(unittest.TestCase):
    def test_valid_ipv4_addresses(self):
        valid_ips = [
            "0.0.0.0",
            "127.0.0.1",
            "192.168.0.1",
            "10.255.0.14",
            "172.16.254.1",
            "255.255.255.255",
            "  8.8.8.8  ",
        ]
        for ip in valid_ips:
            with self.subTest(ip=ip):
                self.assertTrue(is_valid_ipv4(ip))

    def test_invalid_ipv4_addresses(self):
        invalid_ips = [
            "",
            "192.168.1",
            "192.168.1.1.1",
            "256.100.50.25",
            "192.168.1.300",
            "192.168.01.1",
            "192.168.00.1",
            "-1.0.0.1",
            "192.168.1.a",
            "192.168..1",
            "192.168.1.1/24",
            "localhost",
        ]
        for ip in invalid_ips:
            with self.subTest(ip=ip):
                self.assertFalse(is_valid_ipv4(ip))

    def test_find_ipv4_in_text(self):
        sample_text = (
            "Сервер 192.168.1.10 подключен к шлюзу 10.0.0.1.\n"
            "Ошибочные записи: 999.10.10.10, 1.2.3.4.5, 192.168.01.5.\n"
            "DNS Google: 8.8.8.8 и 8.8.4.4."
        )
        expected = ["192.168.1.10", "10.0.0.1", "8.8.8.8", "8.8.4.4"]
        self.assertEqual(find_ipv4_in_text(sample_text), expected)

    def test_find_ipv4_empty_result(self):
        text = "В тексте нет корректных адресов: 300.400.500.600"
        self.assertEqual(find_ipv4_in_text(text), [])

    def test_process_file_creates_output(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            in_file = os.path.join(tmpdir, "in.txt")
            out_file = os.path.join(tmpdir, "out.txt")

            with open(in_file, "w", encoding="utf-8") as f:
                f.write(
                    "host1: 192.168.1.1\nbad: 256.0.0.1\nhost2: 10.10.10.10\n"
                )

            result = process_file(in_file, out_file)

            self.assertEqual(result, ["192.168.1.1", "10.10.10.10"])
            self.assertTrue(os.path.exists(out_file))
            with open(out_file, "r", encoding="utf-8") as f:
                lines = f.read().splitlines()
            self.assertEqual(lines, ["192.168.1.1", "10.10.10.10"])

    @patch("ip_validator.requests.get")
    def test_find_ipv4_on_webpage(self, mock_get):
        mock_response = Mock()
        mock_response.text = "<html><body>Server IP: 93.184.216.34</body></html>"
        mock_response.raise_for_status = Mock()
        mock_get.return_value = mock_response

        result = find_ipv4_on_webpage("https://example.com")
        self.assertEqual(result, ["93.184.216.34"])
        mock_get.assert_called_once()


if __name__ == "__main__":
    unittest.main()