#!/usr/bin/env python3
"""
Generate PDF version of Calvince Odhiambo's research project using ReportLab
Moi University - Bachelor of Business Management (Accounting Option)
Title: THE IMPACT OF TAX POLICIES ON THE PERFORMANCE OF SMALL AND MEDIUM ENTERPRISES
       IN ELDORET CITY, KENYA
"""
import os

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image, Flowable, CondPageBreak
)
from reportlab.lib import colors
from reportlab.graphics.shapes import Drawing, String, Rect, Line, Polygon
from reportlab.pdfbase.pdfmetrics import stringWidth
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import io
os.makedirs('files', exist_ok=True)

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = inch
TEXT_WIDTH = PAGE_WIDTH - MARGIN * 1.25 - MARGIN


class SectionAnchor(Flowable):
    """Zero-height flowable that records its physical page number when rendered."""
    def __init__(self, key, registry):
        super().__init__()
        self.key = key
        self.registry = registry

    def wrap(self, aW, aH):
        return 0, 0

    def draw(self):
        if self.registry is not None:
            self.registry[self.key] = self.canv.getPageNumber()


def to_roman(n):
    vals = [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),
            (50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]
    r = ''
    for v, s in vals:
        while n >= v:
            r += s; n -= v
    return r


def get_styles():
    styles = getSampleStyleSheet()
    c = {}
    c['title_main'] = ParagraphStyle('title_main', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=14, spaceAfter=8, spaceBefore=8,
        alignment=TA_CENTER, textColor=black, leading=20)
    c['title_sub'] = ParagraphStyle('title_sub', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12, spaceAfter=8, spaceBefore=4,
        alignment=TA_CENTER, textColor=black, leading=18)
    c['title_bold'] = ParagraphStyle('title_bold', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12, spaceAfter=8, spaceBefore=4,
        alignment=TA_CENTER, textColor=black, leading=18)
    c['section_heading'] = ParagraphStyle('section_heading', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=13, spaceAfter=10, spaceBefore=16,
        alignment=TA_CENTER, textColor=black, leading=18)
    c['heading2'] = ParagraphStyle('heading2', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12, spaceAfter=6, spaceBefore=14,
        alignment=TA_LEFT, textColor=black, leading=18)
    c['heading3'] = ParagraphStyle('heading3', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12, spaceAfter=4, spaceBefore=10,
        alignment=TA_LEFT, textColor=black, leading=18)
    c['body'] = ParagraphStyle('body', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12, spaceAfter=8, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black, leading=18)
    c['body_indent'] = ParagraphStyle('body_indent', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12, spaceAfter=6, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black, leading=18, leftIndent=24)
    c['caption'] = ParagraphStyle('caption', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=11, spaceAfter=4, spaceBefore=10,
        alignment=TA_LEFT, textColor=black, leading=14)
    c['source'] = ParagraphStyle('source', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=10, spaceAfter=8, spaceBefore=2,
        alignment=TA_LEFT, textColor=black, leading=12)
    c['toc_main'] = ParagraphStyle('toc_main', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=11, spaceAfter=2, spaceBefore=2,
        alignment=TA_LEFT, textColor=black, leading=14)
    c['toc_1'] = ParagraphStyle('toc_1', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=11, spaceAfter=2, spaceBefore=1,
        alignment=TA_LEFT, textColor=black, leading=14, leftIndent=14)
    c['ref'] = ParagraphStyle('ref', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=11, spaceAfter=6, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black, leading=17,
        leftIndent=24, firstLineIndent=-24)
    c['math'] = ParagraphStyle('math', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12, spaceAfter=6, spaceBefore=8,
        alignment=TA_CENTER, textColor=black, leading=18)
    c['bullet'] = ParagraphStyle('bullet', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12, spaceAfter=4, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black, leading=18, leftIndent=24)
    c['fig_caption'] = ParagraphStyle('fig_caption', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=10, spaceAfter=8, spaceBefore=2,
        alignment=TA_CENTER, textColor=black, leading=12)
    return c


def make_table(headers, rows, col_widths=None, left_col_left=True):
    data = [headers] + rows
    if col_widths:
        page_w = PAGE_WIDTH - (MARGIN * 1.25) - MARGIN
        scale = page_w / sum(col_widths)
        col_widths = [w * scale for w in col_widths]
    t = Table(data, colWidths=col_widths, repeatRows=1)
    style = [
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D3D3D3')),
        ('TEXTCOLOR', (0, 0), (-1, 0), black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Times-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTNAME', (0, 1), (-1, -1), 'Times-Roman'),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F9F9F9')]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]
    if left_col_left:
        style.append(('ALIGN', (0, 0), (0, -1), 'LEFT'))
    t.setStyle(TableStyle(style))
    return t


def bar_chart_image(categories, values, title, xlabel, ylabel, color='steelblue'):
    fig, ax = plt.subplots(figsize=(5.5, 3.2))
    bars = ax.bar(categories, values, color=color, edgecolor='black', linewidth=0.5)
    ax.set_title(title, fontsize=10, fontweight='bold', pad=6)
    ax.set_xlabel(xlabel, fontsize=9)
    ax.set_ylabel(ylabel, fontsize=9)
    ax.set_ylim(0, max(values) * 1.3)
    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + max(values) * 0.02,
                f'{val}%', ha='center', va='bottom', fontsize=8, fontweight='bold')
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    plt.xticks(fontsize=7, rotation=15, ha='right')
    plt.tight_layout()
    buf = io.BytesIO()
    plt.savefig(buf, format='png', dpi=150, bbox_inches='tight')
    plt.close()
    buf.seek(0)
    return buf


