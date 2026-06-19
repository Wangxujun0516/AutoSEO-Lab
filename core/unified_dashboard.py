#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Henghong Unified Dashboard - GSC + Umami Data Collector
========================================================

100% 纯原生依赖，将 GSC SEO 数据与 Umami 流量数据合并，
生成 Notion 格式的周报 Markdown，供 Notion Workstation DB 同步使用。

Usage:
    python core/unified_dashboard.py
    python core/unified_dashboard.py --days 7 --output weekly-report.md
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import argparse
from datetime import date, timedelta


PROXY_PORT = 3067
os.environ["http_proxy"] = f"http://127.0.0.1:{PROXY_PORT}"
os.environ["https_proxy"] = f"http://127.0.0.1:{PROXY_PORT}"

proxy_handler = urllib.request.ProxyHandler({
    'http': f'http://127.0.0.1:{PROXY_PORT}',
    'https': f'http://127.0.0.1:{PROXY_PORT}'
})
opener = urllib.request.build_opener(proxy_handler)


# ============================================================================
# GSC Data Fetcher
# ============================================================================
def get_gsc_token():
    """从本地 token.json 加载 GSC 访问令牌"""
    possible_paths = ["token.json", "core/token.json", os.path.join(os.path.dirname(__file__), "token.json")]
    for path in possible_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                token_data = json.load(f)
            access_token = token_data.get("token") or token_data.get("access_token")
            if access_token:
                return access_token
    print("[!] 未找到有效的 GSC token.json")
    return None


