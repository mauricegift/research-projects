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
| Faith Awuor Okumu (BBM/1491/23) | `Faith_Okumu_Research_Project.docx` / `.pdf` — Effect of Audit Committee Characteristics on Firm Performance: A Case of Listed Banks in Kenya |

## Repository layout

```
.
├── README.md
├── .gitignore
├── requirements.txt                # Python dependencies
├── app.py                          # master runner — runs every generator
│
├── assets/
│   └── moi_uni_logo.png            # Moi University crest used on every cover page
│
├── mourice_figures/                # PNG diagrams (architecture, ER, use case, deployment, sequence)
│   ├── fig_6_1_architecture.png
│   ├── fig_6_2_er_diagram.png
│   ├── fig_6_3_use_case.png
│   ├── fig_6_4_deployment.png
│   └── fig_6_5_sequence.png
│
├── generators/                     # All document-generator scripts
│   ├── generate_mourice_diagrams.py    # builds the system diagrams used in Mourice's project
│   ├── generate_mourice_docx.py        # Mourice main project — DOCX
│   ├── generate_mourice_pdf.py         # Mourice main project — PDF
│   ├── generate_mourice_cat_docx.py    # Mourice CAT — DOCX
│   ├── generate_mourice_cat_pdf.py     # Mourice CAT — PDF
│   ├── generate_sophie_research.py     # Sophie — DOCX
│   ├── generate_sophie_pdf.py          # Sophie — PDF
│   ├── generate_calvince_docx.py       # Calvince research project — DOCX
│   ├── generate_calvince_pdf.py        # Calvince research project — PDF
│   ├── generate_calvince_cat_docx.py   # Calvince CAT — DOCX
│   ├── generate_calvince_cat_pdf.py    # Calvince CAT — PDF
│   ├── generate_agnetta_docx.py        # Agnetta research project (DOCX + PDF)
│   ├── generate_james_ngovi_docx.py    # James Ngovi research project — DOCX
│   ├── generate_james_ngovi_pdf.py     # James Ngovi research project — PDF
│   ├── generate_faith_docx.py          # Faith Okumu research project — DOCX
│   └── generate_faith_pdf.py           # Faith Okumu research project — PDF
│
└── files/                          # All generated documents land here
    ├── Mourice_BBM_Annex_Project.docx / .pdf
    ├── Mourice_BBM_453_CAT.docx / .pdf
    ├── Sophie_Research_Project.docx / .pdf
    ├── Calvince_Odhiambo_Research_Project.docx / .pdf
    ├── Calvince_BBM_415_CAT.docx / .pdf
    ├── Agnetta_Opisa_Research_Project.docx / .pdf
    ├── James_Ngovi_Research_Project.docx / .pdf
    └── Faith_Okumu_Research_Project.docx / .pdf
```

## Prerequisites

- **Python 3.10+**
- Python packages — install with:
  ```bash
  pip install -r requirements.txt
  ```
- **LibreOffice** — used by some generators to convert the produced
  `.docx` into a polished `.pdf` (`soffice --headless --convert-to pdf`).
  On Debian / Ubuntu:
  ```bash
  sudo apt-get install libreoffice
  ```

## Usage

### Run everything at once

From the repository root, regenerate every DOCX and PDF in `files/`:

```bash
python3 app.py
```

Run only specific generators by passing one or more name fragments
(matched against the script filenames in `generators/`):

```bash
python3 app.py faith               # Faith only
python3 app.py mourice cat         # any script with 'mourice' or 'cat'
python3 app.py sophie calvince     # both Sophie and Calvince scripts
```

### Run a single generator directly

Each script can also be invoked on its own — paths are resolved relative
to the project root automatically:

```bash
python3 generators/generate_faith_docx.py
python3 generators/generate_faith_pdf.py
```

### (Re)build Mourice's system diagrams

```bash
python3 generators/generate_mourice_diagrams.py
```

## Notes

- The TOC, list of tables, and list of figures in every generated document
  are kept in sync with the actual page numbers in the produced PDFs.
- Front-matter pages are numbered with lower-case roman numerals
  (i, ii, iii…) starting from the page after the cover; chapters restart
  at Arabic 1.

## Author

**Maurice Gift**
Email: <maurice@giftedtech.co.ke>
Web: <https://giftedtech.co.ke>
