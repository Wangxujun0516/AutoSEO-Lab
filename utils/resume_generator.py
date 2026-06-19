#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
B2B SEO Technical Resume Generator
===================================

生成 ATS (Applicant Tracking System) 友好的简历 Markdown，
专门针对 B2B SEO / Technical Writing 远程职位优化。

Usage:
    python utils/resume_generator.py
    python utils/resume_generator.py --format html --output resume.html
"""

import argparse
from datetime import datetime


# ============================================================================
# Resume Data - Edit this section to customize
# ============================================================================
RESUME_DATA = {
    "name": "Wang Xujun",
    "title": "B2B SEO Engineer & Technical Writer",
    "location": "Ningbo, China (Remote)",
    "email": "wangxujun0516@email.com",
    "phone": "+86-574-XXXX-XXXX",
    "website": "https://wangxujun0516.github.io/AutoSEO-Lab/",
    "github": "https://github.com/Wangxujun0516",
    "linkedin": "https://linkedin.com/in/wangxujun",

    "summary": """B2B SEO engineer with 2+ years of experience in technical SEO, GEO (Generative Engine Optimization), and Python automation. Expert in building 100% dependency-free data pipelines that bypass corporate firewall restrictions. Proven track record of generating high-intent B2B traffic for industrial manufacturing clients (RV leveling systems, hydraulic components) through structured data markup and procurement-focused content engineering. Seeking remote SEO/Technical Writing roles at B2B SaaS companies targeting international procurement managers.""",

    "skills": {
        "SEO & Analytics": ["Google Search Console API", "Google Analytics 4", "Umami", "Schema.org JSON-LD", "Sitemap.xml", " robots.txt", "Core Web Vitals", "PageSpeed Insights"],
        "GEO Optimization": ["LLM RAG Optimization", "Perplexity API", "Citation Probability", "Product Schema Markup", "FAQ Schema", "HowTo Schema"],
        "Programming": ["Python 3.10+", "urllib.request", "json", "xml.etree.ElementTree", "argparse", "urllib.parse"],
        "Content Engineering": ["VitePress", "Markdown", "LaTeX", "Technical Writing", "B2B Procurement Content", "OEM Documentation"],
        "Tools": ["Git/GitHub", "Notion", "Vercel", "GitHub Pages", "Clash Proxy"]
    },

    "experience": [
        {
            "company": "Henghong Intelligent Equipment Co., Ltd.",
            "role": "SEO & Technical Content Engineer (Freelance)",
            "period": "2025-01 - Present",
            "location": "Remote",
            "achievements": [
                "Built 100% native Python GSC data pipeline using urllib.request + ProxyHandler, bypassing httplib2/requests proxy deadlock in sandboxed Windows environment",
                "Increased organic search impressions by 340% within 90 days through JSON-LD Product Schema markup targeting B2B procurement keywords (RV leveling jack specifications)",
                "Designed and deployed technical documentation site using VitePress, serving 500+ monthly unique visitors from US/Canada industrial procurement markets",
                "Implemented GEO (Generative Engine Optimization) strategy using structured data markup, achieving top-3 citation probability in Perplexity AI RAG engines for key product queries",
                "Reduced GSC data acquisition time from 4 hours/week (manual) to 15 minutes/week (automated) through Python CLI orchestrator"
            ]
        },
        {
            "company": "AutoSEO-Lab (Open Source Project)",
            "role": "Lead Developer & Technical Writer",
            "period": "2024-06 - Present",
            "location": "Remote",
            "achievements": [
                "Architected and published open-source SEO automation toolkit targeting B2B industrial manufacturing clients",
                "Implemented IndexNow protocol client for Bing/Yandex/Naver instant URL indexing (100% native Python, zero external dependencies)",
                "Created Umami-to-Notion traffic sync pipeline for automated weekly reporting to Notion Workstation database",
                "Developed batch title cleaner with Shadow Ledger algorithm for B2B industrial webpage metadata standardization",
                "Generated 15+ technical documentation pages covering SEO/GEO concepts, Python automation, and B2B procurement compliance"
            ]
        }
    ],

    "projects": [
        {
            "name": "AutoSEO-Lab GitHub Repository",
            "description": "Open-source SEO automation toolkit for B2B industrial sites",
            "tech": "Python 3.10+, VitePress, JSON-LD, Schema.org",
            "link": "https://github.com/Wangxujun0516/AutoSEO-Lab",
            "highlights": [
                "100% dependency-free GSC orchestrator with native proxy tunneling",
                "Batch sitemap indexing via Google Indexing API + IndexNow protocol",
                "SEO metadata audit pipeline with title/description extraction and CSV export"
            ]
        },
        {
            "name": "Henghong GEO Content Strategy",
            "description": "B2B procurement-focused content and structured data optimization",
            "tech": "Product Schema, FAQ Schema, HowTo Schema, VitePress",
            "link": "https://www.henghongrv.com/",
            "highlights": [
                "Implemented Product Schema with Intertek Verified Supplier certification markup",
                "Created 12V vs 24V Electric RV Leveling Jack technical comparison guide (LaTeX formulas, engineering-grade content)",
                "Developed B2B Procurement Compliance Guide covering CE/OSHA/ISO 9001 requirements"
            ]
        },
        {
            "name": "GSC Native Pipeline Breakthrough",
            "description": "Solving Google API authentication in restricted network environments",
            "tech": "urllib.request, ProxyHandler, OAuth 2.0, JSON",
            "link": "https://wangxujun0516.github.io/AutoSEO-Lab/gsc-native-pipeline-breakthrough.html",
            "highlights": [
                "Documented 3-layer technical blockade: pip dependency deadlock, proxy handler blackhole, GSC 403 identity crisis",
                "Published technical chronicle as portfolio piece demonstrating extreme engineering adaptability",
                "Achieved 6x data collection efficiency improvement over manual GSC reporting"
            ]
        }
    ],

    "education": [
        {
            "degree": "Bachelor of Engineering",
            "major": "Mechanical Engineering",
            "school": "Zhejiang University of Technology",
            "period": "2016 - 2020",
            "notes": "Focus on industrial automation and hydraulic systems"
        }
    ],

    "certifications": [
        "Google Analytics Individual Qualification (GAIQ)",
        "Google Search Console Certification",
        "HubSpot SEO Certification",
        "Technical Writing Professional (O'Reilly Media)"
    ],

    "languages": [
        {"name": "Mandarin Chinese", "level": "Native"},
        {"name": "English", "level": "Professional (CET-6)"}
    ]
}


def generate_markdown(resume: dict) -> str:
    """Generate ATS-friendly Markdown resume"""

    md = f"""# {resume['name']}

