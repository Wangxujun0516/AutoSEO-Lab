"""
Report to Markdown — Convert CSV audit reports to beautiful Markdown tables.

Usage:
  python utils/report_to_md.py --input seo_audit_report.csv --output report.md
  python utils/report_to_md.py --input seo_audit_report.csv
"""

import argparse
import csv
import sys
from pathlib import Path


def csv_to_markdown(csv_path: str) -> str:
    """Convert CSV file to Markdown table."""
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    if not rows:
        return "## 空报告\n\n未找到任何数据。"

    headers = rows[0]
    data = rows[1:]

    md = []
    md.append("## SEO 审计报告")
    md.append("")
    md.append(f"**数据总数**: {len(data)} 条")
    md.append("")

    success_count = sum(1 for row in data if "SUCCESS" in row[1].upper())
    failed_count = len(data) - success_count
    md.append(f"**成功**: {success_count} | **失败**: {failed_count}")
    md.append("")

    md.append("| " + " | ".join(headers) + " |")
    md.append("| " + " | ".join(["---"] * len(headers)) + " |")

    for row in data:
        status_cell = f"✅ {row[1]}" if "SUCCESS" in row[1].upper() else f"❌ {row[1]}"
        row_with_status = [row[0], status_cell] + row[2:]
        md.append("| " + " | ".join(row_with_status) + " |")

    return "\n".join(md)


def main():
    parser = argparse.ArgumentParser(description="Convert CSV to Markdown table")
    parser.add_argument("--input", required=True, help="Input CSV file")
    parser.add_argument("--output", help="Output Markdown file (stdout if not specified)")
    args = parser.parse_args()

    if not Path(args.input).exists():
        print(f"错误: 文件 '{args.input}' 不存在")
        sys.exit(1)

    md_content = csv_to_markdown(args.input)

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(md_content)
        print(f"[✓] Markdown 报告已生成 → {args.output}")
    else:
        print(md_content)


if __name__ == "__main__":
    main()