def fetch_gsc_data(site_url: str = "https://www.henghongrv.com/", days: int = 7):
    """抓取 GSC 搜索分析数据"""
    token = get_gsc_token()
    if not token:
        return None

    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    encoded_site = urllib.parse.quote_plus(site_url)
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"

    request_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["query"],
        "rowLimit": 20
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(
            url=api_url,
            data=json.dumps(request_body).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with opener.open(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return {
                "total_clicks": sum(int(row.get("clicks", 0)) for row in res_data.get("rows", [])),
                "total_impressions": sum(int(row.get("impressions", 0)) for row in res_data.get("rows", [])),
                "top_queries": [
                    {
                        "query": row.get("keys", [""])[0],
                        "clicks": int(row.get("clicks", 0)),
                        "impressions": int(row.get("impressions", 0)),
                        "ctr": float(row.get("ctr", 0.0)) * 100,
                        "position": float(row.get("position", 0.0)) + 1
                    }
                    for row in res_data.get("rows", [])[:10]
                ]
            }
    except Exception as e:
        print(f"[!] GSC API 错误: {e}")
        return None


def fetch_gsc_country_data(site_url: str = "https://www.henghongrv.com/", days: int = 7):
    """抓取 GSC 国家维度数据"""
    token = get_gsc_token()
    if not token:
        return None

    end_date = date.today().strftime("%Y-%m-%d")
    start_date = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")
    encoded_site = urllib.parse.quote_plus(site_url)
    api_url = f"https://www.googleapis.com/webmasters/v3/sites/{encoded_site}/searchAnalytics/query"

    request_body = {
        "startDate": start_date,
        "endDate": end_date,
        "dimensions": ["country"],
        "rowLimit": 10
    }

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json"
    }

    try:
        req = urllib.request.Request(
            url=api_url,
            data=json.dumps(request_body).encode('utf-8'),
            headers=headers,
            method='POST'
        )
        with opener.open(req, timeout=15) as response:
            res_data = json.loads(response.read().decode('utf-8'))
            return [
                {
                    "country": row.get("keys", [""])[0].upper(),
                    "clicks": int(row.get("clicks", 0)),
                    "impressions": int(row.get("impressions", 0)),
                    "ctr": float(row.get("ctr", 0.0)) * 100
                }
                for row in res_data.get("rows", [])
            ]
    except Exception as e:
        print(f"[!] GSC Country API 错误: {e}")
        return []


# ============================================================================
# Umami Data Fetcher
# ============================================================================
def fetch_umami_data(umami_url: str = "https://t1q1u6lz37.execute-api.ap-northeast-1.amazonaws.com/default/henghong-analytics", days: int = 7):
    """从 Umami Cloud 抓取网站流量数据"""
    try:
        req = urllib.request.Request(url=umami_url, headers={"User-Agent": "Mozilla/5.0"})
        with opener.open(req, timeout=15) as response:
            raw = response.read().decode('utf-8')
            try:
                data = json.loads(raw)
            except json.JSONDecodeError:
                data = extract_umami_from_html(raw)
            return data
    except Exception as e:
        print(f"[!] Umami API 错误: {e}")
        return None


def extract_umami_from_html(html_content: str) -> dict:
    """从 HTML 页面中提取 Umami 统计数据"""
    import re
    result = {"pageviews": 0, "unique_visitors": 0, "bounce_rate": 0, "avg_duration": 0}

    patterns = {
        "pageviews": r'Pageviews[\s\S]*?<td[^>]*>([\d,]+)</td>',
        "unique_visitors": r'Unique visitors[\s\S]*?<td[^>]*>([\d,]+)</td>',
        "bounce_rate": r'Bounce rate[\s\S]*?<td[^>]*>([0-9.]+)%',
        "avg_duration": r'Average duration[\s\S]*?<td[^>]*>([\d:]+)</td>'
    }

    for key, pattern in patterns.items():
        match = re.search(pattern, html_content, re.IGNORECASE)
        if match:
            value = match.group(1).replace(",", "")
            result[key] = float(value) if "." in value else int(value)

    return result


# ============================================================================
# Notion Markdown Report Generator
# ============================================================================
def generate_notion_report(gsc_data: dict, umami_data: dict, country_data: list, days: int = 7):
    """生成 Notion 兼容的 Markdown 周报"""
    today = date.today().strftime("%Y-%m-%d")
    week_ago = (date.today() - timedelta(days=days)).strftime("%Y-%m-%d")

    report = f"""# Henghong SEO Weekly Report

**Report Period**: {week_ago} → {today}  
**Generated**: {today}  
**Data Sources**: Google Search Console, Umami Analytics

---

## SEO Performance Summary

| Metric | Value |
|--------|-------|
| Total Clicks | {gsc_data.get('total_clicks', 0):,} |
| Total Impressions | {gsc_data.get('total_impressions', 0):,} |
| Average CTR | {(gsc_data.get('total_clicks', 0) / max(gsc_data.get('total_impressions', 1), 1) * 100):.2f}% |

### Traffic Breakdown by Country

| Country | Clicks | Impressions | CTR |
|---------|--------|-------------|-----|
"""

    for item in country_data[:5]:
        report += f"| {item['country']} | {item['clicks']:,} | {item['impressions']:,} | {item['ctr']:.2f}% |\n"

    report += """
### Top 10 Search Queries

| Rank | Query | Clicks | Impressions | CTR | Avg Position |
|------|-------|--------|-------------|-----|--------------|
"""

    for i, q in enumerate(gsc_data.get('top_queries', []), 1):
        report += f"| {i} | {q['query']} | {q['clicks']} | {q['impressions']} | {q['ctr']:.2f}% | {q['position']:.1f} |\n"

    report += """
## Website Traffic (Umami)

| Metric | Value |
|--------|-------|
"""

    if umami_data:
        report += f"| Pageviews | {umami_data.get('pageviews', 'N/A'):,} |\n"
        report += f"| Unique Visitors | {umami_data.get('unique_visitors', 'N/A'):,} |\n"
        report += f"| Bounce Rate | {umami_data.get('bounce_rate', 'N/A')} |\n"
        report += f"| Avg Duration | {umami_data.get('avg_duration', 'N/A')} |\n"
    else:
        report += "| Pageviews | N/A |\n| Unique Visitors | N/A |\n| Bounce Rate | N/A |\n"

    report += """
---

## Key Insights & Actions

### Wins
- 
### Opportunities
- 
### Next Week Priorities
- [ ] 
- [ ] 

---
*Auto-generated by AutoSEO-Lab Unified Dashboard*
"""

    return report


# ============================================================================
# Main
# ============================================================================
def main():
    parser = argparse.ArgumentParser(description="Henghong Unified Dashboard - GSC + Umami")
    parser.add_argument("--days", type=int, default=7, help="查询天数范围 (default: 7)")
    parser.add_argument("--output", "-o", help="输出 Markdown 文件路径")
    args = parser.parse_args()

    print("=" * 60)
    print("[HENGHONG UNIFIED DASHBOARD]")
    print("=" * 60)
    print(f"[*] Period: Last {args.days} days")
    print("[*] Fetching GSC data...")

    gsc_data = fetch_gsc_data(days=args.days)
    country_data = fetch_gsc_country_data(days=args.days)

    print("[*] Fetching Umami data...")
    umami_data = fetch_umami_data(days=args.days)

    print("[*] Generating Notion Markdown report...")
    report = generate_notion_report(gsc_data or {}, umami_data or {}, country_data or [], days=args.days)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[+] Report saved → {args.output}")
    else:
        print("\n" + report)


if __name__ == "__main__":
    main()
