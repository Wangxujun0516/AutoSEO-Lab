# Python 基础学习

> 边写项目边学 Python — 记录实用知识点和踩坑记录

---

## 目录

1. [从零到实用](#从零到实用)
2. [日常实用技巧](#日常实用技巧)
3. [文件与目录操作](#文件与目录操作)
4. [网络请求与 Web Scraping](#网络请求与-web-scraping)
5. [CSV / JSON 数据处理](#csv--json-数据处理)
6. [踩坑记录](#踩坑记录)

---

## 从零到实用

### 语法速览

```python
# 变量 — 不用声明类型
site_name = "Henghong RV"
page_count = 47
ctr = 0.0532

# 列表（类似数组）
keywords = ["b2b", "industrial", "valves"]

# 字典（类似对象）
page = {"url": "https://henghongrv.com/", "title": "Henghong RV - RV Parts"}

# 条件判断
if ctr > 0.05:
    print("不错的 CTR")
elif ctr > 0.02:
    print("需要优化")
else:
    print("需要大改")

# 循环
for kw in keywords:
    print(f"关键词: {kw}")

# 函数
def analyze_ctr(clicks, impressions):
    return clicks / impressions if impressions > 0 else 0
```

### 必装库

```bash
pip install requests         # HTTP 请求（比 urllib 好用 10 倍）
pip install beautifulsoup4   # HTML 解析
pip install pandas           # 数据分析（CSV 处理首选）
pip install lxml             # 快速 HTML/XML 解析器
pip install python-dotenv    # .env 文件管理
```

---

## 日常实用技巧

### f-string 格式化

```python
title = "B2B Industrial Valves"
clicks = 47
print(f"'{title}' got {clicks} clicks from Google")
# → 'B2B Industrial Valves' got 47 clicks from Google

# 格式化百分比
ctr = 0.0527
print(f"CTR: {ctr:.1%}")
# → CTR: 5.3%
```

### 列表推导式（List Comprehension）

```python
# 传统写法
titles = []
for page in pages:
    if len(page['title']) > 30:
        titles.append(page['title'])

# 一行搞定
titles = [p['title'] for p in pages if len(p['title']) > 30]
```

---

## 文件与目录操作

### 读文件

```python
# 读 URL 列表
with open("urls.txt", "r", encoding="utf-8") as f:
    urls = [line.strip() for line in f if line.strip()]
```

### 写 CSV

```python
import csv

data = [
    {"url": "https://example.com/a", "title": "Product A"},
    {"url": "https://example.com/b", "title": "Product B"},
]

with open("output.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.DictWriter(f, fieldnames=["url", "title"])
    w.writeheader()
    w.writerows(data)
```

### 路径拼接

```python
from pathlib import Path

# ✅ 推荐 — 跨平台
base = Path("D:/Projects/AutoSEO-Lab")
creds = base / "credentials.json"

# ❌ 不推荐 — Windows 上容易出问题
creds = "D:\\Projects\\AutoSEO-Lab\\credentials.json"
```

---

## 网络请求与 Web Scraping

### requests（最常用）

```python
import requests

headers = {"User-Agent": "Mozilla/5.0"}
resp = requests.get("https://henghongrv.com/", headers=headers, timeout=10)

if resp.status_code == 200:
    html = resp.text
else:
    print(f"请求失败: {resp.status_code}")
```

### urllib（标准库，少装一个依赖）

```python
import urllib.request

req = urllib.request.Request(
    "https://henghongrv.com/",
    headers={"User-Agent": "AutoSEO-Lab/1.0"},
)
with urllib.request.urlopen(req, timeout=10) as resp:
    html = resp.read().decode("utf-8", errors="replace")
```

### BeautifulSoup 解析 HTML

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

title = soup.title.string.strip()
h1 = soup.find("h1").text.strip()
meta_desc = soup.find("meta", attrs={"name": "description"})
desc = meta_desc["content"] if meta_desc else ""

# 找所有链接
links = [a["href"] for a in soup.find_all("a", href=True)]
```

---

## CSV / JSON 数据处理

### CSV 读取

```python
import csv

with open("data.csv", "r", encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for row in reader:
        print(row["url"], row["title"])
```

### CSV 写入

```python
with open("output.csv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["URL", "Title", "Clicks"])
    w.writerow(["https://...", "Product A", 47])
```

### JSON 读写

```python
import json

# 写
data = {"site": "henghongrv.com", "pages": 47}
with open("data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

# 读
with open("data.json", "r", encoding="utf-8") as f:
    data = json.load(f)
```

---

## 踩坑记录

### 🕳️ Python 踩坑 #1: CSV 空行

在 Windows 上写 CSV 会多一个空行：

```python
# ✅ 解决方法：newline=""
with open("file.csv", "w", newline="", encoding="utf-8") as f:
    ...
```

### 🕳️ Python 踩坑 #2: 中文编码

```python
# ✅ 如果不加 encoding="utf-8"，中文会乱码
with open("file.txt", "r", encoding="utf-8") as f:
    ...
```

### 🕳️ Python 踩坑 #3: 闭包陷阱

```python
# ❌ 错误：所有函数都返回同一个值
funcs = []
for i in range(3):
    funcs.append(lambda: i)
print([f() for f in funcs])  # [2, 2, 2]

# ✅ 正确：捕获当前值
funcs = []
for i in range(3):
    funcs.append(lambda i=i: i)
print([f() for f in funcs])  # [0, 1, 2]
```

### 🕳️ Python 踩坑 #4: mutable 默认参数

```python
# ❌ 大坑 — 默认参数只创建一次
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item(1))  # [1]
print(add_item(2))  # [1, 2]  ← 不是 [2]！

# ✅ 正确
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

### 🕳️ Python 踩坑 #5: 函数重名

```python
# ❌ 在同一个文件里定义两个同名函数，后面会覆盖前面的
def analyze(url):
    return {"url": url}

def analyze(url, depth=1):  # ← 覆盖了上面那个
    return {"url": url, "depth": depth}
# Python 不像其他语言支持同名不同参数的重载！
# ✅ 要么合并到一个函数里用默认参数，要么改名字
```

---

*更新于 2026-06 · 持续学习中*
