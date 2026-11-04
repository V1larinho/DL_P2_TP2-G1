import pathlib
import markdown
from playwright.sync_api import sync_playwright
import pypdf

doc_dir = pathlib.Path(__file__).resolve().parent.parent / "docs"
md_path = doc_dir / "P2-D1.md"
pdf_path = doc_dir / "P2-D1.pdf"
img_path = doc_dir / "mockup_anotacao.png"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Convert markdown to html with table extension
html_body = markdown.markdown(text, extensions=["tables", "fenced_code"])

# Replace relative image with file:/// URI
img_uri = img_path.as_uri()
html_body = html_body.replace('src="mockup_anotacao.png"', f'src="{img_uri}"')

# Add explicit page break right before Section 4
html_body = html_body.replace('<h2>4. Aplicação', '<div style="page-break-before: always;"></div><h2>4. Aplicação')

html_content = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<style>
  @page {{
    size: A4;
    margin: 0.65cm 0.85cm;
    @bottom-right {{
      content: "Página " counter(page) " de " counter(pages);
      font-size: 6.5pt;
      color: #64748b;
    }}
  }}
  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 7.0pt;
    line-height: 1.22;
    color: #1e293b;
    margin: 0;
    padding: 0;
  }}
  h1 {{
    font-size: 11.5pt;
    font-weight: 700;
    color: #0f172a;
    margin: 0 0 1px 0;
    border-bottom: 1.5px solid #2563eb;
    padding-bottom: 1px;
  }}
  h2 {{
    font-size: 8.5pt;
    font-weight: 700;
    color: #1e3a8a;
    margin-top: 4px;
    margin-bottom: 1px;
    border-bottom: 0.5px solid #cbd5e1;
    padding-bottom: 1px;
    text-transform: uppercase;
    letter-spacing: 0.2px;
  }}
  h3 {{
    font-size: 7.2pt;
    font-weight: 700;
    color: #334155;
    margin-top: 2px;
    margin-bottom: 1px;
  }}
  p {{
    margin: 0 0 2px 0;
    text-align: justify;
  }}
  ul, ol {{
    margin: 0 0 2px 0;
    padding-left: 12px;
  }}
  li {{
    margin-bottom: 0.5px;
  }}
  table {{
    width: 100%;
    border-collapse: collapse;
    font-size: 6.2pt;
    margin: 2px 0;
    line-height: 1.12;
  }}
  th, td {{
    border: 0.5px solid #cbd5e1;
    padding: 1.5px 3.5px;
    text-align: left;
    vertical-align: top;
  }}
  th {{
    background-color: #f1f5f9;
    font-weight: 700;
    color: #1e293b;
  }}
  tr:nth-child(even) {{
    background-color: #f8fafc;
  }}
  blockquote {{
    border-left: 2px solid #2563eb;
    background: #eff6ff;
    margin: 2px 0;
    padding: 1.5px 5px;
    font-size: 6.6pt;
    color: #1e40af;
  }}
  code {{
    background-color: #f1f5f9;
    padding: 0 1.5px;
    border-radius: 2px;
    font-family: Consolas, monospace;
    font-size: 6.5pt;
    color: #0f172a;
  }}
  img {{
    max-width: 92%;
    max-height: 160px;
    object-fit: contain;
    border-radius: 4px;
    border: 1px solid #94a3b8;
    margin: 2px auto;
    display: block;
    box-shadow: 0 1px 3px rgba(0,0,0,0.1);
  }}
  hr {{
    border: none;
    border-top: 0.5px solid #e2e8f0;
    margin: 2px 0;
  }}
</style>
</head>
<body>
{html_body}
</body>
</html>
"""

html_tmp = doc_dir / "P2-D1.html"
with open(html_tmp, "w", encoding="utf-8") as f:
    f.write(html_content)

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(html_tmp.as_uri())
    page.wait_for_timeout(1000)
    page.pdf(
        path=str(pdf_path),
        format="A4",
        margin={"top": "0.65cm", "bottom": "0.65cm", "left": "0.85cm", "right": "0.85cm"},
        print_background=True,
    )
    browser.close()

reader = pypdf.PdfReader(str(pdf_path))
print(f"Resultado final: {len(reader.pages)} página(s) gerada(s).")
