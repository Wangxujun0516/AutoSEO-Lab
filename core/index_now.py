"""
IndexNow — Universal URL Submission via IndexNow Protocol
===========================================================
Submit URLs to search engines supporting IndexNow (Bing, Yandex, Naver, et al.)
— the lightweight alternative to Google's Indexing API.

Why IndexNow? No OAuth, no scopes, no service accounts. Just an API key and a POST.

Usage:
  python core/index_now.py --url https://example.com/page
  python core/index_now.py --file urls.txt --key YOUR_API_KEY

Setup:
  1. Get your IndexNow API key — generate via Bing Webmaster Tools
  2. Host the key as `{your-key}.txt` at the root of your site
     (e.g., https://henghongrv.com/YOUR_API_KEY.txt)
  3. Done.
"""

import argparse
import json
import sys
import urllib.request
import urllib.error
import urllib.parse

INDEXNOW_URL = "https://api.indexnow.org/indexnow"


def submit_url(url: str, key: str, key_location: str = None) -> dict:
    """
    Submit a URL via IndexNow protocol.

    Parameters
    ----------
    url : str
        Full URL to submit
    key : str
        IndexNow API key
    key_location : str, optional
        Full URL to the key file (auto-derived if not provided)

    Returns
    -------
    dict
        Response with status, url, http_code
    """
    parsed = urllib.parse.urlparse(url)
    if key_location is None:
        key_location = f"{parsed.scheme}://{parsed.netloc}/{key}.txt"

    payload = {
        "host": parsed.netloc,
        "key": key,
        "keyLocation": key_location,
        "urlList": [url],
    }

    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        INDEXNOW_URL,
        data=data,
        headers={"Content-Type": "application/json; charset=utf-8"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            body = resp.read().decode("utf-8")
            return {"status": "ok", "url": url, "http_code": resp.status, "body": body}
    except urllib.error.HTTPError as e:
        return {"status": "error", "url": url, "http_code": e.code}
    except urllib.error.URLError as e:
        return {"status": "error", "url": url, "error": str(e.reason)}


def batch_submit(filepath: str, key: str, key_location: str = None) -> list:
    """Submit multiple URLs from a text file."""
    with open(filepath, "r", encoding="utf-8") as f:
        urls = [line.strip() for line in f if line.strip()]

    results = []
    for url in urls:
        result = submit_url(url, key, key_location)
        results.append(result)
        ok = "✓" if result["status"] == "ok" else "✗"
        detail = result.get("http_code", result.get("error", "?"))
        print(f"  [{ok}] {url:<60s} HTTP {detail}")

    ok_count = sum(1 for r in results if r["status"] == "ok")
    print(f"\n[✓] {ok_count}/{len(urls)} URLs submitted via IndexNow")
    return results


def main():
    parser = argparse.ArgumentParser(description="IndexNow URL Submitter")
    parser.add_argument("--key", required=True, help="IndexNow API key")
    parser.add_argument("--key-location", help="Full URL to key file (optional)")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--url", help="Single URL to submit")
    group.add_argument("--file", help="Text file with one URL per line")
    args = parser.parse_args()

    if args.url:
        result = submit_url(args.url, args.key, args.key_location)
        ok = "✓" if result["status"] == "ok" else "✗"
        print(f"[{ok}] {result['url']} → HTTP {result.get('http_code', '?')}")
    elif args.file:
        batch_submit(args.file, args.key, args.key_location)


if __name__ == "__main__":
    main()
