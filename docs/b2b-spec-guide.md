# B2B 工业 SEO 写作指南

> 面向制造业/外贸网站的 AEO（AI Engine Optimization）内容编写方法论

---

## 目录

1. [核心理念](#核心理念)
2. [七段式文章结构](#七段式文章结构)
3. [Meta 优化规范](#meta-优化规范)
4. [结构化数据 Schema](#结构化数据-schema)
5. [图片处理规范](#图片处理规范)
6. [内部链接策略](#内部链接策略)
7. [AEO 自检清单](#aeo-自检清单)
8. [常见陷阱](#常见陷阱)

---

## 核心理念

B2B 工业 SEO 和 B2C 有本质区别：

| 维度 | B2C | B2B |
|------|-----|-----|
| 搜索量 | 高（千~万级） | 低（十~百级） |
| 转化周期 | 几分钟~几天 | 几周~几个月 |
| 购买决策 | 个人冲动 | 采购团队决策 |
| 内容深度 | 列表/对比/评测 | 技术参数/认证/标准 |
| 关键词意图 | 信息型为主 | 商业型+交易型为主 |

**核心原则：** B2B SEO 不求量求质。一篇深度技术文章比十篇泛泛而谈的 SEO 文章有价值得多。

### AEO（AI Engine Optimization）

2025-2026 年 SEO 最大的变化是 AI 搜索引擎（如 Google SGE、Perplexity、Bing Copilot）成为流量入口。AEO 的核心：

1. **AI 直接回答的内容 > 点击诱饵** — AI 会提取你的内容作为答案来源
2. **结构化 > 文案风格** — JSON-LD Schema、清晰的标题层级、FAQ 格式
3. **权威信号** — 认证、资质、数据来源、客户案例
4. **实体关联** — 精准使用行业术语，帮助 AI 建立语义关联

---

## 七段式文章结构

每篇博客固定 7 段结构，确保 AI 能快速理解内容框架：

### 结构模板

```
标题: [核心关键词] + [价值主张] | [品牌名]

1️⃣ 引言段落（2-3句）
   - 行业痛点 → 本文解决的问题 → 读者将获得什么

2️⃣ 背景/概述段落（3-4句）
   - 为什么这个问题重要
   - 简单定义/引入核心概念

3️⃣ 技术/方案段落 ①（3-5句）
   - 核心方案 A 的详细介绍
   - 适用场景 + 具体参数/数据

4️⃣ 技术/方案段落 ②（3-5句）
   - 核心方案 B 的详细介绍
   - 对比方案 A，突出差异

5️⃣ 实践指南段落（4-6句）
   - 操作步骤或选型建议
   - 可执行的推荐

6️⃣ 案例/数据段落（3-4句）
   - 实际应用案例 or 行业数据
   - 用具体数字增强可信度

7️⃣ 总结 + CTA（2-3句）
   - 回顾关键结论
   - 引导用户行动（查产品页/联系销售/下载资料）
```

### 配图要求

- 每段至少 1 张配图（共 ≥ 7 张）
- 图片格式：WebP，宽度 ≥ 1200px
- Alt text：中文+英文，含核心关键词

---

## Meta 优化规范

### Title（页面标题）

```
规则: [核心关键词] + [差异化价值] | [品牌名]
长度: 30-60 字符

✅ 好例子:
  Hydraulic Cylinders for Mobile Equipment | Henghong RV
  16 Years of RV Parts Manufacturing | Henghong RV
  B2B Air Conditioner Parts Supplier in China | Henghong

❌ 坏例子:
  Products  ← 太短，没有价值
  Home | Henghong RV Parts Manufacturer  ← Home 是默认标题
  Henghong RV - The Leading Manufacturer...  ← 太长被截断
```

### Meta Description

```
规则: [场景描述] + [解决方案] + [价值点]
长度: 110-160 字符（含空格）

✅ 模板:
  Looking for [产品/方案] for [具体场景]?
  [品牌名] offers [核心卖点] with [差异化优势].
  ✓ [证书1] ✓ [证书2] ✓ [服务承诺]
  Contact us for [价值点].
```

### H1 标签

- 每页必须只有一个 H1
- H1 必须包含核心关键词
- H1 和 Title 可以不同，但不能语义冲突
- 长度建议 20-50 字符

### H2 分段

- 每篇博客使用 6-7 个 H2
- 每个 H2 代表一个段落的核心话题
- H2 尽量包含长尾关键词变体
- H2 → H3 层级深度不超过 2 级

---

## 结构化数据 Schema

### Article Schema（博客文章必加）

```json
{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "文章标题",
  "description": "文章描述",
  "author": {
    "@type": "Organization",
    "name": "Henghong RV"
  },
  "datePublished": "2026-06-01",
  "dateModified": "2026-06-15",
  "image": "https://henghongrv.com/images/featured-image.jpg",
  "publisher": {
    "@type": "Organization",
    "name": "Hangzhou Henghong RV Parts Co., Ltd.",
    "url": "https://henghongrv.com"
  }
}
```

### FAQPage Schema（含 FAQ 段落的文章）

```json
{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [{
    "@type": "Question",
    "name": "问题1？",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "回答内容。"
    }
  }, {
    "@type": "Question",
    "name": "问题2？",
    "acceptedAnswer": {
      "@type": "Answer",
      "text": "回答内容。"
    }
  }]
}
```

### Product Schema（产品页）

```json
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": "产品名称",
  "description": "产品描述",
  "brand": {
    "@type": "Brand",
    "name": "Henghong"
  },
  "category": "RV Parts",
  "image": "https://henghongrv.com/images/product.jpg"
}
```

### BreadcrumbList（面包屑导航）

```json
{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [{
    "@type": "ListItem",
    "position": 1,
    "name": "Home",
    "item": "https://henghongrv.com/"
  }, {
    "@type": "ListItem",
    "position": 2,
    "name": "Blog",
    "item": "https://henghongrv.com/blog"
  }, {
    "@type": "ListItem",
    "position": 3,
    "name": "文章标题"
  }]
}
```

---

## 图片处理规范

| 属性 | 要求 |
|------|------|
| 格式 | WebP（主）+ JPEG（备选） |
| 尺寸 | 宽度 ≥ 1200px，比例 16:9 或 4:3 |
| Alt Text | 中文 + 英文，含核心关键词 |
| 文件名 | kebab-case，描述性（e.g., `hydraulic-cylinder-manufacturing.jpg`） |
| 压缩 | ≤ 200KB（使用 TinyPNG 或 Squoosh） |
| 延迟加载 | `loading="lazy"` |
| 唯一性 | 不要在不同页面重复使用同一张图片 |

### Alt Text 模板

```
[场景] showing [主体] in/with [特征] - [品牌] [关键词]

例:
AC evaporator assembly in RV production line - Henghong RV parts
Factory worker inspecting hydraulic cylinder quality - Henghong
Overhead crane moving RV chassis at 12,000 sqm facility - Henghong
```

---

## 内部链接策略

### 规则

1. **每篇文章至少 3 个内部链接**（1 个回首页，1 个回博客列表，1 个到相关产品页/其他文章）
2. **锚文本用描述性短语** — 不要用"点击这里"或"更多"
3. **链接到相关主题** — 构成主题簇（Topic Cluster）
4. **新文章反向链接旧文章** — 形成永久更新

### 链接分布建议

```
段落 ① → 首页（核心品牌链接）
段落 ③ → 相关产品页
段落 ⑤ → 相关的另一篇博客
段落 ⑦ → 博客列表 / 联系页面
```

### 主题簇结构

```
Pillar Page（核心支柱页）
  ├── Cluster Article 1（长尾关键词）
  ├── Cluster Article 2（长尾关键词）
  └── Cluster Article 3（长尾关键词）
  
每个 Cluster Article 都要链接回 Pillar Page，Pillar Page 链接到所有 Cluster。
```

---

## AEO 自检清单

发布前逐项检查：

### ✅ 元数据

- [ ] Title 标签：30-60 字符，含核心关键词
- [ ] Meta Description：110-160 字符，含行动号召
- [ ] H1 标签：唯一，含核心关键词
- [ ] generateMetadata 导出（Next.js 项目）

### ✅ 内容质量

- [ ] 七段式结构完整
- [ ] 每段 ≥ 3 句
- [ ] 无 AI 套话（"在…中"、"A不仅是…更是…"）
- [ ] 有具体数据/案例（至少 1 个）
- [ ] 图片 ≥ 7 张，全部加 Alt Text

### ✅ Schema

- [ ] Article Schema 已添加
- [ ] 需要时添加 FAQPage Schema
- [ ] BreadcrumbList Schema 存在
- [ ] JSON-LD 语法验证通过（用 https://validator.schema.org/）

### ✅ 链接

- [ ] 内部链接 ≥ 3 个
- [ ] 所有链接有效（200 状态码）
- [ ] 锚文本描述清晰

### ✅ 技术合规

- [ ] 无中文双 Title（Next.js generateMetadata 常见陷阱）
- [ ] H2 缩进正确（无额外空格导致不渲染）
- [ ] 博客列表页已更新
- [ ] 页面不是 404 或 500

---

## 常见陷阱

### 🚨 陷阱 1：Next.js generateMetadata 缺失

在 Next.js App Router 中，如果在布局文件里也有 `metadata` 导出但没有 `generateMetadata`，内容页会出现重复 Title。

### 🚨 陷阱 2：H2 缩进错误

```
## 正确的 H2（紧贴行首，一个井号+一个空格）
## 也要注意文本不要缩进

  ## 错误的 H2（前面有空格，Markdown 不渲染为标题）
```

### 🚨 陷阱 3：Title 双重复

常见原因：
- `layout.tsx` 和 `page.tsx` 同时定义了 `metadata.title`
- `template` 和 `default` 混淆
- 解决：只有 `page.tsx` 用 `generateMetadata` 设置具体标题

### 🚨 陷阱 4：博客列表不更新

新文章发布后，列表页面（如 `/blog`）需要手动添加入口，否则 Google 爬虫找不到新页面。

---

*Made for the B2B SEO trenches · 最后更新 2026-06*
