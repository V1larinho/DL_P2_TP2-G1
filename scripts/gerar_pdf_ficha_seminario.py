import pathlib
import markdown
from playwright.sync_api import sync_playwright

p2_dir = pathlib.Path(__file__).resolve().parent.parent
md_ficha = p2_dir / "seminario" / "FICHA_RESUMO_SEMINARIO.md"
pdf_ficha = p2_dir / "seminario" / "FICHA_RESUMO_SEMINARIO.pdf"

with open(md_ficha, "r", encoding="utf-8") as f:
    text = f.read()

html = markdown.markdown(text)
full_html = f"""<!DOCTYPE html>
<html><head><meta charset="utf-8">
<style>
@page {{ size: A4; margin: 1.4cm 1.6cm; }}
body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; font-size: 8.5pt; line-height: 1.35; color: #1e293b; }}
h1 {{ font-size: 13pt; color: #1e3a8a; border-bottom: 2px solid #2563eb; padding-bottom: 2px; margin-bottom: 4px; }}
h2 {{ font-size: 9.5pt; color: #0f172a; margin-top: 10px; margin-bottom: 4px; font-weight: 700; }}
p {{ margin-bottom: 6px; text-align: justify; }}
blockquote {{ border-left: 2.5px solid #2563eb; padding-left: 8px; margin: 4px 0; color: #475569; font-size: 8pt; }}
strong {{ color: #0f172a; }}
hr {{ border: none; border-top: 1px solid #e2e8f0; margin: 8px 0; }}
</style></head><body>{html}</body></html>"""

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.set_content(full_html)
    page.pdf(path=str(pdf_ficha), format="A4", print_background=True)
    browser.close()

print(f"PDF Ficha Resumo Seminário: {pdf_ficha}")

