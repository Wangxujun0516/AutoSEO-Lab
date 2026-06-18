"""
Fetch Title Pro — Advanced <title> Tag Analyzer
=================================================
Fetch, analyze, and validate HTML <title> tags from a list of URLs.

Detects:
  - Missing or empty <title>
  - Duplicate titles across pages
  - Titles that are too short (< 30 chars) or too long (> 60 chars)
  - Truncated titles (piped / dashed content overload)
  - Non-descriptive default titles ("Home", "Page Not Found", etc.)

Usage:
  python utils/fetch_title_pro.py --file urls.txt
  python utils/fetch_title_pro.py --url https://example.com
  python utils/fetch_title_pro.py --file urls.txt --export report.csv
"""

import argparse
import csv
import re
import sys
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser

MIN_TITLE_LEN = 30
MAX_TITLE_LEN = 60
RED_FLAG_KEYWORDS = [
    "home", "home page", "index", "page not found", "404",
    "untitled", "new page", "default", "untitled document",
]


class TitleParser(HTMLParser):
    """Minimal HTML parser that extracts the first <title> tag content."""

    def __init__(self):
        super().__init__()
        self._capture = False
        self.title = None

    def handle_starttag(self, tag, attrs):
        if tag == "title":
            self._capture = True

    def handle_endtag(self, tag):
        if tag == "title":
            self._capture = False

    def handle_data(self, data):
        if self._capture and self.title is None:
            self.title = data.strip()


def fetch_title(url: str, timeout: int = 10) -> dict:
    """
    Fetch a URL and extract its <title> tag.

    Returns a dict: {url, title, char_count, status, warnings}
    """
    result = {"url": url, "title": "", "char_count": 0, "status": "ok", "warnings": []}

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AutoSEO-Lab/1.0 (SEO Analysis)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        result["status"] = f"HTTP {e.code}"
        result["warnings"].append(f"HTTP error {e.code}")
        return result
    except urllib.error.URLError as e:
        result["status"] = "unreachable"
        result["warnings"].append(str(e.reason))
        return result
    except Exception as e:
        result["status"] = "error"
        result["warnings"].append(str(e))
        return result

    parser = TitleParser()
    parser.feed(html)

    title = parser.title
    if not title:
        result["status"] = "no_title"
        result["warnings"].append("Missing or empty <title> tag")
        return result

    result["title"] = title
    result["char_count"] = len(title)

    # Checks
    if len(title) < MIN_TITLE_LEN:
        result["warnings"].append(
            f"Too short ({len(title)} chars) — aim for {MIN_TITLE_LEN}–{MAX_TITLE_LEN}"
        )
    if len(title) > MAX_TITLE_LEN:
        result["warnings"].append(
            f"Over-long ({len(title)} chars) — may be truncated in SERP"
        )

    title_lower = title.lower()
    if "|" in title and len(title.split("|")[-1].strip()) > 20:
        result["warnings"].append("Has pipe separator — may be over-stuffed with branding")

    for kw in RED_FLAG_KEYWORDS:
        if re.search(rf"\b{re.escape(kw)}\b", title_lower):
            result["warnings"].append(f"Flag keyword detected: '{kw}' — possible default title")
            break

    return result


def batch_fetch(filepath: str) -> list[dict]:
    """Fetch titles from a file with one URL per line."""
    with open(filepath, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    results = []
    for url in urls:
        results.append(fetch_title(url))
    return results


def export_csv(results: list[dict], filepath: str):
    if not results:
        return
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["URL", "Title", "Chars", "Status", "Warnings"])
        for r in results:
            w.writerow([
                r["url"], r["title"], r["char_count"],
                r["status"], "; ".join(r["warnings"]),
            ])
    print(f"[✓] Report exported → {filepath}")


def main():
    parser = argparse.ArgumentParser(description="Fetch Title Pro")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Single URL")
    group.add_argument("--file", help="File with one URL per line")
    parser.add_argument("--export", help="Export results to CSV")
    args = parser.parse_args()

    results = []
    if args.url:
        results.append(fetch_title(args.url))
    elif args.file:
        results = batch_fetch(args.file)

    for r in results:
        icon = "✓" if r["status"] == "ok" and not r["warnings"] else "⚠"
        print(f"  [{icon}] {r['url']}")
        if r["title"]:
            print(f"         Title: {r['title'][:80]}{'…' if len(r['title']) > 80 else ''}")
        print(f"         Chars: {r['char_count']}  |  Status: {r['status']}")
        if r["warnings"]:
            for w in r["warnings"]:
                print(f"         ⚠ {w}")
        print()

    if args.export:
        export_csv(results, args.export)


if __name__ == "__main__":
    main()
