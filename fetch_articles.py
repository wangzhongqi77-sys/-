import json
import os
import re

OUTPUT_DIR = r"d:\新建文件夹\公众号文章"

for subdir in ["智堡Wisburg", "Mikko", "朱尘"]:
    os.makedirs(os.path.join(OUTPUT_DIR, subdir), exist_ok=True)

def clean_filename(name, max_len=80):
    name = re.sub(r'[\\/:*?"<>|\n\r]', '_', name)
    if len(name) > max_len:
        name = name[:max_len]
    return name.strip()

# Combine all search results
zhibao = json.load(open(r'd:\新建文件夹\search_zhibao.json', encoding='utf-8'))
mikko = json.load(open(r'd:\新建文件夹\search_mikko.json', encoding='utf-8'))
zhuchen = json.load(open(r'd:\新建文件夹\search_zhuchen.json', encoding='utf-8'))

# Filter to only target authors' articles
target_sources = ["智堡Wisburg", "善易-智堡网", "华尔街见闻", "固收汇", "郁言债市"]

all_target = []

for a in zhibao['articles']:
    if a['source'] in target_sources:
        all_target.append({**a, "category": "智堡Wisburg"})

for a in mikko['articles']:
    if a['source'] in target_sources:
        all_target.append({**a, "category": "Mikko"})

for a in zhuchen['articles']:
    if a['source'] in target_sources:
        all_target.append({**a, "category": "朱尘"})

# Remove duplicates by title
seen = set()
unique = []
for a in all_target:
    if a['title'] not in seen:
        seen.add(a['title'])
        unique.append(a)

# Generate MD files with search result info
count = 0
for article in unique:
    category = article['category']
    title = article['title']
    date = article.get('date_text', article.get('datetime', ''))
    source = article['source']
    url = article['url']
    summary = article.get('summary', '')
    
    filename = clean_filename(f"{date}_{title}") + ".md"
    filepath = os.path.join(OUTPUT_DIR, category, filename)
    
    md_content = f"""# {title}

> **来源**: {source}  
> **日期**: {date}  
> **原文链接**: {url}

---

## 摘要

{summary}

## 备注

> 因微信公众号反爬限制，本文目前为摘要版本。  
> 如需阅读完整内容，请点击上方原文链接在微信中打开。

---

*本文由 AI 助手自动搜索整理*
"""
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(md_content)
    count += 1
    print(f"  [{count}] {category}/{filename}")

print(f"\nDone! {count} articles saved to {OUTPUT_DIR}")
print(f"\nCategories:")
for subdir in ["智堡Wisburg", "Mikko", "朱尘"]:
    path = os.path.join(OUTPUT_DIR, subdir)
    files = [f for f in os.listdir(path) if f.endswith('.md')]
    print(f"  {subdir}: {len(files)} articles")
