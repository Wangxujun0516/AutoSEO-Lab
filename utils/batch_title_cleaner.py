"""
Batch Title Cleaner — Normalize & Optimize Title Tags
=======================================================
Batch processing pipeline for title tag standardization.

Operations:
  - Strip trailing site name / brand suffix (e.g., " | Example Inc.")
  - Unify casing (Title Case, Sentence case, lowercase)
  - Remove emoji / special characters
  - Truncate to max length
  - Deduplicate across a sitemap or URL list

Usage:
  python utils/batch_title_cleaner.py --input titles.csv --output cleaned.csv
  python utils/batch_title_cleaner.py --input titles.csv --strip-suffix " | SiteName" --case title
"""

import argparse
import csv
import re
import sys
from pathlib import Path


def strip_suffix(title: str, suffix: str) -> str:
    """Remove a trailing suffix (e.g., ' | Company Name')."""
    suffix = suffix.strip()
    if suffix and title.strip().endswith(suffix):
        return title.strip()[:-len(suffix)].strip()
    return title.strip()


def strip_emoji(text: str) -> str:
    """Remove emoji and other special Unicode symbols."""
    emoji_pattern = re.compile(
        "["
        "\U0001F600-\U0001F64F"   # emoticons
        "\U0001F300-\U0001F5FF"   # symbols & pictographs
        "\U0001F680-\U0001F6FF"   # transport & map
        "\U0001F1E0-\U0001F1FF"   # flags
        "\U00002702-\U000027B0"   # dingbats
        "\U000024C2-\U0001F251"   # misc
        "\U00002100-\U000027BF"   # misc
        "\U0001FA00-\U0001FA6F"   # chess symbols
        "\U0001FA70-\U0001FAFF"   # symbols extended-A
        "\U0001FB00-\U0001FBFF"   # symbols extended-B
        "\U0000FE00-\U0000FE0F"   # variation selectors
        "]+", flags=re.UNICODE)
    return emoji_pattern.sub("", text).strip()


def convert_case(title: str, case: str) -> str:
    """Convert title case."""
    if case == "lower":
        return title.lower()
    elif case == "upper":
        return title.upper()
    elif case == "title":
        return title.title()
    elif case == "sentence":
        return title[0].upper() + title[1:] if title else title
    return title


def truncate(title: str, max_len: int) -> str:
    """Truncate to max_len chars, trying to break at a word boundary."""
    if len(title) <= max_len:
        return title
    truncated = title[:max_len].rsplit(" ", 1)[0]
    return truncated if truncated else title[:max_len]


def clean_title(title: str, **kwargs) -> str:
    """Apply all configured cleaning operations."""
    t = title.strip()

    if kwargs.get("strip_suffix"):
        t = strip_suffix(t, kwargs["strip_suffix"])

    if kwargs.get("strip_emoji", False):
        t = strip_emoji(t)

    if kwargs.get("collapse_whitespace", True):
        t = re.sub(r"\s+", " ", t)

    if kwargs.get("case"):
        t = convert_case(t, kwargs["case"])

    if kwargs.get("max_len"):
        t = truncate(t, kwargs["max_len"])

    return t


def batch_clean(input_path: str, output_path: str, **kwargs) -> list[dict]:
    """Read CSV, clean titles, write output CSV."""
    rows = []
    with open(input_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            original = row.get("title", "")
            cleaned = clean_title(original, **kwargs)
            rows.append({
                "url": row.get("url", ""),
                "original_title": original,
                "cleaned_title": cleaned,
            })

    with open(output_path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["url", "original_title", "cleaned_title"])
        w.writeheader()
        w.writerows(rows)

    changed = sum(1 for r in rows if r["original_title"] != r["cleaned_title"])
    print(f"[✓] Cleaned {len(rows)} titles ({changed} modified) → {output_path}")
    return rows


def main():
    parser = argparse.ArgumentParser(description="Batch Title Cleaner")
    parser.add_argument("--input", required=True, help="Input CSV (columns: url, title)")
    parser.add_argument("--output", required=True, help="Output CSV path")
    parser.add_argument("--strip-suffix", help="Remove trailing suffix (e.g., ' | Brand')")
    parser.add_argument("--strip-emoji", action="store_true", help="Remove emoji")
    parser.add_argument("--no-collapse", action="store_true", help="Keep multi-space")
    parser.add_argument("--case", choices=["lower", "upper", "title", "sentence"],
                        help="Case conversion")
    parser.add_argument("--max-len", type=int, help="Truncate to N chars")
    args = parser.parse_args()

    batch_clean(
        args.input, args.output,
        strip_suffix=args.strip_suffix,
        strip_emoji=args.strip_emoji,
        collapse_whitespace=not args.no_collapse,
        case=args.case,
        max_len=args.max_len,
    )


if __name__ == "__main__":
    main()
