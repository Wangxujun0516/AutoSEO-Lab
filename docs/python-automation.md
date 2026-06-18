# Python 自动化

> 这不是一份教程,而是一份**真实的代码进化史**。记录我从一行 `print()` 开始,
> 逐步把 B2B 站点的 SEO 工作,从手工劳作变成自动化流水线的全过程。

---

## 起点:为什么要自动化

B2B 工业站点的 SEO 有一个鲜明的特点——**关键词总量小,但转化意图极强**。
一个 "12V Electric RV Leveling Jacks" 带来的询盘,价值可能抵得上消费站点上千次点击。

但人肉维护的代价是昂贵的:

- 每次产品页更新,都要手动提交给搜索引擎
- 标题标签(`<title>`)在历史迭代中凌乱不堪:大小写混杂、空白符、缺标签
- GSC 的表现数据要逐项点开,无法批量分析
- 贵得离谱的 SaaS 工具,功能却过度通用化

于是我决定,用 Python 把这些重复劳动一行行消灭掉。

---

## 第一阶段:数据清洗的内功

### 🧠 设计思路

抓回来的 HTML 是一坨"脏数据":标签大小写混杂(`<TITLE>` / `<Title>` / `<title>`)、
首尾藏着换行和空格、甚至干脆缺失。清洗函数必须做到三点:

1. **大小写无关**:无论标签怎么写都能定位
2. **原样保留**:切出来的标题保留原始大小写和中文
3. **兜底容错**:找不到时返回明确的错误标识,而不是抛异常

### 💻 核心实现

```python
def get_clean_title(html_content: str) -> str:
    """
    Case-insensitive <title> extractor with whitespace normalization.
    Returns the original-case title; falls back to an error sentinel.
    """
    # Defensive copy: locate positions in lowercase, slice from original
    html_lower = html_content.lower()
    start_tag, end_tag = "<title>", "</title>"

    if start_tag in html_lower and end_tag in html_lower:
        start_index = html_lower.find(start_tag) + len(start_tag)
        end_index = html_lower.find(end_tag)
        # Slice from the ORIGINAL case-sensitive string to preserve casing
        raw_title = html_content[start_index:end_index]
        return raw_title.strip()

    return "STATUS_ERROR: Missing Meta Title"
```

### 📐 技术指标

| 指标 | 数值 |
|---|---|
| Time complexity | O(n) — single pass string scan |
| Memory footprint | 1× lowercase shadow copy |
| Error handling | Sentinel string, no exceptions |
| Case fidelity | 100% preserved from source |

---

## 第二阶段:批量流水线

单件清洗只是内功,真正的生产力来自**批量编排**。
把单件函数套进循环,加上计数器和状态报告,就成了一个微型流水线。

```python
def run_cleaner_pipeline(html_box: list) -> None:
    """Iterate the payload, sanitize each record, report progress."""
    total_tasks = len(html_box)
    print(f"Pipeline started. Tasks detected: {total_tasks}\n" + "=" * 50)

    for index, raw_html in enumerate(html_box, start=1):
        clean_result = clean_single_html(raw_html)
        status = "FAILED" if "STATUS_ERROR" in clean_result else "SUCCESS"
        print(f"  [{index}/{total_tasks}] {status} -> {clean_result}")

    print("=" * 50 + "\nPipeline finished.")
```

---

## 第三阶段:结构化导出

清洗只是过程,**产物必须是结构化的、可被下游消费的**。
这一步把清洗结果落盘成标准 CSV,供后续的 SEO 审计、对比、报表使用。

### 输出 Schema

```csv
Task_ID,Status,Extracted_Meta_Title
SEO-TASK-001,SUCCESS,12V Electric RV Leveling Jacks | High Capacity
SEO-TASK-002,SUCCESS,Heavy-Duty Hydraulic Valve Durability Specs
SEO-TASK-003,FAILED,STATUS_ERROR: Missing Meta Title
```

### 工业级写入姿势

```python
import csv

def export_to_seo_sheet(dataset: list, filename: str) -> None:
    """Write sanitized titles into a structured CSV audit report."""
    fieldnames = ["Task_ID", "Status", "Extracted_Meta_Title"]

    # newline="" is the industrial standard for safe CSV writing on all OSes
    with open(filename, mode="w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for current_id, raw_html in enumerate(dataset, start=1):
            title = extract_title_node(raw_html)
            status = "SUCCESS" if "STATUS_ERROR" not in title else "FAILED"
            writer.writerow({
                "Task_ID": f"SEO-TASK-{current_id:03d}",
                "Status": status,
                "Extracted_Meta_Title": title
            })
```

---

## 当前项目结构

```
AutoSEO-Lab/
├── core/                         # Core orchestration & indexing
│   ├── core_gsc_orchestrator.py  # GSC analytics hub
│   ├── google_quick_index.py     # Indexing API client
│   ├── batch_index.py            # Sitemap-driven bulk submission
│   └── index_now.py              # IndexNow protocol client
├── utils/                        # Data cleansing toolkit
│   ├── fetch_title_pro.py        # Case-insensitive title extraction
│   ├── batch_title_cleaner.py    # Batch normalization pipeline
│   └── seo_metadata_exporter.py  # Metadata -> CSV exporter
└── docs/                         # This documentation site
```

---

## 写在最后

每一个脚本,都对应着我在实操中真真切切遇到过的某个具体问题。
不追求大而全的框架,只追求**确定性、可复现、可审计**。

下一站,是把 GSC 数据拉取和 Indexing API 推送这两块拼图补齐,
让整条流水线从「清洗」延伸到「分发」。
