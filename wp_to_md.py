# wp_to_md.py
import os
import xml.etree.ElementTree as ET
import frontmatter
import csv
from slugify import slugify
from bs4 import BeautifulSoup
import yaml
from image_handler import save_base64_image

# 載入設定
with open("config.yaml", "r") as f:
    config = yaml.safe_load(f)

def extract_alt_text(img_tag):
    return img_tag.get("alt") or img_tag.get("title") or "圖片"

def clean_wp_block_content(html: str, slug: str) -> str:
    soup = BeautifulSoup(html, 'html.parser')

    for img in soup.find_all("img"):
        src = img.get("src", "")

        # 改良後的 base64 偵測（容錯：缺 data: 前綴也支援）
        if "base64," in src and "image/" in src:
            if not src.startswith("data:"):
                src = "data:" + src
            try:
                cdn_url = save_base64_image(src, slug)
                alt = extract_alt_text(img)
                img.replace_with(f"![{alt}]({cdn_url})")
            except Exception as e:
                print(f"⚠️ 圖片處理錯誤：{e}")
                img.decompose()
        elif src.startswith("http"):
            alt = extract_alt_text(img)
            img.replace_with(f"![{alt}]({src})")
        else:
            img.decompose()

    # 處理列表與段落
    for ul in soup.find_all("ul"):
        for li in ul.find_all("li"):
            li.insert_before("- ")
            li.insert_after("\n")
    for p in soup.find_all("p"):
        p.insert_after("\n\n")

    # 解開雜訊 HTML 結構
    for tag in soup.find_all(["figure", "div", "columns", "column"]):
        tag.unwrap()

    return soup.get_text().strip()

# 建立資料夾
os.makedirs("exported_md", exist_ok=True)
os.makedirs("dataset", exist_ok=True)

# 解析 WordPress XML
tree = ET.parse("input/wordpress.xml")
root = tree.getroot()
ns = {'content': 'http://purl.org/rss/1.0/modules/content/'}
items = root.findall(".//item")

rows = []

for item in items:
    title = item.findtext("title", default="Untitled").strip()
    date = item.findtext("pubDate", default="").strip()
    content_html = item.findtext("content:encoded", default="", namespaces=ns)
    tags = [c.text.strip() for c in item.findall("category") if c.attrib.get("domain") == "post_tag"]
    slug = slugify(title)

    markdown_body = clean_wp_block_content(content_html, slug)

    # 使用 frontmatter 套件產出帶 YAML 的 Markdown 檔
    post = frontmatter.Post(markdown_body, **{
        "title": title,
        "date": date,
        "tags": tags
    })

    md_path = f"exported_md/{slug}.md"
    with open(md_path, "w", encoding="utf-8") as f:
        f.write(frontmatter.dumps(post))

    rows.append({
        "slug": slug,
        "title": title,
        "date": date,
        "tags": ", ".join(tags),
        "content": markdown_body
    })

# 匯出語料集 CSV
csv_path = "dataset/articles.csv"
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["slug", "title", "date", "tags", "content"])
    writer.writeheader()
    writer.writerows(rows)

print(f"✅ 完成：{len(rows)} 篇文章已轉換，Markdown 與圖片皆已處理完畢")
