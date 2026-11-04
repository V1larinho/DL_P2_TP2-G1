import pathlib
import markdown
from playwright.sync_api import sync_playwright

p2_dir = pathlib.Path(__file__).resolve().parent.parent
md_resp = p2_dir / "docs" / "RESPOSTAS_PL08.md"
pdf_resp = p2_dir / "docs" / "RESPOSTAS_PL08.pdf"

with open(md_resp, "r", encoding="utf-8") as f:
    text = f.read()

html = markdown.markdown(text)
full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 1.8cm; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 10pt; line-height: 1.45; color: #1e293b; }}
h1 {{ font-size: 13pt; color: #1e3a8a; border-bottom: 2px solid #2563eb; padding-bottom: 4px; margin-bottom: 6px; }}
h2 {{ font-size: 11pt; color: #0f172a; margin-top: 14px; margin-bottom: 4px; }}
p {{ margin-bottom: 8px; text-align: justify; }}
blockquote {{ border-left: 3px solid #2563eb; padding-left: 8px; margin: 4px 0; color: #475569; font-size: 9pt; }}
strong {{ color: #0f172a; }}
hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 10px 0; }}
</style></head><body>{html}</body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(full_html)
    page.pdf(path=str(pdf_resp), format="A4", print_background=True)
    browser.close()

print(f"PDF Respostas PL08: {pdf_resp}")
