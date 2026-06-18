"""
Google Quick Index — Google Indexing API Client
=================================================
Submit URLs to Google for rapid discovery and indexing.

Best for:
  - New or updated pages that need indexing ASAP
  - Job postings, events, news (Google's primary use case)
  - Content refreshes on B2B product pages

Usage:
  python core/google_quick_index.py --url https://example.com/new-page
  python core/google_quick_index.py --file urls.txt --verbose

Setup:
  1. Enable Indexing API in Google Cloud Console
  2. Create a service account, grant owner/editor access on your site in GSC
  3. Save the service account JSON key as service_account_key.json (gitignored)
"""

import argparse
import json
import os
import sys


# ---------------------------------------------------------------------------
# Placeholder — implement with google-api-python-client when dependencies installed
# ---------------------------------------------------------------------------

SCOPES = ["https://www.googleapis.com/auth/indexing"]


def submit_url(url: str, url_type: str = "URL_UPDATED", key_path: str = None):
    """
    Submit a URL to Google Indexing API.

    Parameters
    ----------
    url : str
        Full URL to index
    url_type : str
        'URL_UPDATED' (default) or 'URL_DELETED'
    key_path : str
        Path to service account JSON key

    Returns
    -------
    dict
        API response or error info
    """
    if key_path is None:
        key_path = os.path.join(os.path.dirname(__file__), "..",
                                "service_account_key.json")

    if not os.path.exists(key_path):
        print(f"[!] Service account key not found: {key_path}")
        print("[!] See https://developers.google.com/search/apis/indexing-api")
        sys.exit(1)

    print(f"[*] Submitting: {url}")
    print(f"    Type: {url_type}")
    print("[*] (Stub — actual API call pending google-api-client install)\n")
    return {"status": "stub", "url": url, "type": url_type}


def batch_submit(filepath: str, url_type: str = "URL_UPDATED", key_path: str = None):
    """Submit multiple URLs from a text file (one URL per line)."""
    with open(filepath, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []
    for url in urls:
        result = submit_url(url, url_type, key_path)
        results.append(result)
        print(f"  {'[✓]' if result['status'] == 'stub' else '[✗]'} {url}")

    print(f"\n[✓] Processed {len(urls)} URLs")
    return results


def main():
    parser = argparse.ArgumentParser(description="Google Indexing API Client")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Single URL to submit")
    group.add_argument("--file", help="Text file with one URL per line")
    parser.add_argument("--type", choices=["URL_UPDATED", "URL_DELETED"],
                        default="URL_UPDATED", help="Notification type")
    parser.add_argument("--verbose", action="store_true")
    args = parser.parse_args()

    if args.url:
        submit_url(args.url, args.type)
    elif args.file:
        batch_submit(args.file, args.type)


if __name__ == "__main__":
    main()
