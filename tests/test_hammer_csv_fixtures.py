#!/usr/bin/env python3
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FIXTURES = ROOT / "tests" / "fixtures" / "hammer"
sys.path.insert(0, str(ROOT / "tools"))

import hammer_csv  # noqa: E402


def fixture(name: str) -> str:
    return (FIXTURES / name).read_text(encoding="utf-8")


class HammerCsvFixtureTests(unittest.TestCase):
    def test_proxy_list_fixture_derives_proxy_id(self) -> None:
        text = fixture("proxy-list.csv")
        self.assertEqual(hammer_csv.first_row_id(text), "7")
        rows = hammer_csv.parse_hammer_csv(text)
        self.assertEqual(rows[0]["Name"], "smart-proxy.example.com")

    def test_content_view_version_fixture_extracts_latest(self) -> None:
        text = fixture("content-view-version-list.csv")
        self.assertEqual(hammer_csv.latest_content_view_version(text), {"id": "11", "version": "2.0"})

    def test_product_content_fixture_contains_expected_labels(self) -> None:
        text = fixture("activation-key-product-content.csv")
        self.assertTrue(hammer_csv.contains_content_label(text, "sourceos-live-iso"))
        self.assertTrue(hammer_csv.contains_content_label(text, "sourceos-config-bundles"))
        self.assertFalse(hammer_csv.contains_content_label(text, "sourceos-missing"))


if __name__ == "__main__":
    unittest.main()
