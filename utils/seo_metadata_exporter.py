"""
SEO Metadata Exporter — Structured Metadata Extraction
=======================================================
Extract structured SEO metadata from web pages and export as CSV or JSON.

Fields extracted:
  - URL
  - <title>
  - <meta name="description">
  - <h1> (primary heading)
  - <link rel="canonical">
  - <meta name="robots"> directives
  - Open Graph / Twitter Card tags

Usage:
  python utils/seo_metadata_exporter.py --url https://example.com
  python utils/seo_metadata_exporter.py --file urls.txt --format json
  python utils/seo_metadata_exporter.py --file urls.txt --export metadata.csv
"""

import argparse
import csv
import json
import sys
import urllib.request
import urllib.error
import urllib.parse
from html.parser import HTMLParser


class SEOMetaParser(HTMLParser):
    """Extracts SEO-relevant metadata from HTML."""

    def __init__(self):
        super().__init__()
        self.title = ""
        self.description = ""
        self.h1 = ""
        self.canonical = ""
        self.robots = ""
        self.og_tags = {}
        self.twitter_tags = {}
        self._in_title = False
        self._in_h1 = False

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)

        if tag == "title":
            self._in_title = True
        elif tag == "h1":
            self._in_h1 = True
        elif tag == "meta":
            name = attrs_dict.get("name", attrs_dict.get("property", "")).lower()
            content = attrs_dict.get("content", "")

            if name == "description":
                self.description = content
            elif name == "robots":
                self.robots = content
            elif name.startswith("og:"):
                self.og_tags[name] = content
            elif name.startswith("twitter:"):
                self.twitter_tags[name] = content
        elif tag == "link" and attrs_dict.get("rel") == "canonical":
            self.canonical = attrs_dict.get("href", "")

    def handle_endtag(self, tag):
        if tag == "title":
            self._in_title = False
        elif tag == "h1":
            self._in_h1 = False

    def handle_data(self, data):
        if self._in_title:
            self.title += data.strip()
        elif self._in_h1 and not self.h1:
            self.h1 += data.strip()


def analyze_url(url: str, timeout: int = 10) -> dict:
    """Fetch URL and extract SEO metadata."""
    result = {
        "url": url,
        "title": "",
        "description": "",
        "h1": "",
        "canonical": "",
        "robots": "",
        "og_title": "",
        "og_description": "",
        "og_image": "",
        "twitter_card": "",
        "status": "ok",
        "issues": [],
    }

    try:
        req = urllib.request.Request(
            url,
            headers={"User-Agent": "AutoSEO-Lab/1.0 (SEO Analysis)"},
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            html = resp.read().decode("utf-8", errors="replace")
    except Exception as e:
        result["status"] = "error"
        result["issues"].append(str(e))
        return result

    parser = SEOMetaParser()
    parser.feed(html)

    result["title"] = parser.title
    result["description"] = parser.description
    result["h1"] = parser.h1
    result["canonical"] = parser.canonical
    result["robots"] = parser.robots
    result["og_title"] = parser.og_tags.get("og:title", "")
    result["og_description"] = parser.og_tags.get("og:description", "")
    result["og_image"] = parser.og_tags.get("og:image", "")
    result["twitter_card"] = parser.twitter_tags.get("twitter:card", "")

    # Analysis
    if not parser.title:
        result["issues"].append("Missing <title>")
    if not parser.description:
        result["issues"].append("Missing meta description")
    if not parser.h1:
        result["issues"].append("Missing <h1>")
    if parser.canonical and parser.canonical != url:
        result["issues"].append(f"Canonical points elsewhere: {parser.canonical}")
    if not parser.canonical:
        result["issues"].append("No canonical tag")

    return result


def batch_analyze(filepath: str) -> list[dict]:
    """Analyze URLs from a text file."""
    with open(filepath, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]
    return [analyze_url(url) for url in urls]


def export_csv(results: list[dict], filepath: str):
    """Export metadata to CSV."""
    fields = [
        "url", "title", "description", "h1", "canonical",
        "robots", "og_title", "og_description", "og_image",
        "twitter_card", "status", "issues",
    ]
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in results:
            row = {k: r.get(k, "") for k in fields}
            row["issues"] = "; ".join(r.get("issues", []))
            w.writerow(row)
    print(f"[✓] CSV export → {filepath}")


def export_json(results: list[dict], filepath: str):
    """Export metadata to JSON."""
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"[✓] JSON export → {filepath}")


def main():
    parser = argparse.ArgumentParser(description="SEO Metadata Exporter")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Single URL")
    group.add_argument("--file", help="File with one URL per line")
    parser.add_argument("--format", choices=["csv", "json"], default="csv",
                        help="Export format")
    parser.add_argument("--export", help="Output file path")
    args = parser.parse_args()

    results = []
    if args.url:
        results.append(analyze_url(args.url))
    elif args.file:
        results = batch_analyze(args.file)

    for r in results:
        icon = "✓" if r["status"] == "ok" and not r["issues"] else "⚠"
        print(f"  [{icon}] {r['url']}")
        if r["title"]:
            print(f"         Title       : {r['title'][:70]}")
        print(f"         Description : {'✓' if r['description'] else '✗'} ({len(r['description'])} chars)")
        print(f"         H1          : {'✓' if r['h1'] else '✗'}")
        print(f"         Canonical   : {'✓' if r['canonical'] else '✗'}")
        if r["issues"]:
            for issue in r["issues"]:
                print(f"         ⚠ {issue}")
        print()

    if args.export:
        if args.format == "csv":
            export_csv(results, args.export)
        else:
            export_json(results, args.export)


if __name__ == "__main__":
    main()
