# AutoSEO-Lab 🧪🔍

> 自动化 SEO 工具链 — 专为 B2B 工业网站打造
> Automated SEO toolkit for B2B industrial websites

---

## 这是什么 / What Is This

AutoSEO-Lab 是一套模块化的 SEO 自动化工具箱，专为 B2B 制造业/工业网站场景设计。旨在用 Python 脚本替代昂贵的 SaaS 工具，把 SEO 数据抓取、分析和内容优化掌握在自己手里。

### 核心功能

| 模块 | 功能 |
|------|------|
| **GSC Orchestrator** | Google Search Console 数据拉取 — 点击、展示、CTR、排名 |
| **Google Quick Index** | Google Indexing API — 快速提交 URL 收录 |
| **IndexNow** | 通用 IndexNow 协议提交（Bing / Naver / Yandex） |
| **Fetch Title Pro** | Title 标签抓取与质量检测 |
| **Batch Title Cleaner** | 批量 Title 标准化清洗 |
| **SEO Metadata Exporter** | 页面元数据一键导出 |

### 项目结构

```
AutoSEO-Lab/
├── core/       # 核心自动化脚本
├── utils/      # 数据清洗与提取
├── docs/       # 📊 文档站（就是你正在看的）
└── README.md   # GitHub 主文档（英文）
```

---

## 核心工作流 / Core Workflows

### SEO 数据流水线

```
URL 列表 → Fetch Title Pro → 质量检测 → Batch Cleaner → 标准化
                                       ↓
                         SEO Metadata Exporter → CSV/JSON分析
                                       ↓
                         GSC Orchestrator → 搜索表现追踪
                                       ↓
                         IndexNow / Quick Index → 提交收录
```

### GSC 分析流程

```python
# 30天内按查询维度拉取数据
python core/core_gsc_orchestrator.py --site https://henghongrv.com/ --days 30

# 导出为 CSV 做进一步分析
python core/core_gsc_orchestrator.py --export gsc_report.csv
```

### URL 提交

```python
# IndexNow — 最轻量，不需要 OAuth
python core/index_now.py --url https://henghongrv.com/new-page --key YOUR_API_KEY

# Google Indexing API — 需要服务账号
python core/google_quick_index.py --url https://henghongrv.com/new-page
```

---

## 数据清洗工具链 / Data Toolkit

### Title 质量检测

```python
# 单页检测
python utils/fetch_title_pro.py --url https://henghongrv.com/

# 批量检测 + 导出报告
python utils/fetch_title_pro.py --file urls.txt --export title_report.csv
```

检测项：
- ❌ 缺少 Title
- ⚠️ 太短（< 30 字符）或太长（> 60 字符）
- ⚠️ 重复 Title
- ⚠️ 默认关键词（"Home", "Page Not Found"）

### 批量清洗

```python
# 去尾缀 + 首字母大写
python utils/batch_title_cleaner.py \
  --input titles.csv --output cleaned.csv \
  --strip-suffix " | Henghong RV" --case title
```

### 元数据导出

```python
python utils/seo_metadata_exporter.py --file urls.txt --export metadata.csv
```

---

## 部署说明 / Deployment

1. 将 docs/ 目录部署到 **Vercel** 或 **GitHub Pages**
2. 支持任意 Markdown 静态站生成器（MkDocs, Docusaurus, Nextra）
3. 每次更新 Markdown 文件 → 自动重建站点

> 💡 推荐：Vercel + Nextra 零配置搭建文档站

---

## 为什么做这个 / Why AutoSEO-Lab

- B2B 工业网站 SEO 的痛点：关键词总量小但转化意图强
- SaaS 工具太贵且过度通用化
- 学 Python 最好的方式就是写有用的脚本
- 每一个脚本都解决一个我在实操中真遇到过的具体问题

---

*Made with ❤️ for the B2B SEO trenches*
