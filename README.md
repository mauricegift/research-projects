# Research Projects — Moi University BBM

A collection of Python generators that produce ready-to-submit academic
research project documents (Microsoft Word `.docx` and high-quality `.pdf`)
for Bachelor of Business Management (BBM) students at **Moi University,
Annex Campus**.

Each script writes a complete, properly formatted, university-style
research project — cover page with the Moi University crest, declaration,
dedication, acknowledgement, abstract, table of contents (with accurate
page numbers), list of tables, list of figures, list of abbreviations,
operational definitions, the full body chapters (Introduction, Literature
Review, Methodology, Findings, Conclusions, etc.), references, and
appendices.

All generated documents follow the standard Moi University academic
format:

- Times New Roman, 12 pt body
- 1.5 line spacing throughout the body
- 1.0″ top/bottom and 1.25″ left / 1.0″ right margins
- Roman numerals for the front matter, Arabic numerals from Chapter One
- Centred page numbering at the bottom of every page
- Embedded figures and grid-style tables

## Students covered

| Student | Document |
| --- | --- |
| Mourice Onyango (BBM/1891/22) | `Mourice_BBM_Annex_Project.docx` / `.pdf` — Effectiveness of Software Development on Moi University Students' Learning Behaviour |
| Mourice Onyango | `Mourice_BBM_453_CAT.docx` / `.pdf` |
| Sophie | `Sophie_Research_Project.docx` / `.pdf` |
| Calvince Odhiambo | `Calvince_Odhiambo_Research_Project.docx` / `.pdf` |
| Calvince | `Calvince_BBM_415_CAT.docx` / `.pdf` |
| Agnetta Opisa | `Agnetta_Opisa_Research_Project.docx` / `.pdf` |
| James Ngovi | `James_Ngovi_Research_Project.docx` / `.pdf` |

## Repository layout

```
.
├── README.md
├── .gitignore
│
├── generate_mourice_docx.py        # main project — DOCX
├── generate_mourice_pdf.py         # main project — PDF
├── generate_mourice_cat_docx.py    # CAT — DOCX
├── generate_mourice_cat_pdf.py     # CAT — PDF
├── generate_mourice_diagrams.py    # builds the system diagrams used in Mourice's project
│
├── generate_sophie_research.py     # Sophie — DOCX
├── generate_sophie_pdf.py          # Sophie — PDF
│
├── generate_calvince_docx.py       # Calvince research project — DOCX
├── generate_calvince_pdf.py        # Calvince research project — PDF
├── generate_calvince_cat_docx.py   # Calvince CAT — DOCX
├── generate_calvince_cat_pdf.py    # Calvince CAT — PDF
│
├── generate_agnetta_docx.py        # Agnetta research project
├── generate_research.py            # James Ngovi research project
├── generate_pdf.py                 # generic DOCX → PDF helper
│
├── mourice_figures/                # PNG diagrams (architecture, ER, use case, deployment, sequence)
│   ├── fig_6_1_architecture.png
│   ├── fig_6_2_er_diagram.png
│   ├── fig_6_3_use_case.png
│   ├── fig_6_4_deployment.png
│   └── fig_6_5_sequence.png
│
└── files/                          # All generated documents land here
    ├── Mourice_BBM_Annex_Project.docx
    ├── Mourice_BBM_Annex_Project.pdf
    ├── Mourice_BBM_453_CAT.docx
    ├── Mourice_BBM_453_CAT.pdf
    ├── Sophie_Research_Project.docx
    ├── Sophie_Research_Project.pdf
    ├── Calvince_Odhiambo_Research_Project.docx
    ├── Calvince_Odhiambo_Research_Project.pdf
    ├── Calvince_BBM_415_CAT.docx
    ├── Calvince_BBM_415_CAT.pdf
    ├── Agnetta_Opisa_Research_Project.docx
    ├── Agnetta_Opisa_Research_Project.pdf
    ├── James_Ngovi_Research_Project.docx
    └── James_Ngovi_Research_Project.pdf
```

## Prerequisites

- **Python 3.10+**
- Python packages:
  ```bash
  pip install python-docx reportlab PyMuPDF Pillow
  ```
- **LibreOffice** — used by some generators to convert the produced
  `.docx` into a polished `.pdf` (`soffice --headless --convert-to pdf`).
  On Debian / Ubuntu:
  ```bash
  sudo apt-get install libreoffice
  ```

## Usage

Run any generator from the repository root. Every script writes its
output into the `files/` folder (created automatically if missing):

```bash
# Mourice — full research project (DOCX + PDF)
python3 generate_mourice_docx.py
python3 generate_mourice_pdf.py

# Sophie
python3 generate_sophie_research.py
python3 generate_sophie_pdf.py

# Calvince
python3 generate_calvince_docx.py
python3 generate_calvince_pdf.py

# Calvince — BBM 415 CAT
python3 generate_calvince_cat_docx.py
python3 generate_calvince_cat_pdf.py

# Agnetta
python3 generate_agnetta_docx.py

# James Ngovi
python3 generate_research.py

# (Re)build the system diagrams that appear in Mourice's Chapter Six
python3 generate_mourice_diagrams.py
```

## Notes

- The TOC, list of tables, and list of figures in every generated document
  are kept in sync with the actual page numbers in the produced PDFs.

## Author

**Maurice Gift**
Email: <maurice@giftedtech.co.ke>
Web: <https://giftedtech.co.ke>