**{resume['title']}**  
{resume['location']} | {resume['email']} | {resume['phone']}  
{resume['website']} | {resume['github']} | {resume['linkedin']}

---

## Professional Summary

{resume['summary']}

---

## Core Competencies

"""

    for category, skills in resume['skills'].items():
        md += f"**{category}**: {', '.join(skills)}\n"

    md += "\n---\n\n## Professional Experience\n\n"

    for job in resume['experience']:
        md += f"### {job['role']}\n"
        md += f"**{job['company']}** | {job['period']} | {job['location']}\n\n"
        for achievement in job['achievements']:
            md += f"- {achievement}\n"
        md += "\n"

    md += "---\n\n## Notable Projects\n\n"

    for project in resume['projects']:
        md += f"### {project['name']}\n"
        md += f"{project['description']}\n"
        md += f"**Tech Stack**: {project['tech']}\n"
        md += f"**Link**: {project['link']}\n\n"
        md += "**Highlights**:\n"
        for highlight in project['highlights']:
            md += f"- {highlight}\n"
        md += "\n"

    md += "---\n\n## Education\n\n"
    for edu in resume['education']:
        md += f"**{edu['degree']} in {edu['major']}**  \n"
        md += f"{edu['school']} | {edu['period']}\n"
        if edu.get('notes'):
            md += f"_{edu['notes']}_\n"
        md += "\n"

    md += "---\n\n## Certifications\n\n"
    for cert in resume['certifications']:
        md += f"- {cert}\n"
    md += "\n"

    md += "---\n\n## Languages\n\n"
    for lang in resume['languages']:
        md += f"- **{lang['name']}**: {lang['level']}\n"

    md += f"\n---\n\n*Last Updated: {datetime.now().strftime('%Y-%m-%d')}*  \n*Generated by AutoSEO-Lab Resume Generator*"

    return md


def generate_html(resume: dict) -> str:
    """Generate HTML resume with CSS styling"""

    html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{resume['name']} - Resume</title>
    <style>
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{ font-family: 'Segoe UI', Arial, sans-serif; line-height: 1.6; max-width: 900px; margin: 0 auto; padding: 40px 20px; color: #333; }}
        h1 {{ font-size: 2.2em; color: #1a1a2e; margin-bottom: 5px; }}
        h2 {{ font-size: 1.4em; color: #16213e; border-bottom: 2px solid #0f3460; padding-bottom: 8px; margin: 30px 0 15px; }}
        h3 {{ font-size: 1.1em; color: #0f3460; margin-top: 20px; }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .title {{ font-size: 1.3em; color: #0f3460; margin-bottom: 10px; }}
        .contact {{ color: #666; font-size: 0.95em; }}
        .contact a {{ color: #0f3460; text-decoration: none; }}
        .summary {{ background: #f8f9fa; padding: 20px; border-left: 4px solid #0f3460; margin: 20px 0; }}
        .skills-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 15px; }}
        .skill-category {{ background: #f8f9fa; padding: 12px 15px; border-radius: 5px; }}
        .skill-category strong {{ color: #0f3460; }}
        .job {{ margin-bottom: 25px; }}
        .job-header {{ display: flex; justify-content: space-between; flex-wrap: wrap; }}
        .company {{ font-weight: bold; color: #1a1a2e; }}
        .period {{ color: #666; }}
        .achievements {{ margin-top: 10px; }}
        .achievements li {{ margin-bottom: 8px; margin-left: 20px; }}
        .project {{ background: #f8f9fa; padding: 15px; border-radius: 5px; margin: 15px 0; }}
        .project h3 {{ margin-top: 0; }}
        .tech {{ color: #0f3460; font-size: 0.9em; }}
        .certifications {{ display: flex; flex-wrap: wrap; gap: 10px; }}
        .cert {{ background: #0f3460; color: white; padding: 5px 12px; border-radius: 20px; font-size: 0.85em; }}
        a {{ color: #0f3460; }}
        @media print {{ body {{ padding: 20px; }} }}
    </style>
</head>
<body>
    <header class="header">
        <h1>{resume['name']}</h1>
        <div class="title">{resume['title']}</div>
        <div class="contact">
            {resume['location']} | <a href="mailto:{resume['email']}">{resume['email']}</a> | {resume['phone']}<br>
            <a href="{resume['website']}">{resume['website']}</a> | <a href="{resume['github']}">GitHub</a> | <a href="{resume['linkedin']}">LinkedIn</a>
        </div>
    </header>

    <section class="summary">
        <h2 style="border: none; margin-top: 0;">Professional Summary</h2>
        <p>{resume['summary']}</p>
    </section>

    <section>
        <h2>Core Competencies</h2>
        <div class="skills-grid">
"""

    for category, skills in resume['skills'].items():
        html += f'            <div class="skill-category"><strong>{category}</strong><br>{", ".join(skills)}</div>\n'

    html += """        </div>
    </section>

    <section>
        <h2>Professional Experience</h2>
"""

    for job in resume['experience']:
        html += f"""        <div class="job">
            <div class="job-header">
                <span class="company">{job['role']} @ {job['company']}</span>
                <span class="period">{job['period']} | {job['location']}</span>
            </div>
            <ul class="achievements">
"""
        for achievement in job['achievements']:
            html += f"                <li>{achievement}</li>\n"
        html += "            </ul>\n        </div>\n"

    html += """    </section>

    <section>
        <h2>Notable Projects</h2>
"""

    for project in resume['projects']:
        html += f"""        <div class="project">
            <h3><a href="{project['link']}">{project['name']}</a></h3>
            <p>{project['description']}</p>
            <p class="tech"><strong>Tech:</strong> {project['tech']}</p>
            <ul>
"""
        for highlight in project['highlights']:
            html += f"                <li>{highlight}</li>\n"
        html += "            </ul>\n        </div>\n"

    html += """    </section>

    <section>
        <h2>Education</h2>
"""

    for edu in resume['education']:
        html += f"""        <p><strong>{edu['degree']} in {edu['major']}</strong><br>
        {edu['school']} | {edu['period']}"""
        if edu.get('notes'):
            html += f"<br><em>{edu['notes']}</em>"
        html += "</p>\n"

    html += """    </section>

    <section>
        <h2>Certifications</h2>
        <div class="certifications">
"""

    for cert in resume['certifications']:
        html += f'            <span class="cert">{cert}</span>\n'

    html += """        </div>
    </section>

    <section>
        <h2>Languages</h2>
        <ul>
"""

    for lang in resume['languages']:
        html += f'            <li><strong>{lang["name"]}</strong>: {lang["level"]}</li>\n'

    html += f"""        </ul>
    </section>

    <footer style="margin-top: 40px; text-align: center; color: #666; font-size: 0.85em;">
        <p>Last Updated: {datetime.now().strftime('%Y-%m-%d')} | Generated by AutoSEO-Lab Resume Generator</p>
    </footer>
</body>
</html>"""

    return html


def main():
    parser = argparse.ArgumentParser(description="B2B SEO Technical Resume Generator")
    parser.add_argument("--format", "-f", choices=["md", "html"], default="md", help="输出格式")
    parser.add_argument("--output", "-o", help="输出文件路径")
    args = parser.parse_args()

    if args.format == "html":
        content = generate_html(RESUME_DATA)
        ext = ".html"
    else:
        content = generate_markdown(RESUME_DATA)
        ext = ".md"

    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"[+] Resume saved → {args.output}")
    else:
        print(content)


if __name__ == "__main__":
    main()
