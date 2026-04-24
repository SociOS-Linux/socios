#!/usr/bin/env python3
"""Small helpers for parsing Hammer CLI CSV output.

The Foreman/Katello automation scaffolds intentionally use Hammer CLI first.
This module centralizes the small CSV parsing rules needed by receipts/tests so
we stop relying on ad hoc string splitting in every follow-on.
"""

from __future__ import annotations

import csv
from io import StringIO
from typing import Iterable, Mapping


def parse_hammer_csv(text: str) -> list[dict[str, str]]:
    """Parse Hammer CSV text into dictionaries.

    Empty input, whitespace-only input, or header-only input returns an empty list.
    Header keys and row values are stripped. Missing values are normalized to an
    empty string.
    """

    text = (text or "").strip()
    if not text:
        return []

    reader = csv.DictReader(StringIO(text))
    rows: list[dict[str, str]] = []
    for row in reader:
        cleaned: dict[str, str] = {}
        for key, value in row.items():
            if key is None:
                continue
            cleaned[str(key).strip()] = "" if value is None else str(value).strip()
        if any(cleaned.values()):
            rows.append(cleaned)
    return rows


def first_row_id(text: str, id_field: str = "Id") -> str | None:
    """Return the first row ID from Hammer CSV output, if present."""

    rows = parse_hammer_csv(text)
    if not rows:
        return None
    return rows[0].get(id_field) or None


def latest_content_view_version(text: str) -> dict[str, str] | None:
    """Return the latest content-view version row from Hammer CSV output.

    Hammer's version list output is expected as CSV with at least Id and Version.
    The current scaffold treats the last row as latest; this helper makes that
    convention explicit and test-covered.
    """

    rows = parse_hammer_csv(text)
    if not rows:
        return None
    latest = rows[-1]
    return {
        "id": latest.get("Id", ""),
        "version": latest.get("Version", ""),
    }


def contains_content_label(text: str, label: str) -> bool:
    """Return whether a content label is visible in Hammer product-content output."""

    if not label:
        return False
    needle = label.strip()
    if not needle:
        return False
    rows = parse_hammer_csv(text)
    if rows:
        for row in rows:
            if any(value == needle for value in row.values()):
                return True
            if any(needle in value for value in row.values()):
                return True
    return needle in (text or "")


def require_fields(row: Mapping[str, str], fields: Iterable[str]) -> list[str]:
    """Return the missing/empty fields from a parsed row."""

    missing: list[str] = []
    for field in fields:
        if not row.get(field):
            missing.append(field)
    return missing