def generate_pdf(output_path='files/Calvince_Odhiambo_Research_Project.pdf',
                 _page_data=None, _anchor_reg=None):

    def on_page(canvas, doc):
        canvas.saveState()
        canvas.setFont('Times-Roman', 11)
        phys = canvas.getPageNumber()
        if phys == 1:
            pass  # No number on cover page
        else:
            ch1 = (_page_data or {}).get('ch1_physical')
            if ch1 is not None and phys < ch1:
                canvas.drawCentredString(PAGE_WIDTH / 2.0, 0.5 * inch, to_roman(phys - 1))
            elif ch1 is not None and phys >= ch1:
                canvas.drawCentredString(PAGE_WIDTH / 2.0, 0.5 * inch, str(phys - ch1 + 1))
            else:
                canvas.drawCentredString(PAGE_WIDTH / 2.0, 0.5 * inch, str(phys))
        canvas.restoreState()

    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=inch * 1.25,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        title='The Impact of Tax Policies on the Performance of Small and Medium Enterprises '
              'in Eldoret City, Kenya',
        author='Odhiambo Calvince',
    )

    styles = get_styles()
    story = []

    def P(text, style='body'):
        if isinstance(style, str):
            return Paragraph(text, styles[style])
        return Paragraph(text, style)

    def SP(h=10):
        return Spacer(1, h)

    def HR():
        return HRFlowable(width='100%', thickness=0.5, color=black, spaceAfter=6)

    def pg(key, fallback='?'):
        """Return page label (Roman or Arabic) from _page_data, else fallback."""
        if _page_data:
            v = _page_data.get(key)
            if v is not None:
                ch1 = _page_data.get('ch1_physical')
                if ch1 is not None and v >= ch1:
                    return str(v - ch1 + 1)
                elif v > 1:
                    return to_roman(v - 1)
                else:
                    return '?'
        return fallback

    def A(key):
        return SectionAnchor(key, _anchor_reg)

    # ======================== TITLE PAGE ========================
    story += [SP(12)]
    logo = Image('attached_assets/moi_logo_1773763714167.png', width=1.2 * inch, height=1.2 * inch)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story += [SP(6)]
    story.append(P('MOI UNIVERSITY', 'title_main'))
    story.append(P('SCHOOL OF BUSINESS AND ECONOMICS', 'title_main'))
    story.append(P('DEPARTMENT OF ACCOUNTING AND FINANCE', 'title_bold'))
    story += [SP(18)]
    story.append(HR())
    story.append(P('THE IMPACT OF TAX POLICIES ON THE PERFORMANCE OF SMALL AND MEDIUM'
                   ' ENTERPRISES IN ELDORET CITY, KENYA', 'title_main'))
    story.append(HR())
    story += [SP(14)]
    story.append(P('A RESEARCH PROJECT SUBMITTED IN PARTIAL FULFILMENT FOR THE REQUIREMENTS'
                   ' OF THE AWARD OF BACHELOR OF BUSINESS MANAGEMENT (ACCOUNTING OPTION)'
                   ' OF MOI UNIVERSITY', 'title_sub'))
    story += [SP(14)]
    story.append(P('BY', 'title_bold'))
    story += [SP(4)]
    story.append(P('ODHIAMBO CALVINCE', 'title_main'))
    story.append(P('BBM/1483/23', 'title_sub'))
    story += [SP(14)]
    story.append(P('<b>SUPERVISOR: DR. NICHOLAS SILE</b>', 'title_sub'))
    story.append(P('Department of Accounting and Finance', 'title_sub'))
    story.append(P('Moi University', 'title_sub'))
    story += [SP(14)]
    story.append(P('MARCH 2026', 'title_bold'))
    story.append(PageBreak())

    # ======================== DECLARATION ========================
    story.append(A('DECLARATION'))
    story.append(P('DECLARATION', 'section_heading'))
    story.append(P('This research project is my original work and has not been presented for'
                   ' the award of any degree in any other university.'))
    story += [SP(20)]
    sig_sty = ParagraphStyle('sig', fontName='Times-Roman', fontSize=12, leading=20,
                              alignment=TA_LEFT)
    story.append(P('Signature: .............................................&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                   'Date: .............................', sig_sty))
    story += [SP(6)]
    story.append(P('<b>ODHIAMBO CALVINCE</b>', sig_sty))
    story.append(P('BBM/1483/23', sig_sty))
    story += [SP(20)]
    story.append(P("<b>SUPERVISOR'S APPROVAL</b>",
                   ParagraphStyle('sh', fontName='Times-Bold', fontSize=12, leading=18,
                                  alignment=TA_LEFT)))
    story += [SP(4)]
    story.append(P('This research project has been submitted for examination with my approval'
                   ' as the university supervisor.'))
    story += [SP(16)]
    story.append(P('<b>DR. NICHOLAS SILE</b>',
                   ParagraphStyle('sh2', fontName='Times-Bold', fontSize=12, leading=18,
                                  alignment=TA_LEFT)))
    story.append(P('Department of Accounting and Finance, Moi University'))
    story += [SP(10)]
    story.append(P('Signature: .............................................&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;'
                   'Date: .............................', sig_sty))
    story.append(PageBreak())

    # ======================== DEDICATION ========================
    story.append(A('DEDICATION'))
    story.append(P('DEDICATION', 'section_heading'))
    story += [SP(36)]
    ded_sty = ParagraphStyle('ded', fontName='Times-Italic', fontSize=12, leading=18,
                              alignment=TA_CENTER, spaceAfter=14)
    story.append(P('<i>I dedicate this research project to my beloved mother, Irene Odhiambo,'
                   ' whose unwavering love, sacrifices, prayers, and constant encouragement'
                   ' have been the foundation of my academic journey. Your strength, resilience,'
                   ' and belief in my potential have inspired me to persevere through every'
                   ' challenge. This achievement is a reflection of your support and the values'
                   ' you have instilled in me.</i>', ded_sty))
    story.append(PageBreak())

    # ======================== ACKNOWLEDGEMENT ========================
    story.append(A('ACKNOWLEDGEMENT'))
    story.append(P('ACKNOWLEDGEMENT', 'section_heading'))
    for t in [
        'The completion of this research project would not have been possible were it not'
        ' for the invaluable contribution from several people some of whom I would like to'
        ' acknowledge. I sincerely thank the Almighty God for granting me good health, wisdom,'
        ' strength, and guidance throughout the period of this study. Without His grace, this'
        ' work would not have been possible.',
        'I extend my profound gratitude to my supervisor, <b>Dr. Nicholas Sile</b>, for the'
        ' invaluable guidance, constructive criticism, and continuous support offered during'
        ' the development of this research project. Your insights and academic direction greatly'
        ' contributed to the successful completion of this study.',
        'I also appreciate my lecturers for equipping me with the knowledge and skills necessary'
        ' to undertake this research. My gratitude further goes to my classmates and friends for'
        ' their encouragement, cooperation, and moral support throughout my academic journey.',
        'Special thanks go to the SME owners and managers in Eldoret City who willingly'
        ' participated in this study and provided the necessary information. Your cooperation'
        ' and openness made the data collection process successful.',
        'Finally, I thank my family for their endless support, patience, and understanding'
        ' throughout my academic journey. May God bless you all abundantly.',
    ]:
        story.append(P(t))
        story.append(SP(4))
    story.append(PageBreak())

    # ======================== ABSTRACT ========================
    story.append(A('ABSTRACT'))
    story.append(P('ABSTRACT', 'section_heading'))
    for t in [
        'Small and medium enterprises (SMEs) play a vital role in Kenya\'s economic development'
        ' by contributing significantly to employment creation, income generation, and Gross'
        ' Domestic Product (GDP). Despite their importance, many SMEs face challenges that hinder'
        ' their growth and sustainability, including the burden imposed by tax policies. This study'
        ' examined the impact of tax policies on the performance of small and medium enterprises'
        ' in Eldoret City, Kenya.',
        'The specific objectives of the study were: to evaluate the influence of tax compliance'
        ' procedures on SME operational efficiency; to evaluate the effect of tax rates on'
        ' performance of SMEs in Eldoret City; and to ascertain the effect of tax reforms on'
        ' the performance of SMEs in Eldoret City, Kenya. The study was anchored on the'
        ' Ability-to-Pay Theory, Economic-Based Theories, and Optimal Tax Theory.',
        'The study adopted a cross-sectional survey design. The target population comprised 100'
        ' SMEs registered in Eldoret City. Stratified random sampling was used to select a sample'
        ' of 80 SMEs. A structured questionnaire was used to collect primary data. Data was'
        ' analyzed using both descriptive and inferential statistics with the aid of SPSS'
        ' Version 23.',
        'The findings revealed that tax rates had a significant negative impact on SME'
        ' profitability (M=4.2, SD=0.8). Tax reforms created uncertainty in business planning'
        ' (M=4.12, SD=0.89) and increased compliance costs (M=4.05, SD=0.89). Tax incentives,'
        ' however, positively influenced SME performance by improving profitability (M=4.31,'
        ' SD=0.74) and encouraging business growth (M=4.25, SD=0.78). Regression analysis'
        ' showed that tax policies collectively explained 46.4% of variance in SME performance'
        ' (R&sup2;=0.464). The study concluded that tax policies significantly affect SME'
        ' performance in Eldoret City. The study recommended that the government should reduce'
        ' tax rates for SMEs, simplify tax compliance procedures, and ensure that tax incentives'
        ' are accessible and well-publicized to SME owners.',
        '<b>Keywords:</b> Tax Policies, Tax Rates, Tax Reforms, Tax Incentives, SME Performance,'
        ' Eldoret City',
    ]:
        story.append(P(t))
        story.append(SP(4))
    story.append(PageBreak())

    # ======================== TABLE OF CONTENTS ========================
    story.append(A('TABLE OF CONTENTS'))
    story.append(P('TABLE OF CONTENTS', 'section_heading'))

    TEXTW = 6.25 * inch

    def toc_draw(text, page, level=0, bold=None):
        if bold is None:
            bold = (level == 0)
        font = 'Times-Bold' if bold else 'Times-Roman'
        sz = 11
        row_h = 16
        indent_map = {0: 0, 1: 18, 2: 36}
        indent_w = indent_map.get(level, 0)
        label = text.strip()
        pg_str = str(page)
        label_w = stringWidth(label, font, sz)
        pg_w = stringWidth(pg_str, font, sz)
        dot_w = stringWidth('.', font, sz)
        gap = 4
        available = TEXTW - indent_w - label_w - pg_w - gap * 2
        n_dots = max(3, int(available / dot_w))
        d = Drawing(TEXTW, row_h)
        d.add(String(indent_w, 4, label, fontName=font, fontSize=sz))
        d.add(String(indent_w + label_w + gap, 4, '.' * n_dots, fontName=font, fontSize=sz))
        d.add(String(TEXTW - pg_w, 4, pg_str, fontName=font, fontSize=sz))
        return d

    toc_entries = [
        ('DECLARATION',                                         pg('DECLARATION', 'i'),           0),
        ('DEDICATION',                                          pg('DEDICATION', 'ii'),            0),
        ('ACKNOWLEDGEMENT',                                     pg('ACKNOWLEDGEMENT', 'iii'),      0),
        ('ABSTRACT',                                            pg('ABSTRACT', 'iv'),              0),
        ('TABLE OF CONTENTS',                                   pg('TABLE OF CONTENTS', 'v'),      0),
        ('LIST OF TABLES',                                      pg('LIST OF TABLES', 'vii'),       0),
        ('LIST OF FIGURES',                                     pg('LIST OF FIGURES', 'viii'),     0),
        ('DEFINITION OF TERMS',                                 pg('DEFINITION OF TERMS', 'ix'),   0),
        ('LIST OF ABBREVIATIONS',                               pg('LIST OF ABBREVIATIONS', 'x'),  0),
        ('CHAPTER ONE: INTRODUCTION',                           pg('CHAPTER ONE: INTRODUCTION', '1'),      0),
        ('1.1 Background of the Study',                         pg('1.1 Background of the Study', '1'),    1),
        ('1.2 Statement of the Problem',                        pg('1.2 Statement of the Problem', '5'),   1),
        ('1.3 Objectives of the Study',                         pg('1.3 Objectives of the Study', '7'),    1),
        ('1.3.1 General Objective',                             pg('1.3.1 General Objective', '7'),        2),
        ('1.3.2 Specific Objectives',                           pg('1.3.2 Specific Objectives', '7'),      2),
        ('1.4 Research Hypotheses',                             pg('1.4 Research Hypotheses', '7'),        1),
        ('1.5 Research Questions',                              pg('1.5 Research Questions', '8'),         1),
        ('1.6 Significance of the Study',                       pg('1.6 Significance of the Study', '8'),  1),
        ('1.7 Scope of the Study',                              pg('1.7 Scope of the Study', '9'),         1),
        ('1.8 Justification of the Study',                      pg('1.8 Justification of the Study', '9'), 1),
        ('CHAPTER TWO: LITERATURE REVIEW',                      pg('CHAPTER TWO: LITERATURE REVIEW', '10'),       0),
        ('2.1 Introduction',                                    pg('2.1 Introduction', '10'),               1),
        ('2.2 Theoretical Review',                              pg('2.2 Theoretical Review', '10'),         1),
        ('2.2.1 Ability-to-Pay Theory of Taxation',             pg('2.2.1 Ability-to-Pay Theory of Taxation', '10'), 2),
        ('2.2.2 Economic Based Theories',                       pg('2.2.2 Economic Based Theories', '11'), 2),
        ('2.2.3 Optimal Tax Theory',                            pg('2.2.3 Optimal Tax Theory', '12'),      2),
        ('2.3 Conceptual Framework',                            pg('2.3 Conceptual Framework', '13'),      1),
        ('2.4 Review of Study Variables',                       pg('2.4 Review of Study Variables', '14'), 1),
        ('2.4.1 Tax Rates',                                     pg('2.4.1 Tax Rates', '14'),               2),
        ('2.4.2 Tax Reforms',                                   pg('2.4.2 Tax Reforms', '15'),             2),
        ('2.4.3 Tax Incentives',                                pg('2.4.3 Tax Incentives', '16'),          2),
        ('2.4.4 SMEs Performance',                              pg('2.4.4 SMEs Performance', '17'),        2),
        ('2.5 Empirical Review',                                pg('2.5 Empirical Review', '18'),          1),
        ('CHAPTER THREE: RESEARCH METHODOLOGY',                 pg('CHAPTER THREE: RESEARCH METHODOLOGY', '20'),   0),
        ('3.1 Introduction',                                    pg('3.1 Introduction', '20'),               1),
        ('3.2 Research Design',                                 pg('3.2 Research Design', '20'),            1),
        ('3.3 Population',                                      pg('3.3 Population', '21'),                 1),
        ('3.4 Sampling Frame',                                  pg('3.4 Sampling Frame', '22'),             1),
        ('3.5 Sample Size and Sampling Technique',              pg('3.5 Sample Size and Sampling Technique', '22'), 1),
        ('3.6 Data Collection',                                 pg('3.6 Data Collection', '23'),            1),
        ('3.7 Data Collection Instruments',                     pg('3.7 Data Collection Instruments', '24'),1),
        ('3.8 Piloting Testing',                                pg('3.8 Piloting Testing', '24'),           1),
        ('3.8.1 Validity',                                      pg('3.8.1 Validity', '24'),                 2),
        ('3.8.2 Reliability',                                   pg('3.8.2 Reliability', '25'),              2),
        ('3.9 Data Analysis and Presentation',                  pg('3.9 Data Analysis and Presentation', '25'), 1),
        ('CHAPTER FOUR: DATA ANALYSIS AND DISCUSSIONS',         pg('CHAPTER FOUR: DATA ANALYSIS AND DISCUSSIONS', '27'), 0),
        ('4.1 Introduction',                                    pg('4.1 Introduction', '27'),               1),
        ('4.2 Response Rate',                                   pg('4.2 Response Rate', '27'),              1),
        ('4.3 Demographic Information of Respondents',          pg('4.3 Demographic Information of Respondents', '28'), 1),
        ('4.3.1 Type of Business',                              pg('4.3.1 Type of Business', '28'),         2),
        ('4.3.2 SMEs Years of Operations',                      pg('4.3.2 SMEs Years of Operations', '30'), 2),
        ('4.3.3 Number of Employees in the SME',                pg('4.3.3 Number of Employees in the SME', '31'), 2),
        ('4.3.4 Turnover of SMEs in Eldoret City',              pg('4.3.4 Turnover of SMEs in Eldoret City', '33'), 2),
        ('4.4 Descriptive Analysis',                            pg('4.4 Descriptive Analysis', '35'),      1),
        ('4.4.1 Tax Rates',                                     pg('4.4.1 Tax Rates', '35'),               2),
        ('4.4.2 Tax Reforms',                                   pg('4.4.2 Tax Reforms', '36'),             2),
        ('4.4.3 Tax Incentives',                                pg('4.4.3 Tax Incentives', '37'),          2),
        ('4.4.4 SMEs Performance',                              pg('4.4.4 SMEs Performance', '38'),        2),
        ('4.5 Inferential Statistics',                          pg('4.5 Inferential Statistics', '39'),    1),
        ('4.5.1 Correlation Analysis',                          pg('4.5.1 Correlation Analysis', '39'),    2),
        ('4.5.2 Regression Analysis',                           pg('4.5.2 Regression Analysis', '40'),     2),
        ('CHAPTER FIVE: SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', pg('CHAPTER FIVE: SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', '43'), 0),
        ('5.1 Introduction',                                    pg('5.1 Introduction', '43'),              1),
        ('5.2 Summary of Findings',                             pg('5.2 Summary of Findings', '43'),       1),
        ('5.3 Conclusions',                                     pg('5.3 Conclusions', '46'),               1),
        ('5.4 Recommendations',                                 pg('5.4 Recommendations', '47'),           1),
        ('5.5 Suggestions for Further Research',                pg('5.5 Suggestions for Further Research', '49'), 1),
        ('REFERENCES',                                          pg('REFERENCES', '51'),                    0),
        ('APPENDICES',                                          pg('APPENDICES', '55'),                    0),
    ]

    for text, page, level in toc_entries:
        story.append(toc_draw(text, page, level))

    story.append(PageBreak())

    # ======================== LIST OF TABLES ========================
    story.append(A('LIST OF TABLES'))
    story.append(P('LIST OF TABLES', 'section_heading'))
    tables_list = [
        ('Table 3.1', 'Target Population',                      pg('Table 3.1', '?')),
        ('Table 3.2', 'Sampling Table',                         pg('Table 3.2', '?')),
        ('Table 4.1', 'Response Rate',                          pg('Table 4.1', '?')),
        ('Table 4.2', 'Type of Business',                       pg('Table 4.2', '?')),
        ('Table 4.3', 'SMEs Years of Operations',               pg('Table 4.3', '?')),
        ('Table 4.4', 'Number of Employees in the SME',         pg('Table 4.4', '?')),
        ('Table 4.5', 'Turnover of SMEs in Eldoret City',       pg('Table 4.5', '?')),
        ('Table 4.6', 'Tax Rates',                              pg('Table 4.6', '?')),
        ('Table 4.7', 'Tax Reforms',                            pg('Table 4.7', '?')),
        ('Table 4.8', 'Tax Incentives',                         pg('Table 4.8', '?')),
        ('Table 4.9', 'SMEs Performance',                       pg('Table 4.9', '?')),
        ('Table 4.10', 'Pearson Correlation Analysis',          pg('Table 4.10', '?')),
        ('Table 4.11', 'Model Summary',                         pg('Table 4.11', '?')),
        ('Table 4.12', 'ANOVA',                                 pg('Table 4.12', '?')),
        ('Table 4.13', 'Regression Coefficients',               pg('Table 4.13', '?')),
    ]
    for tnum, tname, tpg in tables_list:
        story.append(toc_draw(f'{tnum}: {tname}', tpg, level=0, bold=False))
    story.append(PageBreak())

    # ======================== LIST OF FIGURES ========================
    story.append(A('LIST OF FIGURES'))
    story.append(P('LIST OF FIGURES', 'section_heading'))
    figures_list = [
        ('Figure 2.1', 'Conceptual Framework',                  pg('Figure 2.1', '?')),
        ('Figure 4.1', 'Type of Business Distribution',         pg('Figure 4.1', '?')),
        ('Figure 4.2', 'SMEs Years of Operations',              pg('Figure 4.2', '?')),
        ('Figure 4.3', 'Number of Employees in SMEs',           pg('Figure 4.3', '?')),
        ('Figure 4.4', 'Turnover of SMEs in Eldoret City',      pg('Figure 4.4', '?')),
    ]
    for fnum, fname, fpg in figures_list:
        story.append(toc_draw(f'{fnum}: {fname}', fpg, level=0, bold=False))
    story.append(PageBreak())

    # ======================== DEFINITION OF TERMS ========================
    story.append(A('DEFINITION OF TERMS'))
    story.append(P('DEFINITION OF TERMS', 'section_heading'))
    def_sty = ParagraphStyle('def_body', fontName='Times-Roman', fontSize=12,
                              leading=18, alignment=TA_JUSTIFY, spaceAfter=6, spaceBefore=2)
    for term, definition in [
        ('Tax Policy',
         'Government laws, regulations, and guidelines governing the imposition, assessment,'
         ' and collection of taxes.'),
        ('Small and Medium Enterprises (SMEs)',
         'Businesses classified based on size, number of employees, or annual turnover as'
         ' defined by Kenya regulatory authorities.'),
        ('Tax Rate',
         'The percentage at which income, sales, or turnover is taxed by the government.'),
        ('Tax Compliance',
         'The act of adhering to tax laws by filing accurate returns and paying taxes within'
         ' the stipulated deadlines.'),
        ('Tax Administration',
         'The processes and systems used by the government to assess, collect, and enforce'
         ' tax laws.'),
        ('Turnover Tax',
         'A simplified tax charged on the gross sales of small businesses below a specified'
         ' turnover threshold.'),
        ('Value Added Tax (VAT)',
         'An indirect tax charged on the value added to goods and services at each stage of'
         ' production or distribution.'),
        ('Corporate Income Tax',
         'A direct tax imposed on the net income or profits of companies.'),
        ('Business Performance',
         'The level of success of an enterprise measured in terms of profitability, growth,'
         ' efficiency and sustainability.'),
        ('Tax Incentive',
         'A government measure that reduces the tax burden on businesses with the aim of'
         ' stimulating economic activity, investment, and business growth.'),
        ('Tax Reforms',
         'Changes made to the tax system by government with the objective of improving'
         ' revenue collection, fairness, and economic efficiency.'),
    ]:
        story.append(P(f'<b>{term}:</b> {definition}', def_sty))
    story.append(PageBreak())

    # ======================== LIST OF ABBREVIATIONS ========================
    story.append(A('LIST OF ABBREVIATIONS'))
    story.append(P('LIST OF ABBREVIATIONS', 'section_heading'))
    abbr_sty = ParagraphStyle('abbr', fontName='Times-Roman', fontSize=12,
                               leading=17, alignment=TA_LEFT, spaceAfter=4)
    for abbr, meaning in [
        ('ANOVA',  'Analysis of Variance'),
        ('BBM',    'Bachelor of Business Management'),
        ('GDP',    'Gross Domestic Product'),
        ('IEA',    'Institute of Economic Affairs'),
        ('KES',    'Kenya Shillings'),
        ('KRA',    'Kenya Revenue Authority'),
        ('MSEA',   'Micro and Small Enterprises Authority'),
        ('SD',     'Standard Deviation'),
        ('SME',    'Small and Medium Enterprise'),
        ('SPSS',   'Statistical Package for Social Sciences'),
        ('VAT',    'Value Added Tax'),
    ]:
        story.append(P(f'<b>{abbr}</b>&nbsp;&nbsp;&nbsp;&nbsp;{meaning}', abbr_sty))
    story.append(PageBreak())

    # ======================== CHAPTER ONE ========================
    story.append(A('CHAPTER ONE: INTRODUCTION'))
    story.append(P('CHAPTER ONE', 'section_heading'))
    story.append(P('INTRODUCTION', 'section_heading'))

    story.append(A('1.1 Background of the Study'))
    story.append(P('1.1 Background of the Study', 'heading2'))
    for t in [
        'Small and Medium Enterprises have always been considered an important force for'
        ' economic development and industrialization in smaller economies. These small'
        ' enterprises have increasingly been recognized as enterprises that contribute'
        ' considerably to the creation of jobs, economic growth and eradication of poverty'
        ' in Africa. World Bank (2015) reported that the creating of "sustainable" jobs and'
        ' opportunities for smaller entrepreneurs are the key strategies to take people out'
        ' of poverty.',
        'Globally, governments rely on taxation as one of the main sources of revenue used'
        ' to finance public services and development programs. Tax policies therefore play an'
        ' essential role in shaping the business environment. Tax policies include tax rates,'
        ' tax compliance requirements, tax incentives, and administrative procedures established'
        ' by governments to regulate taxation. These policies can either encourage or discourage'
        ' business growth depending on their structure and implementation.',
        'In many developing countries, SMEs face numerous challenges including limited access'
        ' to finance, inadequate managerial skills, poor infrastructure, and unfavorable'
        ' regulatory environments. Among these challenges, taxation has been identified as a'
        ' significant factor influencing the growth and sustainability of small businesses.'
        ' High tax rates, complex tax regulations, and costly compliance requirements can'
        ' reduce profitability and discourage business expansion (Atawodi &amp; Ojeka, 2012).',
        'In Kenya, SMEs play a key role in economic development and job creation. In 2014,'
        ' 80 percent of jobs created were dominated by these enterprises. Under the Micro and'
        ' Small Enterprise Act of 2012, micro enterprises have a maximum annual turnover of'
        ' KES 500,000 and employ less than 10 people. Small enterprises have between KES 500,000'
        ' and 5 million annual turnover and employ 10-49 people. However, medium enterprises are'
        ' not covered under the act, but have been reported as comprising between KES 5 million'
        ' and KES 800 million in annual turnover (Mukras, 2003).',
        'Some studies estimate that informal businesses account for 35-50% of GDP in many'
        ' developing countries. Similarly, in Kenya, the informal sector is quite large,'
        ' estimated at 34.3% and accounting for 77% of employment statistics. Over 60% of'
        ' those working in the informal sector are the youth, aged between 18-35 years, 50%'
        ' being women (IEA 2012). The First 1993 Small &amp; Medium Enterprises (SME) baseline'
        ' survey revealed that there were approximately 910,000 SMEs employing up to 2 million'
        ' people.',
        'The Ability-to-Pay Principle proposes that taxes should be levied on the basis of the'
        ' taxable capacity of an individual. This theory states that citizens should not be'
        ' charged taxes that they are not able to pay. The Equal Distribution Principle proposes'
        ' that the incomes, wealth as well as the monetary transactions of individuals should be'
        ' taxed at a fixed percentage, ensuring fairness across all taxpayers.',
        'Eldoret City, located in Uasin Gishu County, is one of the fastest-growing urban centers'
        ' in Kenya and serves as a commercial hub in the North Rift region. The city hosts a large'
        ' number of SMEs operating in sectors such as retail trade, agriculture, manufacturing,'
        ' and services. These businesses contribute significantly to local economic development by'
        ' creating employment opportunities and stimulating regional trade. However, many SMEs in'
        ' Eldoret face challenges related to taxation, particularly in terms of high tax rates,'
        ' complex compliance requirements, and frequent changes in tax policies.',
        'The Kenya Revenue Authority (KRA) has progressively introduced reforms to broaden the tax'
        ' base and streamline tax administration. However, the effectiveness of these reforms in'
        ' improving SME compliance while reducing their tax burden remains a subject of debate.'
        ' Many SME operators in Eldoret City lack sufficient tax knowledge, which makes it'
        ' difficult for them to fully comply with existing tax laws. This creates a tension between'
        ' revenue targets and the operational sustainability of SMEs (Wagacha, 2019).',
        'Prior studies conducted within Kenya and other African economies indicate a complex and'
        ' sometimes contradictory relationship between tax policy and business performance.'
        ' Some findings suggest that moderate and well-designed tax policies can stimulate'
        ' growth through public investments, while others emphasize that excessive taxation'
        ' stifles entrepreneurship and drives businesses into the informal sector (Cobham, 2012).'
        ' It is against this backdrop that this study investigated the impact of tax policies on'
        ' the performance of SMEs in Eldoret City, Kenya.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('1.2 Statement of the Problem'))
    story.append(P('1.2 Statement of the Problem', 'heading2'))
    for t in [
        'Small and Medium Enterprises (SMEs) are widely recognized as key drivers of economic'
        ' growth, employment creation, innovation, and poverty reduction in Kenya. Despite their'
        ' importance, many SMEs continue to struggle with sustainability and profitability. One'
        ' critical challenge frequently cited is the burden posed by tax policies including tax'
        ' rates, compliance requirements, and enforcement mechanisms.',
        'In Kenya, tax policy reforms have been implemented periodically to broaden the tax base,'
        ' increase government revenue, and enhance fairness in the tax system. However, there is'
        ' growing concern that these policies may disproportionately affect SMEs due to their'
        ' limited financial resources, low levels of tax literacy, and high compliance costs.'
        ' Complex tax filing procedures and frequent changes in tax regulations may increase the'
        ' administrative burden on small business owners, potentially stifling growth and'
        ' discouraging formalization.',
        'The Kenya Revenue Authority introduced a Simplified Tax Regime for small businesses in'
        ' the form of a turnover tax. However, many SME owners remain uninformed about its'
        ' provisions, and those who are aware often find the compliance procedures burdensome.'
        ' The introduction of electronic tax systems (iTax) has also posed challenges for SME'
        ' owners, particularly those with limited digital literacy. These structural issues'
        ' suggest that tax policy implementation in Kenya has not fully accounted for the unique'
        ' constraints faced by SMEs (Osambo, 2019).',
        'Despite these concerns, there is limited empirical evidence on the actual impact of tax'
        ' policies on SME performance in Kenya. Existing studies are either outdated, focus mainly'
        ' on large firms, or lack robust analysis of specific tax policy elements. Consequently,'
        ' policymakers, SMEs, and stakeholders lack adequate insight into how tax policies'
        ' influence the growth, competitiveness, and sustainability of SMEs. Therefore, this'
        ' research sought to establish the various tax policies that generally affect the SMEs'
        ' in Eldoret City, Kenya.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('1.3 Objectives of the Study'))
    story.append(P('1.3 Objectives of the Study', 'heading2'))
    story.append(A('1.3.1 General Objective'))
    story.append(P('1.3.1 General Objective', 'heading3'))
    story.append(P('The general objective of this study was to establish the impact of tax'
                   ' policies on the performance of small and medium enterprises in Eldoret'
                   ' City, Kenya.'))
    story.append(A('1.3.2 Specific Objectives'))
    story.append(P('1.3.2 Specific Objectives', 'heading3'))
    for obj in [
        'i) To evaluate the influence of tax compliance procedures on SME operational efficiency.',
        'ii) To evaluate the effect of tax rates on performance of SMEs in Eldoret City, Kenya.',
        'iii) To ascertain the effect of tax reforms on the performance of SMEs in Eldoret City, Kenya.',
    ]:
        story.append(P(obj, 'bullet'))

    story.append(A('1.4 Research Hypotheses'))
    story.append(P('1.4 Research Hypotheses', 'heading2'))
    story.append(P('The study was guided by the following null hypotheses:'))
    for hyp in [
        'H<sub>01</sub>: Tax rates have no significant effect on the performance of SMEs'
        ' in Eldoret City, Kenya.',
        'H<sub>02</sub>: Tax reforms have no significant effect on the performance of SMEs'
        ' in Eldoret City, Kenya.',
        'H<sub>03</sub>: Tax incentives have no significant effect on the performance of SMEs'
        ' in Eldoret City, Kenya.',
    ]:
        story.append(P(hyp, 'bullet'))

    story.append(A('1.5 Research Questions'))
    story.append(P('1.5 Research Questions', 'heading2'))
    story.append(P('The research answered the following questions:'))
    for rq in [
        'i. How do tax policies affect performance of Small and Medium Enterprises in'
        ' Eldoret City, Kenya?',
        'ii. What is the effect of tax rates on performance of Small and Medium Enterprises'
        ' in Eldoret City, Kenya?',
        'iii. How do tax reforms affect the performance of Small and Medium Enterprises in'
        ' Eldoret City, Kenya?',
    ]:
        story.append(P(rq, 'bullet'))

    story.append(A('1.6 Significance of the Study'))
    story.append(P('1.6 Significance of the Study', 'heading2'))
    for t in [
        'The study will help to ascertain how tax as one of the main costs in SMEs affects'
        ' the overall operation of several SMEs within Eldoret City in Uasin Gishu County.'
        ' The research will try to establish whether several taxes imposed to SMEs affect'
        ' their general performance.',
        'Micro, Small and Medium firms (SMEs) constitute 98 percent of businesses in Kenya,'
        ' contribute 30 percent of jobs as well as 3 percent of Kenya\'s Gross Domestic'
        ' Product (GDP). KRA can use this research to assist SMEs by making the working'
        ' environment conducive so that they can generate more income hence paying their'
        ' taxes on time.',
        'The government will benefit from this research since it will know how to help SMEs'
        ' so that they can be more efficient in their operation hence contributing to the'
        ' economy. County government collects fees from all businesses conducted within their'
        ' territory, and this research will enable the county government to project how much'
        ' they can collect from SMEs within Eldoret City.',
        'Future researchers and scholars will benefit from this research since it will add'
        ' to the existing body of knowledge on the subject matter. It will also provide a'
        ' reference point and a basis for further research on tax policies and SME performance'
        ' in Kenya.',
        'Financial institutions and lending agencies will also gain from this study. The'
        ' findings shed light on how tax burdens affect SME creditworthiness and repayment'
        ' capacity. Banks and microfinance institutions can use these insights to better'
        ' tailor their credit products and risk assessment frameworks to the specific financial'
        ' realities faced by SMEs in Eldoret City.',
        'Students of business, economics, and public policy at Moi University and other'
        ' institutions of higher learning in Kenya will find this study a useful reference'
        ' material for understanding the interplay between fiscal policy and private sector'
        ' performance. The empirical data and analytical framework employed herein can guide'
        ' undergraduate and postgraduate research in related disciplines.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('1.7 Scope of the Study'))
    story.append(P('1.7 Scope of the Study', 'heading2'))
    story.append(P('The study was undertaken in Eldoret City, Uasin Gishu County, whereby'
                   ' questionnaires were employed on a target number of respondents. The study'
                   ' considered observation methods which the researcher used to come up with'
                   ' this conclusive evidence. This is because Eldoret formed the centre of most'
                   ' general stores, shops, markets, supermarkets, kiosks and hotels. The study'
                   ' focused on SMEs registered within Eldoret City and was conducted during'
                   ' the period January 2026 to March 2026. The study was confined to the three'
                   ' tax policy variables: tax rates, tax reforms, and tax incentives, and their'
                   ' effect on the operational performance of SMEs.'))
    story.append(P('In terms of subject scope, the study focused exclusively on SMEs with an'
                   ' annual turnover not exceeding KES 50 million, as defined by the Kenya Revenue'
                   ' Authority classification. The dependent variable was SME performance,'
                   ' measured through three indicators: profitability, sales revenue, and'
                   ' business expansion. The study did not extend to large corporations, publicly'
                   ' listed companies, or informal sector enterprises, as these operate under'
                   ' fundamentally different tax regimes and business frameworks.'))
    story.append(P('Geographically, the study was limited to SMEs physically located and'
                   ' operating within Eldoret City\'s central business district and immediate'
                   ' environs. Although Eldoret has grown significantly as an economic hub for'
                   ' the North Rift region, the findings may not be directly extrapolated to'
                   ' rural SMEs or those in other Kenyan urban centres, where tax administration'
                   ' practices, business environments, and access to information may differ'
                   ' considerably.'))

    story.append(A('1.8 Justification of the Study'))
    story.append(P('1.8 Justification of the Study', 'heading2'))
    for t in [
        'This study is justified on three grounds. Theoretically, the study contributes to'
        ' the body of knowledge by applying the Ability-to-Pay Theory, Economic Based Theories,'
        ' and Optimal Tax Theory to explain the relationship between tax policies and SME'
        ' performance in an African developing economy context.',
        'Practically, the findings of this study will provide actionable insights to the Kenya'
        ' Revenue Authority (KRA), policy makers, and county government of Uasin Gishu on how'
        ' to design tax policies that are sensitive to the operational realities of SMEs.'
        ' This may contribute to a more conducive business environment and improved tax'
        ' compliance among SMEs.',
        'Methodologically, the study employs a rigorous cross-sectional survey design with both'
        ' descriptive and inferential statistics, thereby providing a reliable empirical framework'
        ' that future researchers can replicate or build upon in related studies.',
    ]:
        story.append(P(t))
        story.append(SP(4))
    story.append(PageBreak())

    # ======================== CHAPTER TWO ========================
    story.append(A('CHAPTER TWO: LITERATURE REVIEW'))
    story.append(P('CHAPTER TWO', 'section_heading'))
    story.append(P('LITERATURE REVIEW', 'section_heading'))

    story.append(A('2.1 Introduction'))
    story.append(P('2.1 Introduction', 'heading2'))
    story.append(P('This chapter reviews literature related to the impact of tax policies on'
                   ' the performance of Small and Medium Enterprises (SMEs). It examines'
                   ' theoretical literature, empirical studies, and the conceptual framework'
                   ' that explains the relationship between tax policies and SME performance.'
                   ' The chapter is organized into five sections: theoretical review,'
                   ' conceptual framework, review of study variables, and empirical review.'))

    story.append(A('2.2 Theoretical Review'))
    story.append(P('2.2 Theoretical Review', 'heading2'))
    story.append(P('The Impact of tax policies on Small and Medium Enterprises can be explained'
                   ' by three main theories. These theories provide the conceptual foundation'
                   ' upon which the study is anchored.'))

    story.append(A('2.2.1 Ability-to-Pay Theory of Taxation'))
    story.append(P('2.2.1 Ability-to-Pay Theory of Taxation', 'heading3'))
    for t in [
        'The most popular and commonly accepted principle of equity or justice in taxation is'
        ' that citizens of a country should pay taxes to the government in accordance with their'
        ' ability to pay. It appears very reasonable and just that taxes should be levied on the'
        ' basis of the taxable capacity of an individual. This theory states that citizens should'
        ' not be charged taxes that they are not able to pay.',
        'The principle is grounded in horizontal equity — the idea that taxpayers with the same'
        ' income should pay the same amount of tax — and vertical equity, which requires that'
        ' those with higher incomes should pay proportionately more. In the context of SMEs,'
        ' horizontal equity implies that businesses generating similar revenues should face'
        ' similar tax obligations, regardless of their sector or location.',
        'The theory will be relevant to the study because it justifies equity as a principle'
        ' of taxation and can also be applicable to SMEs to improve performance. The SMEs'
        ' sacrifice part of their income and it is turned over to the government to be spent'
        ' on public services. This theory helps to evaluate whether the tax burden imposed on'
        ' SMEs in Eldoret City is proportional to their ability to pay, or whether it exceeds'
        ' their financial capacity.',
        'According to Muriithi and Moyi (2003), tax structures that respect the ability-to-pay'
        ' principle tend to generate greater voluntary compliance from small business owners,'
        ' as they perceive the system to be fair. Conversely, when SMEs feel overtaxed relative'
        ' to their income, they are more likely to underreport sales or shift activities to the'
        ' informal sector.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.2.2 Economic Based Theories'))
    story.append(P('2.2.2 Economic Based Theories', 'heading3'))
    for t in [
        'These are also known as deterrence theories and they place emphasis on incentives.'
        ' The theory suggests that taxpayers are amoral utility maximizers — they are influenced'
        ' by economic motives such as profit maximization and probability of detection. As such'
        ' they analyze alternative compliance paths and then select the alternative that maximizes'
        ' their expected tax returns after adjusting for the costs of non-compliance.',
        "Ibn Khaldun's economic theory of taxation has been considered as one of the most"
        ' important contributions to economic thought. Khaldun related the theory of taxation'
        ' with the government expenditure and argued for low tax rates so that incentive to work'
        ' is not killed and taxes are paid happily. This argument resonates with modern-day'
        ' discussions about the relationship between tax rates and business activity.',
        'The economic-based approach is also linked to the concept of tax elasticity, which'
        ' measures how sensitive tax revenues are to changes in economic activity. When tax'
        ' rates are set too high, the resulting disincentive effects may reduce taxable activity'
        ' and ultimately decrease government revenues — a phenomenon captured by the Laffer'
        ' Curve. For SMEs in Eldoret City, this theory suggests that excessively high tax rates'
        ' may discourage business formalization and investment.',
        'Allingham and Sandmo (1972) built on deterrence theory by modeling tax compliance as'
        ' a function of the probability of detection and the penalty imposed. Their model implies'
        ' that SMEs will comply with tax obligations only if the expected benefits of compliance'
        ' outweigh the costs, including the opportunity cost of the time spent on compliance'
        ' activities. This theory is directly applicable to this study as it provides a framework'
        ' for understanding the non-compliance behavior observed among some SMEs in Kenya.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.2.3 Optimal Tax Theory'))
    story.append(P('2.2.3 Optimal Tax Theory', 'heading3'))
    for t in [
        'Optimal Tax Theory suggests that governments should design tax systems that maximize'
        ' revenue collection while minimizing negative effects on economic activities. The theory'
        ' emphasizes efficiency in taxation by balancing revenue generation with economic growth.'
        ' This theory is relevant to the study as it provides a framework for evaluating whether'
        ' the current tax policies in Kenya are optimal for SME performance.',
        'According to Mirrlees (1971), the optimal tax structure should balance equity and'
        ' efficiency concerns. From an equity standpoint, the tax system should distribute the'
        ' tax burden fairly across different income groups. From an efficiency standpoint, taxes'
        ' should be designed to minimize distortions in economic decision-making. This dual'
        ' objective is particularly important for SMEs, which are sensitive to changes in tax'
        ' rates and compliance costs.',
        'The theory implies that the government should evaluate the trade-off between the revenue'
        ' generated from SME taxation and the potential loss in business activity caused by the'
        ' tax burden. If the current tax regime in Kenya is not optimal, it may be contributing'
        ' to reduced SME performance, informal sector expansion, and lower overall tax revenues.'
        ' This study uses the optimal tax framework to assess whether current tax policies'
        ' in Eldoret City are designed in a way that supports SME growth while meeting'
        ' revenue objectives.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.3 Conceptual Framework'))
    story.append(P('2.3 Conceptual Framework', 'heading2'))
    story.append(P('According to Hong and Pluye (2018), a conceptual framework is a network, or'
                   ' \u201ca plane\u201d of interconnected concepts that together provide a'
                   ' comprehensive understanding of a phenomenon or phenomena. The researcher'
                   ' adopted the following framework, where independent variables (tax rates,'
                   ' tax reforms and tax incentives) are interlinked with the dependent variable'
                   ' (SMEs performance).'))

    # Conceptual Framework Diagram
    _cf_W = 5.4 * inch
    _cf_H = 3.5 * inch
    _iv_box_w = 1.85 * inch
    _iv_box_h = 0.85 * inch
    _iv_gap   = 0.15 * inch
    _label_h  = 0.40 * inch
    _b3_y = _label_h
    _b2_y = _b3_y + _iv_box_h + _iv_gap
    _b1_y = _b2_y + _iv_box_h + _iv_gap
    _dv_y = _b3_y
    _dv_h = _b1_y + _iv_box_h - _b3_y
    _junction_x = _iv_box_w + 0.50 * inch
    _dv_x = _junction_x + 0.25 * inch
    _dv_w = _cf_W - _dv_x
    _cf_d = Drawing(_cf_W, _cf_H)

    def _box(x, y, w, h):
        _cf_d.add(Rect(x, y, w, h, strokeColor=black, strokeWidth=0.8, fillColor=white))

    def _s(x, y, txt, bold=False, sz=9):
        fn = 'Times-Bold' if bold else 'Times-Roman'
        _cf_d.add(String(x, y, txt, fontName=fn, fontSize=sz, fillColor=black))

    def _ul(x, y, txt, bold=False, sz=9):
        fn = 'Times-Bold' if bold else 'Times-Roman'
        tw = stringWidth(txt, fn, sz)
        _cf_d.add(Line(x, y - 1, x + tw, y - 1, strokeColor=black, strokeWidth=0.7))

    _box(0, _b1_y, _iv_box_w, _iv_box_h)
    _t1 = 'Tax Rates'; _t1x = (_iv_box_w - stringWidth(_t1, 'Times-Bold', 9)) / 2
    _t1y = _b1_y + _iv_box_h - 14
    _s(_t1x, _t1y, _t1, bold=True); _ul(_t1x, _t1y, _t1, bold=True)
    for _i, _item in enumerate(['Marginal Tax Rates', 'Specific Tax Rates', 'Tax Rate Calculations']):
        _s(6, _t1y - 11 - _i * 11, _item)

    _box(0, _b2_y, _iv_box_w, _iv_box_h)
    _t2 = 'Tax Reforms'; _t2x = (_iv_box_w - stringWidth(_t2, 'Times-Bold', 9)) / 2
    _t2y = _b2_y + _iv_box_h - 14
    _s(_t2x, _t2y, _t2, bold=True); _ul(_t2x, _t2y, _t2, bold=True)
    for _i, _item in enumerate(['Tax Remittance', 'Tax Education', 'Tax Enforcement']):
        _s(6, _t2y - 11 - _i * 11, _item)

    _box(0, _b3_y, _iv_box_w, _iv_box_h)
    _t3 = 'Tax Incentives'; _t3x = (_iv_box_w - stringWidth(_t3, 'Times-Bold', 9)) / 2
    _t3y = _b3_y + _iv_box_h - 14
    _s(_t3x, _t3y, _t3, bold=True); _ul(_t3x, _t3y, _t3, bold=True)
    for _i, _item in enumerate(['Tax Holidays', 'VAT Exemptions', 'Turnover Tax']):
        _s(6, _t3y - 11 - _i * 11, _item)

    _box(_dv_x, _dv_y, _dv_w, _dv_h)
    _dv_title = "SME's Performance"
    _dtx = _dv_x + (_dv_w - stringWidth(_dv_title, 'Times-BoldItalic', 9)) / 2
    _dty = _dv_y + _dv_h / 2 + 22
    _cf_d.add(String(_dtx, _dty, _dv_title, fontName='Times-BoldItalic', fontSize=9, fillColor=black))
    _cf_d.add(Line(_dtx, _dty - 1, _dtx + stringWidth(_dv_title, 'Times-BoldItalic', 9), _dty - 1,
                   strokeColor=black, strokeWidth=0.7))
    for _i, _item in enumerate(['Profitability', 'Sales Revenue', 'Expansion']):
        _dix = _dv_x + (_dv_w - stringWidth(_item, 'Times-Roman', 9)) / 2
        _s(_dix, _dty - 12 - _i * 11, _item)

    for _by in [_b1_y, _b2_y, _b3_y]:
        _ay = _by + _iv_box_h / 2
        _cf_d.add(Line(_iv_box_w, _ay, _junction_x, _ay, strokeColor=black, strokeWidth=0.8))
    _cf_d.add(Line(_junction_x, _b1_y + _iv_box_h / 2, _junction_x, _b3_y + _iv_box_h / 2,
                   strokeColor=black, strokeWidth=0.8))
    _junc_y_mid = _dv_y + _dv_h / 2
    _cf_d.add(Line(_junction_x, _junc_y_mid, _dv_x, _junc_y_mid, strokeColor=black, strokeWidth=0.8))
    _ah = 5; _aw = 4
    _cf_d.add(Polygon([_dv_x, _junc_y_mid, _dv_x - _ah, _junc_y_mid + _aw,
                       _dv_x - _ah, _junc_y_mid - _aw],
                      strokeColor=black, fillColor=black))

    _iv_lbl = 'Independent variables'
    _cf_d.add(String((_iv_box_w - stringWidth(_iv_lbl, 'Times-Bold', 9)) / 2, 4, _iv_lbl,
                     fontName='Times-Bold', fontSize=9, fillColor=black))
    _dv_lbl = 'Dependent Variable'
    _cf_d.add(String(_dv_x + (_dv_w - stringWidth(_dv_lbl, 'Times-Bold', 9)) / 2, 4, _dv_lbl,
                     fontName='Times-Bold', fontSize=9, fillColor=black))

    story.append(SP(8))
    story.append(A('Figure 2.1'))
    story.append(_cf_d)
    story.append(P('Figure 2.1: Conceptual Framework', 'fig_caption'))
    story.append(P('<b>Source:</b> Researcher (2026)', 'source'))

    story.append(A('2.4 Review of Study Variables'))
    story.append(P('2.4 Review of Study Variables', 'heading2'))

    story.append(A('2.4.1 Tax Rates'))
    story.append(P('2.4.1 Tax Rates', 'heading3'))
    for t in [
        'The tax rate is the percentage of an income or an amount of money that has to be paid'
        ' as tax. A proportional tax applies the same tax rate across low, middle, and high-income'
        ' earners regardless of how much they earn (Bolboros, 2016). A progressive tax system,'
        ' on the other hand, imposes higher rates on higher income brackets, which can be more'
        ' equitable but also more burdensome for growing SMEs.',
        'In Kenya, different rates are applied to different tax heads as directed by Kenya Revenue'
        ' Authority. Bolboros (2016) studied the impact of tax rate and financial performance in'
        ' Vintila. The study found that a lower tax rate was associated with higher profitability'
        ' and business growth, particularly for small enterprises.',
        'Ali, Sjursen and Michelsen (2015) studied factors affecting tax compliance attitude in'
        ' Africa. Findings indicated that the impact of corporate income tax rates is borne by'
        ' business owners through decreased profits, either by employees through decreased wages,'
        ' or by customers through higher prices. These findings illustrate the cascading effect'
        ' that tax rate increases can have across the entire business ecosystem.',
        'In the Kenyan context, the introduction of a Turnover Tax (TOT) at a rate of 1% on'
        ' gross sales for businesses with an annual turnover of KES 1 million to KES 50 million'
        ' was intended to simplify taxation for SMEs. However, research by Noor-Halp (2011)'
        ' suggests that even seemingly low turnover tax rates can adversely affect SME cash'
        ' flows when businesses operate on narrow profit margins, as is common in Eldoret\'s'
        ' retail and services sectors.',
        'Ocheni (2015) studied the effect of multiple taxation on the performance of small and'
        ' medium scale business enterprises and found that the multiplicity of taxes — levied'
        ' by both national and county governments — erodes SME profitability disproportionately'
        ' compared with larger firms. The study concluded that rationalizing the number of tax'
        ' heads applicable to SMEs would have a measurable positive effect on their growth and'
        ' survival rates. This finding is particularly relevant to Eldoret City, where county'
        ' levies on market stalls, business permits, and waste management are applied alongside'
        ' national tax obligations, compounding the overall tax burden.',
        'The World Bank (2015) report on SME finance and development observed that high'
        ' effective tax rates are among the top three constraints cited by SME owners in'
        ' Sub-Saharan Africa. The report recommended that governments implement differential'
        ' tax rate schedules for SMEs, recognizing their limited capacity relative to large'
        ' corporations. This recommendation aligns with the findings of this study and'
        ' underscores the need for a deliberate SME-focused tax policy framework in Kenya.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.4.2 Tax Reforms'))
    story.append(P('2.4.2 Tax Reforms', 'heading3'))
    for t in [
        'Tax reform is a main component of macroeconomic policy. Tax reforms are considered as'
        ' the most important part of fiscal policy. The aim of tax reform is to raise revenue'
        ' effectively in consistence with each country\'s uniqueness and administrative capacity.',
        'Regulatory and tax burdens mostly fall disproportionately on SMEs due to the limited'
        ' size and structure (Pope &amp; Abdul-Jabbar, 2018). This makes tax compliance an'
        ' important issue for SMEs as they are constrained in resources and relevant skills to'
        ' comply with tax codes. The proliferation of multiple taxes — including income tax,'
        ' VAT, excise duties, and county levies — further increases the compliance burden on'
        ' small business operators.',
        'Osambo (2019) found that the nature of business is the main obstacle which hinders'
        ' government from ensuring that the SMEs are brought into the tax net. Atawodi and'
        ' Ojeka (2012) in their study on factors that affect tax compliance among SMEs in Nigeria'
        ' found that tax rate is the main challenge facing SMEs. Similarly, a report by the Kenya'
        ' Private Sector Alliance (2017) noted that frequent amendments to the Value Added Tax'
        ' Act and income tax provisions created operational uncertainty for SME owners who lacked'
        ' legal expertise.',
        'Bjork (2013) emphasized that the legitimacy of the tax system in the eyes of taxpayers'
        ' is critical for voluntary compliance. When SME owners perceive tax reforms as arbitrary'
        ' or unfair, they are less likely to comply. This perception issue is particularly'
        ' relevant in Eldoret City, where many SME operators report feeling marginalized from'
        ' policy discussions despite being the most directly affected stakeholders.',
        'Wagacha (2019) in his analysis of tax reform and economic development in Kenya argued'
        ' that although tax reforms have been generally aimed at broadening the tax base and'
        ' improving efficiency, their implementation has often been disruptive for SMEs that'
        ' lack the administrative capacity to adapt quickly. He recommended a phased approach'
        ' to tax reform implementation, with dedicated support mechanisms for small businesses'
        ' during transition periods.',
        'Muriithi and Moyi (2003) studied tax reforms and revenue mobilization in Kenya and'
        ' concluded that the success of tax reform efforts depends not only on the design of the'
        ' new tax system but also on the quality of tax administration and the level of taxpayer'
        ' education. Their findings underscore the importance of complementing legislative reforms'
        ' with investments in taxpayer education, particularly for SME operators who may lack'
        ' formal accounting training.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.4.3 Tax Incentives'))
    story.append(P('2.4.3 Tax Incentives', 'heading3'))
    for t in [
        'Tax incentives are fiscal policy tools used by governments to encourage investment,'
        ' entrepreneurship, and business growth through reductions in tax liability. These'
        ' incentives may take different forms such as tax holidays, reduced tax rates, VAT'
        ' exemptions, and Turnover Tax.',
        'According to Bird and Zolt (2008), tax incentives can improve business performance by'
        ' reducing the effective tax rate faced by firms and increasing the resources available'
        ' for productive investment. This can lead to increased profitability, business expansion,'
        ' and job creation. The effectiveness of tax incentives, however, depends on their design,'
        ' accessibility, and awareness among the target beneficiaries.',
        'In Kenya, the government has implemented various tax incentive programs targeting SMEs,'
        ' including investment deductions, capital allowances, and sector-specific exemptions.'
        ' However, many SME operators in Eldoret City remain unaware of these incentives or find'
        ' the application processes too cumbersome to navigate. This accessibility challenge'
        ' undermines the intended impact of tax incentive policies on SME performance.',
        'Holban (2017) argued that the mere existence of tax incentives is insufficient to'
        ' stimulate SME growth; effective communication, simplified procedures, and targeted'
        ' outreach are necessary to ensure that small businesses actually benefit from these'
        ' provisions. The findings from this study will shed light on the extent to which'
        ' SMEs in Eldoret City are benefiting from available tax incentives.',
        'Cobham (2012) observed that in many developing economies, tax incentives are often'
        ' poorly designed, leading to foregone government revenue without commensurate gains'
        ' in investment or business performance. He recommended evidence-based design of tax'
        ' incentive programs, with regular evaluation of their impact on targeted beneficiary'
        ' groups. For Kenya, this implies that incentive programs targeting SMEs should be'
        ' systematically evaluated against measurable performance indicators.',
        'The Kenya Revenue Authority (KRA) launched the Turnover Tax (TOT) regime to simplify'
        ' tax obligations for SMEs earning between KES 1 million and KES 50 million annually.'
        ' While this represents a positive reform, its uptake has been limited by inadequate'
        ' awareness, complex registration requirements, and mistrust of the tax authority among'
        ' SME operators. These barriers highlight the need for targeted policy interventions to'
        ' improve the reach and effectiveness of SME-oriented tax incentive programs.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.4.4 SMEs Performance'))
    story.append(P('2.4.4 SMEs Performance', 'heading3'))
    for t in [
        'The performance of Small and Medium Enterprises (SMEs) refers to the ability of these'
        ' businesses to achieve their operational and financial objectives over a given period'
        ' of time. Business performance is commonly measured using indicators such as'
        ' profitability, growth in sales, and business expansion.',
        'Several indicators are commonly used to measure SME performance. One of the most widely'
        ' used indicators is profitability, which refers to the ability of a business to generate'
        ' income after deducting operational expenses. Another important indicator is business'
        ' growth, which can be measured through increases in sales revenue, number of employees,'
        ' and market share.',
        'Ocheni (2015) found that multiple taxation adversely affected SME performance in Lokoja,'
        ' Nigeria, leading to reduced profitability and stunted growth. The findings indicated'
        ' that SMEs subjected to high and multiple taxes were more likely to reduce their'
        ' workforce, cut back on investment in equipment, and lower the quality of goods and'
        ' services offered to customers.',
        'In Kenya, studies by Osambo (2019) and Wagacha (2019) suggest that SME performance is'
        ' significantly correlated with the tax environment. Businesses operating in a stable,'
        ' transparent, and predictable tax regime tend to show better performance metrics than'
        ' those in highly volatile or complex tax environments. This study evaluates these'
        ' dynamics specifically in the context of Eldoret City SMEs.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('2.5 Empirical Review'))
    story.append(P('2.5 Empirical Review', 'heading2'))
    for t in [
        'On the global perspective, Awirothanon (2019) studied the relationship between tax'
        ' planning and financial performance in Thailand Stock Exchange. The study concluded that'
        ' tax planning significantly and positively affects financial performance while high tax'
        ' planning burdens have a negative effect on financial planning. The study recommended'
        ' that firms adopt proactive tax management strategies as part of their overall financial'
        ' planning to optimize their performance.',
        'Tee, Boadi and Opoku (2016), examined the effect of tax payment on the performance of'
        ' SMEs in West Municipal Assembly in Ghana. The study found out that taxes imposed on'
        ' small and medium enterprises impact their growth in terms of profits. It was further'
        ' established that changes in tax rates lead to the changes in prices of various goods'
        ' and services, with implications for consumer spending and demand within SME markets.',
        'Cobham (2012) examined the issue of tax havens and illicit financial flows, noting that'
        ' the prevalence of large-scale corporate tax avoidance shifts a disproportionate burden'
        ' onto smaller enterprises that lack the resources or structures to benefit from offshore'
        ' tax arrangements. This systemic imbalance underscores the importance of designing tax'
        ' policies that protect the competitiveness of SMEs.',
        'Locally, Osambo (2019) found that the nature of business is the main obstacle which'
        ' hinders government from ensuring that SMEs are brought into the tax net. Atawodi and'
        ' Ojeka (2012) in their study on factors that affect tax compliance among SMEs in Nigeria'
        ' found that tax rate is the main challenge facing SMEs, where high tax rates mostly aid'
        ' non-compliance. Their findings highlight the need for tax authorities to consider the'
        ' revenue-generating capacity of SMEs before setting compliance thresholds.',
        'Cooper and Schindler (2013) noted that research methodology choices significantly'
        ' affect the reliability and validity of findings in social science studies. This insight'
        ' informed the methodological choices made in this study, particularly the adoption of a'
        ' cross-sectional survey design with structured questionnaires, which allows for both'
        ' breadth and depth of data collection from SME operators in Eldoret City.',
    ]:
        story.append(P(t))
        story.append(SP(4))
    story.append(PageBreak())

    # ======================== CHAPTER THREE ========================
    story.append(A('CHAPTER THREE: RESEARCH METHODOLOGY'))
    story.append(P('CHAPTER THREE', 'section_heading'))
    story.append(P('RESEARCH METHODOLOGY', 'section_heading'))

    story.append(A('3.1 Introduction'))
    story.append(P('3.1 Introduction', 'heading2'))
    story.append(P('This chapter presents the methodology that was used to collect data for the'
                   ' study. It covers the research design, the target population, sampling frame,'
                   ' sample size and sampling technique, data collection instruments, piloting,'
                   ' validity, reliability, and data analysis and presentation procedures.'))

    story.append(A('3.2 Research Design'))
    story.append(P('3.2 Research Design', 'heading2'))
    for t in [
        'This research adopted a cross-sectional survey design where the population of interest'
        ' in the Eldoret City SME environment were visited and data collected through'
        ' questionnaire administration. A cross-sectional survey is defined as an observational'
        ' research type that analyzes data from a population or a representative subset at a'
        ' specific point in time (Borg &amp; Gall, 2013).',
        'A cross-sectional design was considered appropriate for this study because it allowed'
        ' the researcher to collect data from multiple respondents simultaneously, thereby'
        ' providing a snapshot of the current state of tax policy impacts on SMEs. The design is'
        ' cost-effective and allows for large-scale data collection within a relatively short'
        ' period. Moreover, since the study sought to describe the relationship between tax'
        ' policies and SME performance at a specific point in time, a cross-sectional approach'
        ' was deemed most suitable (Creswell, 2010).',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('3.3 Population'))
    story.append(P('3.3 Population', 'heading2'))
    for t in [
        'The target population for this study was 100 SMEs from all the SMEs registered in'
        ' Eldoret City database of 2026. The table below presents the target population'
        ' distribution across different business categories in Eldoret City.',
        'The choice of this population was informed by the fact that Eldoret City is the'
        ' commercial hub of the North Rift region of Kenya. The city\'s diverse SME landscape'
        ' — spanning retail, services, manufacturing, transport, and financial services — made'
        ' it an ideal study environment for examining the differential impacts of tax policies'
        ' across various business sectors.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story += [SP(6)]
    story.append(A('Table 3.1'))
    story.append(P('Table 3.1: Target Population', 'caption'))
    story.append(make_table(
        ['Categories', 'SMEs', 'Percentage'],
        [['Financial Services', '10', '10%'],
         ['Transport Services', '15', '15%'],
         ['Supermarkets & Shops', '20', '20%'],
         ['Hoteliers', '15', '15%'],
         ['Information & Technology Services', '17', '17%'],
         ['General Hardwares', '13', '13%'],
         ['Production', '10', '10%'],
         ['Total', '100', '100%']],
        col_widths=[3.0, 1.0, 1.0]))
    story.append(P('Source: Field Survey (2026)', 'source'))

    story.append(A('3.4 Sampling Frame'))
    story.append(P('3.4 Sampling Frame', 'heading2'))
    story.append(P('The sampling frame for this study consisted of all 100 SMEs registered in'
                   ' the Eldoret City business registry as of 2026. A sampling frame is a list'
                   ' of all individuals of the population a researcher intends to study'
                   ' (Borg &amp; Gall, 2013). The Eldoret City business registry was used as the'
                   ' sampling frame because it provided a comprehensive and up-to-date listing'
                   ' of all formally registered SMEs operating within the study area. This'
                   ' ensured that only active, registered businesses were included in the sample,'
                   ' thereby enhancing the reliability of the data collected.'))

    story.append(A('3.5 Sample Size and Sampling Technique'))
    story.append(P('3.5 Sample Size and Sampling Technique', 'heading2'))
    for t in [
        'The study adopted a stratified random sampling procedure. The sample size was determined'
        " using Yamane's formula as follows:",
    ]:
        story.append(P(t))
        story.append(SP(4))
    story.append(P('n = N / (1 + N(e)<sup>2</sup>)', 'math'))
    story.append(P('Where: n = sample size, N = population size (100), e = margin of error (0.05)'))
    story += [SP(4)]
    story.append(P('n = 100 / (1 + 100(0.05)<sup>2</sup>) = 100 / (1 + 0.25) = 100 / 1.25'
                   ' = <b>80</b>', 'math'))
    story += [SP(6)]
    story.append(P('Therefore, the sample size for this study was 80 SMEs. The sample was'
                   ' distributed proportionately across the different business categories as'
                   ' shown in Table 3.2 below:'))
    story += [SP(6)]
    story.append(A('Table 3.2'))
    story.append(P('Table 3.2: Sampling Table', 'caption'))
    story.append(make_table(
        ['Categories', 'SMEs', 'Sample Proportion', 'Sample Size'],
        [['Financial Services', '10', '80%', '8'],
         ['Transport Services', '15', '80%', '12'],
         ['Supermarkets & Shops', '20', '80%', '16'],
         ['Hoteliers', '15', '80%', '12'],
         ['Information & Technology Services', '17', '80%', '14'],
         ['General Hardwares', '13', '80%', '10'],
         ['Production', '10', '80%', '8'],
         ['Total', '100', '80%', '80']],
        col_widths=[2.5, 0.9, 1.2, 0.9]))
    story.append(P('Source: Field Survey (2026)', 'source'))
    story.append(P('Stratified random sampling was used to ensure that all business categories'
                   ' were adequately represented in the sample. Within each stratum, simple'
                   ' random sampling was applied using a random number table to select individual'
                   ' SMEs. This approach enhanced the representativeness of the sample and allowed'
                   ' for inferences to be drawn about each business category.'))

    story.append(A('3.6 Data Collection'))
    story.append(P('3.6 Data Collection', 'heading2'))
    story.append(P('The researcher used a structured questionnaire as the primary data collection'
                   ' instrument. The questionnaire was designed to elicit background information'
                   ' about the SMEs and was divided into sections representing the various'
                   ' variables adopted for the study. Questionnaires were administered through'
                   ' the drop-and-pick method or face-to-face interviews with the selected SME'
                   ' owners or managers. The researcher also employed research assistants who'
                   ' were trained on the objectives of the study and the questionnaire content'
                   ' prior to data collection. A period of two weeks was allocated for data'
                   ' collection.'))
    story.append(P('Secondary data was also collected from published reports by the Kenya Revenue'
                   ' Authority (KRA), the Kenya National Bureau of Statistics (KNBS), and the'
                   ' Uasin Gishu County Government to supplement the primary data. These sources'
                   ' provided contextual information on the tax policy environment, the number of'
                   ' registered SMEs in Eldoret City, and broader economic indicators relevant'
                   ' to the study.'))
    story.append(P('To ensure data quality, completed questionnaires were checked for completeness'
                   ' and consistency upon collection. Questionnaires with more than 20% of items'
                   ' unanswered were excluded from the final analysis. This screening process'
                   ' resulted in 70 usable questionnaires out of 78 returned, representing a'
                   ' final response rate of 89.7%.'))

    story.append(A('3.7 Data Collection Instruments'))
    story.append(P('3.7 Data Collection Instruments', 'heading2'))
    story.append(P('The study adopted a structured questionnaire with a Likert scale of 1-5'
                   ' indicating the extent to which one agrees or disagrees. The questionnaire'
                   ' comprised two sections: Section A captured the demographic information of'
                   ' the respondents, while Section B captured information on the study variables'
                   ' (tax rates, tax reforms, tax incentives and SMEs performance). The Likert'
                   ' scale used was: 1 = Strongly Disagree, 2 = Disagree, 3 = Neutral, 4 = Agree,'
                   ' and 5 = Strongly Agree. The use of a Likert scale enabled the quantification'
                   ' of respondents\' perceptions and attitudes, which is appropriate for'
                   ' measuring constructs that are not directly observable (Neuman, 2014).'))

    story.append(A('3.8 Piloting Testing'))
    story.append(P('3.8 Piloting Testing', 'heading2'))
    story.append(P('Piloting refers to the conduct of preliminary research, prior to the main'
                   ' study. It provides a structured opportunity for informed reflection on, and'
                   ' modification of, the research design, the research instruments, costing,'
                   ' timing, and a whole gamut of issues concerning the everyday conduct of the'
                   ' research (Kothari, 2013). The pilot study was conducted on 10 SMEs selected'
                   ' from Eldoret City but not included in the main study sample. Feedback from'
                   ' the pilot study was used to refine the questionnaire for clarity,'
                   ' comprehensiveness, and ease of completion.'))

    story.append(A('3.8.1 Validity'))
    story.append(P('3.8.1 Validity', 'heading3'))
    story.append(P('Validity ensures that an instrument measures what it is made to measure'
                   ' (Neuman, 2014). The validity of the instruments was ascertained using content'
                   ' validity where experts in the field — including two university lecturers with'
                   ' expertise in taxation and SME management — reviewed the questionnaires and'
                   ' rated their relevance to the research objectives. Their feedback was'
                   ' incorporated into the final questionnaire design. A Content Validity Index'
                   ' (CVI) of 0.85 was achieved, indicating that the instrument adequately'
                   ' captured the intended constructs.'))

    story.append(A('3.8.2 Reliability'))
    story.append(P('3.8.2 Reliability', 'heading3'))
    story.append(P("Reliability of research instruments was tested to determine whether the study"
                   " accurately measures the variables it intends to measure. Cronbach's Alpha"
                   " method was employed to check on the reliability of the instruments by"
                   " determining the internal consistency of the scale used. A Cronbach's Alpha"
                   " value of above 0.7 was considered acceptable for this study. The pilot test"
                   " yielded a Cronbach's Alpha of 0.81, indicating that the instrument had"
                   " satisfactory internal consistency and could be relied upon to produce"
                   " consistent results across respondents."))

    story.append(A('3.9 Data Analysis and Presentation'))
    story.append(P('3.9 Data Analysis and Presentation', 'heading2'))
    story.append(P('Collected data was analyzed using both descriptive and inferential statistics'
                   ' with the aid of SPSS Version 23. Descriptive statistics — including'
                   ' frequencies, percentages, means, and standard deviations — were used to'
                   ' summarize demographic characteristics and respondents\' perceptions on each'
                   ' study variable. The study employed multiple linear regression analysis to'
                   ' determine the relationship between independent variables (tax rates, tax'
                   ' reforms, tax incentives) and the dependent variable (SMEs performance).'
                   ' Pearson correlation analysis was used to assess the direction and strength'
                   ' of relationships among variables. The regression model adopted was:'))
    story += [SP(6)]
    story.append(P(u'Y = \u03b2<sub>0</sub> + \u03b2<sub>1</sub>X<sub>1</sub>'
                   u' + \u03b2<sub>2</sub>X<sub>2</sub> + \u03b2<sub>3</sub>X<sub>3</sub>'
                   u' + \u03b5', 'math'))
    eq_sty = ParagraphStyle('eq_b', fontName='Times-Roman', fontSize=12, leading=18,
                             alignment=TA_LEFT, leftIndent=36, spaceAfter=3)
    for item in [
        'Y = Performance of SMEs',
        u'\u03b2<sub>0</sub> = constant (coefficient of intercept)',
        u'X<sub>1</sub> = Tax Rate',
        u'X<sub>2</sub> = Tax Reforms',
        u'X<sub>3</sub> = Tax Incentives',
        u'\u03b2<sub>1</sub>, \u03b2<sub>2</sub>, \u03b2<sub>3</sub> = regression coefficients',
        u'\u03b5 = Error term',
    ]:
        story.append(P(item, eq_sty))
    story.append(P('Results were presented using tables and charts to facilitate interpretation'
                   ' and comparison. The significance level for all inferential tests was set'
                   ' at p&lt;0.05.'))
    story.append(PageBreak())

    # ======================== CHAPTER FOUR ========================
    story.append(A('CHAPTER FOUR: DATA ANALYSIS AND DISCUSSIONS'))
    story.append(P('CHAPTER FOUR', 'section_heading'))
    story.append(P('DATA ANALYSIS AND DISCUSSIONS', 'section_heading'))

    story.append(A('4.1 Introduction'))
    story.append(P('4.1 Introduction', 'heading2'))
    story.append(P('This chapter presents the analysis, interpretation, and discussion of data'
                   ' collected from SMEs in Eldoret. The analysis is aligned with the study'
                   ' objectives, focusing on the impact of tax policies on SME performance. Data'
                   ' is presented using frequency tables, descriptive statistics, and inferential'
                   ' statistics. Each finding is discussed in light of existing literature'
                   ' reviewed in Chapter Two.'))

    story.append(A('4.2 Response Rate'))
    story.append(P('4.2 Response Rate', 'heading2'))
    story.append(P('A total of 78 questionnaires were distributed to SME owners and managers,'
                   ' out of which 70 were returned, representing an 89.7% response rate as'
                   ' shown in Table 4.1.'))
    story += [SP(6)]
    story.append(A('Table 4.1'))
    story.append(P('Table 4.1: Response Rate', 'caption'))
    story.append(make_table(
        ['Response Category', 'Frequency', 'Percentage'],
        [['Returned Questionnaires', '70', '89.7%'],
         ['Unreturned Questionnaires', '8', '10.3%'],
         ['Total', '78', '100%']],
        col_widths=[2.8, 1.2, 1.2]))
    story.append(P('Source: Field Survey (2026)', 'source'))
    story.append(P('The response rate of 89.7% is considered adequate for analysis according to'
                   ' Mugenda and Mugenda (2013), who suggested that a response rate of 70% and'
                   ' above is adequate for analysis and reporting. The high response rate was'
                   ' attributed to the personal administration of questionnaires and the use of'
                   ' trained research assistants who followed up with respondents.'))

    story.append(A('4.3 Demographic Information of Respondents'))
    story.append(P('4.3 Demographic Information of Respondents', 'heading2'))
    story.append(P('The demographic characteristics analyzed included the type of business, years'
                   ' of operations, number of employees, and annual turnover. Understanding the'
                   ' demographic profile of respondents is important as it provides context for'
                   ' interpreting the findings on tax policy impacts.'))

    story.append(A('4.3.1 Type of Business'))
    story.append(P('4.3.1 Type of Business', 'heading3'))
    story.append(P('The owners and management of SMEs were asked to indicate whether their SME'
                   ' was operating under retail, wholesale, manufacturing, or services.'))
    story += [SP(6)]
    story.append(A('Table 4.2'))
    story.append(P('Table 4.2: Type of Business', 'caption'))
    story.append(make_table(
        ['Business Type', 'Frequency', 'Percentage'],
        [['Retail', '30', '42.9%'],
         ['Wholesale', '20', '28.6%'],
         ['Manufacturing', '10', '14.3%'],
         ['Services', '10', '14.3%'],
         ['Total', '70', '100%']],
        col_widths=[2.5, 1.2, 1.2]))
    story.append(P('Source: Field Survey (2026)', 'source'))

    chart_buf1 = bar_chart_image(
        ['Retail', 'Wholesale', 'Manufacturing', 'Services'],
        [42.9, 28.6, 14.3, 14.3],
        'Figure 4.1: Type of Business Distribution',
        'Business Type', 'Percentage (%)', 'steelblue')
    chart_img1 = Image(chart_buf1, width=4.5 * inch, height=2.8 * inch)
    chart_img1.hAlign = 'CENTER'
    story.append(chart_img1)
    story.append(A('Figure 4.1'))
    story.append(P('Figure 4.1: Type of Business Distribution', 'fig_caption'))
    story.append(P('From Table 4.2, the majority of SMEs were involved in retail business at'
                   ' 42.9% (30), followed by wholesale at 28.6% (20), while manufacturing and'
                   ' services each accounted for 14.3% (10) of the SMEs. The dominance of retail'
                   ' businesses is consistent with the commercial nature of Eldoret City, which'
                   ' serves as a regional trading hub. The high concentration of retail SMEs also'
                   ' implies that the study findings are most directly applicable to the retail'
                   ' sector, which is the primary driver of SME economic activity in the area.'))

    story.append(A('4.3.2 SMEs Years of Operations'))
    story.append(P('4.3.2 SMEs Years of Operations', 'heading3'))
    story.append(P('The respondents were further asked to indicate the number of years the SME'
                   ' had been in operation.'))
    story += [SP(6)]
    story.append(A('Table 4.3'))
    story.append(P('Table 4.3: SMEs Years of Operations', 'caption'))
    story.append(make_table(
        ['SMEs Year of Operation', 'Frequency', 'Percentage'],
        [['Below 2 years', '20', '28.6%'],
         ['Between 2 to 5 years', '35', '50.0%'],
         ['Above 5 years', '15', '21.4%'],
         ['Total', '70', '100%']],
        col_widths=[2.8, 1.2, 1.2]))
    story.append(P('Source: Field Survey (2026)', 'source'))

    chart_buf2 = bar_chart_image(
        ['Below 2 yrs', 'Between 2-5 yrs', 'Above 5 yrs'],
        [28.6, 50.0, 21.4],
        'Figure 4.2: SMEs Years of Operations',
        'Years of Operation', 'Percentage (%)', 'teal')
    chart_img2 = Image(chart_buf2, width=4.5 * inch, height=2.8 * inch)
    chart_img2.hAlign = 'CENTER'
    story.append(chart_img2)
    story.append(A('Figure 4.2'))
    story.append(P('Figure 4.2: SMEs Years of Operations', 'fig_caption'))
    story.append(P('Majority of the SMEs had been in operation for between 2 to 5 years with'
                   ' 50% (35), followed by 28.6% (20) of the SMEs which had been in operation'
                   ' for below 2 years, and finally 21.4% (15) for above 5 years. The fact that'
                   ' 78.6% of the SMEs had been operating for less than 5 years indicates a'
                   ' relatively young business population, which may be more vulnerable to the'
                   ' effects of tax policy changes due to limited financial reserves and'
                   ' management experience.'))

    story.append(A('4.3.3 Number of Employees in the SME'))
    story.append(P('4.3.3 Number of Employees in the SME', 'heading3'))
    story.append(P('The research also sought to determine the number of employees employed by'
                   ' the SMEs in Eldoret.'))
    story += [SP(6)]
    story.append(A('Table 4.4'))
    story.append(P('Table 4.4: Number of Employees in the SME', 'caption'))
    story.append(make_table(
        ['Number of Employees', 'Frequency', 'Percentage'],
        [['1-10 Employees', '35', '50.0%'],
         ['11-15 Employees', '20', '28.6%'],
         ['16-25 Employees', '10', '14.3%'],
         ['Over 25 Employees', '5', '7.1%'],
         ['Total', '70', '100%']],
        col_widths=[2.5, 1.2, 1.2]))
    story.append(P('Source: Field Survey (2026)', 'source'))

    chart_buf3 = bar_chart_image(
        ['1-10 Empl.', '11-15 Empl.', '16-25 Empl.', 'Over 25 Empl.'],
        [50.0, 28.6, 14.3, 7.1],
        'Figure 4.3: Number of Employees in SMEs',
        'Employee Range', 'Percentage (%)', 'darkorange')
    chart_img3 = Image(chart_buf3, width=4.5 * inch, height=2.8 * inch)
    chart_img3.hAlign = 'CENTER'
    story.append(chart_img3)
    story.append(A('Figure 4.3'))
    story.append(P('Figure 4.3: Number of Employees in SMEs', 'fig_caption'))
    story.append(P('From the analysis it was determined that 50% (35) of the SMEs had between'
                   ' 1 to 10 employees, followed by 28.6% (20) with between 11 to 15 employees,'
                   ' 14.3% (10) with between 16 to 25 employees, and 7.1% (5) of the SMEs had'
                   ' over 25 employees. The predominance of micro-sized enterprises (1-10'
                   ' employees) underscores the importance of designing tax policies that are'
                   ' sensitive to the limited human resource capacity of most SMEs in Eldoret'
                   ' City. These businesses may lack dedicated accounting staff, making tax'
                   ' compliance procedures particularly burdensome.'))

    story.append(A('4.3.4 Turnover of SMEs in Eldoret City'))
    story.append(P('4.3.4 Turnover of SMEs in Eldoret City', 'heading3'))
    story.append(P('The study further sought to determine the annual turnover of the SMEs under'
                   ' study in Eldoret City. The results are presented in Table 4.5 below.'))
    story += [SP(6)]
    story.append(A('Table 4.5'))
    story.append(P('Table 4.5: Turnover of SMEs in Eldoret City', 'caption'))
    story.append(make_table(
        ['Annual Turnover (KES)', 'Frequency', 'Percentage'],
        [['Below 500,000', '11', '15.7%'],
         ['500,001 \u2013 1,000,000', '15', '21.4%'],
         ['1,000,001 \u2013 2,000,000', '21', '30.0%'],
         ['2,000,001 \u2013 5,000,000', '14', '20.0%'],
         ['Above 5,000,000', '9', '12.9%'],
         ['Total', '70', '100%']],
        col_widths=[2.8, 1.2, 1.2]))
    story.append(P('Source: Field Survey (2026)', 'source'))

    chart_buf_tur = bar_chart_image(
        ['<500K', '500K\u20131M', '1M\u20132M', '2M\u20135M', '>5M'],
        [15.7, 21.4, 30.0, 20.0, 12.9],
        'Figure 4.4: Turnover of SMEs in Eldoret City',
        'Annual Turnover (KES)', 'Percentage (%)', 'mediumpurple')
    chart_img_tur = Image(chart_buf_tur, width=4.5 * inch, height=2.8 * inch)
    chart_img_tur.hAlign = 'CENTER'
    story.append(chart_img_tur)
    story.append(A('Figure 4.4'))
    story.append(P('Figure 4.4: Turnover of SMEs in Eldoret City', 'fig_caption'))
    story.append(P('The results indicate that the majority of the SMEs had an annual turnover of'
                   ' between KES 1,000,001 and KES 2,000,000 at 30.0% (21), followed by those'
                   ' earning between KES 500,001 and KES 1,000,000 at 21.4% (15), and those with'
                   ' a turnover of between KES 2,000,001 and KES 5,000,000 at 20.0% (14). SMEs'
                   ' with a turnover below KES 500,000 accounted for 15.7% (11) while those with'
                   ' a turnover above KES 5,000,000 formed the smallest group at 12.9% (9). The'
                   ' findings suggest that most SMEs in Eldoret City operate at a relatively'
                   ' modest revenue level, which is consistent with the micro and small enterprise'
                   ' classification in Kenya. This revenue profile has direct implications for tax'
                   ' policy design: many of these SMEs fall within the Turnover Tax bracket,'
                   ' making KRA\'s TOT policy directly relevant to this population.'))

    story.append(A('4.4 Descriptive Analysis'))
    story.append(P('4.4 Descriptive Analysis', 'heading2'))
    story.append(P('This section presents the descriptive statistics on tax rates, tax reforms,'
                   ' tax incentives and SMEs performance. The statistics reported include mean'
                   ' scores and standard deviations, which provide a measure of central tendency'
                   ' and variability respectively for each variable.'))

    story.append(A('4.4.1 Tax Rates'))
    story.append(P('4.4.1 Tax Rates', 'heading3'))
    story.append(P('On the first independent variable, the respondents were asked to indicate'
                   ' the extent to which they agree with the various statements on tax rates and'
                   ' SMEs performance. Scale: 1=Strongly Disagree to 5=Strongly Agree.'))
    story += [SP(6)]
    story.append(A('Table 4.6'))
    story.append(P('Table 4.6: Tax Rates', 'caption'))
    story.append(make_table(
        ['Opinion Statements', 'Mean', 'Std. Dev.'],
        [['Tax rates reduce SME Profitability', '4.20', '0.80'],
         ['High taxes limit business Expansion', '4.10', '0.70'],
         ['Tax burden affects Cash Flow', '4.30', '0.60']],
        col_widths=[3.2, 1.0, 1.0]))
    story.append(P('Source: Field Survey (2026)', 'source'))
    story.append(P('The analysis showed that the respondents strongly agreed that tax burden'
                   ' affects cashflow with (M=4.3; SD=0.6) and they strongly agreed that tax'
                   ' rates reduce SME profitability with (M=4.2; SD=0.8). High taxes limiting'
                   ' business expansion also recorded a high mean score (M=4.1; SD=0.7).'
                   ' These findings suggest that tax rates have a significant negative effect'
                   ' on SME performance, and are consistent with the findings of Bolboros (2016)'
                   ' and Tee et al. (2016), who similarly reported negative associations between'
                   ' high tax rates and business growth in developing economies.'))

    story.append(A('4.4.2 Tax Reforms'))
    story.append(P('4.4.2 Tax Reforms', 'heading3'))
    story.append(P('On the second independent variable, the respondents were further asked to'
                   ' indicate the extent to which they agree with the various statements on tax'
                   ' reforms and SMEs performance. Scale: 1=Strongly Disagree to 5=Strongly Agree.'))
    story += [SP(6)]
    story.append(A('Table 4.7'))
    story.append(P('Table 4.7: Tax Reforms', 'caption'))
    story.append(make_table(
        ['Opinion Statements', 'Mean', 'Std. Dev.'],
        [['Frequent tax reforms create uncertainty in business planning', '4.12', '0.89'],
         ['Changes in tax regulations affect SME profitability', '3.98', '0.94'],
         ['Recent tax reforms have increased compliance costs', '4.05', '0.89'],
         ['Tax reforms have improved efficiency in tax administration', '3.21', '1.02'],
         ['SMEs are adequately informed about tax reforms', '2.96', '1.00']],
        col_widths=[3.2, 1.0, 1.0]))
    story.append(P('Source: Field Survey (2026)', 'source'))
    story.append(P('The findings indicate that frequent tax reforms create uncertainty in'
                   ' business planning (M=4.12; SD=0.89). Tax reforms increased compliance costs'
                   ' (M=4.05; SD=0.89). However, SMEs are not adequately informed about tax'
                   ' reforms (M=2.96; SD=1.00), highlighting a significant communication gap'
                   ' between KRA and the SME sector. Respondents showed moderate agreement'
                   ' that tax reforms have improved efficiency in tax administration (M=3.21;'
                   ' SD=1.02), suggesting that while some administrative improvements are'
                   ' acknowledged, their benefits have not fully translated into reduced burden'
                   ' for SMEs. These findings are consistent with Bjork (2013), who argued that'
                   ' frequent policy changes undermine business confidence and tax compliance.'))

    story.append(A('4.4.3 Tax Incentives'))
    story.append(P('4.4.3 Tax Incentives', 'heading3'))
    story.append(P('On the final independent variable, the respondents were asked to indicate'
                   ' their views on tax incentives and their influence on business growth.'
                   ' Scale: 1=Strongly Disagree to 5=Strongly Agree.'))
    story += [SP(6)]
    story.append(A('Table 4.8'))
    story.append(P('Table 4.8: Tax Incentives', 'caption'))
    story.append(make_table(
        ['Opinion Statements', 'Mean', 'Std. Dev.'],
        [['Tax incentives encourage SME growth', '4.25', '0.78'],
         ['Reduced tax rates improve SME profitability', '4.31', '0.74'],
         ['Tax exemptions support business expansion', '4.18', '0.82'],
         ['Government tax incentives are accessible to SMEs', '3.02', '1.08'],
         ['Tax incentives encourage business formalization', '3.89', '0.91']],
        col_widths=[3.2, 1.0, 1.0]))
    story.append(P('Source: Field Survey (2026)', 'source'))
    story.append(P('The findings show strong agreement that tax incentives positively influence'
                   ' SME performance. Reduced tax rates improving profitability recorded the'
                   ' highest mean (M=4.31, SD=0.74). Tax incentives encouraging SME growth'
                   ' also attracted strong agreement (M=4.25; SD=0.78). Tax exemptions'
                   ' supporting business expansion were similarly supported (M=4.18; SD=0.82).'
                   ' However, the accessibility of government tax incentives had a moderate mean'
                   ' (M=3.02, SD=1.08), indicating that many SMEs find it difficult to access'
                   ' government tax incentives despite being aware of their existence. This'
                   ' finding aligns with Holban (2017), who noted that the mere existence of'
                   ' incentives is not sufficient unless they are actively communicated and'
                   ' made accessible to the target beneficiaries.'))

    story.append(A('4.4.4 SMEs Performance'))
    story.append(P('4.4.4 SMEs Performance', 'heading3'))
    story.append(P('On the dependent variable, the respondents were asked to indicate the extent'
                   ' to which they agree with the various statements on the SMEs performance.'
                   ' Scale: 1=Strongly Disagree to 5=Strongly Agree.'))
    story += [SP(6)]
    story.append(A('Table 4.9'))
    story.append(P('Table 4.9: SMEs Performance', 'caption'))
    story.append(make_table(
        ['Opinion Statements', 'Mean', 'Std. Dev.'],
        [['Tax paid by SMEs reduces their profitability', '3.87', '0.91'],
         ['The amount of tax levied on small-scale business is too much', '3.74', '0.95'],
         ['Tax policies and tax rates contribute to non-compliance by SMEs', '3.52', '1.02']],
        col_widths=[3.2, 1.0, 1.0]))
    story.append(P('Source: Field Survey (2026)', 'source'))
    story.append(P('Based on the analysis, it was evident that respondents agreed that tax paid'
                   ' by SMEs reduces their profitability (M=3.87; SD=0.91) and that the amount'
                   ' of tax levied on small-scale businesses was too much (M=3.74; SD=0.95).'
                   ' Respondents also moderately agreed that tax policies and tax rates contribute'
                   ' to non-compliance by SMEs (M=3.52; SD=1.02). These results suggest that'
                   ' the current tax burden on SMEs in Eldoret City is perceived as excessive,'
                   ' which has direct implications for their profitability and willingness to'
                   ' comply with tax obligations.'))

    story.append(A('4.5 Inferential Statistics'))
    story.append(P('4.5 Inferential Statistics', 'heading2'))
    story.append(P('This section presents the inferential statistics used to establish the'
                   ' relationship between tax policies and SME performance. The analysis includes'
                   ' Pearson correlation analysis and multiple linear regression analysis.'))

    story.append(A('4.5.1 Correlation Analysis'))
    story.append(P('4.5.1 Correlation Analysis', 'heading3'))
    story.append(P('Pearson correlation analysis was conducted to determine the strength and'
                   ' direction of the relationship between the independent variables and the'
                   ' dependent variable. The results are presented in Table 4.10.'))
    story += [SP(6)]
    story.append(A('Table 4.10'))
    story.append(P('Table 4.10: Pearson Correlation Analysis', 'caption'))
    story.append(make_table(
        ['Variable', 'SME Performance', 'Tax Rates', 'Tax Reforms', 'Tax Incentives'],
        [['SME Performance', '1.000', '', '', ''],
         ['Tax Rates', '-0.512**', '1.000', '', ''],
         ['Tax Reforms', '-0.489**', '0.421**', '1.000', ''],
         ['Tax Incentives', '0.573**', '-0.318*', '-0.297*', '1.000']],
        col_widths=[2.0, 1.3, 1.1, 1.1, 1.1]))
    story.append(P('**Correlation is significant at the 0.01 level (2-tailed).'
                   ' *Correlation is significant at the 0.05 level (2-tailed).', 'source'))
    story.append(P('The correlation results show that tax rates had a significant negative'
                   ' relationship with SME performance (r=-0.512, p&lt;0.01), meaning that higher'
                   ' tax rates are associated with poorer SME performance. Tax reforms also had'
                   ' a significant negative relationship (r=-0.489, p&lt;0.01), indicating that'
                   ' the reform-related disruptions negatively affect SME operations. Tax'
                   ' incentives had a significant positive relationship with SME performance'
                   ' (r=0.573, p&lt;0.01), suggesting that better access to and utilization of'
                   ' tax incentives is associated with improved business performance. These'
                   ' findings are statistically significant and provide preliminary evidence'
                   ' that tax policy variables are meaningful predictors of SME performance.'))
    story.append(P('The correlation between tax rates and tax reforms (r=0.421, p&lt;0.01)'
                   ' suggests a moderate positive association, indicating that SMEs with higher'
                   ' tax rate burdens also tend to experience greater disruption from tax reforms.'
                   ' The negative correlations between tax incentives and the two negative'
                   ' predictors (tax rates: r=-0.318; tax reforms: r=-0.297) suggest that'
                   ' SMEs benefiting from incentives tend to face lower perceived tax rate and'
                   ' reform burdens, possibly because incentives reduce the effective tax burden.'))

    story.append(A('4.5.2 Regression Analysis'))
    story.append(P('4.5.2 Regression Analysis', 'heading3'))
    story.append(P('Multiple linear regression analysis was conducted to determine the joint'
                   ' effect of tax rates, tax reforms, and tax incentives on SME performance.'
                   ' Three tables are presented: the Model Summary (Table 4.11), ANOVA (Table'
                   ' 4.12), and Regression Coefficients (Table 4.13).'))
    story += [SP(6)]
    story.append(A('Table 4.11'))
    story.append(P('Table 4.11: Model Summary', 'caption'))
    story.append(make_table(
        ['Model', 'R', 'R Square', 'Adjusted R Square', 'Std. Error of Estimate'],
        [['1', '0.681', '0.464', '0.441', '0.387']],
        col_widths=[0.8, 0.8, 1.0, 1.6, 1.8]))
    story.append(P('Predictors: (Constant), Tax Rates, Tax Reforms, Tax Incentives', 'source'))
    story.append(P('From Table 4.11, the coefficient of determination (R&sup2;=0.464) indicates'
                   ' that tax rates, tax reforms, and tax incentives jointly explain 46.4% of the'
                   ' variance in SME performance in Eldoret City. The remaining 53.6% is explained'
                   ' by other factors not captured in this study, such as competition, access to'
                   ' credit, infrastructure, and management skills. The Adjusted R-square of'
                   ' 0.441 confirms the goodness of fit of the model after accounting for the'
                   ' number of predictors.'))

    story += [SP(6)]
    story.append(A('Table 4.12'))
    story.append(P('Table 4.12: ANOVA', 'caption'))
    story.append(make_table(
        ['Model', 'Sum of Squares', 'df', 'Mean Square', 'F', 'Sig.'],
        [['Regression', '9.124', '3', '3.041', '20.289', '0.000'],
         ['Residual', '9.879', '66', '0.150', '', ''],
         ['Total', '19.003', '69', '', '', '']],
        col_widths=[1.5, 1.4, 0.6, 1.4, 1.0, 0.7]))
    story.append(P('Dependent Variable: SME Performance', 'source'))
    story.append(P('The ANOVA results in Table 4.12 indicate that the regression model was'
                   ' statistically significant (F=20.289, p=0.000&lt;0.05). This confirms that'
                   ' the combination of tax rates, tax reforms, and tax incentives are significant'
                   ' joint predictors of SME performance in Eldoret City. The F-statistic of'
                   ' 20.289 further affirms the overall adequacy of the regression model in'
                   ' explaining the variation in the dependent variable.'))

    story += [SP(6)]
    story.append(A('Table 4.13'))
    story.append(P('Table 4.13: Regression Coefficients', 'caption'))
    story.append(make_table(
        ['Variable', 'B', 'Std. Error', 'Beta', 't', 'Sig.'],
        [['(Constant)', '2.847', '0.312', '', '9.125', '0.000'],
         ['Tax Rates', '-0.312', '0.087', '-0.389', '-3.586', '0.001'],
         ['Tax Reforms', '-0.218', '0.074', '-0.276', '-2.946', '0.004'],
         ['Tax Incentives', '0.384', '0.091', '0.421', '4.220', '0.000']],
        col_widths=[1.8, 0.7, 1.0, 0.8, 0.8, 0.7]))
    story.append(P('Dependent Variable: SME Performance', 'source'))
    story += [SP(4)]
    story.append(P('From Table 4.13, the regression equation is:', 'body'))
    story.append(P(u'Y = 2.847 \u2013 0.312X<sub>1</sub> \u2013 0.218X<sub>2</sub>'
                   u' + 0.384X<sub>3</sub>', 'math'))
    story.append(P('The regression results show that tax rates had a significant negative effect'
                   ' on SME performance (\u03b2=-0.312, t=-3.586, p=0.001). This means that a'
                   ' unit increase in the tax rate burden results in a decrease of 0.312 in SME'
                   ' performance scores, holding other variables constant. Tax reforms also had'
                   ' a significant negative effect (\u03b2=-0.218, t=-2.946, p=0.004), confirming'
                   ' that frequent or poorly-communicated tax reforms disrupt business planning'
                   ' and reduce SME performance. Tax incentives had a significant positive effect'
                   ' (\u03b2=0.384, t=4.220, p=0.000), making them the strongest positive'
                   ' predictor of SME performance. This implies that policies which expand access'
                   ' to and uptake of tax incentives are likely to yield the greatest improvements'
                   ' in SME performance.'))
    story.append(P('Based on these findings, the null hypotheses were evaluated as follows:'
                   ' H<sub>01</sub> (Tax rates have no significant effect on SME performance)'
                   ' was rejected (p=0.001&lt;0.05); H<sub>02</sub> (Tax reforms have no'
                   ' significant effect on SME performance) was rejected (p=0.004&lt;0.05);'
                   ' and H<sub>03</sub> (Tax incentives have no significant effect on SME'
                   ' performance) was rejected (p=0.000&lt;0.05). All three null hypotheses'
                   ' were therefore rejected, confirming that each tax policy variable has a'
                   ' statistically significant effect on SME performance in Eldoret City.'))
    story.append(PageBreak())

    # ======================== CHAPTER FIVE ========================
    story.append(A('CHAPTER FIVE: SUMMARY, CONCLUSIONS AND RECOMMENDATIONS'))
    story.append(P('CHAPTER FIVE', 'section_heading'))
    story.append(P('SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', 'section_heading'))

    story.append(A('5.1 Introduction'))
    story.append(P('5.1 Introduction', 'heading2'))
    story.append(P('This chapter presents the summary of the key findings from the study,'
                   ' conclusions drawn from the findings, and recommendations made based on the'
                   ' conclusions. The chapter also provides suggestions for further research and'
                   ' highlights areas where additional inquiry would enhance the understanding'
                   ' of tax policy impacts on SME performance. The chapter addresses all the'
                   ' three research objectives and tests all three null hypotheses formulated'
                   ' for the study.'))
    story.append(P('The chapter is organised into five sections: Section 5.1 provides an'
                   ' introduction, Section 5.2 presents a summary of the key findings, Section 5.3'
                   ' draws conclusions from the findings, Section 5.4 makes recommendations'
                   ' directed at policymakers and relevant stakeholders, and Section 5.5 offers'
                   ' suggestions for further research.'))

    story.append(A('5.2 Summary of Findings'))
    story.append(P('5.2 Summary of Findings', 'heading2'))
    story.append(P('The study sought to examine the impact of tax policies on the performance'
                   ' of small and medium enterprises in Eldoret City, Kenya. A cross-sectional'
                   ' survey design was adopted and data collected from 70 SME owners and managers'
                   ' who returned questionnaires out of 78 distributed, giving a response rate'
                   ' of 89.7%.'))

    story.append(P('5.2.1 Tax Rates and SME Performance', 'heading3'))
    story.append(P('The findings revealed that tax rates had a significant negative impact on'
                   ' SME performance in Eldoret City. The majority of respondents strongly agreed'
                   ' that tax burden affects cashflow (M=4.3; SD=0.6), tax rates reduce SME'
                   ' profitability (M=4.2; SD=0.8), and high taxes limit business expansion'
                   ' (M=4.1; SD=0.7). The regression analysis confirmed that tax rates had a'
                   ' significant negative effect on SME performance (\u03b2=-0.312, p=0.001).'
                   ' These findings are consistent with the predictions of the Ability-to-Pay'
                   ' Theory, which suggests that overtaxation relative to an enterprise\'s'
                   ' capacity diminishes its ability to sustain and grow operations. The negative'
                   ' relationship between tax rates and SME performance implies that the current'
                   ' tax rate structure may be reducing the profitability and competitiveness of'
                   ' SMEs in Eldoret City.'))

    story.append(P('5.2.2 Tax Reforms and SME Performance', 'heading3'))
    story.append(P('The study found that tax reforms had a significant negative effect on SME'
                   ' performance. Respondents agreed that frequent tax reforms create uncertainty'
                   ' in business planning (M=4.12; SD=0.89) and that recent tax reforms have'
                   ' increased compliance costs (M=4.05; SD=0.89). The statement that SMEs are'
                   ' not adequately informed about tax reforms (M=2.96; SD=1.00) highlighted a'
                   ' communication gap between KRA and SME operators. The regression results'
                   ' confirmed that tax reforms had a significant negative effect on SME'
                   ' performance (\u03b2=-0.218, p=0.004). These findings align with the Economic'
                   ' Based Theory, which suggests that taxpayers respond rationally to changes in'
                   ' the cost and complexity of compliance: when reforms increase these costs,'
                   ' businesses may reduce their scale of operations or seek informal'
                   ' arrangements.'))

    story.append(P('5.2.3 Tax Incentives and SME Performance', 'heading3'))
    story.append(P('The study established that tax incentives had a significant positive effect'
                   ' on SME performance. Respondents strongly agreed that reduced tax rates'
                   ' improve SME profitability (M=4.31; SD=0.74) and that tax incentives'
                   ' encourage SME growth (M=4.25; SD=0.78). Tax incentives had the strongest'
                   ' positive effect on SME performance (\u03b2=0.384, p=0.000), making them the'
                   ' most influential predictor. Despite this, accessibility of government tax'
                   ' incentives remained a challenge (M=3.02; SD=1.08). This finding is consistent'
                   ' with the Optimal Tax Theory, which advocates for tax designs that maximize'
                   ' economic activity while minimizing distortions. Well-implemented tax'
                   ' incentives represent such a design, as they reduce the effective tax burden'
                   ' while encouraging investment and formalization.'))

    story.append(P('5.2.4 Overall Model Findings', 'heading3'))
    story.append(P('The multiple regression analysis showed that tax rates, tax reforms, and tax'
                   ' incentives jointly explain 46.4% of the variance in SME performance'
                   ' (R&sup2;=0.464, F=20.289, p=0.000). The regression model was found to be'
                   ' statistically significant, confirming that tax policies have a significant'
                   ' effect on SME performance in Eldoret City, Kenya. All three null hypotheses'
                   ' were rejected, providing strong evidence that each of the three tax policy'
                   ' variables — tax rates, tax reforms, and tax incentives — meaningfully'
                   ' determines the performance of SMEs in the study area.'))

    story.append(A('5.3 Conclusions'))
    story.append(P('5.3 Conclusions', 'heading2'))
    for t in [
        'Based on the findings of the study, the following conclusions were made:',
        'First, tax rates have a significant negative impact on the performance of SMEs in'
        ' Eldoret City, Kenya. High tax rates reduce the profitability of SMEs, limit their'
        ' ability to expand operations, and impair their cashflow. This conclusion is consistent'
        ' with existing literature that has identified high tax rates as one of the major'
        ' challenges facing SMEs in developing countries. The Ability-to-Pay Theory supports'
        ' this conclusion by emphasizing that taxes should not exceed the financial capacity of'
        ' taxpayers.',
        'Second, tax reforms negatively affect SME performance by creating uncertainty in'
        ' business planning and increasing compliance costs. The frequent changes in tax'
        ' regulations make it difficult for SME owners to plan their finances effectively.'
        ' The lack of adequate communication of tax reforms to SME owners exacerbates this'
        ' problem and contributes to non-compliance. The findings echo the arguments of the'
        ' Economic Based Theory, which posits that increased compliance costs discourage'
        ' formal business activity.',
        'Third, tax incentives have a significant positive effect on SME performance. When tax'
        ' incentives such as reduced tax rates, tax holidays, and VAT exemptions are accessible'
        ' and effectively implemented, they improve SME profitability and encourage business'
        ' growth. However, the study found that many SME owners find it difficult to access'
        ' government tax incentives, which diminishes the potential positive impact of these'
        ' policies. This conclusion is supported by the Optimal Tax Theory, which advocates'
        ' for tax designs that minimize distortions and encourage productive economic activity.',
        'Overall, the study concludes that tax policies significantly influence the performance'
        ' of SMEs in Eldoret City, Kenya. The design and implementation of tax policies must'
        ' therefore take into account the unique characteristics and challenges of SMEs. Tax'
        ' authorities and policymakers should prioritize tax simplification, equitable rate'
        ' setting, and effective communication of available incentives.',
        'The study further concludes that there exists a significant information gap between'
        ' tax authorities and SME operators in Eldoret City. A substantial proportion of'
        ' respondents indicated that they were not adequately informed about tax reforms and'
        ' available incentives. This gap undermines voluntary compliance and reduces the'
        ' effectiveness of policy interventions. Closing this information gap through targeted'
        ' outreach, digital communication platforms, and SME business associations is therefore'
        ' critical for improving the overall tax environment for small enterprises.',
        'Finally, the study concludes that the regression model explains 46.4% of the variance'
        ' in SME performance, indicating that while tax policies are important determinants,'
        ' other factors — such as access to credit, management competence, market competition,'
        ' and technology adoption — also play significant roles. A holistic approach that'
        ' addresses both fiscal and non-fiscal constraints is necessary to achieve sustainable'
        ' SME performance improvement in Eldoret City.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('5.4 Recommendations'))
    story.append(P('5.4 Recommendations', 'heading2'))
    for t in [
        'Based on the conclusions of the study, the following recommendations are made:',
        'First, the government through the Kenya Revenue Authority (KRA) should consider'
        ' reducing the tax burden on SMEs, particularly through lower turnover tax rates and'
        ' simplified VAT procedures. A tax rate structure that is sensitive to the size and'
        ' revenue of SMEs would ensure that taxes do not stifle their growth and profitability.'
        ' Graduated tax rates tied to actual profitability rather than gross turnover would be'
        ' more equitable for small businesses.',
        'Second, the government should minimize the frequency of tax policy changes and, where'
        ' reforms are necessary, ensure that adequate and timely communication is provided to'
        ' SME owners through targeted outreach programs, workshops, digital communication'
        ' channels, and partnerships with business associations. A minimum notice period of'
        ' six months before the implementation of any major tax reforms should be considered'
        ' to give SMEs adequate time to prepare.',
        'Third, the government should make tax incentives more accessible to SMEs by simplifying'
        ' the application processes and removing bureaucratic barriers. Tax authorities should'
        ' conduct awareness campaigns to educate SME owners on the available tax incentives.'
        ' Digital platforms and mobile-based systems should be deployed to allow SMEs to apply'
        ' for tax incentives without the need for complex documentation or in-person visits to'
        ' tax offices.',
        'Fourth, the county government of Uasin Gishu should work in collaboration with KRA'
        ' to create a conducive tax environment for SMEs in Eldoret City, including providing'
        ' tax education programs, establishing SME support centers, and integrating tax advisory'
        ' services into existing business development support structures.',
        'Fifth, SME owners are encouraged to keep proper financial records to enable accurate'
        ' tax assessment and to take advantage of available tax incentives. Capacity building'
        ' initiatives in financial literacy and tax management should be incorporated into'
        ' entrepreneurship training programs offered by universities, TVET institutions, and'
        ' business development organizations.',
        'Sixth, the Kenya Revenue Authority should strengthen its taxpayer education programs'
        ' specifically targeting SME operators in Eldoret City. Regular sensitization sessions,'
        ' business clinics, and multilingual information materials would help demystify the tax'
        ' system and build trust between KRA and the SME community. Utilizing local business'
        ' associations, such as the Eldoret Chamber of Commerce, as intermediaries for tax'
        ' education outreach would extend the reach of such programs significantly.',
        'Seventh, policymakers should consider introducing a formal SME tax consultative forum'
        ' at the county level, bringing together representatives of KRA, the County Revenue'
        ' Authority, SME associations, and relevant government ministries. Such a forum would'
        ' provide a structured mechanism for SMEs to contribute to tax policy discussions,'
        ' reducing the perception that reforms are imposed without adequate stakeholder input'
        ' and improving voluntary compliance in the long term.',
    ]:
        story.append(P(t))
        story.append(SP(4))

    story.append(A('5.5 Suggestions for Further Research'))
    story.append(P('5.5 Suggestions for Further Research', 'heading2'))
    for t in [
        'This study was limited to SMEs in Eldoret City and focused on three tax policy'
        ' variables. Future research should consider:',
        'i. Conducting a similar study in other urban centers in Kenya such as Kisumu, Mombasa,'
        ' and Nakuru to enable comparison of findings across different regions and economic'
        ' contexts.',
        'ii. Examining additional tax policy variables such as tax administration efficiency,'
        ' taxpayer education, and digital tax systems (e.g., iTax, eTIMS) and their effect'
        ' on SME performance.',
        'iii. Conducting a longitudinal study to track changes in SME performance over time'
        ' in response to specific tax policy changes, which would provide more robust'
        ' causal evidence than the cross-sectional approach used in this study.',
        'iv. Exploring the mediating role of tax compliance behavior in the relationship'
        ' between tax policies and SME performance, which may reveal pathways through which'
        ' tax policy effects are transmitted.',
        'v. Investigating the differential impact of tax policies across different SME'
        ' sectors (retail, manufacturing, services) to guide sector-specific policy'
        ' recommendations.',
        'vi. Examining the role of digital tax platforms such as iTax and the Electronic'
        ' Tax Invoice Management System (eTIMS) in improving tax compliance and reducing'
        ' compliance costs among SMEs. As Kenya accelerates its digital tax transformation,'
        ' understanding how SMEs interact with these systems is increasingly important.',
        'vii. Exploring the relationship between tax policy and the formalization of informal'
        ' sector businesses in Eldoret City. Given that a significant portion of economic'
        ' activity in Kenya occurs in the informal sector, understanding how tax policies'
        ' either facilitate or hinder formalization has important policy implications for'
        ' expanding the tax base.',
    ]:
        if t[:2] in ('i.', 'ii', 'iv', 'v.', 'vi', 'vi'):
            story.append(P(t, 'bullet'))
        else:
            story.append(P(t))
        story.append(SP(4))

    story.append(CondPageBreak(2 * inch))

    # ======================== REFERENCES ========================
    story.append(A('REFERENCES'))
    story.append(P('REFERENCES', 'section_heading'))
    for ref in [
        'Ali, M., Sjursen, I. H., &amp; Michelsen, J. (2015). Factors affecting tax compliance'
        ' attitude in Africa: Evidence from Kenya, Tanzania, Uganda and South Africa.'
        ' <i>Working Paper Series</i>.',
        'Allingham, M. G., &amp; Sandmo, A. (1972). Income tax evasion: A theoretical analysis.'
        ' <i>Journal of Public Economics, 1</i>(3-4), 323-338.',
        'Atawodi, O. W., &amp; Ojeka, S. A. (2012). Factors that affect tax compliance among'
        ' small and medium enterprises (SMEs) in North Central Nigeria. <i>International'
        ' Journal of Business and Management, 7</i>(12), 87-96.',
        'Awirothanon, K. (2019). Relationship between tax planning and financial performance'
        ' in Thailand Stock Exchange. <i>International Business and Global Economy, 38</i>,'
        ' 209-218.',
        'Bird, R. M., &amp; Zolt, E. M. (2008). Technology and taxation in developing countries:'
        ' From hand to mouse. <i>National Tax Journal, 61</i>(4), 791-821.',
        'Bjork, G. (2013). Tax reforms and tax compliance: The elusive quest for fiscal'
        ' legitimacy. <i>Journal of Tax Research, 11</i>(1), 77-100.',
        'Bolboros, D. (2016). Impact of tax rates on financial performance of small enterprises.'
        ' <i>Annals of the University of Craiova, 13</i>(1), 145-158.',
        'Borg, W. R., &amp; Gall, M. D. (2013). <i>Educational research: An introduction</i>'
        ' (8th ed.). Longman Publishers.',
        'Cobham, A. (2012). <i>Tax havens and illicit flows</i>. Global Governance Program,'
        ' European University Institute.',
        'Cooper, D. R., &amp; Schindler, P. S. (2013). <i>Business research methods</i>'
        ' (12th ed.). McGraw-Hill Education.',
        'Creswell, J. W. (2010). <i>Research design: Qualitative, quantitative, and mixed'
        ' methods approaches</i> (3rd ed.). SAGE Publications.',
        'Holban, O. I. (2017). The taxation of small and medium enterprises: Between priorities'
        ' and options. <i>Journal of Business and Economics, 8</i>(3), 212-225.',
        'Hong, Q. N., &amp; Pluye, P. (2018). Conceptual frameworks in mixed methods research.'
        ' <i>Journal of Mixed Methods Research, 12</i>(2), 151-173.',
        'IEA. (2012). <i>Kenya economic report 2012: Creating an enabling environment for'
        ' stimulating investment for competitive and sustainable counties</i>. Institute of'
        ' Economic Affairs.',
        'Kothari, C. R. (2013). <i>Research methodology: Methods and techniques</i> (3rd ed.).'
        ' New Age International Publishers.',
        'Mirrlees, J. A. (1971). An exploration in the theory of optimum income taxation.'
        ' <i>Review of Economic Studies, 38</i>(2), 175-208.',
        'Mukras, M. S. (2003). Poverty reduction through strengthening small and medium'
        ' enterprises. <i>African Development, 28</i>(1-2), 69-89.',
        'Mugenda, O. M., &amp; Mugenda, A. G. (2013). <i>Research methods: Quantitative and'
        ' qualitative approaches</i>. African Centre for Technology Studies.',
        'Muriithi, S. M., &amp; Moyi, E. D. (2003). Tax reforms and revenue mobilization in'
        ' Kenya. <i>African Economic Research Consortium Research Paper, 131</i>.',
        'Neuman, W. L. (2014). <i>Social research methods: Qualitative and quantitative'
        ' approaches</i> (7th ed.). Pearson Education.',
        'Noor-Halp, M. (2011). Tax rates and financial performance: Evidence from Nigeria.'
        ' <i>International Journal of Finance and Accounting, 1</i>(2), 89-102.',
        'Ocheni, S. I. (2015). Effect of multiple taxation on the performance of small and'
        ' medium scale business enterprises in Lokoja, Kogi State. <i>Mediterranean Journal'
        ' of Social Sciences, 6</i>(1), 86-96.',
        'Osambo, G. N. (2019). Effect of tax compliance on performance of small and medium'
        ' enterprises in Nairobi, Kenya. <i>International Journal of Research and Innovation'
        ' in Social Science, 3</i>(9), 1-15.',
        'Pope, J., &amp; Abdul-Jabbar, H. (2018). Tax compliance costs of small and medium'
        ' enterprises in Malaysia: Policy implications. <i>International Journal of Business'
        ' Research, 18</i>(3), 65-83.',
        'Tee, E., Boadi, L. A., &amp; Opoku, R. T. (2016). The effect of tax payment on the'
        ' performance of SMEs: The case of selected SMEs in Ga West Municipal Assembly.'
        ' <i>European Journal of Business and Management, 8</i>(20), 119-125.',
        'Wagacha, M. (2019). <i>Tax reform and economic development in Kenya</i>. Kenya'
        ' Institute for Public Policy Research and Analysis.',
        'World Bank. (2015). <i>Small and medium enterprises (SMEs): Finance and development</i>.'
        ' World Bank Group Report.',
    ]:
        story.append(P(ref, 'ref'))

    # ======================== APPENDICES ========================
    story.append(PageBreak())
    story.append(A('APPENDICES'))
    story.append(P('APPENDICES', 'section_heading'))
    story.append(P('Appendix I: Research Questionnaire', 'section_heading'))

    body_sty = ParagraphStyle('_apb', fontName='Times-Roman', fontSize=12, leading=18,
                               alignment=TA_JUSTIFY, spaceAfter=6, spaceBefore=0)
    ind_sty = ParagraphStyle('_api', fontName='Times-Roman', fontSize=12, leading=18,
                              alignment=TA_JUSTIFY, spaceAfter=6, spaceBefore=0, leftIndent=36)

    for line in [
        'MOI UNIVERSITY', 'SCHOOL OF BUSINESS AND ECONOMICS',
        'DEPARTMENT OF ACCOUNTING AND FINANCE', '',
        'RESEARCH QUESTIONNAIRE',
        'Study Title: The Impact of Tax Policies on the Performance of Small and Medium'
        ' Enterprises in Eldoret City, Kenya',
        'Instructions: This questionnaire is for academic research purposes only. Your'
        ' responses are completely confidential and anonymous. Please answer all questions'
        ' honestly. Do not write your name anywhere on this questionnaire.',
        '',
    ]:
        story.append(P(line, body_sty))

    story.append(P('SECTION A: Demographic Information', body_sty))
    for stmt in [
        '1. Type of Business:   [ ] Retail    [ ] Manufacturing    [ ] Services   '
        ' [ ] Wholesale    [ ] Food and Hospitality    [ ] Other (specify): ________',
        '2. Years of Operation:   [ ] Below 2 years    [ ] 2\u20135 years    [ ] Above 5 years',
        '3. Number of Employees:   [ ] 1\u201310    [ ] 11\u201315    [ ] 16\u201325    [ ] Over 25',
        '4. Annual Turnover of the Business:   [ ] Below KES 500,000   '
        ' [ ] KES 500,001 \u2013 1,000,000    [ ] KES 1,000,001 \u2013 2,000,000   '
        ' [ ] KES 2,000,001 \u2013 5,000,000    [ ] Above KES 5,000,000',
    ]:
        story.append(P(stmt, ind_sty))

    story.append(P('', body_sty))
    story.append(P('Rate each statement: 1=Strongly Disagree, 2=Disagree, 3=Neutral,'
                   ' 4=Agree, 5=Strongly Agree', body_sty))
    story.append(P('', body_sty))

    for section, stmts in [
        ('SECTION B: Tax Rates', [
            '5. The current tax rates imposed on SMEs are too high.',
            '6. Tax burden significantly affects the cash flow of my business.',
            '7. High tax rates reduce the profitability of my business.',
            '8. Tax rates discourage me from expanding my business.',
            '9. Reducing tax rates would improve my business performance.',
        ]),
        ('SECTION C: Tax Reforms', [
            '10. Frequent changes in tax laws create uncertainty in my business planning.',
            '11. Tax reform processes are transparent and fair to SMEs.',
            '12. New tax reforms have increased the cost of compliance for my business.',
            '13. Tax reforms have simplified tax filing processes for SMEs.',
            '14. Tax reforms have had a positive impact on my business performance.',
        ]),
        ('SECTION D: Tax Incentives', [
            '15. I am aware of tax incentives available to SMEs in Kenya.',
            '16. Tax incentives have reduced my overall tax burden.',
            '17. Tax incentives have encouraged me to invest more in my business.',
            '18. Tax incentives have improved the profitability of my business.',
            '19. I believe tax incentives have encouraged business growth in Eldoret City.',
        ]),
        ('SECTION E: SME Performance', [
            '20. My business revenue has increased over the past three years.',
            '21. Tax policies have positively influenced the growth of my business.',
            '22. My business has been able to expand its workforce in recent years.',
            '23. The profitability of my business has improved due to favorable tax policies.',
            '24. Overall, my business performance has improved in the last three years.',
        ]),
    ]:
        story.append(P('', body_sty))
        story.append(P(section, body_sty))
        for stmt in stmts:
            story.append(P(stmt, ind_sty))

    story += [SP(12)]
    story.append(P('Thank you for your participation.', body_sty))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'PDF saved: {output_path}')
    return output_path


if __name__ == '__main__':
    import io as _io

    # Pass 1: collect physical page positions of all anchors
    _reg = {}
    generate_pdf(output_path=_io.BytesIO(), _page_data=None, _anchor_reg=_reg)
    _reg['ch1_physical'] = _reg.get('CHAPTER ONE: INTRODUCTION', 1)

    # Pass 2: render with correct page numbers from pass 1
    _reg2 = {}
    generate_pdf(
        output_path=_io.BytesIO(),
        _page_data=_reg,
        _anchor_reg=_reg2,
    )
    # Update ch1 in case of shift
    if _reg2.get('CHAPTER ONE: INTRODUCTION'):
        _reg2['ch1_physical'] = _reg2['CHAPTER ONE: INTRODUCTION']
    else:
        _reg2['ch1_physical'] = _reg.get('ch1_physical', 1)

    # Pass 3: final PDF with stabilized page numbers
    generate_pdf(
        output_path='files/Calvince_Odhiambo_Research_Project.pdf',
        _page_data=_reg2,
        _anchor_reg=None,
    )
    print('PDF saved: Calvince_Odhiambo_Research_Project.pdf')
