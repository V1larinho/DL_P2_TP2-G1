import pathlib
import re
import bs4
import markdown
from playwright.sync_api import sync_playwright
import pypdf

doc_dir = pathlib.Path(__file__).resolve().parent.parent / "docs"
md_path = doc_dir / "P2-D1.md"
pdf_path = doc_dir / "P2-D1.pdf"
html_path = doc_dir / "P2-D1.html"
img_path = doc_dir / "mockup_anotacao.png"

with open(md_path, "r", encoding="utf-8") as f:
    text = f.read()

# Convert markdown to HTML with tables & code extensions
raw_html = markdown.markdown(text, extensions=["tables", "fenced_code"])
soup = bs4.BeautifulSoup(raw_html, "html.parser")

# Split elements into Page 1 and Page 2
p1_elements = []
p2_elements = []
current_page = 1

for el in list(soup.children):
    if not getattr(el, 'name', None):
        continue
    # When we reach Section 4, switch to Page 2
    if el.name == 'h2' and '4. Aplicação' in el.text:
        current_page = 2
    
    if current_page == 1:
        p1_elements.append(el)
    else:
        p2_elements.append(el)

# Build custom header for Page 1
header_html = """
<header class="doc-header">
  <div class="header-top-bar">
    <div class="header-academic">
      <span class="degrees">MEI / MEB / MECD / MMC</span>
      <span class="sep">·</span>
      <span class="uc">DEEP LEARNING APLICADO (2026/2027)</span>
    </div>
    <div class="header-status">
      <span class="badge-deliverable">PROPOSTA DE PROJETO · P2-D1</span>
    </div>
  </div>
  <div class="header-main">
    <h1 class="doc-title">Active Learning para defeitos em pontes de betão: quantos rótulos são mesmo precisos?</h1>
    <div class="header-meta">
      <span class="meta-item"><strong>Tema C (AL 1):</strong> Poucos Rótulos</span>
      <span class="meta-sep">·</span>
      <span class="meta-item"><strong>Turno:</strong> TP2</span>
      <span class="meta-sep">·</span>
      <span class="meta-item"><strong>Grupo:</strong> 1</span>
      <span class="meta-sep">·</span>
      <span class="meta-item"><strong>Data:</strong> 29 de Outubro de 2026</span>
    </div>
  </div>
</header>
"""

# Process Page 1 elements
# 1. Skip original h1, the first p (sub-header), and the title paragraph if present
filtered_p1 = []
skip_next_hr = False

for el in p1_elements:
    if el.name == 'h1':
        continue
    if el.name == 'p' and 'Tema C (AL 1)' in el.text:
        continue
    if el.name == 'p' and 'Título de trabalho:' in el.text:
        skip_next_hr = True
        continue
    if el.name == 'hr' and skip_next_hr:
        skip_next_hr = False
        continue
    filtered_p1.append(el)

# Format members table (the first table in filtered_p1)
for el in filtered_p1:
    if el.name == 'table':
        el['class'] = el.get('class', []) + ['table-members']
        # Enhance role cells
        for tr in el.find_all('tr'):
            tds = tr.find_all('td')
            if len(tds) >= 3:
                # Member name bold
                tds[0].string = tds[0].text
                # Role cell formatting
                role_text = tds[2].decode_contents()
                # Replace **A1** etc.
                role_text = re.sub(r'<strong>(A[1-5])</strong>', r'<span class="badge-role">\1</span>', role_text)
                role_text = re.sub(r'\b(A[1-5])\b', r'<span class="badge-role">\1</span>', role_text)
                role_text = re.sub(r'<strong>\(porta-voz\)</strong>|\(<strong>porta-voz</strong>\)', r'<span class="badge-spokesperson">porta-voz</span>', role_text)
                tds[2].clear()
                tds[2].append(bs4.BeautifulSoup(role_text, 'html.parser'))
        break

# Format Table 2.1 (second table in filtered_p1)
table_count = 0
for el in filtered_p1:
    if el.name == 'table':
        table_count += 1
        if table_count == 2:
            el['class'] = el.get('class', []) + ['table-problem-analysis']
            for tr in el.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    tds[0]['class'] = tds[0].get('class', []) + ['col-pergunta']
        elif table_count == 3:
            el['class'] = el.get('class', []) + ['table-sim-params']
            for tr in el.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 2:
                    tds[0]['class'] = tds[0].get('class', []) + ['col-param']

