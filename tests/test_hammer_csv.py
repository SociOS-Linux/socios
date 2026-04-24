#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import hammer_csv  # noqa: E402


class HammerCsvTests(unittest.TestCase):
    def test_parse_empty_and_header_only(self) -> None:
        self.assertEqual(hammer_csv.parse_hammer_csv(""), [])
        self.assertEqual(hammer_csv.parse_hammer_csv("Id,Name\n"), [])

    def test_parse_basic_rows(self) -> None:
        text = "Id,Name,Url\n7,smart-proxy.example.com,https://smart-proxy.example.com:9090\n"
        self.assertEqual(
            hammer_csv.parse_hammer_csv(text),
            [{"Id": "7", "Name": "smart-proxy.example.com", "Url": "https://smart-proxy.example.com:9090"}],
        )

    def test_first_row_id(self) -> None:
        self.assertEqual(hammer_csv.first_row_id("Id,Name\n42,sourceos-workstation\n"), "42")
        self.assertIsNone(hammer_csv.first_row_id("Id,Name\n"))

    def test_latest_content_view_version_uses_last_row(self) -> None:
        text = "Id,Version\n10,1.0\n11,2.0\n"
        self.assertEqual(hammer_csv.latest_content_view_version(text), {"id": "11", "version": "2.0"})

    def test_contains_content_label_from_csv_value(self) -> None:
        text = "Id,Content Label,Override\n1,sourceos-live-iso,enabled\n"
        self.assertTrue(hammer_csv.contains_content_label(text, "sourceos-live-iso"))
        self.assertFalse(hammer_csv.contains_content_label(text, "sourceos-unknown"))

    def test_contains_content_label_fallback_plain_text(self) -> None:
        self.assertTrue(hammer_csv.contains_content_label("label: sourceos-config-bundles", "sourceos-config-bundles"))

    def test_require_fields(self) -> None:
        row = {"Id": "9", "Version": ""}
        self.assertEqual(hammer_csv.require_fields(row, ["Id", "Version"]), ["Version"])


if __name__ == "__main__":
    unittest.main()
