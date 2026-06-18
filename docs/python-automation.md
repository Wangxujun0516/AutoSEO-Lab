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

### 🛠️ 模块一:高级标题提取器 (`fetch_title_pro.py`)

这是我们用来处理 B2B 工业网页"脏数据"的核心工具。

**技术亮点**:
- **Shadow Ledger(影子账本)**:利用 `.lower()` 生成副本定位,原件切片
- **Whitespace Stripping**:自动修剪首尾换行符

```python
def get_clean_title(html_content: str) -> str:
    """
    升级版：能够自动识别大小写、自动修剪空格的网页标题提取器。
    """
    # 核心防御 1：不管三七二十一，先复制一份全小写的源代码用来"找位置"
    # 这样可以100%防御大写的 <TITLE> 或者 <Title>
    html_lower = html_content.lower()
    
    start_tag = "<title>"
    end_tag = "</title>"
    
    # 在小写账本里找位置
    if start_tag in html_lower and end_tag in html_lower:
        # 找起点：同样要加上标签自身的长度
        start_index = html_lower.find(start_tag) + len(start_tag)
        end_index = html_lower.find(end_tag)
        
        # 🚨 注意看这里！
        # 我们找位置是在小写账本（html_lower）里找的
        # 但切片的时候，我们必须去【原版账本（html_content）】里切！
        # 这样才能保证切出来的中文或英文大小写是原汁原味的，不会被强行变成小写。
        raw_title = html_content[start_index:end_index]
        
        # 核心防御 2：用 .strip() 拔掉两边可能存在的换行符和空格
        clean_title = raw_title.strip()
        
        return clean_title
    else:
        return "错误：未能在网页中检测到标准的标题标签。"
```

### 💻 核心实现解析

上面的代码展示了一个精妙的"影子账本"策略:

1. **第 7 行**:创建一个小写副本 `html_lower`,用于定位标签位置
2. **第 14-15 行**:在小写副本中找到 `<title>` 标签的起止索引
3. **第 21 行**:**关键步骤**—在**原版**字符串上切片,保留原始大小写和中文
4. **第 24 行**:用 `.strip()` 去除首尾空白符

这种设计既解决了大小写不敏感的定位问题,又完美保留了原始内容的格式。

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

### 🛠️ 模块二:批量标题清洗器 (`batch_title_cleaner.py`)

这个模块实现了工业级的标题标准化流水线,支持多种清洗操作。

**技术亮点**:
- **Pipeline Architecture**:可配置的多步骤清洗流程
- **CSV I/O**:标准化的输入输出格式
- **Statistics**:自动统计变更数量

```python
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
```

### 💻 核心功能

上面的代码展示了批量清洗器的核心功能:

1. **第 12-18 行**:`strip_suffix()` — 移除品牌后缀(如 " | Company Name")
2. **第 20-32 行**:`strip_emoji()` — 使用正则表达式移除 emoji 和特殊符号
3. **第 34-43 行**:`convert_case()` — 支持多种大小写转换
4. **第 45-51 行**:`truncate()` — 智能截断,优先在单词边界处断开
5. **第 53-66 行**:`clean_title()` — 主清洗函数,按配置执行所有操作

### 📊 批量处理流程

```python
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
```

### 🎯 使用示例

```bash
# 基础清洗:移除品牌后缀
python utils/batch_title_cleaner.py \
  --input titles.csv \
  --output cleaned.csv \
  --strip-suffix " | AutoSEO-Lab"

# 高级清洗:移除 emoji + 统一大小写 + 限制长度
python utils/batch_title_cleaner.py \
  --input titles.csv \
  --output cleaned.csv \
  --strip-emoji \
  --case title \
  --max-len 60
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