# Enhance section headers in P1
for el in filtered_p1:
    if el.name == 'h2':
        el['class'] = el.get('class', []) + ['sec-heading']
        m = re.match(r'(\d+)\.\s*(.*)', el.text.strip())
        if m:
            sec_num, sec_title = m.groups()
            el.clear()
            el.append(bs4.BeautifulSoup(f'<span class="sec-num">§{sec_num}</span> <span class="sec-title">{sec_title}</span>', 'html.parser'))
    elif el.name == 'h3':
        el['class'] = el.get('class', []) + ['subsec-heading']
    elif el.name == 'blockquote':
        el['class'] = el.get('class', []) + ['callout-box']
    elif el.name == 'p' and 'Hipóteses.' in el.text:
        # Style hypotheses
        content = el.decode_contents()
        content = re.sub(r'<strong>(H[1-4](?:\s*\(exploratória\))?)</strong>', r'<span class="badge-hyp">\1</span>', content)
        el.clear()
        el.append(bs4.BeautifulSoup(content, 'html.parser'))

# Process Page 2 elements
# Section 4 image formatting
img_uri = img_path.as_uri()

filtered_p2 = []
for el in p2_elements:
    if el.name == 'h2':
        el['class'] = el.get('class', []) + ['sec-heading']
        m = re.match(r'(\d+)\.\s*(.*)', el.text.strip())
        if m:
            sec_num, sec_title = m.groups()
            el.clear()
            el.append(bs4.BeautifulSoup(f'<span class="sec-num">§{sec_num}</span> <span class="sec-title">{sec_title}</span>', 'html.parser'))
        filtered_p2.append(el)
    elif el.name == 'p' and el.find('img'):
        # Replace p containing img with structured figure
        fig_html = f"""
        <figure class="mockup-figure">
          <div class="mockup-frame">
            <img src="{img_uri}" alt="Assistente de anotação — Interface Gradio">
          </div>
          <figcaption><strong>Figura 1</strong> — Assistente de anotação interativo (Gradio) com re-treino em tempo real e visualização da composição de classes rotuladas.</figcaption>
        </figure>
        """
        filtered_p2.append(bs4.BeautifulSoup(fig_html, 'html.parser'))
    elif el.name == 'table':
        # There are 2 tables in page 2: Schedule and Computational Estimate
        if not any('table-schedule' in x.get('class', []) for x in filtered_p2 if getattr(x, 'name', None) == 'table'):
            el['class'] = el.get('class', []) + ['table-schedule']
            for tr in el.find_all('tr'):
                tds = tr.find_all('td')
                if len(tds) >= 3:
                    # In Responsável column, add badge to A1..A5
                    resp_html = tds[2].decode_contents()
                    resp_html = re.sub(r'\b(A[1-5])\b', r'<span class="badge-role-mini">\1</span>', resp_html)
                    tds[2].clear()
                    tds[2].append(bs4.BeautifulSoup(resp_html, 'html.parser'))
            filtered_p2.append(el)
        else:
            el['class'] = el.get('class', []) + ['table-computational']
            filtered_p2.append(el)
    else:
        filtered_p2.append(el)

body_p1 = "".join(str(el) for el in filtered_p1)
body_p2 = "".join(str(el) for el in filtered_p2)

