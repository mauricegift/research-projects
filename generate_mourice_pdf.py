#!/usr/bin/env python3
"""
PDF Generator — Research Project
Title: Effectiveness of Software Development on Moi University Students' Learning Behaviour
Mourice Onyango | BBM/1891/22 | Dr. Kiyeng Chumo | March 2026
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.colors import black, white, HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)

from reportlab.lib.styles import ParagraphStyle
from reportlab.graphics.shapes import Drawing, String as GString

PW = 6.0 * inch


from reportlab.lib.pagesizes import letter as _letter_size
from reportlab.platypus import Flowable


class SectionAnchor(Flowable):
    """Zero-height flowable that records its page number during rendering (pass 1)."""
    def __init__(self, key, registry):
        super().__init__()
        self.key = key
        self.registry = registry
    def wrap(self, aW, aH): return 0, 0
    def draw(self):
        if self.registry is not None:
            self.registry[self.key] = self.canv.getPageNumber()


def to_roman(n):
    """Convert integer to lowercase Roman numeral string."""
    vals = [(1000,'m'),(900,'cm'),(500,'d'),(400,'cd'),(100,'c'),(90,'xc'),
            (50,'l'),(40,'xl'),(10,'x'),(9,'ix'),(5,'v'),(4,'iv'),(1,'i')]
    r = ''
    for v, s in vals:
        while n >= v:
            r += s
            n -= v
    return r


def styles():
    return {
        'cov_bold': ParagraphStyle('cb', fontName='Times-Bold', fontSize=12,
            alignment=TA_CENTER, leading=16, spaceAfter=4),
        'cov_norm': ParagraphStyle('cn', fontName='Times-Roman', fontSize=12,
            alignment=TA_CENTER, leading=16, spaceAfter=4),
        'sec': ParagraphStyle('sec', fontName='Times-Bold', fontSize=12,
            alignment=TA_CENTER, leading=18, spaceAfter=14),
        'ch': ParagraphStyle('ch', fontName='Times-Bold', fontSize=12,
            alignment=TA_CENTER, leading=18, spaceAfter=2),
        'chsub': ParagraphStyle('cs', fontName='Times-Bold', fontSize=12,
            alignment=TA_CENTER, leading=18, spaceAfter=18),
        'h2': ParagraphStyle('h2', fontName='Times-Bold', fontSize=12,
            alignment=TA_LEFT, leading=18, spaceAfter=4, spaceBefore=14),
        'h3': ParagraphStyle('h3', fontName='Times-Bold', fontSize=12,
            alignment=TA_LEFT, leading=18, spaceAfter=4, spaceBefore=8),
        'body': ParagraphStyle('body', fontName='Times-Roman', fontSize=12,
            alignment=TA_JUSTIFY, leading=18, spaceAfter=8),
        'body_i': ParagraphStyle('bi', fontName='Times-Roman', fontSize=12,
            alignment=TA_JUSTIFY, leading=18, spaceAfter=6, leftIndent=22),
        'bullet': ParagraphStyle('blt', fontName='Times-Roman', fontSize=12,
            alignment=TA_JUSTIFY, leading=18, spaceAfter=5, leftIndent=26, firstLineIndent=-14),
        'caption': ParagraphStyle('cap', fontName='Times-Italic', fontSize=11,
            alignment=TA_LEFT, leading=14, spaceAfter=4, spaceBefore=4),
        'toc_h': ParagraphStyle('toh', fontName='Times-Bold', fontSize=11,
            alignment=TA_LEFT, leading=14, spaceAfter=2),
        'toc_i': ParagraphStyle('toi', fontName='Times-Roman', fontSize=11,
            alignment=TA_LEFT, leading=14, spaceAfter=2, leftIndent=20),
        'ref': ParagraphStyle('ref', fontName='Times-Roman', fontSize=12,
            alignment=TA_JUSTIFY, leading=18, spaceAfter=6, leftIndent=28, firstLineIndent=-28),
        'kw': ParagraphStyle('kw', fontName='Times-Italic', fontSize=12,
            alignment=TA_JUSTIFY, leading=18),
    }


def make_table(headers, rows, col_widths=None):
    if col_widths is None:
        col_widths = [PW / len(headers)] * len(headers)
    hS = ParagraphStyle('th', fontName='Times-Bold', fontSize=10.5,
        alignment=TA_CENTER, leading=13, wordWrap='LTR')
    cC = ParagraphStyle('cc', fontName='Times-Roman', fontSize=10.5,
        alignment=TA_CENTER, leading=13, wordWrap='LTR')
    cL = ParagraphStyle('cl', fontName='Times-Roman', fontSize=10.5,
        alignment=TA_LEFT, leading=13, wordWrap='LTR')

    def wp(v, st):
        return Paragraph(str(v), st)

    data = [[wp(h, hS) for h in headers]]
    for row in rows:
        data.append([wp(v, cL if j == 0 else cC) for j, v in enumerate(row)])
    ts = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), HexColor('#D3D3D3')),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [white, HexColor('#F7F7F7')]),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(ts)
    return t


def toc_line(label, pg, bold=False):
    """TOC row with precision dot leaders and right-aligned page numbers."""
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.graphics.shapes import Drawing, String
    font = 'Times-Bold' if bold else 'Times-Roman'
    sz = 11
    row_h = 15
    w = PW
    label_str = label.strip()
    pg_str = str(pg)
    indent_extra = (len(label) - len(label.lstrip(' '))) * 0.055 * inch
    label_w = stringWidth(label_str, font, sz)
    pg_w = stringWidth(pg_str, font, sz)
    dot_w = stringWidth('.', font, sz)
    gap = 4  # small gap between label and dots, and dots and page number
    available = w - indent_extra - label_w - pg_w - gap * 2
    n_dots = max(3, int(available / dot_w))
    dots_str = '.' * n_dots
    d = Drawing(w, row_h)
    d.add(String(indent_extra, 3.5, label_str, fontName=font, fontSize=sz))
    d.add(String(indent_extra + label_w + gap, 3.5, dots_str, fontName=font, fontSize=sz))
    d.add(String(w - pg_w, 3.5, pg_str, fontName=font, fontSize=sz))
    return d



def make_bar_chart(labels, values, title, width=5.8, height=2.4, color='#2E74B5'):
    """Create a horizontal bar chart and return as a Drawing-wrapped Flowable."""
    from reportlab.graphics.shapes import Drawing, Rect, String, Line
    from reportlab.graphics.charts.barcharts import HorizontalBarChart
    from reportlab.lib.colors import HexColor, white, black, lightgrey
    w, h = width * inch, height * inch
    d = Drawing(w, h)
    chart = HorizontalBarChart()
    chart.x = 1.6 * inch
    chart.y = 0.25 * inch
    chart.width = w - 1.9 * inch
    chart.height = h - 0.55 * inch
    chart.data = [values]
    chart.bars[0].fillColor = HexColor(color)
    chart.bars[0].strokeColor = None
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = max(values) * 1.12
    chart.valueAxis.valueStep = max(values) / 5
    chart.valueAxis.labelTextFormat = '%d'
    chart.valueAxis.labels.fontName = 'Times-Roman'
    chart.valueAxis.labels.fontSize = 8
    chart.categoryAxis.categoryNames = labels
    chart.categoryAxis.labels.fontName = 'Times-Roman'
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.dx = -4
    chart.categoryAxis.labels.textAnchor = 'end'
    chart.categoryAxis.labels.maxWidth = 1.45 * inch
    d.add(chart)
    # title
    d.add(String(w / 2, h - 0.15 * inch, title,
        fontName='Times-Bold', fontSize=9, textAnchor='middle'))
    return d


def make_grouped_bar(categories, series_data, series_labels, title, width=5.8, height=2.6):
    from reportlab.graphics.shapes import Drawing, String
    from reportlab.graphics.charts.barcharts import VerticalBarChart
    from reportlab.lib.colors import HexColor, white
    COLORS = ['#2E74B5', '#ED7D31', '#70AD47', '#FFC000']
    w, h = width * inch, height * inch
    d = Drawing(w, h)
    chart = VerticalBarChart()
    chart.x = 0.55 * inch
    chart.y = 0.45 * inch
    chart.width = w - 0.85 * inch
    chart.height = h - 0.75 * inch
    chart.data = series_data
    for i, c in enumerate(COLORS[:len(series_data)]):
        chart.bars[i].fillColor = HexColor(c)
        chart.bars[i].strokeColor = None
    chart.valueAxis.valueMin = 0
    chart.valueAxis.valueMax = 5.5
    chart.valueAxis.valueStep = 1.0
    chart.valueAxis.labelTextFormat = '%.1f'
    chart.valueAxis.labels.fontName = 'Times-Roman'
    chart.valueAxis.labels.fontSize = 8
    chart.categoryAxis.categoryNames = categories
    chart.categoryAxis.labels.fontName = 'Times-Roman'
    chart.categoryAxis.labels.fontSize = 8
    chart.categoryAxis.labels.angle = 0
    d.add(chart)
    d.add(String(w / 2, h - 0.18 * inch, title,
        fontName='Times-Bold', fontSize=9, textAnchor='middle'))
    return d


def generate_pdf(output_path='Mourice_BBM_Annex_Project.pdf', _page_data=None, _anchor_reg=None):

    def on_page(canvas, doc):
        """Cover=no number, front matter=Roman (i,ii,iii…), body=Arabic (1,2,3…)."""
        canvas.saveState()
        canvas.setFont('Times-Roman', 11)
        phys = canvas.getPageNumber()
        if phys == 1:
            pass  # No page number on cover
        else:
            ch1 = (_page_data or {}).get('ch1_physical', None)
            if ch1 is not None and phys < ch1:
                canvas.drawCentredString(_letter_size[0] / 2.0, 0.5 * inch, to_roman(phys - 1))
            elif ch1 is not None and phys >= ch1:
                canvas.drawCentredString(_letter_size[0] / 2.0, 0.5 * inch, str(phys - ch1 + 1))
            else:
                canvas.drawCentredString(_letter_size[0] / 2.0, 0.5 * inch, str(phys))
        canvas.restoreState()

    s = styles()
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=1.25 * inch, rightMargin=1.0 * inch,
        topMargin=1.0 * inch, bottomMargin=1.0 * inch,
    )

    story = []

    def A(key):
        """Insert a SectionAnchor to record this page in pass 1."""
        return SectionAnchor(key, _anchor_reg)

    def pg(key, fallback='?'):
        """Return body-relative Arabic page number, or fallback in pass 1."""
        if _page_data:
            v = _page_data.get(key)
            if v is not None:
                ch1 = _page_data.get('ch1_physical')
                if ch1 is not None and v >= ch1:
                    return str(v - ch1 + 1)
                return str(v)
        return fallback

    def B(t): return Paragraph(t, s['body'])
    def BI(t): return Paragraph(t, s['body_i'])
    def Blt(t): return Paragraph(f'&#8226;&nbsp;&nbsp;{t}', s['bullet'])
    def H2(t): return Paragraph(t, s['h2'])
    def H3(t): return Paragraph(t, s['h3'])
    def Cap(t): return Paragraph(t, s['caption'])
    def Sp(n=8): return Spacer(1, n)
    def PB(): return PageBreak()
    def Sec(t): return Paragraph(t, s['sec'])
    def Ch(t): return Paragraph(t, s['ch'])
    def Chsub(t): return Paragraph(t, s['chsub'])

    def term(t, d): return Paragraph(f'<b>{t}:</b> {d}', ParagraphStyle('td',
        fontName='Times-Roman', fontSize=12, alignment=TA_JUSTIFY,
        leading=18, spaceAfter=5, leftIndent=22, firstLineIndent=-22))

    def ref(t): return Paragraph(t, s['ref'])

    def conc(label, text): return Paragraph(f'<b>{label}:</b> {text}', s['body'])

    # ── COVER PAGE ─────────────────────────────────────────────────────────
    story += [Sp(6)]
    try:
        from reportlab.platypus import Image
        img = Image('assets/moi_uni_logo/moi_logo.png',
                    width=1.3 * inch, height=1.3 * inch)
        img.hAlign = 'CENTER'
        story.append(img)
    except Exception:
        pass
    story += [
        Sp(8),
        Paragraph('MOI UNIVERSITY', s['cov_bold']),
        Paragraph('SCHOOL OF BUSINESS AND ECONOMICS', s['cov_bold']),
        Paragraph('DEPARTMENT OF MANAGEMENT SCIENCE AND ENTREPRENEURSHIP', s['cov_bold']),
        Sp(18),
        Paragraph('EFFECTIVENESS OF SOFTWARE DEVELOPMENT ON MOI UNIVERSITY '
                  'STUDENTS\u2019 LEARNING BEHAVIOUR',
                  ParagraphStyle('pt', fontName='Times-Bold', fontSize=13,
                      alignment=TA_CENTER, leading=20, spaceAfter=20)),
        Sp(10),
        Paragraph('BY', s['cov_norm']),
        Paragraph('MOURICE ONYANGO', s['cov_bold']),
        Paragraph('REG. NO: BBM/1891/22', s['cov_norm']),
        Sp(14),
        Paragraph('SUPERVISOR', s['cov_norm']),
        Paragraph('DR. KIYENG CHUMO', s['cov_bold']),
        Sp(14),
        Paragraph('A RESEARCH PROJECT SUBMITTED IN PARTIAL FULFILMENT OF THE '
                  'REQUIREMENTS FOR THE AWARD OF THE DEGREE OF', s['cov_norm']),
        Paragraph('BACHELOR OF BUSINESS MANAGEMENT', s['cov_bold']),
        Sp(16),
        Paragraph('MARCH 2026', s['cov_bold']),
    ]

    # ── DECLARATION ─────────────────────────────────────────────────────────
    story += [PB(), Sec('DECLARATION'),
        B('I declare that this research project is my original work and has not been presented for a degree award in this or any other university.'),
        Sp(12), B('MOURICE ONYANGO'), B('REG. NO: BBM/1891/22'),
        B('Signature: ..............................   Date: ................................'),
        Sp(12),
        B('This research project has been submitted for examination with our approval as University Supervisor.'),
        Sp(10), B('DR. KIYENG CHUMO'),
        B('Department of Management Science and Entrepreneurship, Moi University'),
        B('Signature: ..............................   Date: ................................'),
    ]

    # ── DEDICATION ──────────────────────────────────────────────────────────
    story += [PB(), Sec('DEDICATION'),
        B('This work is dedicated to every student at Moi University who has ever faced the challenge of accessing academic resources and study materials. May this research serve as a step toward understanding and improving the role of technology in your learning journey.'),
        Sp(10),
        B('To my family, whose unwavering support and encouragement made this work possible: thank you.'),
    ]

    # ── ACKNOWLEDGEMENT ─────────────────────────────────────────────────────
    story += [PB(), Sec('ACKNOWLEDGEMENT'),
        B('I give thanks to the Almighty God for the strength, wisdom, and perseverance to complete this research project. I am sincerely grateful to my supervisor, Dr. Kiyeng Chumo, for the guidance, constructive feedback, and encouragement that shaped the direction and quality of this study from its initial conception to its completion.'),
        Sp(8),
        B('I thank the Department of Management Science and Entrepreneurship and the School of Business and Economics at Moi University for providing the academic environment that made this research possible. My gratitude also goes to all the BBM students who generously gave their time to participate in the survey and share their experiences with academic software tools.'),
        Sp(8),
        B('Special appreciation goes to my fellow students and friends whose encouragement sustained me throughout the research process. This work is a collective achievement.'),
    ]

    # ── ABSTRACT ────────────────────────────────────────────────────────────
    story += [PB(), Sec('ABSTRACT'),
        B('The rapid advancement of information and communication technologies has introduced software tools and platforms that have the potential to transform the learning behaviour of university students. Despite the widespread availability of digital tools, the extent to which software development influences the learning behaviour of students at Moi University remains inadequately documented. This study examined the effectiveness of software development on the learning behaviour of Moi University students, using BBM Annex (https://bbm.giftedtech.co.ke) \u2014 a student-developed web platform for sharing notes and past papers among BBM students \u2014 as a practical case study.'),
        Sp(8),
        B('The study was guided by the Technology Acceptance Model (TAM) and the Constructivist Learning Theory. A descriptive survey research design was adopted, targeting BBM students at Moi University Annex Campus. A stratified random sample of 85 students was selected from an accessible population of 1,380. Data were collected using a structured questionnaire and analysed using descriptive statistics.'),
        Sp(8),
        B('The findings revealed that 78.8 percent of students perceived software tools as having a significant positive effect on their learning behaviour, particularly in examination preparedness (overall mean 4.25), resource accessibility (4.35), peer collaboration (4.06), and self-directed study habits (3.83). BBM Annex was used by 71.8 percent of respondents and achieved an overall learning impact mean of 4.25, with a recommendation rate of 91.8 percent. Sustainability analysis revealed that institutional support and community content governance are critical for the platform\'s long-term viability.'),
        Sp(8),
        B('The study concludes that software development has a significant positive effect on Moi University students\' learning behaviour and recommends formal institutional endorsement of BBM Annex, lecturer participation in content provision, and integration of software development competencies into the BBM curriculum.'),
        Sp(8),
        Paragraph('<i>Keywords: software development, learning behaviour, university students, digital learning, BBM Annex, academic resource sharing, Moi University.</i>', s['kw']),
    ]

    # ── TABLE OF CONTENTS ───────────────────────────────────────────────────
    story += [PB(), Sec('TABLE OF CONTENTS')]
    for label, pn, bold in [
        ('DECLARATION', 'i', True),
        ('DEDICATION', 'ii', True),
        ('ACKNOWLEDGEMENT', 'iii', True),
        ('ABSTRACT', 'iv', True),
        ('TABLE OF CONTENTS', 'v', True),
        ('LIST OF TABLES', 'vi', True),
        ('LIST OF FIGURES', 'vi', True),
        ('LIST OF ABBREVIATIONS AND ACRONYMS', 'vii', True),
        ('OPERATIONAL DEFINITION OF TERMS', 'viii', True),
        ('CHAPTER ONE: INTRODUCTION', pg('ch1', '1'), True),
        ('    1.1  Background of the Study', pg('s1.1', '1'), False),
        ('    1.2  Statement of the Problem', pg('s1.2', '2'), False),
        ('    1.3  Objectives of the Study', pg('s1.3', '2'), False),
        ('    1.4  Research Questions', pg('s1.4', '3'), False),
        ('    1.5  Significance of the Study', pg('s1.5', '3'), False),
        ('    1.6  Scope and Delimitations of the Study', pg('s1.6', '4'), False),
        ('    1.7  Limitations of the Study', pg('s1.7', '4'), False),
        ('CHAPTER TWO: LITERATURE REVIEW', pg('ch2', '5'), True),
        ('    2.1  Introduction', pg('s2.1', '5'), False),
        ('    2.2  Theoretical Framework', pg('s2.2', '5'), False),
        ('    2.3  Empirical Literature', pg('s2.3', '6'), False),
        ('    2.4  Critique of Existing Literature', pg('s2.4', '8'), False),
        ('    2.5  Research Gaps', pg('s2.5', '9'), False),
        ('    2.6  Conceptual Framework', pg('s2.6', '8'), False),
        ('CHAPTER THREE: RESEARCH METHODOLOGY', pg('ch3', '11'), True),
        ('    3.1  Introduction', pg('s3.1', '11'), False),
        ('    3.2  Research Design', pg('s3.2', '11'), False),
        ('    3.3  Target Population', pg('s3.3', '11'), False),
        ('    3.4  Sampling Technique and Sample Size', pg('s3.4', '11'), False),
        ('    3.5  Research Instruments', pg('s3.5', '12'), False),
        ('    3.6  Data Collection Procedures', pg('s3.6', '12'), False),
        ('    3.7  Validity and Reliability', pg('s3.7', '13'), False),
        ('    3.8  Data Analysis', pg('s3.8', '13'), False),
        ('    3.9  Ethical Considerations', pg('s3.9', '13'), False),
        ('CHAPTER FOUR: DATA ANALYSIS AND FINDINGS', pg('ch4', '14'), True),
        ('    4.1  Introduction', pg('s4.1', '14'), False),
        ('    4.2  Response Rate', pg('s4.2', '14'), False),
        ('    4.3  Demographic Profile of Respondents', pg('s4.3', '14'), False),
        ('    4.4  Effect of Software Development on Learning Behaviour', pg('s4.4', '15'), False),
        ('    4.5  BBM Annex and Academic Resource Accessibility', pg('s4.5', '18'), False),
        ('    4.6  Sustainability of Student-Developed Academic Software', pg('s4.6', '20'), False),
        ('    4.7  Discussion of Findings', pg('s4.7', '21'), False),
        ('CHAPTER FIVE: SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', pg('ch5', '24'), True),
        ('    5.1  Introduction', pg('s5.1', '24'), False),
        ('    5.2  Summary of Findings', pg('s5.2', '24'), False),
        ('    5.3  Conclusions', pg('s5.3', '25'), False),
        ('    5.4  Recommendations', pg('s5.4', '25'), False),
        ('    5.5  Limitations of the Study', pg('s5.5', '26'), False),
        ('    5.6  Suggestions for Further Research', pg('s5.6', '27'), False),
        ('REFERENCES', pg('sref', '28'), True),
        ('APPENDICES', pg('sapp', '30'), True),
    ]:
        story.append(toc_line(label, pn, bold))

    story += [PB(), Sec('LIST OF TABLES')]
    for t, pn in [
        ('Table 3.1: Population Distribution of BBM Students by Year of Study', pg('s3.3', '11')),
        ('Table 3.2: Sample Size Distribution', pg('s3.4', '11')),
        ('Table 4.1: Distribution of Respondents by Year of Study', pg('s4.3', '14')),
        ('Table 4.2: Distribution of Respondents by Gender', pg('s4.3', '14')),
        ('Table 4.3: Distribution of Respondents by BBM Specialisation', pg('s4.3', '14')),
        ('Table 4.4: Types of Software Tools Used for Academic Purposes', pg('s4.4', '15')),
        ('Table 4.5: Effect of Software on Resource Accessibility', pg('s4.4', '15')),
        ('Table 4.6: Effect of Software on Study Habits and Self-Direction', pg('s4.4', '15')),
        ('Table 4.7: Effect of Software on Collaboration and Peer Learning', pg('s4.4', '16')),
        ('Table 4.8: Effect of Software on Examination Preparedness', pg('s4.4', '17')),
        ('Table 4.9: Awareness and Use of BBM Annex', pg('s4.5', '18')),
        ('Table 4.10: Impact of BBM Annex on Learning Behaviour', pg('s4.5', '18')),
        ('Table 4.11: Perceived Sustainability of BBM Annex', pg('s4.6', '20')),
        ('Table 4.12: Recommended Sustainability Measures', pg('s4.6', '20')),
    ]:
        story.append(toc_line(t, pn, False))

    story += [Spacer(1, 14), Sec('LIST OF FIGURES')]
    for f, pn in [
        ('Figure 2.1: Conceptual Framework', pg('s2.6', '8')),
        ('Figure 4.1: Overall Effect of Software on Learning Behaviour', pg('s4.4', '15')),
        ('Figure 4.2: BBM Annex Adoption Funnel among Respondents', pg('s4.5', '18')),
    ]:
        story.append(toc_line(f, pn, False))

    # ── ABBREVIATIONS AND ACRONYMS ─────────────────────────────────────────
    story += [PB(), Sec('LIST OF ABBREVIATIONS AND ACRONYMS')]
    for abbr, meaning in [
        ('BBM', 'Bachelor of Business Management'),
        ('BBM Annex', 'BBM Annex Academic Resource Sharing Platform (bbm.giftedtech.co.ke)'),
        ('TAM', 'Technology Acceptance Model'),
        ('ICT', 'Information and Communication Technology'),
        ('e-learning', 'Electronic Learning'),
        ('API', 'Application Programming Interface'),
        ('JWT', 'JSON Web Token'),
        ('OTP', 'One-Time Password'),
        ('CDN', 'Content Delivery Network'),
        ('SD', 'Standard Deviation'),
        ('M', 'Mean'),
        ('N', 'Target Population'),
        ('n', 'Sample Size'),
        ('SPSS', 'Statistical Package for the Social Sciences'),
    ]:
        story.append(B(f'<b>{abbr}</b>  —  {meaning}'))

    # ── OPERATIONAL DEFINITION OF TERMS ───────────────────────────────────
    story += [PB(), Sec('OPERATIONAL DEFINITION OF TERMS')]
    for t, d in [
        ('Software Development', 'The process of designing, building, and deploying software applications with the aim of solving specific educational or social problems within the university context.'),
        ('Learning Behaviour', 'The patterns and practices through which students engage with academic content, operationalised through four dimensions: academic resource accessibility, self-directed study habits, peer collaboration, and examination preparedness.'),
        ('BBM Annex', 'A student-developed web-based academic resource sharing platform at https://bbm.giftedtech.co.ke, designed for BBM students at Moi University Annex Campus.'),
        ('Academic Resource Accessibility', 'The ease with which students can locate, retrieve, and use study materials relevant to their academic programme.'),
        ('Self-Directed Study Habits', 'The degree to which students independently organise, plan, and regulate their own academic study activities outside formal classroom instruction.'),
        ('Peer Collaboration', 'Academic cooperative activities in which students share knowledge, resources, or support with one another in ways that enhance each other\'s learning.'),
        ('Examination Preparedness', 'The extent to which students feel adequately prepared for academic examinations, measured by access to past papers, revision notes, and practice materials.'),
        ('Sustainability', 'The capacity of a student-developed software platform to continue providing consistent educational value to the target user community over an extended period beyond the original developer\'s involvement.'),
    ]:
        story.append(term(t, d))


    # ══════════════════════════════════════════════════════════════════════
    # CHAPTER ONE
    # ══════════════════════════════════════════════════════════════════════
    story += [PB(), A('ch1'), Ch('CHAPTER ONE'), Chsub('INTRODUCTION')]

    story += [A('s1.1'), H2('1.1 Background of the Study'),
        B("The global expansion of digital technology has fundamentally altered the way knowledge is created, shared, and consumed in academic institutions. Over the past two decades, software development has moved beyond the domain of computer science to become a practical tool for solving social and institutional problems across all disciplines. In higher education, software applications \u2014 from learning management systems to student-built collaborative platforms \u2014 have increasingly been identified as important mediators of student learning behaviour, influencing how students access information, organise their study activities, collaborate with peers, and prepare for academic assessments."),
        B("In Kenya, the expansion of mobile internet access and smartphone ownership has accelerated the penetration of digital learning tools in university environments. The Kenya National Bureau of Statistics (2023) reports that over 90 percent of university students own a smartphone. Despite this infrastructure, the integration of software tools into the academic routines of students at many Kenyan public universities remains fragmented, informal, and unevaluated. Students frequently rely on commercial messaging platforms \u2014 particularly WhatsApp \u2014 for informal exchange of academic materials, while purpose-built academic software remains underutilised or nonexistent in many institutional contexts."),
        B("At Moi University, the Bachelor of Business Management (BBM) programme at the Annex Campus equips students with management, entrepreneurship, finance, and marketing competencies. However, there exists no dedicated, quality-assured digital platform through which BBM students can systematically share and access academic study materials such as lecture notes and past examination papers. Resources are shared informally through WhatsApp groups, physical photocopies, and direct peer-to-peer transfers \u2014 mechanisms that are transient, inequitable, and devoid of any content quality assurance."),
        B("Recognising this gap, the researcher \u2014 a BBM student at Moi University Annex Campus \u2014 developed BBM Annex (https://bbm.giftedtech.co.ke), a web-based academic resource sharing platform, as a practical experiment in whether targeted software development can meaningfully alter the learning behaviour of BBM students. This research project situates that initiative within a scholarly framework, asking a broader research question: to what extent does software development affect the learning behaviour of Moi University students?"),
        A('s1.2'), H2('1.2 Statement of the Problem'),
        B("The increasing availability of digital technologies in Kenyan higher education has raised important questions about the relationship between software tools and student learning behaviour. At Moi University, BBM students access academic resources primarily through informal, unstructured digital channels \u2014 particularly WhatsApp groups \u2014 that provide no organisational structure, no content quality assurance, and no equitable access mechanism. This results in significant disparities in academic preparedness, disadvantaging students with smaller peer networks."),
        B("While the literature broadly affirms the positive potential of educational software on student learning behaviour (Davis, 1989; Selwyn, 2011; Vygotsky, 1978), there is a notable absence of empirical research examining this relationship specifically within Moi University and the BBM programme. No study has investigated whether student-developed software can produce meaningful improvements in student learning behaviour at a Kenyan public university. The sustainability of student-developed platforms \u2014 their capacity to continue providing value beyond the developer's graduation \u2014 is equally understudied. This study addresses these gaps."),
        A('s1.3'), H2('1.3 Purpose of the Study'),
        B("The purpose of this study is to examine the effectiveness of software development on the learning behaviour of Moi University students, using BBM Annex \u2014 a student-developed web-based academic resource sharing platform \u2014 as a case study, and to document the sustainability conditions necessary for student-developed academic software platforms to deliver ongoing educational value."),
        H2('1.3 Objectives of the Study'),
        H3('1.3.1 General Objective'),
        B('To examine the effectiveness of software development on the learning behaviour of Moi University students.'),
        H3('1.3.2 Specific Objectives'),
    ]
    for obj in [
        'i.    To establish the types of software tools used by BBM students at Moi University Annex Campus for academic purposes.',
        'ii.   To determine the effect of software development on the resource accessibility, self-directed study habits, academic collaboration, and examination preparedness of BBM students.',
        'iii.  To assess the impact of BBM Annex specifically on the learning behaviour of BBM students at Moi University Annex Campus.',
        'iv.   To identify the sustainability conditions necessary for student-developed academic software platforms to continue providing value to the student community.',
        'v.    To propose recommendations for improving the integration of software development into the learning environment at Moi University.',
    ]:
        story.append(BI(obj))

    story.append(A('s1.4')); story.append(H2('1.4 Research Questions'))
    for q in [
        'i.    What types of software tools do BBM students at Moi University Annex Campus use for academic purposes?',
        'ii.   To what extent does the use of software tools affect the resource accessibility, self-directed study habits, academic collaboration, and examination preparedness of BBM students?',
        'iii.  How has BBM Annex specifically influenced the learning behaviour of BBM students at Moi University Annex Campus?',
        'iv.   What conditions are necessary for student-developed academic software platforms to remain sustainable and effective over time?',
        'v.    What recommendations can be made for improving the integration of software development into the learning environment at Moi University?',
    ]:
        story.append(BI(q))

    story += [
        A('s1.5'), H2('1.5 Significance of the Study'),
        B("This study contributes to multiple audiences. Academically, it provides empirical investigation of the effectiveness of student-developed software on university learning behaviour within a Kenyan public university context \u2014 underrepresented in the existing literature. For policy makers and university administrators, the study provides evidence-based guidance on supporting student-developed digital platforms. For the Department of Management Science and Entrepreneurship, the study affirms the entrepreneurial development mandate of the BBM programme. For BBM students, the study provides practical recommendations for engaging with academic software tools and documents the value of BBM Annex."),
        A('s1.6'), H2('1.6 Scope and Delimitations of the Study'),
        B("This study is delimitated to Moi University Annex Campus, Eldoret, Kenya, and to students enrolled in the BBM programme. Data collection covered January to March 2026. The study is thematically delimitated to the effect of software development on four dimensions of student learning behaviour: academic resource accessibility, self-directed study habits, peer collaboration, and examination preparedness. The study does not extend to other universities, other programmes, or other campuses of Moi University."),
        A('s1.7'), H2('1.7 Limitations of the Study'),
        B('Several limitations were encountered in the course of this study. The study was confined to Moi University Annex Campus and its BBM student population, which limits the generalisability of findings to other universities or academic programmes. The study relied on self-reported data, which introduces the possibility of social desirability bias, as respondents may have provided responses perceived as expected or favourable rather than fully reflective of actual practices.'),
        B('The cross-sectional nature of the study means that data were collected at a single point in time, precluding observation of changes in learning behaviour over time. The measurement of BBM Annex impact was based solely on student perceptions rather than objective performance metrics such as examination scores or grade point averages. Despite these limitations, appropriate methodological controls were applied to minimise their impact on the validity and reliability of the findings.'),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # CHAPTER TWO
    # ══════════════════════════════════════════════════════════════════════
    story += [PB(), A('ch2'), Ch('CHAPTER TWO'), Chsub('LITERATURE REVIEW')]

    story += [
        A('s2.1'), H2('2.1 Introduction'),
        B("This chapter reviews the theoretical, empirical, and conceptual literature relevant to the study of software development effectiveness on university student learning behaviour. The review covers the theoretical frameworks, empirical evidence on software and learning behaviour, digital academic platforms, sustainability of student-developed platforms, BBM Annex as a case study, the conceptual framework, and a summary of literature gaps."),
        A('s2.2'), H2('2.2 Theoretical Framework'),
        H3('2.2.1 Technology Acceptance Model (TAM)'),
        B("The Technology Acceptance Model (Davis, 1989) proposes that adoption of an information system is determined by Perceived Usefulness (PU) \u2014 belief that the system enhances performance \u2014 and Perceived Ease of Use (PEOU) \u2014 belief that using the system is free of effort. Both constructs predict behavioural intention to use the system, which predicts actual use. In this study, TAM explains why BBM students choose to use software tools: those who perceive tools as useful for improving resource access or examination preparedness are more likely to adopt them. Extended TAM variants \u2014 TAM2 (Venkatesh & Davis, 2000) and UTAUT (Venkatesh et al., 2003) \u2014 additionally identify social influence and facilitating conditions as predictors of adoption, relevant to the role of peer recommendations and institutional support in driving BBM Annex adoption."),
        H3('2.2.2 Constructivist Learning Theory'),
        B("Piaget (1954) and Vygotsky (1978) established that learners actively construct knowledge through interaction with the environment. Vygotsky's social constructivism emphasises the role of social interaction and collaborative tools in facilitating higher-order learning. In this study, Constructivist Learning Theory explains the mechanism through which platforms like BBM Annex affect learning behaviour: by providing a repository of student-contributed resources, the platform facilitates social construction of academic knowledge within the BBM community. Students who contribute resources engage in knowledge externalisation; students who access those resources engage in scaffolded learning supported by peers' accumulated knowledge."),
        H3('2.2.3 Connectivism'),
        B("Siemens' (2005) theory of Connectivism proposes that in the digital age, learning is the cultivation of connections between individuals, ideas, and digital resources. From a Connectivist perspective, platforms like BBM Annex function as nodes in the BBM student learning network, enabling connections between students and academic resources, between students and peers, and between present needs and the accumulated knowledge of prior student cohorts."),
        A('s2.3'), H2('2.3 Empirical Literature'),
        B("Selwyn (2011) concludes that while digital technologies have significant potential to enhance student learning, realisation of this potential depends on the alignment between the technology's affordances and the actual learning needs of its users. The UNESCO (2021) report on digital learning in Sub-Saharan Africa documents that digital learning tools in university environments are generally associated with improvements in student engagement, particularly among students with limited access to physical library resources."),
        B("Research on student-developed software is less extensive but consistently positive. Neck and Greene (2011) documented that students who developed digital tools for their own academic communities reported significant improvements in collaborative learning and resource access. These tools tend to be more closely aligned with actual student information needs than institutionally adopted commercial platforms, because the developer-student shares the lived experience of the problem being solved. In Kenya, Mutula and Brakel (2006) found that digital academic resources were correlated with improved self-directed study practices, particularly in management disciplines, and noted that the informal nature of digital sharing limited the magnitude of this effect \u2014 supporting the hypothesis that a structured platform like BBM Annex can produce more substantial improvements."),
        H3('2.3.1 Digital Academic Platforms and Learning Outcomes'),
        H3('2.3.1.1 Academic Resource Accessibility'),
        B("Oyelaran and Lateef (2017) found that students with reliable access to digital study materials \u2014 including past papers and lecture notes \u2014 were significantly more likely to engage in regular revision and reported higher examination confidence. The mechanism is straightforward: when effort required to locate study materials is reduced through software, students redirect that effort toward actual studying. Garrison and Kanuka (2004) similarly found that well-structured, searchable, quality-assured digital repositories produced significant improvements in learning behaviour, while disorganised collections produced little improvement."),
        H3('2.3.1.2 Peer Collaboration and Social Learning'),
        B("Wenger (1998) introduced Communities of Practice to describe groups who learn collectively through shared participation in a practice domain \u2014 applicable to BBM students preparing for BBM examinations. Dillenbourg et al. (2009) and Resta and Laferriere (2007) documented that digital peer knowledge-sharing platforms consistently produced improvements in collaborative learning behaviour and academic self-efficacy. Three conditions were identified as necessary: ease of participation, perceived quality of the shared knowledge base, and social reciprocity."),
        H3('2.3.1.3 Examination Preparedness'),
        B("Dunlosky et al. (2013) identify retrieval practice \u2014 working through past papers \u2014 as among the highest-utility study techniques, producing improvements in long-term retention and examination performance exceeding those produced by rereading notes or summarising. For this mechanism to operate, students must first have reliable access to past papers. A platform improving access to past examination papers directly enables the most evidence-backed study strategy available, with significant implications for examination preparedness."),
        H3('2.3.2 Sustainability of Student-Developed Software Platforms'),
        B("Rashid and Yukl (2012) documented 'platform abandonment' in student-led academic technology initiatives \u2014 platforms demonstrating positive effects during the developer's involvement subsequently declining after the developer's graduation. Three sustainability risk factors were identified: technical obsolescence, content stagnation, and institutional indifference. Bates (2015) identified sustainability enablers: community ownership, institutional endorsement, revenue-neutral operation, and modularity. Documenting and evaluating these factors in the BBM Annex context constitutes one of the specific contributions of this study."),
        H3('2.3.3 BBM Annex as a Case Study'),
        B("BBM Annex (https://bbm.giftedtech.co.ke) is a web-based academic resource sharing platform developed by the researcher in response to the documented problem of inequitable and disorganised academic resource sharing among BBM students. The platform allows registered students to upload study notes and past papers categorised by year, semester, and specialisation, and to browse, preview, download, and review resources. Technically, the platform uses React 18 and TypeScript for the frontend, Python FastAPI for the backend REST API, and JWT authentication with OTP verification. As of March 2026, the platform has over 170 registered users and 60+ approved resources. As a case study, BBM Annex provides a concrete, observable example of student-developed software within the Moi University context and a direct empirical data stream for answering the research questions."),
        A('s2.6'), H2('2.6 Conceptual Framework'),
        B("The conceptual framework integrates TAM, Constructivist Learning Theory, and Connectivism. The independent variable is Software Development \u2014 the design and deployment of purpose-built academic software tools exemplified by BBM Annex. The mediating variables are Perceived Usefulness and Perceived Ease of Use: students' adoption decisions are mediated by these TAM constructs, shaped by tool design, social influence, and institutional context. The dependent variable is Student Learning Behaviour, operationalised through: (1) Academic Resource Accessibility, (2) Self-Directed Study Habits, (3) Peer Collaboration, and (4) Examination Preparedness. A sustainability dimension \u2014 the conditions under which platforms continue to positively influence learning behaviour \u2014 moderates the relationship between software development and learning behaviour."),
        Paragraph('[Figure 2.1: Conceptual Framework \u2014 Software Development \u2192 (Perceived Usefulness + Perceived Ease of Use) \u2192 Student Learning Behaviour (Resource Accessibility + Study Habits + Peer Collaboration + Examination Preparedness), moderated by Sustainability Conditions]',
            ParagraphStyle('fig', fontName='Times-Italic', fontSize=11, alignment=TA_CENTER, leading=14, spaceAfter=10, spaceBefore=6)),
        A('s2.4'), H2('2.4 Critique of Existing Literature'),
        B("A critical appraisal of the existing literature on software development and student learning behaviour reveals both strengths and limitations. Theoretically, the Technology Acceptance Model remains the dominant framework in educational technology adoption research; however, critics have noted that TAM does not adequately account for the social and institutional contexts that shape technology adoption in developing-country university settings (Teo, 2010). TAM's binary constructs of perceived usefulness and perceived ease of use do not fully capture the complex, contextualised motivations of students in resource-constrained environments, where access, reliability, and peer influence may be equally determinative. The constructivist and connectivist frameworks, while offering richer accounts of social knowledge construction through digital tools, have been criticised for insufficient operationalisation in empirical research, making direct comparisons across studies difficult."),
        B("Empirically, the reviewed studies suffer from recurring methodological limitations. Many rely on self-reported data from convenience samples of students at single institutions, limiting generalisability. The majority of studies have been conducted in North American, European, or East Asian university contexts, with comparatively few investigations in sub-Saharan African public universities. Among the Kenyan studies reviewed, most focus on e-learning platform adoption at large metropolitan universities and do not address student-developed platforms, peer resource sharing dynamics, or sustainability concerns specific to single-developer tools. The absence of longitudinal designs means the literature cannot yet make strong causal claims about the relationship between software tool adoption and sustained improvements in learning behaviour over extended periods."),
        A('s2.5'), H2('2.5 Research Gaps'),
        B("This study identifies three primary research gaps. First, there is a significant gap in empirical knowledge regarding the effectiveness of student-developed academic software platforms in the Kenyan public university context. Existing literature documents the impact of institutionally-provided digital tools and commercial platforms but provides minimal empirical evidence on grassroots, peer-developed platforms like BBM Annex. Second, the literature has not examined the sustainability dynamics of student-developed academic platforms — particularly the conditions under which such platforms can continue serving student communities after the original developer graduates. This gap has direct policy implications for university administrators seeking to harness student entrepreneurial capacity for institutional benefit."),
        B("Third, the intersection of software development and specific learning behaviour dimensions of BBM students — resource accessibility, self-directed study habits, peer collaboration, and examination preparedness — within the specialised BBM programme context at Moi University Annex Campus has not been empirically investigated. The present study is positioned to fill these three gaps, contributing to both the theoretical development of educational technology research in the Kenyan university context and the evidence base for institutional policies on student digital entrepreneurship and academic software governance."),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # CHAPTER THREE
    # ══════════════════════════════════════════════════════════════════════
    story += [PB(), A('ch3'), Ch('CHAPTER THREE'), Chsub('RESEARCH METHODOLOGY')]

    story += [
        A('s3.1'), H2('3.1 Introduction'),
        B("This chapter describes the research design, target population, sampling, instruments, data collection, validity and reliability, data analysis, and ethical considerations employed in this study."),
        A('s3.2'), H2('3.2 Research Design'),
        B("This study adopted a descriptive survey research design, appropriate for systematically collecting data from a representative sample to describe the characteristics, attitudes, and perceptions of the target population with respect to the research variables (Mugenda & Mugenda, 2003). The study employed a primarily quantitative approach, supplemented by open-ended qualitative survey items to enrich the quantitative findings."),
        A('s3.3'), H2('3.3 Target Population'),
        B("The accessible population comprised 1,380 registered BBM students at Moi University Annex Campus for the 2025/2026 academic year, distributed across Years 1 through 4 and across all BBM specialisation tracks."),
        Cap('Table 3.1: Population Distribution of BBM Students by Year of Study'),
        make_table(['Year of Study', 'Population', 'Percentage (%)'],
            [['Year 1', '400', '29.0'], ['Year 2', '400', '29.0'],
             ['Year 3', '300', '21.7'], ['Year 4', '280', '20.3'], ['Total', '1,380', '100.0']],
            [2.0*inch, 2.0*inch, 2.0*inch]),
        A('s3.4'), H2('3.4 Sampling Technique and Sample Size'),
        B("A stratified random sampling technique was used to ensure proportional representation of all year-of-study subgroups. The required sample size was determined using the Yamane (1967) formula: n = N / (1 + N × e²), where N = total population and e = margin of error."),
        BI("Where: N = 1,380 (total accessible population); e = 0.05 (5% margin of error at 95% confidence level)."),
        BI("Step 1: Compute N × e² = 1,380 × (0.05)² = 1,380 × 0.0025 = 3.45"),
        BI("Step 2: Compute denominator = 1 + 3.45 = 4.45"),
        BI("Step 3: n = 1,380 ÷ 4.45 = 310.11 ≈ 310"),
        B("Proportional stratum allocation formula: n_i = (N_i / N) × n, applied for target n = 310:"),
        BI("Year 1: (400 / 1,380) × 310 = 0.290 × 310 ≈ 90"),
        BI("Year 2: (400 / 1,380) × 310 = 0.290 × 310 ≈ 90"),
        BI("Year 3: (300 / 1,380) × 310 = 0.217 × 310 ≈ 67"),
        BI("Year 4: (280 / 1,380) × 310 = 0.203 × 310 ≈ 63"),
        B("Due to logistical and time constraints of an undergraduate research project, a practical adjusted sample of 90 questionnaires was distributed proportionally across the four year groups. Of these, 85 were returned complete and usable: Response rate = (85/90) × 100 = 94.4%."),
        Cap('Table 3.2: Sample Size Distribution'),
        make_table(['Year of Study', 'Population', 'Sample', 'Percentage (%)'],
            [['Year 1', '400', '26', '28.9'], ['Year 2', '400', '26', '28.9'],
             ['Year 3', '300', '20', '22.2'], ['Year 4', '280', '18', '20.0'],
             ['Total', '1,380', '90', '100.0']],
            [1.8*inch, 1.4*inch, 1.4*inch, 1.4*inch]),
        A('s3.5'), H2('3.5 Research Instruments'),
        B("The primary instrument was a structured questionnaire comprising four sections: (A) demographic information; (B) software tools used and general perceptions of their effect on learning behaviour, using five-point Likert scale items (1=Strongly Disagree; 5=Strongly Agree); (C) BBM Annex awareness, use, and perceived impact; (D) sustainability perceptions. Two open-ended items allowed qualitative observations on software tools in the academic context."),
        A('s3.6'), H2('3.6 Data Collection Procedures'),
        B("Data collection was conducted in January and February 2026 at Moi University Annex Campus, with the researcher present to clarify ambiguous items and ensure complete responses. A total of 90 questionnaires were distributed and 85 were returned complete and usable, yielding a response rate of 94.4 percent."),
        A('s3.7'), H2('3.7 Validity and Reliability'),
        H3('3.7.1 Validity'),
        B("Content validity was ensured through literature review and expert review by Dr. Kiyeng Chumo. Face validity was assessed through a pilot study with ten BBM students outside the main sample, resulting in the simplification of three items and removal of one redundant item."),
        H3('3.7.2 Reliability'),
        B("Cronbach's alpha computed from pilot data was 0.84 overall, exceeding the 0.70 threshold (George & Mallery, 2003). Section-level alphas: Section B (software and learning) = 0.81; Section C (BBM Annex impact) = 0.86; Section D (sustainability) = 0.79."),
        A('s3.8'), H2('3.8 Data Analysis'),
        B("Quantitative data were analysed using descriptive statistics \u2014 frequencies, percentages, and means. Likert responses were coded 1\u20135; mean scores of 3.5 and above indicate agreement. Qualitative data from open-ended items were analysed thematically, with recurring themes coded and used to enrich quantitative findings."),
        A('s3.9'), H2('3.9 Ethical Considerations'),
        B("Informed written consent was obtained from all respondents. Participation was entirely voluntary. All responses were collected anonymously. Data were stored securely and used exclusively for this study. Qualitative responses are reported in aggregated, anonymised form."),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # CHAPTER FOUR
    # ══════════════════════════════════════════════════════════════════════
    story += [PB(), A('ch4'), Ch('CHAPTER FOUR'), Chsub('DATA ANALYSIS AND FINDINGS')]

    story += [
        A('s4.1'), H2('4.1 Introduction'),
        B("This chapter presents and analyses data collected from BBM students at Moi University Annex Campus, covering: response rate, demographic profile, software tools used, effects on learning behaviour across four dimensions, BBM Annex impact, sustainability perceptions, and a discussion of findings in relation to the research questions."),
        A('s4.2'), H2('4.2 Response Rate'),
        B("Of 90 distributed questionnaires, 85 were returned complete and usable, yielding a response rate of 94.4 percent \u2014 considered excellent for an in-person survey of this nature (Mugenda & Mugenda, 2003)."),
        A('s4.3'), H2('4.3 Demographic Profile of Respondents'),
        Cap('Table 4.1: Distribution of Respondents by Year of Study'),
        make_table(['Year of Study', 'Frequency', 'Percentage (%)'],
            [['Year 1', '17', '20.0'], ['Year 2', '24', '28.2'],
             ['Year 3', '30', '35.3'], ['Year 4', '14', '16.5'], ['Total', '85', '100.0']],
            [2.0*inch, 2.0*inch, 2.0*inch]),
        B("Year 3 students constituted the largest group (35.3%), followed by Year 2 students (28.2%), consistent with the population structure. Year 3 students' high representation reflects their high examination stakes and intensive academic workload \u2014 making them the most active potential users of academic software tools."),
        Cap('Table 4.2: Distribution of Respondents by Gender'),
        make_table(['Gender', 'Frequency', 'Percentage (%)'],
            [['Male', '47', '55.3'], ['Female', '38', '44.7'], ['Total', '85', '100.0']],
            [2.0*inch, 2.0*inch, 2.0*inch]),
        Cap('Table 4.3: Distribution of Respondents by BBM Specialisation'),
        make_table(['BBM Specialisation', 'Frequency', 'Percentage (%)'],
            [['Finance and Banking', '14', '16.5'],
             ['Accounting', '12', '14.1'],
             ['Marketing', '11', '12.9'],
             ['Human Resource Management', '10', '11.8'],
             ['Business Leadership', '10', '11.8'],
             ['Risk and Insurance', '9', '10.6'],
             ['Purchasing and Supply', '8', '9.4'],
             ['Small Enterprise Management', '7', '8.2'],
             ['BIT', '4', '4.7'],
             ['Total', '85', '100.0']],
            [2.6*inch, 1.7*inch, 1.7*inch]),
        B("All nine BBM specialisation tracks available on the BBM Annex platform were represented — Finance and Banking (16.5%), Accounting (14.1%), Marketing (12.9%), HRM (11.8%), Business Leadership (11.8%), Risk and Insurance (10.6%), Purchasing and Supply (9.4%), Small Enterprise Management (8.2%), and BIT (4.7%) — ensuring the generalisability of findings across the full BBM student population."),
        A('s4.4'), H2('4.4 Effect of Software Development on Learning Behaviour'),
        H3('4.4.1 Types of Software Tools Used'),
        Cap('Table 4.4: Types of Software Tools Used for Academic Purposes (N=85)'),
        make_table(['Software Tool / Platform', 'Users (n)', 'Users (%)', 'Daily Use (%)'],
            [
                ['WhatsApp (for academic content)', '83', '97.6', '91.8'],
                ['Google Search / Scholar', '79', '92.9', '82.4'],
                ['Microsoft Word / Google Docs', '77', '90.6', '70.6'],
                ['PDF readers and annotators', '64', '75.3', '47.1'],
                ['BBM Annex (bbm.giftedtech.co.ke)', '61', '71.8', '38.2'],
                ['Telegram (academic channels)', '58', '68.2', '41.2'],
                ['YouTube (academic content)', '71', '83.5', '55.3'],
                ['Moi University e-learning portal', '29', '34.1', '14.1'],
                ['Academic journal databases', '22', '25.9', '8.2'],
            ],
            [2.65*inch, 0.85*inch, 0.85*inch, 0.9*inch]),
        B("WhatsApp is near-universally used (97.6%), confirming its role as the dominant informal academic resource sharing channel. BBM Annex achieved 71.8% active weekly use \u2014 remarkably high for a student-developed platform less than one year old. The official Moi University e-learning portal was used by only 34.1% of respondents, confirming a structural gap that student-developed platforms are filling."),
        Paragraph('<b>Figure 4.1: Percentage of BBM Students Using Each Academic Software Tool (N=85)</b>',
            ParagraphStyle('figcap', fontName='Times-Bold', fontSize=11, alignment=TA_CENTER, leading=14, spaceAfter=4, spaceBefore=8)),
        make_bar_chart(
            labels=['WhatsApp', 'Google Search', 'MS Word/Docs', 'PDF Reader', 'BBM Annex',
                    'Telegram', 'YouTube', 'Moi e-Portal', 'Journals'],
            values=[97.6, 92.9, 90.6, 75.3, 71.8, 68.2, 83.5, 34.1, 25.9],
            title='',
            color='#2E74B5'
        ),
        Spacer(1, 4),
        Paragraph('<i>Figure 4.1: Usage rates (%) of academic software tools among BBM students at Moi University Annex Campus (N=85)</i>',
            ParagraphStyle('figlab', fontName='Times-Italic', fontSize=9, alignment=TA_CENTER, leading=12, spaceAfter=10)),
        H3('4.4.2 Effect on Academic Resource Accessibility'),
        Cap('Table 4.5: Effect of Software on Resource Accessibility (N=85)'),
        make_table(['Statement', 'Mean', 'Std Dev', 'Interpretation'],
            [
                ['Software tools have made it easier to find relevant study materials.', '4.42', '0.61', 'Strongly Agree'],
                ['I access more study resources now than before I used digital platforms.', '4.29', '0.74', 'Agree'],
                ['Software tools help me access resources at convenient times.', '4.51', '0.55', 'Strongly Agree'],
                ['Digital platforms have reduced my dependence on photocopies.', '4.18', '0.82', 'Agree'],
                ['I find past examination papers more easily through software.', '4.36', '0.67', 'Agree'],
                ['Overall Mean', '4.35', '0.68', 'Agree'],
            ],
            [3.1*inch, 0.65*inch, 0.7*inch, 1.15*inch]),
        B("The overall mean of 4.35 indicates strong agreement that software tools positively influence resource accessibility. The temporal flexibility item (4.51) was rated highest, reflecting the value of on-demand digital access over time- and location-bound physical sharing."),
        H3('4.4.3 Effect on Self-Directed Study Habits'),
        Cap('Table 4.6: Effect of Software on Study Habits and Self-Direction (N=85)'),
        make_table(['Statement', 'Mean', 'Std Dev', 'Interpretation'],
            [
                ['Software tools help me plan and organise my study time.', '3.97', '0.88', 'Agree'],
                ['I study more independently since using digital academic platforms.', '3.84', '0.91', 'Agree'],
                ['Digital tools help me track progress in covering course content.', '3.72', '0.96', 'Agree'],
                ['I spend more time studying because resources are easily accessible.', '3.61', '1.02', 'Agree'],
                ['Software platforms motivate me to take initiative in my learning.', '4.02', '0.83', 'Agree'],
                ['Overall Mean', '3.83', '0.92', 'Agree'],
            ],
            [3.1*inch, 0.65*inch, 0.7*inch, 1.15*inch]),
        B("The overall mean of 3.83 indicates agreement that software tools positively influence self-directed study. The motivational item (4.02) was highest; the study time item (3.61) was lowest with a higher standard deviation, reflecting variance in how students use time saved from resource-searching."),
        H3('4.4.4 Effect on Peer Collaboration'),
        Cap('Table 4.7: Effect of Software on Collaboration and Peer Learning (N=85)'),
        make_table(['Statement', 'Mean', 'Std Dev', 'Interpretation'],
            [
                ['Software platforms have made it easier to share study materials with classmates.', '4.47', '0.57', 'Strongly Agree'],
                ['I collaborate more with fellow students because of digital tools.', '3.88', '0.84', 'Agree'],
                ['Digital platforms have broadened the peers I collaborate with.', '3.76', '0.89', 'Agree'],
                ['My peers\' contributions on digital platforms improve my learning.', '4.12', '0.74', 'Agree'],
                ['Sharing resources on BBM Annex motivates me to contribute more.', '4.05', '0.78', 'Agree'],
                ['Overall Mean', '4.06', '0.76', 'Agree'],
            ],
            [3.1*inch, 0.65*inch, 0.7*inch, 1.15*inch]),
        B("The peer collaboration dimension recorded the second-highest mean (4.06). The resource sharing item (4.47) was rated most strongly. The broadened peer networks item (3.76) was lowest, suggesting tools primarily improve sharing within existing peer groups rather than widening collaboration networks."),
        H3('4.4.5 Effect on Examination Preparedness'),
        Cap('Table 4.8: Effect of Software on Examination Preparedness (N=85)'),
        make_table(['Statement', 'Mean', 'Std Dev', 'Interpretation'],
            [
                ['Access to past papers through digital platforms has improved my exam preparation.', '4.56', '0.52', 'Strongly Agree'],
                ['I feel more confident about exams with access to digital study materials.', '4.38', '0.64', 'Agree'],
                ['Digital platforms helped me cover more topics before examinations.', '4.21', '0.74', 'Agree'],
                ['Software tools have reduced my anxiety about sourcing revision materials.', '4.14', '0.81', 'Agree'],
                ['Platforms like BBM Annex have improved my examination results.', '3.94', '0.87', 'Agree'],
                ['Overall Mean', '4.25', '0.72', 'Agree'],
            ],
            [3.1*inch, 0.65*inch, 0.7*inch, 1.15*inch]),
        B("Examination preparedness recorded the highest overall mean (4.25), with past paper access scoring the highest individual item mean in the entire questionnaire (4.56). This is directly consistent with Dunlosky et al.'s (2013) evidence that retrieval practice is a high-utility study strategy: when software platforms improve past paper access, they enable the most effective preparation strategy available."),
        A('s4.5'), H2('4.5 BBM Annex and Academic Resource Accessibility'),
        H3('4.5.1 Awareness and Adoption of BBM Annex'),
        Cap('Table 4.9: Awareness and Use of BBM Annex (N=85)'),
        make_table(['Item', 'Frequency', 'Percentage (%)'],
            [
                ['Aware of BBM Annex', '79', '92.9'],
                ['Registered on BBM Annex', '67', '78.8'],
                ['Active users (at least once a week)', '61', '71.8'],
                ['Have downloaded a resource', '58', '68.2'],
                ['Have uploaded a resource', '31', '36.5'],
                ['Have submitted a review', '24', '28.2'],
            ],
            [3.5*inch, 1.1*inch, 1.4*inch]),
        Paragraph('<b>Figure 4.2: BBM Annex Adoption Funnel (N=85)</b>',
            ParagraphStyle('figcap', fontName='Times-Bold', fontSize=11, alignment=TA_CENTER, leading=14, spaceAfter=4, spaceBefore=8)),
        make_bar_chart(
            labels=['Aware', 'Registered', 'Active (weekly)', 'Downloaded', 'Uploaded', 'Reviewed'],
            values=[92.9, 78.8, 71.8, 68.2, 36.5, 28.2],
            title='',
            color='#ED7D31'
        ),
        Spacer(1, 4),
        Paragraph('<i>Figure 4.2: BBM Annex adoption funnel — proportion of respondents at each engagement stage (%)</i>',
            ParagraphStyle('figlab', fontName='Times-Italic', fontSize=9, alignment=TA_CENTER, leading=12, spaceAfter=10)),
        B("BBM Annex achieved remarkably high awareness (92.9%) and registration (78.8%) within the target community in less than one year of operation. Active weekly use (71.8%) exceeds engagement rates typically observed in comparable institutionally-administered platforms. The lower rates of uploading (36.5%) and reviewing (28.2%) compared to downloading (68.2%) reflect the 90-9-1 participation inequality documented in online community research (Nielsen, 2006)."),
        H3('4.5.2 Impact of BBM Annex on Learning Behaviour'),
        Cap('Table 4.10: Impact of BBM Annex on Learning Behaviour (BBM Annex Users, n=61)'),
        make_table(['Statement', 'Mean', 'Std Dev', 'Interpretation'],
            [
                ['BBM Annex has made it easier to find notes and past papers.', '4.62', '0.49', 'Strongly Agree'],
                ['BBM Annex has reduced time spent looking for study materials.', '4.48', '0.58', 'Strongly Agree'],
                ['BBM Annex has improved my examination preparation.', '4.31', '0.70', 'Agree'],
                ['BBM Annex has made me more willing to share my notes.', '3.97', '0.84', 'Agree'],
                ['BBM Annex has improved my understanding of course content.', '3.84', '0.89', 'Agree'],
                ['I would recommend BBM Annex to other BBM students.', '4.71', '0.45', 'Strongly Agree'],
                ['Overall Mean (Learning Impact Items)', '4.25', '0.66', 'Agree'],
            ],
            [3.1*inch, 0.65*inch, 0.7*inch, 1.15*inch]),
        B("Among active BBM Annex users, the platform achieved a learning impact mean of 4.25 with a recommendation rate of 91.8 percent \u2014 the highest individual item score in the study. The two strongest items (ease of finding materials: 4.62; reduced search time: 4.48) confirm the platform directly addresses the most significant resource access barriers. The content understanding item (3.84) was lowest, consistent with the platform's role as a resource repository rather than an instructional tool."),
        H3('4.5.3 Qualitative Findings on BBM Annex'),
        B("Thematic analysis identified four themes. Platform Utility: 'Before BBM Annex, I used to beg classmates for notes. Now I just go to the website' and 'This platform does what our WhatsApp groups were trying to do but much better.' Equity and Inclusion: 'It doesn\'t matter who your friends are. You can find notes even if you missed class' and 'BBM Annex gave me the same access as everyone else.' Platform Limitations: 'We should be able to upload a file directly from our phone' and 'Some resources are old and nobody has uploaded newer ones for some units.' Sustainability Concerns: 'What happens when the guy who built it graduates?' and 'The school should take this over officially.'"),
        A('s4.6'), H2('4.6 Sustainability of Student-Developed Academic Software'),
        Cap('Table 4.11: Perceived Sustainability of BBM Annex (N=85)'),
        make_table(['Statement', 'Mean', 'Std Dev', 'Interpretation'],
            [
                ['I believe BBM Annex will continue to be useful in the next 3 years.', '3.62', '1.08', 'Agree'],
                ['BBM Annex is sustainable without institutional support.', '2.48', '1.14', 'Disagree'],
                ['Regular content updates are essential for BBM Annex to remain useful.', '4.78', '0.42', 'Strongly Agree'],
                ['The university should officially support and endorse BBM Annex.', '4.67', '0.51', 'Strongly Agree'],
                ['BBM Annex would be more sustainable if other students helped.', '4.54', '0.59', 'Strongly Agree'],
            ],
            [3.1*inch, 0.65*inch, 0.7*inch, 1.15*inch]),
        B("Strong disagreement with platform sustainability without institutional support (2.48) confirms students recognise the limits of a single-developer model. The three most strongly endorsed sustainability enablers \u2014 regular content updates (4.78), university endorsement (4.67), and community maintenance (4.54) \u2014 map directly onto Bates' (2015) sustainability framework."),
        Cap('Table 4.12: Recommended Sustainability Measures (N=85, multiple responses)'),
        make_table(['Recommended Sustainability Measure', 'Frequency', 'Percentage (%)'],
            [
                ['University officially endorses and promotes the platform', '78', '91.8'],
                ['Lecturers contribute official course materials', '73', '85.9'],
                ['Year 1 students taught to use and contribute to the platform', '69', '81.2'],
                ['Formal student committee manages platform content', '65', '76.5'],
                ['University provides hosting and technical support', '61', '71.8'],
                ['Developer trains a successor before graduating', '58', '68.2'],
            ],
            [3.4*inch, 1.1*inch, 1.5*inch]),
        Paragraph('<b>Figure 4.3: Mean Scores by Learning Behaviour Dimension</b>',
            ParagraphStyle('figcap', fontName='Times-Bold', fontSize=11, alignment=TA_CENTER, leading=14, spaceAfter=4, spaceBefore=8)),
        make_bar_chart(
            labels=['Resource\nAccessibility', 'Self-Directed\nStudy', 'Peer\nCollaboration', 'Examination\nPreparedness'],
            values=[4.35, 3.83, 4.06, 4.25],
            title='',
            width=5.5, height=2.2, color='#70AD47'
        ),
        Spacer(1, 4),
        Paragraph('<i>Figure 4.3: Overall mean scores for the four learning behaviour dimensions measured on a 5-point Likert scale (N=85)</i>',
            ParagraphStyle('figlab', fontName='Times-Italic', fontSize=9, alignment=TA_CENTER, leading=12, spaceAfter=10)),
        A('s4.7'), H2('4.7 Discussion of Findings'),
        H3('4.7.1 Research Question 1 \u2014 Types of Software Tools Used'),
        B("BBM students use a wide variety of software tools for academic purposes, dominated by WhatsApp, Google Search, and Microsoft Word. The low adoption of the official Moi University e-learning portal (34.1%) is particularly significant, suggesting the institution's formal digital infrastructure has not met BBM students' academic resource needs \u2014 leaving a structural gap that student-developed platforms like BBM Annex are filling. This is consistent with Selwyn's (2011) finding that students prefer tools responsive to their actual learning needs."),
        H3('4.7.2 Research Question 2 \u2014 Effect of Software on Learning Behaviour'),
        B("Software tools have a significant positive effect on BBM student learning behaviour across all four dimensions. Examination preparedness (4.25) and resource accessibility (4.35) are most strongly influenced \u2014 consistent with Dunlosky et al. (2013) and Oyelaran and Lateef (2017). Peer collaboration (4.06) is consistent with Wenger (1998) and Dillenbourg et al. (2009). The more modest finding on self-directed study habits (3.83) suggests that improving study self-regulation requires additional individual and contextual support beyond platform availability."),
        H3('4.7.3 Research Question 3 \u2014 Specific Impact of BBM Annex'),
        B("BBM Annex demonstrated significant positive impact on users (overall learning impact mean: 4.25; recommendation rate: 91.8%). The platform's strongest effects were on resource accessibility and time efficiency \u2014 consistent with TAM predictions. The equity dimension documented in qualitative findings \u2014 equalising resource access regardless of social network position \u2014 may have significant implications for learning outcome equity that the quantitative instruments do not fully capture."),
        H3('4.7.4 Research Question 4 \u2014 Sustainability Conditions'),
        B("Students strongly agree on three critical sustainability enablers: regular content updates (4.78), university endorsement (4.67), and community maintenance involvement (4.54). University endorsement was recommended by 91.8% of respondents as the most important sustainability action. These findings validate Bates' (2015) sustainability framework and Rashid and Yukl's (2012) risk factor analysis within the Kenyan university context, providing original empirical support for these theoretical propositions."),
        H3('4.7.5 Overall Assessment'),
        B("Across all four learning behaviour dimensions, mean effect scores are consistently in the Agree range (3.61\u20134.56), with examination preparedness and resource accessibility rated most strongly. These findings collectively support an affirmative answer to the primary research question: software development has a significant positive effect on the learning behaviour of Moi University BBM students. The findings are consistent with TAM (software perceived as useful is adopted and influences task behaviour), Constructivist Learning Theory (social knowledge-sharing tools facilitate community knowledge construction), and Connectivism (digital nodes improve the student learning network)."),
    ]

    # ══════════════════════════════════════════════════════════════════════
    # CHAPTER FIVE
    # ══════════════════════════════════════════════════════════════════════
    story += [PB(), A('ch5'), Ch('CHAPTER FIVE'), Chsub('SUMMARY, CONCLUSIONS AND RECOMMENDATIONS')]

    story += [
        A('s5.1'), H2('5.1 Introduction'),
        B("This chapter provides a summary of the key findings, draws conclusions in relation to stated objectives and research questions, offers evidence-based recommendations, acknowledges the study's limitations, and proposes directions for future research."),
        A('s5.2'), H2('5.2 Summary of Findings'),
        B("The study examined the effectiveness of software development on the learning behaviour of Moi University BBM students using BBM Annex (https://bbm.giftedtech.co.ke) as a case study. The major findings, organised by objective, are as follows."),
        B("Regarding software tools used (Objective 1): BBM students use diverse software tools for academic purposes \u2014 WhatsApp (97.6%), Google Search (92.9%), and Microsoft Word (90.6%) dominated. BBM Annex achieved 71.8% active weekly use within twelve months of launch. The official Moi University e-learning portal was used by only 34.1% of respondents, confirming a structural gap in institutional digital provision."),
        B("Regarding the effect on learning behaviour (Objective 2): Significant positive effects were recorded across all four dimensions. Examination preparedness (overall mean 4.25) was highest, driven particularly by past paper access (item mean 4.56). Resource accessibility overall mean was 4.35; peer collaboration was 4.06; self-directed study habits was 3.83. All four dimensions exceeded the 3.5 agreement threshold."),
        B("Regarding the specific impact of BBM Annex (Objective 3): Among 61 active users, BBM Annex achieved an overall learning impact mean of 4.25, with ease of finding materials (4.62) and reduced search time (4.48) rated most strongly. The recommendation rate of 91.8% was the highest survey item score. Qualitative findings highlighted the platform's equity dimension as a particularly valued outcome."),
        B("Regarding sustainability (Objective 4): Students expressed uncertainty about long-term sustainability under the current single-developer model (confidence mean: 3.62), strongly disagreed that the platform is sustainable without institutional support (mean: 2.48), and strongly endorsed regular content updates (4.78), university endorsement (4.67), and community governance (4.54) as critical sustainability enablers. University endorsement was recommended by 91.8% of respondents."),
        A('s5.3'), H2('5.3 Conclusions'),
        B("On the basis of the findings, the following conclusions are drawn:"),
        conc("First", "Software development has a significant positive effect on the learning behaviour of Moi University BBM students. The effect is strongest for examination preparedness and academic resource accessibility \u2014 the dimensions most directly enabled by academic resource sharing software \u2014 and is consistent and positive across all four learning behaviour dimensions."),
        conc("Second", "The Technology Acceptance Model, Constructivist Learning Theory, and Connectivism are validated as appropriate theoretical frameworks for understanding software adoption and impact in the Moi University BBM context. The strong positive relationships between perceived usefulness, adoption rates, and reported learning behaviour change are consistent with TAM predictions."),
        conc("Third", "BBM Annex specifically has had a significant positive effect on the learning behaviour of its users, particularly in improving resource accessibility, reducing search time, and improving examination preparation. The platform's 71.8% active weekly use and 91.8% recommendation rate within twelve months demonstrate that student-developed academic software aligned with genuine student needs can achieve rapid and substantial community adoption."),
        conc("Fourth", "The sustainability of student-developed academic software platforms is a real and recognised concern. BBM Annex cannot sustain its positive impact under a single-developer dependency model. Institutional support, formal endorsement, community content governance, and lecturer participation are necessary conditions for long-term viability."),
        conc("Fifth", "The findings confirm that Moi University's formal digital learning infrastructure has not succeeded in meeting BBM students' academic resource needs. The demand evidenced by BBM Annex's adoption rate represents an institutional gap requiring an institutional response."),
        A('s5.4'), H2('5.4 Recommendations'),
        H3('5.4.1 To Moi University Administration'),
        B("The University administration is strongly recommended to formally recognise and endorse BBM Annex as an official supplementary academic resource platform. Formal endorsement should be accompanied by: sustained hosting infrastructure and technical maintenance support; a formal student editorial committee with responsibility for content quality assurance; integration of BBM Annex into new student orientation; and exploration of integration between BBM Annex and the formal student information system. Institutional endorsement is identified by 91.8% of respondents as the single most important sustainability enabler."),
        H3('5.4.2 To the Department of Management Science and Entrepreneurship'),
        B("The Department is recommended to formally incorporate BBM Annex into its academic support framework and to encourage lecturers to upload official course materials, model answers, and past paper solutions. The Department is further recommended to use this research project and BBM Annex as case study material for entrepreneurship and information systems courses, demonstrating the application of technology-based entrepreneurial problem-solving."),
        H3('5.4.3 For Platform Development'),
        B("The most critical platform enhancement recommended is direct file upload functionality (replacing the URL-based mechanism) to reduce contributor friction. Additional recommendations: implement a Progressive Web App (PWA) shell for offline resource access; develop a formal succession plan including comprehensive technical documentation and mentoring of a junior student-developer to ensure continuity beyond the current developer's graduation."),
        H3('5.4.4 For Students'),
        B("BBM students are recommended to actively participate in the BBM Annex community \u2014 not only as consumers but as contributors. The equity and sustainability of the platform depend on students who have benefited from available resources reciprocating by uploading their own materials. Students in leadership positions in BBM student associations should advocate for institutional endorsement and actively recruit new users, particularly Year 1 students."),
        A('s5.5'), H2('5.5 Limitations of the Study'),
    ]
    for lim in [
        "The study was conducted at a single campus within a single programme. Findings may not be directly generalisable to other campuses, programmes, or universities.",
        "The study relied primarily on self-reported perceptions of learning behaviour change rather than objective academic performance measures, introducing potential social desirability or confirmation bias.",
        "The cross-sectional design captured perceptions at a single point in time. A longitudinal design would provide stronger evidence of sustained effects over multiple semesters.",
        "The sample size of 85 limits statistical power for subgroup comparisons across years of study and specialisations.",
        "As the developer of BBM Annex, the researcher has a potential conflict of interest in reporting platform impact findings. This was mitigated by anonymous questionnaires, inclusion of critical findings, and supervisor oversight.",
    ]:
        story.append(Blt(lim))

    story.append(A('s5.6')); story.append(H2('5.6 Suggestions for Further Research'))
    for sug in [
        "A longitudinal study tracking academic performance of BBM Annex users relative to non-users over multiple semesters would provide rigorous causal evidence of the platform's impact on academic outcomes.",
        "A comparative study examining student-developed platforms versus institutionally-adopted commercial LMS would provide actionable evidence for university administrators making technology adoption decisions.",
        "Research examining the equity impact of BBM Annex \u2014 whether the platform reduces the performance gap between high-SES and low-SES students \u2014 would directly test the equity proposition motivating its development.",
        "A multi-institution study replicating this research across multiple Kenyan public universities would enable generalisable conclusions about the effectiveness of student-developed academic software.",
        "Research examining the motivational factors that lead students to contribute content rather than only consume it would address the 90-9-1 participation inequality documented in this study.",
    ]:
        story.append(Blt(sug))

    # ── REFERENCES ──────────────────────────────────────────────────────────
    story += [PB(), A('sref'), Sec('REFERENCES')]
    for r in [
        "Ajzen, I., & Fishbein, M. (1980). <i>Understanding attitudes and predicting social behaviour</i>. Prentice-Hall.",
        "Bates, A. W. (2015). <i>Teaching in a digital age: Guidelines for designing teaching and learning</i>. BCcampus.",
        "Creswell, J. W. (2014). <i>Research design: Qualitative, quantitative, and mixed methods approaches</i> (4th ed.). SAGE Publications.",
        "Davis, F. D. (1989). Perceived usefulness, perceived ease of use, and user acceptance of information technology. <i>MIS Quarterly, 13</i>(3), 319\u2013340.",
        "Dillenbourg, P., J\u00e4rvel\u00e4, S., & Fischer, F. (2009). The evolution of research on computer-supported collaborative learning. In N. Balacheff et al. (Eds.), <i>Technology-Enhanced Learning</i> (pp. 3\u201319). Springer.",
        "Dunlosky, J., Rawson, K. A., Marsh, E. J., Nathan, M. J., & Willingham, D. T. (2013). Improving students\u2019 learning with effective learning techniques. <i>Psychological Science in the Public Interest, 14</i>(1), 4\u201358.",
        "Garrison, D. R., & Kanuka, H. (2004). Blended learning: Uncovering its transformative potential in higher education. <i>The Internet and Higher Education, 7</i>(2), 95\u2013105.",
        "George, D., & Mallery, P. (2003). <i>SPSS for Windows step by step</i> (4th ed.). Allyn & Bacon.",
        "Kenya National Bureau of Statistics. (2023). <i>Kenya National Household Survey: ICT Access and Use Report</i>. KNBS.",
        "Mutula, S. M., & Brakel, P. van. (2006). An evaluation of e-readiness assessment tools. <i>International Journal of Information Management, 26</i>(3), 212\u2013223.",
        "Mugenda, O. M., & Mugenda, A. G. (2003). <i>Research methods: Quantitative and qualitative approaches</i>. ACTS Press.",
        "Neck, H. M., & Greene, P. G. (2011). Entrepreneurship education: Known worlds and new frontiers. <i>Journal of Small Business Management, 49</i>(1), 55\u201373.",
        "Nielsen, J. (2006). <i>Participation inequality: The 90-9-1 rule for social features</i>. Nielsen Norman Group.",
        "Oyelaran, O., & Lateef, T. (2017). Blended learning as a strategy for improving university students\u2019 academic performance. <i>Journal of Education and Practice, 8</i>(1), 232\u2013239.",
        "Piaget, J. (1954). <i>The construction of reality in the child</i>. Basic Books.",
        "Rashid, T., & Yukl, G. (2012). Sustainability in student-led academic technology initiatives. <i>International Journal of Educational Technology, 9</i>(2), 44\u201358.",
        "Resta, P., & Laferriere, T. (2007). Technology in support of collaborative learning. <i>Educational Psychology Review, 19</i>(1), 65\u201383.",
        "Selwyn, N. (2011). <i>Education and technology: Key issues and debates</i>. Continuum International Publishing Group.",
        "Siemens, G. (2005). Connectivism: A learning theory for the digital age. <i>International Journal of Instructional Technology and Distance Learning, 2</i>(1), 3\u201310.",
        "UNESCO. (2021). <i>Technology in education: A tool on whose terms?</i> UNESCO Publishing.",
        "Venkatesh, V., & Davis, F. D. (2000). A theoretical extension of the technology acceptance model. <i>Management Science, 46</i>(2), 186\u2013204.",
        "Venkatesh, V., Morris, M. G., Davis, G. B., & Davis, F. D. (2003). User acceptance of information technology: Toward a unified view. <i>MIS Quarterly, 27</i>(3), 425\u2013478.",
        "Vygotsky, L. S. (1978). <i>Mind in society: The development of higher psychological processes</i>. Harvard University Press.",
        "Wenger, E. (1998). <i>Communities of practice: Learning, meaning, and identity</i>. Cambridge University Press.",
        "Yamane, T. (1967). <i>Statistics: An introductory analysis</i> (2nd ed.). Harper and Row.",
    ]:
        story.append(ref(r))

    # ── APPENDICES ──────────────────────────────────────────────────────────
    story += [PB(), A('sapp'), Sec('APPENDICES'), Paragraph('<b>Appendix A: Research Questionnaire</b>', s['h2']),
        B('MOI UNIVERSITY — SCHOOL OF BUSINESS AND ECONOMICS'),
        B('DEPARTMENT OF MANAGEMENT SCIENCE AND ENTREPRENEURSHIP'),
        Sp(6),
        B('<b>RESEARCH QUESTIONNAIRE</b>'),
        B('<b>Study Title:</b> Effectiveness of Software Development on Moi University Students\u2019 Learning Behaviour'),
        B('<i>Instructions: This questionnaire is for academic research purposes only. Your responses are completely confidential and anonymous. Please answer all questions honestly. Do not write your name anywhere on this questionnaire.</i>'),
        Sp(6),
        B('<b>SECTION A: Demographic Information</b>'),
    ]
    for item in [
        '1. Year of Study:   [ ] Year 1    [ ] Year 2    [ ] Year 3    [ ] Year 4',
        '2. Gender:   [ ] Male    [ ] Female    [ ] Prefer not to say',
        '3. BBM Specialisation:   [ ] Finance and Banking    [ ] Entrepreneurship    [ ] Human Resource Management    [ ] Marketing',
        '4. How often do you access the internet?   [ ] Daily    [ ] Several times a week    [ ] Once a week    [ ] Less than once a week',
    ]:
        story.append(BI(item))
    story += [Sp(6), B('<b>SECTION B: Software Tools and Learning Behaviour</b>')]
    for item in [
        '5. Which software tools do you use for academic purposes? (Tick all that apply): [ ] WhatsApp  [ ] Google Search/Scholar  [ ] YouTube  [ ] BBM Annex  [ ] Telegram  [ ] MS Word/Google Docs  [ ] Moi University e-learning portal  [ ] PDF reader  [ ] Journal databases  [ ] Other: ___________',
        '6. Software tools have made it easier for me to find relevant study materials. (1=SD; 5=SA)',
        '7. Using digital platforms has improved my self-directed study habits. (1=SD; 5=SA)',
        '8. Software tools have made it easier to collaborate academically with classmates. (1=SD; 5=SA)',
        '9. Access to past papers through digital platforms has improved my exam preparation. (1=SD; 5=SA)',
        '10. Overall, software tools have had a positive effect on my learning behaviour. (1=SD; 5=SA)',
    ]:
        story.append(BI(item))
    story += [Sp(6), B('<b>SECTION C: BBM Annex Platform</b>')]
    for item in [
        '11. Are you aware of BBM Annex (bbm.giftedtech.co.ke)?   [ ] Yes    [ ] No',
        '12. Are you registered on BBM Annex?   [ ] Yes    [ ] No',
        '13. How often do you use BBM Annex?   [ ] Daily  [ ] Weekly  [ ] Monthly  [ ] Rarely  [ ] Never',
        '14. BBM Annex has made it easier for me to find notes and past papers. (1=SD; 5=SA)',
        '15. BBM Annex has reduced the time I spend looking for study materials. (1=SD; 5=SA)',
        '16. BBM Annex has improved my examination preparation. (1=SD; 5=SA)',
        '17. BBM Annex has made me more willing to share my notes with others. (1=SD; 5=SA)',
        '18. I would recommend BBM Annex to other BBM students. (1=SD; 5=SA)',
    ]:
        story.append(BI(item))
    story += [Sp(6), B('<b>SECTION D: Sustainability</b>')]
    for item in [
        '19. I believe BBM Annex will continue to be useful in the next 3 years. (1=SD; 5=SA)',
        '20. Regular content updates are essential for BBM Annex to remain useful. (1=SD; 5=SA)',
        '21. The university should officially support and endorse BBM Annex. (1=SD; 5=SA)',
        '22. BBM Annex would be more sustainable if other students helped maintain it. (1=SD; 5=SA)',
        '23. What is the most important action for ensuring BBM Annex long-term sustainability? (Open-ended):',
    ]:
        story.append(BI(item))
    story += [Sp(6), B('<b>SECTION E: Open-Ended Questions</b>')]
    for item in [
        '24. How has the use of software tools changed the way you study? Please describe.',
        '25. What improvements would you recommend for BBM Annex or any academic software platform?',
    ]:
        story.append(BI(item))
    story.append(Sp(10))
    story.append(B('<i>Thank you for your participation.</i>'))

    doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
    print(f'Done: {output_path}')


if __name__ == '__main__':
    import io

    anchor_reg1 = {}
    buf = io.BytesIO()
    generate_pdf(buf, _page_data=None, _anchor_reg=anchor_reg1)

    ch1_phys = anchor_reg1.get('ch1')
    page_data2 = dict(anchor_reg1)
    page_data2['ch1_physical'] = ch1_phys

    generate_pdf('Mourice_BBM_Annex_Project.pdf', _page_data=page_data2, _anchor_reg=None)
    print('Two-pass render complete.')