full_html = f"""<!DOCTYPE html>
<html lang="pt">
<head>
<meta charset="utf-8">
<title>P2-D1 — Proposta do Projeto (Tema C: Active Learning)</title>
<style>
  @page {{
    size: A4;
    margin: 0.60cm 0.75cm 0.85cm 0.75cm;
  }}

  :root {{
    --primary: #1e3a8a;
    --primary-dark: #0f172a;
    --primary-accent: #2563eb;
    --primary-light: #eff6ff;
    --primary-border: #bfdbfe;
    --slate-text: #1e293b;
    --slate-muted: #475569;
    --slate-light: #f8fafc;
    --border-color: #cbd5e1;
    --border-subtle: #e2e8f0;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    font-size: 6.6pt;
    line-height: 1.20;
    color: var(--slate-text);
    margin: 0;
    padding: 0;
    background: #ffffff;
    -webkit-print-color-adjust: exact;
    print-color-adjust: exact;
  }}

  /* Page container layout */
  .page-container {{
    width: 100%;
    position: relative;
  }}

  .page-break {{
    page-break-before: always;
    break-before: page;
  }}

  /* Header Styling */
  .doc-header {{
    border-bottom: 2px solid var(--primary-accent);
    padding-bottom: 2px;
    margin-bottom: 3px;
  }}

  .header-top-bar {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    border-bottom: 0.5px solid var(--border-subtle);
    padding-bottom: 1.5px;
    margin-bottom: 2px;
  }}

  .header-academic {{
    font-size: 6.2pt;
    font-weight: 700;
    letter-spacing: 0.3px;
    color: var(--primary);
  }}

  .header-academic .sep {{
    color: var(--border-color);
    margin: 0 4px;
  }}

  .badge-deliverable {{
    background: var(--primary);
    color: #ffffff;
    font-size: 5.6pt;
    font-weight: 700;
    letter-spacing: 0.4px;
    padding: 1.5px 5px;
    border-radius: 3px;
    text-transform: uppercase;
  }}

  .doc-title {{
    font-size: 10.5pt;
    font-weight: 800;
    color: var(--primary-dark);
    line-height: 1.15;
    margin: 1.5px 0 2px 0;
    letter-spacing: -0.2px;
  }}

  .header-meta {{
    font-size: 6.0pt;
    color: var(--slate-muted);
    display: flex;
    align-items: center;
    gap: 4px;
  }}

  .meta-sep {{
    color: var(--border-color);
  }}

  /* Section Headings */
  .sec-heading {{
    font-size: 7.8pt;
    font-weight: 700;
    color: var(--primary);
    margin: 3.5px 0 1.5px 0;
    padding-bottom: 1px;
    border-bottom: 1px solid var(--border-color);
    display: flex;
    align-items: center;
    letter-spacing: 0.2px;
    text-transform: uppercase;
  }}

  .sec-num {{
    background: var(--primary);
    color: #ffffff;
    font-size: 6.2pt;
    font-weight: 700;
    padding: 0.5px 3.5px;
    border-radius: 2px;
    margin-right: 4px;
    display: inline-block;
  }}

  .subsec-heading {{
    font-size: 6.8pt;
    font-weight: 700;
    color: var(--primary-dark);
    margin: 2.5px 0 1px 0;
  }}

  /* Paragraphs and Lists */
  p {{
    margin: 0 0 1.8px 0;
    text-align: justify;
    text-justify: inter-word;
  }}

  ul, ol {{
    margin: 0 0 2px 0;
    padding-left: 11px;
  }}

  li {{
    margin-bottom: 0.5px;
    text-align: justify;
  }}

  /* Tables */
  table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    font-size: 5.9pt;
    margin: 2px 0;
    line-height: 1.12;
    border: 0.5px solid var(--border-color);
    border-radius: 3px;
    overflow: hidden;
  }}

  th {{
    background-color: var(--primary);
    color: #ffffff;
    font-weight: 700;
    font-size: 5.9pt;
    letter-spacing: 0.2px;
    padding: 1.8px 3.5px;
    text-align: left;
    border: none;
    border-bottom: 0.5px solid var(--primary-dark);
  }}

  td {{
    border: none;
    border-bottom: 0.5px solid var(--border-subtle);
    border-right: 0.5px solid var(--border-subtle);
    padding: 1.3px 3.5px;
    vertical-align: top;
    color: var(--slate-text);
  }}

  td:last-child {{
    border-right: none;
  }}

  tr:last-child td {{
    border-bottom: none;
  }}

  tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}

  tr:nth-child(odd) td {{
    background-color: #ffffff;
  }}

  /* Table-specific column formatting */
  .table-members th:nth-child(1), .table-members td:nth-child(1) {{ width: 22%; font-weight: 600; color: var(--primary-dark); }}
  .table-members th:nth-child(2), .table-members td:nth-child(2) {{ width: 12%; font-family: Consolas, monospace; }}
  .table-members th:nth-child(3), .table-members td:nth-child(3) {{ width: 30%; }}
  .table-members th:nth-child(4), .table-members td:nth-child(4) {{ width: 36%; }}

  .table-problem-analysis th:nth-child(1), .table-problem-analysis td:nth-child(1) {{
    width: 26%;
    font-weight: 700;
    color: var(--primary);
    background-color: #f1f5f9;
  }}
  .table-problem-analysis th:nth-child(2), .table-problem-analysis td:nth-child(2) {{
    width: 74%;
  }}

  .table-sim-params th:nth-child(1), .table-sim-params td:nth-child(1) {{
    width: 25%;
    font-weight: 700;
    color: var(--primary-dark);
  }}
  .table-sim-params th:nth-child(2), .table-sim-params td:nth-child(2) {{
    width: 75%;
  }}

  .table-schedule th:nth-child(1), .table-schedule td:nth-child(1) {{ width: 15%; font-weight: 600; }}
  .table-schedule th:nth-child(2), .table-schedule td:nth-child(2) {{ width: 55%; }}
  .table-schedule th:nth-child(3), .table-schedule td:nth-child(3) {{ width: 30%; }}

  .table-computational th:nth-child(1), .table-computational td:nth-child(1) {{ width: 22%; font-weight: 600; }}
  .table-computational th:nth-child(2), .table-computational td:nth-child(2) {{ width: 52%; }}
  .table-computational th:nth-child(3), .table-computational td:nth-child(3) {{ width: 26%; }}

  /* Badges */
  .badge-role {{
    display: inline-block;
    background: #e0e7ff;
    color: #1e3a8a;
    font-weight: 700;
    font-size: 5.6pt;
    padding: 0.5px 3.5px;
    border-radius: 3px;
    border: 0.5px solid #c7d2fe;
    margin-right: 2px;
  }}

  .badge-role-mini {{
    display: inline-block;
    background: #e0e7ff;
    color: #1e3a8a;
    font-weight: 700;
    font-size: 5.4pt;
    padding: 0.5px 3px;
    border-radius: 2.5px;
    border: 0.5px solid #c7d2fe;
  }}

  .badge-spokesperson {{
    display: inline-block;
    background: #eff6ff;
    color: #1d4ed8;
    font-weight: 700;
    font-size: 5.2pt;
    padding: 0.5px 3px;
    border-radius: 2.5px;
    border: 0.5px solid #bfdbfe;
    text-transform: uppercase;
    margin-left: 2px;
  }}

  .badge-hyp {{
    display: inline-block;
    background: var(--primary);
    color: #ffffff;
    font-weight: 700;
    font-size: 5.6pt;
    padding: 0.5px 3.5px;
    border-radius: 2.5px;
    margin-right: 2px;
    vertical-align: baseline;
  }}

  /* Callout Blockquote */
  .callout-box {{
    border-left: 3px solid var(--primary-accent);
    background-color: var(--primary-light);
    border-top: 0.5px solid var(--primary-border);
    border-right: 0.5px solid var(--primary-border);
    border-bottom: 0.5px solid var(--primary-border);
    border-radius: 0 3px 3px 0;
    margin: 2px 0;
    padding: 2px 5px;
    font-size: 6.2pt;
    line-height: 1.18;
    color: var(--slate-text);
  }}

  .callout-box p {{
    margin: 0 0 1px 0;
  }}

  .callout-box p:last-child {{
    margin-bottom: 0;
  }}

  /* Code */
  code {{
    background-color: #f1f5f9;
    padding: 0 2px;
    border-radius: 2px;
    font-family: Consolas, monospace;
    font-size: 6.0pt;
    color: var(--primary-dark);
    border: 0.5px solid var(--border-subtle);
  }}

  /* Mockup Figure */
  .mockup-figure {{
    margin: 3px auto 2px auto;
    text-align: center;
  }}

  .mockup-frame {{
    display: inline-block;
    background: #ffffff;
    padding: 2px;
    border: 0.5px solid var(--border-color);
    border-radius: 4px;
    box-shadow: 0 1px 4px rgba(0, 0, 0, 0.08);
  }}

  .mockup-frame img {{
    display: block;
    max-height: 185px;
    max-width: 95%;
    margin: 0 auto;
    border-radius: 2px;
  }}

  figcaption {{
    font-size: 6.1pt;
    color: var(--slate-muted);
    margin-top: 2px;
    font-style: italic;
  }}

  figcaption strong {{
    font-style: normal;
    color: var(--primary);
  }}
</style>
</head>
<body>

<div class="page-container" id="page-1">
{header_html}
{body_p1}
</div>

<div class="page-break"></div>

<div class="page-container" id="page-2">
{body_p2}
</div>

</body>
</html>
"""

# Save enriched HTML
with open(html_path, "w", encoding="utf-8") as f:
    f.write(full_html)

# Generate PDF with Playwright
with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(html_path.as_uri())
    page.wait_for_timeout(1000)
    
    # Save preview screenshots of Page 1 and Page 2 for visual QA
    page.locator("#page-1").screenshot(path=str(doc_dir / "preview_p1.png"))
    page.locator("#page-2").screenshot(path=str(doc_dir / "preview_p2.png"))

    footer_tmpl = """
    <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; font-size: 6.2pt; width: 100%; display: flex; justify-content: space-between; align-items: center; padding: 0 0.75cm; color: #64748b; border-top: 0.5px solid #cbd5e1; padding-top: 2px;">
      <span><strong>MEI/MEB/MECD/MMC</strong> · Deep Learning Aplicado (2026/2027) · TP2 — Grupo 1 (Tema C: Active Learning)</span>
      <span>Página <span class="pageNumber"></span> de <span class="totalPages"></span></span>
    </div>
    """

    page.pdf(
        path=str(pdf_path),
        format="A4",
        margin={"top": "0.60cm", "bottom": "0.80cm", "left": "0.75cm", "right": "0.75cm"},
        display_header_footer=True,
        header_template="<div></div>",
        footer_template=footer_tmpl,
        print_background=True,
    )
    browser.close()

reader = pypdf.PdfReader(str(pdf_path))
num_pages = len(reader.pages)
print(f"Resultado final: {num_pages} página(s) gerada(s).")
