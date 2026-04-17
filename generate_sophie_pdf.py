#!/usr/bin/env python3
"""Generate PDF research project for Sophie Wanyonyi — Moi University"""
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY, TA_RIGHT
from reportlab.graphics.shapes import Drawing, String as GString
from reportlab.pdfbase.pdfmetrics import stringWidth as SW
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                 Table, TableStyle, HRFlowable, Image, KeepTogether)
from reportlab.platypus.flowables import HRFlowable
from reportlab.lib.colors import black, white, HexColor
import os
os.makedirs('files', exist_ok=True)

PW, PH = letter
LM, RM, TM, BM = 1.25*inch, 1.0*inch, 1.0*inch, 1.0*inch
CW = PW - LM - RM

def get_styles():
    s = {}
    s['title_center'] = ParagraphStyle('tc', fontName='Times-Bold', fontSize=13,
        alignment=TA_CENTER, spaceAfter=6, spaceBefore=4, leading=18, textColor=black)
    s['title_sub'] = ParagraphStyle('ts', fontName='Times-Roman', fontSize=11,
        alignment=TA_CENTER, spaceAfter=4, spaceBefore=2, leading=16, textColor=black)
    s['title_bold'] = ParagraphStyle('tb', fontName='Times-Bold', fontSize=12,
        alignment=TA_CENTER, spaceAfter=4, spaceBefore=4, leading=18, textColor=black)
    s['section_heading'] = ParagraphStyle('sh', fontName='Times-Bold', fontSize=13,
        alignment=TA_CENTER, spaceAfter=10, spaceBefore=4, leading=18, textColor=black)
    s['heading2'] = ParagraphStyle('h2', fontName='Times-Bold', fontSize=12,
        alignment=TA_LEFT, spaceAfter=6, spaceBefore=10, leading=18, textColor=black)
    s['heading3'] = ParagraphStyle('h3', fontName='Times-Bold', fontSize=12,
        alignment=TA_LEFT, spaceAfter=4, spaceBefore=6, leading=18, textColor=black)
    s['body'] = ParagraphStyle('body', fontName='Times-Roman', fontSize=12,
        alignment=TA_JUSTIFY, spaceAfter=8, spaceBefore=0, leading=18, textColor=black)
    s['body_indent'] = ParagraphStyle('bi', fontName='Times-Roman', fontSize=12,
        alignment=TA_LEFT, spaceAfter=4, spaceBefore=2, leading=18, leftIndent=20, textColor=black)
    s['caption'] = ParagraphStyle('cap', fontName='Times-Italic', fontSize=11,
        alignment=TA_LEFT, spaceAfter=4, spaceBefore=4, leading=14, textColor=black)
    s['toc_bold'] = ParagraphStyle('tb2', fontName='Times-Bold', fontSize=11,
        alignment=TA_LEFT, spaceAfter=2, spaceBefore=2, leading=14, textColor=black)
    s['toc_item'] = ParagraphStyle('ti', fontName='Times-Roman', fontSize=11,
        alignment=TA_LEFT, spaceAfter=2, spaceBefore=2, leading=14, leftIndent=18, textColor=black)
    s['toc_sub'] = ParagraphStyle('ts2', fontName='Times-Roman', fontSize=11,
        alignment=TA_LEFT, spaceAfter=2, spaceBefore=2, leading=14, leftIndent=36, textColor=black)
    s['ref'] = ParagraphStyle('ref', fontName='Times-Roman', fontSize=12,
        leading=18, alignment=TA_JUSTIFY, spaceAfter=8, leftIndent=24, firstLineIndent=-24)
    s['letter'] = ParagraphStyle('let', fontName='Times-Roman', fontSize=12,
        leading=18, alignment=TA_LEFT, spaceAfter=8)
    s['abbrev'] = ParagraphStyle('abb', fontName='Times-Roman', fontSize=12,
        leading=18, alignment=TA_LEFT, spaceAfter=4)
    s['term'] = ParagraphStyle('trm', fontName='Times-Roman', fontSize=12,
        leading=18, alignment=TA_JUSTIFY, spaceAfter=8)
    s['center_eq'] = ParagraphStyle('ceq', fontName='Times-Bold', fontSize=12,
        alignment=TA_CENTER, spaceAfter=8, spaceBefore=6, leading=18, textColor=black)
    return s

def P(text, sty_key, styles=None):
    if styles is None:
        styles = get_styles()
    return Paragraph(text, styles[sty_key])

def make_table(headers, rows, col_widths=None, header_bg=HexColor('#D3D3D3')):
    if col_widths is None:
        col_widths = [CW / len(headers)] * len(headers)
    hdr_sty = ParagraphStyle('th', fontName='Times-Bold', fontSize=11,
        alignment=TA_CENTER, leading=13, textColor=black, wordWrap='LTR')
    cell_c = ParagraphStyle('tcc', fontName='Times-Roman', fontSize=11,
        alignment=TA_CENTER, leading=13, textColor=black, wordWrap='LTR')
    cell_l = ParagraphStyle('tcl', fontName='Times-Roman', fontSize=11,
        alignment=TA_LEFT, leading=13, textColor=black, wordWrap='LTR')
    def wrap(val, sty): return Paragraph(str(val), sty)
    data = [[wrap(h, hdr_sty) for h in headers]]
    for row in rows:
        data.append([wrap(v, cell_l if j == 0 else cell_c) for j, v in enumerate(row)])
    style = TableStyle([
        ('BACKGROUND', (0,0), (-1,0), header_bg),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('GRID', (0,0), (-1,-1), 0.5, black),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [white, HexColor('#F9F9F9')]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ])
    t = Table(data, colWidths=col_widths, repeatRows=1)
    t.setStyle(style)
    return t

from reportlab.lib.pagesizes import letter as _letter_size
from reportlab.pdfgen import canvas as _rl_canvas


class NumberedCanvas(_rl_canvas.Canvas):
    """Canvas that draws 'Page X of X' at bottom-right, skipping cover page."""
    def __init__(self, *args, **kwargs):
        _rl_canvas.Canvas.__init__(self, *args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        total = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self._draw_page_footer(total)
            _rl_canvas.Canvas.showPage(self)
        _rl_canvas.Canvas.save(self)

    def _draw_page_footer(self, total):
        if self._pageNumber > 1:
            self.saveState()
            self.setFont('Times-Roman', 10)
            right_x = _letter_size[0] - 1.0 * inch
            self.drawRightString(right_x, 0.5 * inch, f'Page {self._pageNumber - 1} of {total - 1}')
            self.restoreState()


def sophie_toc_draw(text, page, level='item'):
    """Precise dot-leader TOC row as a Drawing (text area = 6.25 inch)."""
    from reportlab.graphics.shapes import Drawing, String
    from reportlab.pdfbase.pdfmetrics import stringWidth
    from reportlab.lib.units import inch
    TEXTW = 6.25 * inch
    bold = (level == 'bold')
    font = 'Times-Bold' if bold else 'Times-Roman'
    sz = 11
    row_h = 15
    indent_map = {'bold': 0, 'item': 18, 'sub': 36}
    indent_w = indent_map.get(level, 0)
    label = text.strip()
    pg = str(page)
    label_w = stringWidth(label, font, sz)
    pg_w    = stringWidth(pg, font, sz)
    dot_w   = stringWidth('.', font, sz)
    gap = 4
    available = TEXTW - indent_w - label_w - pg_w - gap * 2
    n_dots = max(3, int(available / dot_w))
    d = Drawing(TEXTW, row_h)
    d.add(String(indent_w, 3.5, label, fontName=font, fontSize=sz))
    d.add(String(indent_w + label_w + gap, 3.5, '.' * n_dots, fontName=font, fontSize=sz))
    d.add(String(TEXTW - pg_w, 3.5, pg, fontName=font, fontSize=sz))
    return d


def generate_pdf():
    styles = get_styles()
    def P(text, sty): return Paragraph(text, styles[sty])
    def SP(n=6): return Spacer(1, n)
    def PB(): return PageBreak()

    story = []

    # ===================== COVER PAGE =====================
    story.append(SP(20))
    logo_path = 'attached_assets/moi_logo_1773763714167.png'
    if os.path.exists(logo_path):
        logo = Image(logo_path, width=1.0*inch, height=1.0*inch)
        logo.hAlign = 'CENTER'
        story.append(logo)
    story.append(SP(10))
    story.append(P('THE EFFECT OF FINANCIAL CAPABILITIES ON RISK-TAKING', 'title_center'))
    story.append(P('AMONG UNIVERSITY STUDENTS', 'title_center'))
    story.append(SP(20))
    story.append(P('PRESENTED', 'title_sub'))
    story.append(P('BY:', 'title_sub'))
    story.append(P('<b>WANYONYI NAFULA SOPHIE</b>', 'title_bold'))
    story.append(P('BBM/4452/23', 'title_sub'))
    story.append(SP(18))
    story.append(P('A RESEARCH PROJECT SUBMITTED IN PARTIAL FULFILMENT FOR THE REQUIREMENTS OF THE AWARD OF DEGREE OF BACHELOR OF BUSINESS MANAGEMENT (FINANCE AND BANKING OPTION)', 'title_sub'))
    story.append(SP(18))
    story.append(P('<b>DEPARTMENT OF ACCOUNTING AND FINANCE</b>', 'title_bold'))
    story.append(P('<b>SCHOOL OF BUSINESS AND ECONOMICS</b>', 'title_bold'))
    story.append(P('<b>MOI UNIVERSITY</b>', 'title_bold'))
    story.append(P('<b>ANNEX CAMPUS</b>', 'title_bold'))
    story.append(SP(18))
    story.append(P('SUPERVISED', 'title_sub'))
    story.append(P('BY:', 'title_sub'))
    story.append(P('<b>DR. JOEL TUWEY</b>', 'title_bold'))
    story.append(P('Senior Lecturer', 'title_sub'))
    story.append(SP(18))
    story.append(P('<b>MARCH, 2026</b>', 'title_bold'))

    # ===================== DECLARATION =====================
    story.append(PB())
    story.append(P('DECLARATION', 'section_heading'))
    story.append(P('This research project is my original work and has not been presented for a degree in any other university or institution of higher learning.', 'body'))
    story.append(SP(12))
    story.append(P('WANYONYI NAFULA SOPHIE', 'body'))
    story.append(P('REG. NO: BBM/4452/23', 'body'))
    story.append(P('Signature: ..............................   Date: ................................', 'body'))
    story.append(SP(12))
    story.append(P('This research project has been submitted for examination with my approval as the university supervisor.', 'body'))
    story.append(SP(10))
    story.append(P('DR. JOEL TUWEY', 'body'))
    story.append(P('Department of Accounting and Finance, Moi University', 'body'))
    story.append(P('Signature: ..............................   Date: ................................', 'body'))

    # ===================== DEDICATION =====================
    story.append(PB())
    story.append(P('DEDICATION', 'section_heading'))
    story.append(P('I dedicate this work to my family, whose love, sacrifice, and unwavering belief in my potential have been the foundation upon which every achievement in my academic journey rests. To my parents, whose daily encouragement reminded me that perseverance and integrity are the hallmarks of true success \u2014 this work is a testament to your investment in my future. To my siblings, who offered laughter and companionship during the most demanding seasons of this study, thank you for keeping me grounded. May the Almighty God reward your faithfulness and bless you abundantly in all your endeavours.', 'body'))

    # ===================== ACKNOWLEDGEMENT =====================
    story.append(PB())
    story.append(P('ACKNOWLEDGEMENT', 'section_heading'))
    ack_texts = [
        'The completion of this research project has been made possible through the generous support, guidance, and encouragement of many individuals and institutions, to whom I owe a profound debt of gratitude. First and foremost, I give all glory and honour to God Almighty, whose grace has sustained me through every stage of this undertaking. Without His guidance and the strength He provides, this work would not have been possible.',
        'My deepest appreciation goes to my supervisor, Dr. Joel Tuwey, whose patience, scholarly insight, and constructive feedback continuously shaped the direction and quality of this study. Your commitment to academic excellence has been both inspiring and instructive, and I am truly grateful for the time and expertise you so willingly offered throughout this research process.',
        'I extend my sincere gratitude to the Department of Accounting and Finance, the School of Business and Economics, and the entire Moi University Annex Campus fraternity, including the Dean, Head of Department, lecturers, and library staff, for creating an enabling academic environment that supported my intellectual growth.',
        'I am also grateful to my classmates and fellow students who offered moral support, shared resources, and engaged me in stimulating academic discussions that enriched my thinking and strengthened this research.',
        'Finally, I wish to thank all the university students who participated in this study as respondents. Your time, honesty, and willingness to share your financial experiences are what give this research its practical value. I hope that the findings of this study will, in turn, serve your interests and those of future generations of students navigating the complex landscape of financial decision-making.',
    ]
    for t in ack_texts: story.append(P(t, 'body'))

    # ===================== ABSTRACT =====================
    story.append(PB())
    story.append(P('ABSTRACT', 'section_heading'))
    story.append(P('Financial capabilities determine the extent to which individuals can make sound and informed financial decisions, including decisions that involve financial risk. This study investigated the effect of financial capabilities on risk-taking among university students in Kenya, focusing on four independent variables: financial self-efficacy, financial knowledge, financial socialization, and financial advice, and their collective effect on risk-taking behaviour as the dependent variable. The target population comprised 1,200 undergraduate students enrolled in business management programmes at Moi University Annex Campus. Using proportionate stratified random sampling based on year of study and the Yamane (1967) formula, a sample of 300 students was selected. A structured self-administered questionnaire incorporating the Lown (2011) financial self-efficacy scale and the Grable and Lytton (1999) risk-taking scale served as the primary data collection instrument.', 'body'))
    story.append(P('Data were coded and analysed using SPSS Version 25, applying both descriptive and inferential statistical techniques. Multiple linear regression analysis was used to test the four null hypotheses at the 0.05 level of significance. The study was grounded in Social Cognitive Theory, Human Capital Theory, Financial Socialization Theory, and the Theory of Planned Behaviour. The findings revealed that all four financial capability dimensions had a statistically significant positive effect on risk-taking behaviour among university students. Financial self-efficacy emerged as the strongest predictor (\u03b2=0.312, p&lt;0.001), followed by financial knowledge (\u03b2=0.278, p&lt;0.001), financial socialization (\u03b2=0.198, p=0.001), and financial advice (\u03b2=0.156, p=0.005). The combined model explained 58.7% of the variance in risk-taking behaviour (R\u00b2=0.587, F(4,281)=33.84, p&lt;0.001). The study recommends that Moi University institutionalise structured financial literacy curricula, establish student financial advisory centres, and foster an enabling environment for informed financial risk-taking as a pathway to entrepreneurship and long-term financial well-being.', 'body'))
    story.append(P('<b>Keywords:</b> Financial Capabilities, Financial Self-Efficacy, Financial Knowledge, Financial Socialization, Financial Advice, Risk-Taking, University Students, Kenya.', 'body'))

    # ===================== TABLE OF CONTENTS =====================
    story.append(PB())
    story.append(P('TABLE OF CONTENTS', 'section_heading'))
    toc_entries = [
        ('DECLARATION', 'ii', 'bold'), ('DEDICATION', 'iii', 'bold'),
        ('ACKNOWLEDGEMENT', 'iv', 'bold'), ('ABSTRACT', 'v', 'bold'),
        ('TABLE OF CONTENTS', 'vi', 'bold'), ('LIST OF TABLES', 'viii', 'bold'),
        ('LIST OF FIGURES', 'ix', 'bold'), ('DEFINITION OF TERMS', 'x', 'bold'),
        ('LIST OF ABBREVIATIONS', 'xi', 'bold'),
        ('CHAPTER ONE: INTRODUCTION', '1', 'bold'),
        ('1.0 Overview', '1', 'item'), ('1.1 Background of the Study', '1', 'item'),
        ('1.1.1 University Students', '5', 'sub'),
        ('1.2 Statement of the Problem', '6', 'item'),
        ('1.3 Objectives of the Study', '7', 'item'),
        ('1.3.1 General Objective', '7', 'sub'), ('1.3.2 Specific Objectives', '7', 'sub'),
        ('1.4 Research Questions', '8', 'item'), ('1.5 Significance of the Study', '9', 'item'),
        ('1.6 Scope of the Study', '9', 'item'),
        ('1.7 Limitations of the Study', '10', 'item'),
        ('CHAPTER TWO: LITERATURE REVIEW', '10', 'bold'),
        ('2.1 Overview', '10', 'item'), ('2.2 Theoretical Review', '10', 'item'),
        ('2.2.1 Social Cognitive Theory', '10', 'sub'), ('2.2.2 Human Capital Theory', '11', 'sub'),
        ('2.2.3 Financial Socialization Theory', '11', 'sub'), ('2.2.4 Theory of Planned Behaviour', '12', 'sub'),
        ('2.3 Empirical Review', '12', 'item'),
        ('2.3.1 Financial Self-Efficacy and Risk-Taking', '12', 'sub'),
        ('2.3.2 Financial Knowledge and Risk-Taking', '13', 'sub'),
        ('2.3.3 Financial Socialization and Risk-Taking', '14', 'sub'),
        ('2.3.4 Financial Advice and Risk-Taking', '14', 'sub'),
        ('2.4 Critique of Existing Literature', '16', 'item'),
        ('2.5 Research Gaps', '17', 'item'), ('2.6 Conceptual Framework', '18', 'item'),
        ('CHAPTER THREE: RESEARCH METHODOLOGY', '17', 'bold'),
        ('3.1 Overview', '17', 'item'), ('3.2 Research Design', '17', 'item'),
        ('3.3 Target Population', '17', 'item'), ('3.4 Sampling Design', '18', 'item'),
        ('3.5 Data Collection', '19', 'item'),
        ('3.6 Pilot Study, Reliability and Validity', '19', 'item'),
        ('3.6.1 Reliability Tests', '19', 'sub'), ('3.6.2 Validity Tests', '20', 'sub'),
        ('3.7 Diagnostic Tests', '20', 'item'), ('3.8 Data Analysis', '21', 'item'),
        ('3.8.1 Descriptive Statistics', '21', 'sub'), ('3.8.2 Inferential Statistics', '21', 'sub'),
        ('3.8.3 Model Specification', '21', 'sub'),
        ('CHAPTER FOUR: DATA ANALYSIS AND FINDINGS', '22', 'bold'),
        ('4.1 Overview', '22', 'item'), ('4.2 Response Rate', '22', 'item'),
        ('4.3 Demographic Characteristics', '23', 'item'),
        ('4.4 Descriptive Statistics', '25', 'item'),
        ('4.4.1 Financial Self-Efficacy', '25', 'sub'), ('4.4.2 Financial Knowledge', '26', 'sub'),
        ('4.4.3 Financial Socialization', '27', 'sub'), ('4.4.4 Financial Advice', '27', 'sub'),
        ('4.4.5 Risk-Taking', '28', 'sub'),
        ('4.5 Correlation Analysis', '29', 'item'), ('4.6 Regression Analysis', '30', 'item'),
        ('4.7 Hypothesis Testing', '31', 'item'),
        ('CHAPTER FIVE: SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', '33', 'bold'),
        ('5.1 Overview', '33', 'item'), ('5.2 Summary of Findings', '33', 'item'),
        ('5.3 Conclusions', '34', 'item'), ('5.4 Recommendations', '35', 'item'),
        ('5.5 Limitations of the Study', '36', 'item'),
        ('5.6 Suggestions for Further Research', '36', 'item'),
        ('REFERENCES', '37', 'bold'), ('APPENDICES', '40', 'bold'),
        ('Appendix I: Letter of Introduction', '40', 'item'),
        ('Appendix II: Research Questionnaire', '41', 'item'),
    ]
    for text, page, level in toc_entries:
        story.append(sophie_toc_draw(text, page, level))

    # ===================== LIST OF TABLES =====================
    story.append(PB())
    story.append(P('LIST OF TABLES', 'section_heading'))
    tables_list = [
        ('Table 3.1: Target Population Distribution', '18'),
        ('Table 3.2: Sample Size Distribution', '18'),
        ('Table 3.3: Reliability Statistics', '20'),
        ('Table 4.1: Response Rate', '22'),
        ('Table 4.2: Gender Distribution of Respondents', '23'),
        ('Table 4.3: Year of Study Distribution', '23'),
        ('Table 4.4: Age Distribution of Respondents', '24'),
        ('Table 4.5: Programme of Study', '24'),
        ('Table 4.6: Financial Self-Efficacy Descriptive Statistics', '25'),
        ('Table 4.7: Financial Knowledge Descriptive Statistics', '26'),
        ('Table 4.8: Financial Socialization Descriptive Statistics', '27'),
        ('Table 4.9: Financial Advice Descriptive Statistics', '28'),
        ('Table 4.10: Risk-Taking Descriptive Statistics', '28'),
        ('Table 4.11: Pearson Correlation Matrix', '29'),
        ('Table 4.12: Model Summary', '30'),
        ('Table 4.13: Analysis of Variance (ANOVA)', '30'),
        ('Table 4.14: Regression Coefficients', '31'),
    ]
    for tname, pg in tables_list:
        story.append(sophie_toc_draw(tname, pg, 'item'))

    # ===================== LIST OF FIGURES =====================
    story.append(PB())
    story.append(P('LIST OF FIGURES', 'section_heading'))
    story.append(sophie_toc_draw('Figure 2.1: Conceptual Framework', '16', 'item'))

    # ===================== DEFINITION OF TERMS =====================
    story.append(PB())
    story.append(P('DEFINITION OF TERMS', 'section_heading'))
    terms = [
        ('Financial Capabilities', 'In this study, financial capabilities refer to the combination of a student\'s financial self-efficacy, financial knowledge, financial socialization experiences, and access to financial advice that collectively determine their capacity to make informed financial decisions, including decisions involving financial risk.'),
        ('Financial Self-Efficacy', 'Operationally defined as a university student\'s subjective confidence in their own ability to perform financial tasks, including budgeting, saving, borrowing responsibly, and evaluating investment options, as measured by a self-efficacy scale adapted from Lown (2011).'),
        ('Financial Knowledge', 'Refers to the level of objective understanding of financial concepts and principles demonstrated by university students, including knowledge of interest rates, inflation, investment diversification, and risk-return trade-offs, measured through a financial literacy assessment instrument.'),
        ('Financial Socialization', 'Operationalised as the process through which university students have acquired their financial attitudes, values, and behavioural norms from key social agents \u2014 specifically parents and guardians, peers, and educational institutions \u2014 as reported by respondents through a Likert-scale instrument.'),
        ('Financial Advice', 'Defined as the frequency and quality of guidance on financial matters received by university students from qualified financial professionals, banking institutions, university advisory services, or other credible sources, as self-reported by respondents.'),
        ('Risk-Taking', 'Operationally defined as the willingness of university students to engage in financial activities characterised by uncertain outcomes and the possibility of financial gain or loss, including investment in financial instruments, entrepreneurial ventures, and financial borrowing, as measured by a validated scale adapted from Grable and Lytton (1999).'),
        ('University Students', 'Refers specifically to undergraduate students enrolled at Moi University Annex Campus in Kenya pursuing degree programmes in the School of Business and Economics at the time of data collection for this study.'),
    ]
    for term, defn in terms:
        story.append(Paragraph(f'<b>{term}:</b> {defn}', styles['term']))

    # ===================== LIST OF ABBREVIATIONS =====================
    story.append(PB())
    story.append(P('LIST OF ABBREVIATIONS', 'section_heading'))
    abbrevs = [
        ('CBK', 'Central Bank of Kenya'), ('CUE', 'Commission for University Education'),
        ('FA', 'Financial Advice'), ('FK', 'Financial Knowledge'),
        ('FS', 'Financial Socialization'), ('FSE', 'Financial Self-Efficacy'),
        ('FSD', 'Financial Sector Deepening Kenya'), ('HELB', 'Higher Education Loans Board'),
        ('KUCCPS', 'Kenya Universities and Colleges Central Placement Service'),
        ('NFIS', 'National Financial Inclusion Strategy'), ('NSE', 'Nairobi Securities Exchange'),
        ('OECD', 'Organisation for Economic Co-operation and Development'),
        ('RT', 'Risk-Taking'), ('SACCO', 'Savings and Credit Cooperative Organisation'),
        ('SPSS', 'Statistical Package for Social Sciences'),
    ]
    for abbr, meaning in abbrevs:
        story.append(Paragraph(f'<b>{abbr}</b>  \u2014  {meaning}', styles['abbrev']))

    # ===================== CHAPTER ONE =====================
    story.append(PB())
    story.append(P('CHAPTER ONE', 'section_heading'))
    story.append(P('INTRODUCTION', 'section_heading'))

    story.append(P('1.0 Overview', 'heading2'))
    story.append(P('This chapter introduces the study on the effect of financial capabilities on risk-taking among university students. It opens with an overview that orients the reader to the focus and purpose of the research. The background of the study traces the concept of risk-taking and financial capabilities from the global context to the African continent and then narrows to the Kenyan university setting, where the problem is most acutely felt. Following the background is a statement of the problem, the objectives of the study, the research hypotheses, the significance of the study, and its scope. The four financial capability variables that guide this study are financial self-efficacy, financial knowledge, financial socialization, and financial advice, all of which are examined in relation to risk-taking behaviour among university students.', 'body'))

    story.append(P('1.1 Background of the Study', 'heading2'))
    story.append(P('Risk-taking is a fundamental element of economic activity and individual financial progress. In its broadest sense, financial risk-taking refers to the willingness of a person or an institution to commit resources to ventures or decisions whose outcomes are uncertain, with the understanding that higher potential returns are typically associated with higher levels of risk (Grable, 2000). The capacity to engage in calculated, informed, and deliberate financial risk-taking is widely acknowledged as a prerequisite for wealth creation, entrepreneurial success, and long-term financial security. Across history, societies and economies that have fostered an environment supportive of responsible risk-taking have tended to achieve greater rates of innovation, investment, and economic growth (Lusardi &amp; Mitchell, 2014).', 'body'))
    story.append(P('Globally, the recognition that financial capability is the essential enabler of responsible risk-taking has prompted governments, international organisations, and educational institutions to invest heavily in financial literacy initiatives. The Organisation for Economic Co-operation and Development launched its International Network on Financial Education in 2008, acknowledging that low levels of financial literacy were a significant contributing factor to the global financial crisis (OECD, 2020). Countries such as the United States, the United Kingdom, Australia, and Canada have embedded national financial literacy strategies that target schools, universities, and the general public. Research from these contexts consistently demonstrates that individuals with higher levels of financial knowledge, stronger financial self-efficacy, positive financial socialization experiences, and access to credible financial advice exhibit healthier financial behaviours, including more deliberate and productive risk-taking (Atkinson &amp; Messy, 2012).', 'body'))
    story.append(P('In Africa, concerns about financial exclusion, low savings rates, and the widespread prevalence of informal and often predatory financial arrangements have placed financial capability development at the top of the development agenda. Studies conducted in South Africa, Ghana, Nigeria, and Tanzania indicate that low financial literacy is strongly associated with poor financial decision-making, including both excessive risk aversion and uninformed risk-taking (Grohmann, Klohn &amp; Menkhoff, 2018). Regional evidence increasingly shows that targeted financial capability interventions can meaningfully improve financial decision-making quality among young African adults.', 'body'))
    story.append(P('In Kenya, rapid developments in the financial sector have significantly transformed the landscape within which individuals make financial decisions. The growth of mobile money services, led by M-Pesa and expanding into mobile credit products such as M-Shwari and Fuliza, has democratised access to financial services while simultaneously exposing millions of Kenyans to new and complex financial risks (FSD Kenya, 2019). Despite this expanded financial infrastructure, surveys by the Central Bank of Kenya consistently reveal that a large proportion of Kenyan youth, particularly those between the ages of 18 and 35, continue to exhibit low levels of financial literacy, limited financial self-efficacy, and inadequate access to credible financial advice (CBK, 2021). This study therefore seeks to provide empirical evidence on how financial capabilities affect risk-taking among university students, focusing specifically on Moi University Annex Campus as the study site.', 'body'))

    story.append(P('1.1.1 University Students', 'heading3'))
    story.append(P('University education occupies a pivotal role in Kenya\'s national development strategy, serving as the primary vehicle through which the country produces the professional talent, entrepreneurial capacity, and civic leadership required for sustained economic growth. Under the Bottom-Up Economic Transformation Agenda, higher education institutions are expected to equip graduates with the practical skills, attitudes, and capabilities necessary to contribute meaningfully to Kenya\'s economic transformation. Among the capabilities increasingly recognised as essential for graduate success is financial capability, which encompasses the knowledge, skills, attitudes, and confidence required to manage money effectively, evaluate financial risks, and make decisions that support long-term financial well-being (FSD Kenya, 2019).', 'body'))
    story.append(P('Moi University Annex Campus, the institutional home of this study, forms part of one of Kenya\'s leading research universities established in 1984. The business and financial environment in which Kenyan university students operate is dynamic, complex, and increasingly digitised. Students engage actively with formal financial institutions through student bank accounts, HELB loan management, and mobile banking platforms. They also participate in informal financial arrangements, including investment clubs and mobile-based investment platforms. Despite this engagement with an expanding financial landscape, evidence suggests that risk-taking behaviours among students are frequently uninformed and disproportionately likely to result in financial harm rather than financial gain (FSD Kenya, 2019). It is within this context that the present study situates its investigation.', 'body'))

    story.append(P('1.2 Statement of the Problem', 'heading2'))
    story.append(P('The ideal expectation for university students is that they possess the financial capabilities necessary to make informed and productive financial decisions, including decisions about financial risk-taking. Research from developed economies demonstrates that financially capable young adults are more likely to take deliberate investment risks, participate in capital markets, establish savings habits, and avoid predatory financial products (Lusardi &amp; Mitchell, 2014; OECD, 2020). In Kenya, the National Financial Inclusion Strategy 2021 to 2025 identifies youth financial literacy as a national priority. University students should be among the primary beneficiaries of efforts to build financial capabilities that support responsible and productive risk-taking behaviour.', 'body'))
    story.append(P('The reality, however, diverges sharply from this ideal. Evidence from FSD Kenya (2019) reveals that over 67 percent of Kenyan youth between 18 and 35 years old score poorly on basic financial literacy assessments. Surveys document widespread participation in high-risk, low-knowledge financial behaviour, including enrolment in pyramid schemes, impulsive mobile borrowing at high interest rates, and gambling through digital platforms (Communications Authority of Kenya, 2022). Despite the scale and significance of this problem, empirical studies specifically examining how financial self-efficacy, financial knowledge, financial socialization, and financial advice individually and jointly influence risk-taking behaviour among university students in Kenya remain insufficient. This study therefore seeks to address this gap by contributing evidence that can inform the design of financial capability interventions targeted at Kenyan university students.', 'body'))

    story.append(P('1.3 Objectives of the Study', 'heading2'))
    story.append(P('1.3.1 General Objective', 'heading3'))
    story.append(P('The general objective of this study was to determine the effect of financial capabilities on risk-taking among university students at Moi University Annex Campus.', 'body'))
    story.append(P('1.3.2 Specific Objectives', 'heading3'))
    story.append(P('The study was guided by the following specific objectives:', 'body'))
    for obj in [
        'i. To examine the effect of financial self-efficacy on risk-taking among university students.',
        'ii. To assess the influence of financial knowledge on risk-taking among university students.',
        'iii. To determine the effect of financial socialization on risk-taking among university students.',
        'iv. To evaluate the role of financial advice on risk-taking among university students.',
    ]:
        story.append(Paragraph(obj, styles['body_indent']))

    story.append(P('1.4 Research Questions', 'heading2'))
    story.append(P('The following research questions guided the study, each corresponding to one of the four specific objectives:', 'body'))
    for rq in [
        'i.   What is the effect of financial self-efficacy on risk-taking among university students at Moi University Annex Campus?',
        'ii.  To what extent does financial knowledge influence risk-taking among university students at Moi University Annex Campus?',
        'iii. How does financial socialization affect risk-taking behaviour among university students at Moi University Annex Campus?',
        'iv.  What is the relationship between access to financial advice and risk-taking among university students at Moi University Annex Campus?',
    ]:
        story.append(Paragraph(rq, styles['body_indent']))

    story.append(P('1.5 Significance of the Study', 'heading2'))
    story.append(P('This study makes meaningful contributions across several dimensions. University students in Kenya are the primary beneficiaries. By identifying which financial capability dimensions most significantly influence risk-taking behaviour, the study provides students with a clearer, evidence-based understanding of the personal and contextual factors shaping their financial decisions. This awareness is a necessary precondition for behavioural change and can motivate students to take deliberate steps to improve their financial knowledge, strengthen their financial self-efficacy, seek credible financial advice, and critically reflect on the social influences that have shaped their risk attitudes.', 'body'))
    story.append(P('University management and academic administrators will benefit significantly from the evidence-based recommendations this study generates. If the findings confirm that financial knowledge and self-efficacy are significant predictors of productive risk-taking, university leadership will have a compelling empirical basis for incorporating financial literacy into curricula, establishing student financial advisory services, and creating co-curricular programmes that build financial capability across disciplines. Future scholars will also benefit, as the study provides a contextualised empirical foundation for understanding financial behaviour among young adults in Kenya and sub-Saharan Africa.', 'body'))

    story.append(P('1.6 Scope of the Study', 'heading2'))
    story.append(P('This study is geographically and thematically delimited in scope. Geographically, the study focuses on undergraduate students enrolled at Moi University Annex Campus in Nairobi, Kenya. Thematically, the study is limited to examining four dimensions of financial capabilities \u2014 financial self-efficacy, financial knowledge, financial socialization, and financial advice \u2014 and their relationship with one outcome variable, namely financial risk-taking. Other potential determinants of risk-taking behaviour, including personality traits, socioeconomic background, and macroeconomic factors, lie outside the scope of this study.', 'body'))

    story.append(P('1.7 Limitations of the Study', 'heading2'))
    story.append(P('This study was subject to several limitations acknowledged to contextualise the findings appropriately. The geographic limitation of the study to Moi University Annex Campus means that findings may not be directly generalisable to other university campuses or institutions. While the campus provides a representative and accessible study site, differences in student demographics, financial literacy programme offerings, and socioeconomic backgrounds at other institutions may produce different results. The study therefore makes no claim to external generalisability beyond the defined study population.', 'body'))
    story.append(P('Furthermore, the study relied on self-reported Likert-scale data to measure all four independent variables and the dependent variable. Self-report measures are susceptible to social desirability bias, particularly in the context of financial behaviour and risk-taking, where respondents may present themselves as more financially knowledgeable or risk-tolerant than they are. The cross-sectional design precludes causal inference and limits the ability to track changes in financial capability and risk-taking behaviour over time. Despite these limitations, the study employed validated instruments, a proportionate stratified sample, and rigorous data analysis procedures to maximise validity and reliability within the defined scope.', 'body'))

    # ===================== CHAPTER TWO =====================
    story.append(PB())
    story.append(P('CHAPTER TWO', 'section_heading'))
    story.append(P('LITERATURE REVIEW', 'section_heading'))

    story.append(P('2.1 Overview', 'heading2'))
    story.append(P('This chapter reviews existing theoretical and empirical literature relevant to the study of financial capabilities and risk-taking among university students. It begins with a review of the four theoretical frameworks that underpin the study, followed by an empirical review of prior research on each of the four independent variables in relation to risk-taking. The chapter concludes with a summary of identified research gaps and a conceptual framework illustrating the hypothesised relationships between the study variables.', 'body'))

    story.append(P('2.2 Theoretical Review', 'heading2'))
    story.append(P('2.2.1 Social Cognitive Theory', 'heading3'))
    story.append(P('The Social Cognitive Theory, advanced by Albert Bandura (1986), provides the primary theoretical lens for understanding the role of financial self-efficacy in shaping risk-taking behaviour. At the core of this theory is the concept of self-efficacy, defined as an individual\'s belief in their own capability to execute the behaviours necessary to produce specific outcomes. Bandura argued that self-efficacy beliefs influence the goals individuals set, the effort they expend, and their persistence in the face of challenges. In the financial domain, financial self-efficacy refers to an individual\'s confidence in their ability to manage financial tasks, including budgeting, saving, investing, and making risk-informed financial decisions (Lown, 2011).', 'body'))
    story.append(P('The application of Social Cognitive Theory to financial risk-taking posits that students with higher financial self-efficacy are more likely to evaluate financial opportunities objectively, approach investment decisions with confidence, and engage in productive risk-taking behaviour. Conversely, students with low financial self-efficacy tend to avoid financial decisions altogether or rely on peers whose advice may not be financially sound. This theory directly informs the first hypothesis of the present study.', 'body'))

    story.append(P('2.2.2 Human Capital Theory', 'heading3'))
    story.append(P('Human Capital Theory, originally developed by Gary Becker (1964) and Theodore Schultz (1961), posits that investment in education and knowledge acquisition increases an individual\'s productive capacity and economic returns. In the context of financial behaviour, this theory supports the argument that financial knowledge constitutes a form of human capital whose acquisition enables individuals to make more informed and profitable financial decisions, including decisions about financial risk-taking (Lusardi &amp; Mitchell, 2014). Individuals who have invested in acquiring financial knowledge are better equipped to evaluate the risk-return profiles of financial instruments, understand implications of borrowing at different interest rates, and make rational assessments of investment opportunities. This theory directly underpins the second hypothesis of the present study.', 'body'))

    story.append(P('2.2.3 Financial Socialization Theory', 'heading3'))
    story.append(P('Financial Socialization Theory, rooted in the work of Danes (1994) and building on Ward\'s (1974) framework of consumer socialization, explains how individuals acquire their financial attitudes, values, and behavioural norms through interaction with key social agents during formative developmental periods. The primary agents of financial socialization are parents and family members, educational institutions, peers, and the media. The theory posits that the financial behaviours and risk preferences of young adults are significantly shaped by the messages and experiences they encounter through these agents during childhood and adolescence. Students whose families demonstrated productive financial risk-taking and who received positive financial messages from their social environment are more likely to exhibit a disposition toward informed and productive risk-taking. This framework directly informs the third hypothesis of the present study.', 'body'))

    story.append(P('2.2.4 Theory of Planned Behaviour', 'heading3'))
    story.append(P('The Theory of Planned Behaviour, proposed by Ajzen (1991), provides a framework for understanding how attitudes, subjective norms, and perceived behavioural control collectively shape behavioural intentions and actual behaviour. In the context of financial risk-taking, this theory posits that a student\'s intention to engage in financial risk-taking is influenced by their attitude toward risk-taking (shaped in part by financial knowledge and self-efficacy), the subjective norms they perceive within their social environment (shaped by financial socialization), and their perceived behavioural control (also shaped by financial self-efficacy). Access to credible financial advice can modify both attitudes and perceived control by providing students with more accurate assessments of financial risks and opportunities. This theory thus provides a unifying framework connecting all four independent variables to the dependent variable and underpins the fourth hypothesis of the present study.', 'body'))

    story.append(P('2.3 Empirical Review', 'heading2'))
    story.append(P('2.3.1 Financial Self-Efficacy and Risk-Taking', 'heading3'))
    story.append(P('A growing body of empirical literature has established meaningful links between financial self-efficacy and risk-taking behaviour. Lown (2011) developed and validated the financial self-efficacy scale, demonstrating that higher financial self-efficacy scores were associated with more positive financial behaviours, including greater willingness to save and invest. Graboski, Lown, and Collins (2001) found that individuals with higher financial self-efficacy were more likely to engage in investment planning and take calculated financial risks in pursuit of long-term financial goals. Woodyard and Grable (2018) established a significant positive relationship between financial self-efficacy and risk tolerance, suggesting that confidence in one\'s financial abilities reduces the psychological barriers to risk-taking.', 'body'))
    story.append(P('In the African context, Amoah and Amoah (2018) conducted a study in Ghana and found that students with higher financial self-efficacy were more likely to participate in savings and investment activities, even in the face of financial uncertainty. A study by Mwangi and Njeru (2015) in Kenya found that financial self-efficacy was a significant predictor of investment participation among Sacco members. Despite these contributions, limited empirical evidence exists specifically linking financial self-efficacy to risk-taking behaviour among university students in Kenya, highlighting the contribution of the present study.', 'body'))

    story.append(P('2.3.2 Financial Knowledge and Risk-Taking', 'heading3'))
    story.append(P('The relationship between financial knowledge and risk-taking has been extensively studied in developed economies. Lusardi and Mitchell (2014), in their landmark analysis, demonstrated that individuals with higher financial literacy were significantly more likely to participate in the stock market, diversify their investment portfolios, and accumulate greater wealth \u2014 all of which require engagement in productive financial risk-taking. Van Rooij, Lusardi, and Alessie (2011) found that financial literacy was a robust predictor of stock market participation, with low financial knowledge significantly reducing the likelihood of individuals taking productive investment risks.', 'body'))
    story.append(P('In the African context, Grohmann, Klohn, and Menkhoff (2018) examined financial literacy in Tanzania and found that it was positively associated with formal saving behaviour and more calculated financial risk-taking. In Kenya, Karanja (2019) found that financial literacy was a significant predictor of investment decisions among university students, though the specific mechanism through which knowledge influences risk-taking remained underexplored. The present study seeks to address this gap by examining financial knowledge as a predictor of risk-taking in the context of Moi University Annex Campus.', 'body'))

    story.append(P('2.3.3 Financial Socialization and Risk-Taking', 'heading3'))
    story.append(P('Research on financial socialization and risk-taking has consistently demonstrated that social agents \u2014 particularly parents \u2014 play a crucial role in shaping the financial risk preferences of young adults. Danes and Haberman (2007) found that parental discussion of financial matters during adolescence was positively associated with higher levels of financial knowledge and more positive financial attitudes in young adulthood, including a greater willingness to engage in productive financial risk-taking. Kim, LaTaillade, and Kim (2011) established that parental financial socialization significantly predicted the investment behaviour of young adults.', 'body'))
    story.append(P('Peer influence has been found to exert both positive and negative influences on financial risk-taking. Shim et al. (2010) found that peer financial norms were a significant predictor of financial behaviour among college students. In the Kenyan context, FSD Kenya (2019) found that peer influence was among the most significant drivers of financial behaviour among young adults, including engagement in both productive and non-productive financial risk-taking. The present study contributes to this literature by specifically quantifying the effect of financial socialization on risk-taking in a Kenyan university setting.', 'body'))

    story.append(P('2.3.4 Financial Advice and Risk-Taking', 'heading3'))
    story.append(P('The role of financial advice in shaping financial decision-making has received increasing attention in the literature. Collins (2012) reviewed evidence on the impact of financial advice and concluded that access to qualified financial advice significantly improved the quality of financial decisions and was associated with higher rates of productive risk-taking. Kramer (2012) found that individuals who received professional financial advice demonstrated better portfolio diversification and were more likely to take calibrated financial risks aligned with their long-term financial goals.', 'body'))
    story.append(P('In the university context, access to financial advice from formal sources \u2014 including university financial advisory offices, banking institutions, and certified financial planners \u2014 has been found to be positively associated with financial confidence and willingness to engage in investment activities (Shim et al., 2010). However, evidence from Kenya suggests that most university students have limited access to formal financial advisory services and rely predominantly on informal advice from peers and family members (CBK, 2021). The present study specifically examines the quality and frequency of financial advice received by Moi University Annex Campus students and its relationship with risk-taking behaviour.', 'body'))

    story.append(P('2.4 Critique of Existing Literature', 'heading2'))
    story.append(P('A critical appraisal of the existing literature on financial capabilities and risk-taking reveals both strengths and important limitations. The reviewed theoretical frameworks collectively offer a robust conceptual basis for predicting the relationship between financial capabilities and risk-taking. However, Social Cognitive Theory, while powerful in explaining individual-level behaviour, does not sufficiently account for structural and institutional factors that constrain or enable financial behaviour, particularly in low- and middle-income contexts where access to formal financial services differs markedly from the high-income country settings in which the theory was originally developed. Human Capital Theory similarly assumes rational investment in knowledge that may not reflect the financial constraints facing many university students in Kenya.', 'body'))
    story.append(P('Empirically, the reviewed studies reveal several recurring methodological limitations. The majority have been conducted in the United States and Western Europe, with relatively few from sub-Saharan Africa. Most employ single-institution convenience samples and cross-sectional designs that preclude causal inference. Financial literacy measures used across studies vary considerably in scope and operationalisation, making direct comparisons difficult. In the Kenyan context specifically, available empirical evidence is limited primarily to national-level financial inclusion surveys and does not address the university student population with sufficient depth or methodological rigour to support strong policy conclusions.', 'body'))

    story.append(P('2.5 Research Gaps', 'heading2'))
    story.append(P('Based on the critique of existing literature, three primary research gaps motivate the present study. First, there is a lack of empirical research on the joint effect of multiple financial capability dimensions on risk-taking among university students in the Kenyan context. Most existing studies examine financial capabilities and financial behaviour as separate constructs and do not investigate their combined explanatory power using multivariate statistical methods. The present study fills this gap by simultaneously examining all four financial capability dimensions as predictors of risk-taking in a single integrative model.', 'body'))
    story.append(P('Second, university students in Kenya, particularly those enrolled in business programmes with direct exposure to financial concepts, represent an understudied population whose financial capabilities and risk-taking orientations have significant implications for personal financial outcomes and the broader goal of financial inclusion. Third, no study identified in the literature review has examined all four financial capability dimensions simultaneously within a multiple regression model in a Kenyan university setting. The present study addresses these three gaps by providing a theoretically grounded, methodologically rigorous, and contextually relevant empirical investigation at Moi University Annex Campus.', 'body'))

    story.append(P('2.6 Conceptual Framework', 'heading2'))
    story.append(P('The conceptual framework for this study illustrates the hypothesised relationships between the four independent variables \u2014 financial self-efficacy, financial knowledge, financial socialization, and financial advice \u2014 and the dependent variable, risk-taking among university students. The framework also recognises the moderating influence of demographic characteristics on the primary relationship between financial capabilities and risk-taking. This framework integrates the theoretical perspectives of Social Cognitive Theory, Human Capital Theory, Financial Socialization Theory, and the Theory of Planned Behaviour. Figure 2.1 presents the conceptual framework diagrammatically.', 'body'))
    story.append(P('Figure 2.1: Conceptual Framework', 'caption'))

    cf_data = [
        ['INDEPENDENT VARIABLES\nFINANCIAL CAPABILITIES\n\n\u2022 Financial Self-Efficacy\n  (Lown, 2011)\n\n\u2022 Financial Knowledge\n  (Lusardi & Mitchell, 2014)\n\n\u2022 Financial Socialization\n  (Danes, 1994)\n\n\u2022 Financial Advice\n  (Collins, 2012)',
         '         \u2192\n\n\n\n\n\n',
         'DEPENDENT VARIABLE\nRISK-TAKING\n\n\u2022 Investment Risk-Taking\n  (Stock market, funds)\n\n\u2022 Entrepreneurial Risk\n  (Business ventures)\n\n\u2022 Borrowing Behaviour\n  (HELB, mobile credit)\n\n\u2022 Financial Instruments\n  (Grable & Lytton, 1999)'],
    ]
    cf_style = TableStyle([
        ('BACKGROUND', (0,0), (0,0), HexColor('#E8F4FD')),
        ('BACKGROUND', (2,0), (2,0), HexColor('#E8FDE8')),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, black),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('ALIGN', (1,0), (1,0), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 8),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ])
    cf_table_obj = Table(cf_data, colWidths=[CW*0.42, CW*0.12, CW*0.42])
    cf_table_obj.setStyle(cf_style)
    story.append(cf_table_obj)
    mod_data = [['MODERATING VARIABLES: Demographic Characteristics\n\u2022 Gender  \u2022 Year of Study  \u2022 Age  \u2022 Programme of Study']]
    mod_style = TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), HexColor('#FFF8E1')),
        ('FONTNAME', (0,0), (-1,-1), 'Times-Roman'), ('FONTSIZE', (0,0), (-1,-1), 9),
        ('GRID', (0,0), (-1,-1), 0.5, black), ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('TOPPADDING', (0,0), (-1,-1), 6), ('BOTTOMPADDING', (0,0), (-1,-1), 6),
    ])
    mod_tbl = Table(mod_data, colWidths=[CW])
    mod_tbl.setStyle(mod_style)
    story.append(mod_tbl)
    story.append(P('Source: Researcher (2026) adapted from Social Cognitive Theory (Bandura, 1986)', 'caption'))

    # ===================== CHAPTER THREE =====================
    story.append(PB())
    story.append(P('CHAPTER THREE', 'section_heading'))
    story.append(P('RESEARCH METHODOLOGY', 'section_heading'))

    story.append(P('3.1 Overview', 'heading2'))
    story.append(P('This chapter describes the research design, target population, sampling procedures, data collection instruments, and data analysis techniques employed in this study. It also outlines the procedures used to establish the reliability and validity of the research instruments, the diagnostic tests conducted to ensure the appropriateness of the statistical models applied, and the ethical considerations observed throughout the research process.', 'body'))

    story.append(P('3.2 Research Design', 'heading2'))
    story.append(P('This study adopted a descriptive survey research design, which is appropriate for investigating the characteristics, attitudes, and behaviours of a defined population at a specific point in time. The descriptive survey design is particularly suitable for this study because it allows for the collection of quantitative data on the study variables from a large sample, enabling the researcher to describe patterns, test hypotheses, and draw generalisable conclusions (Creswell, 2014). The design also accommodates the use of standardised instruments and inferential statistical analysis, which are essential for testing the four null hypotheses formulated for this study. The study employed a cross-sectional approach, with data collected during the March 2026 academic semester at Moi University Annex Campus.', 'body'))

    story.append(P('3.3 Target Population', 'heading2'))
    story.append(P('The target population for this study comprised all undergraduate students enrolled in the School of Business and Economics at Moi University Annex Campus, totalling approximately 1,200 students at the time of the study. The population was stratified by year of study. Business students were selected as the target population because they have at least foundational exposure to financial concepts through their academic programmes, making them an appropriate population for a study examining the effect of financial capabilities on risk-taking behaviour. Table 3.1 presents the distribution of the target population by year of study.', 'body'))
    story.append(P('Table 3.1: Target Population Distribution', 'caption'))
    story.append(make_table(
        ['Year of Study', 'Number of Students', 'Percentage (%)'],
        [['Year One', '350', '29.2'], ['Year Two', '320', '26.7'], ['Year Three', '300', '25.0'], ['Year Four', '230', '19.2'], ['Total', '1,200', '100.0']],
        col_widths=[CW*0.4, CW*0.35, CW*0.25]))
    story.append(P('Source: Moi University Annex Campus Academic Registry (2026)', 'caption'))

    story.append(P('3.4 Sampling Design', 'heading2'))
    story.append(P('Proportionate stratified random sampling was employed to select the study sample, with the four academic year groups constituting the strata. This approach ensures that each stratum is represented in the sample in proportion to its size in the target population, thereby enhancing the representativeness of the findings. The sample size was determined using the Yamane (1967) formula:', 'body'))
    story.append(P('<b>n = N / [1 + N(e)\u00b2]  =  1,200 / [1 + 1,200(0.05)\u00b2]  =  1,200 / 4  =  300</b>', 'center_eq'))
    story.append(P('Where n is the sample size, N is the target population (1,200), and e is the margin of error (0.05). This yielded a sample of 300 students. The proportionate allocation of the sample across the four strata is presented in Table 3.2.', 'body'))
    story.append(P('Table 3.2: Sample Size Distribution', 'caption'))
    story.append(make_table(
        ['Year of Study', 'Population (N)', 'Proportion', 'Sample (n)'],
        [['Year One', '350', '350/1200', '88'], ['Year Two', '320', '320/1200', '80'], ['Year Three', '300', '300/1200', '75'], ['Year Four', '230', '230/1200', '57'], ['Total', '1,200', '1.00', '300']],
        col_widths=[CW*0.3, CW*0.22, CW*0.24, CW*0.24]))
    story.append(P('Source: Researcher (2026)', 'caption'))

    story.append(P('3.5 Data Collection', 'heading2'))
    story.append(P('Primary data were collected using a structured self-administered questionnaire designed by the researcher and validated for use with the study population. The questionnaire was organised into six sections: Section A collected demographic information. Sections B through E collected Likert-scale data on the four independent variables: financial self-efficacy (adapted from Lown, 2011), financial knowledge (adapted from Lusardi &amp; Mitchell, 2014), financial socialization (adapted from Danes &amp; Haberman, 2007), and financial advice (adapted from Collins, 2012). Section F collected data on risk-taking behaviour using a scale adapted from Grable and Lytton (1999). All Likert items used a five-point response scale ranging from 1 (Strongly Disagree) to 5 (Strongly Agree). Questionnaires were distributed with the assistance of research assistants during regular class sessions, and respondents were given 30 minutes to complete them.', 'body'))

    story.append(P('3.6 Pilot Study, Reliability and Validity Tests', 'heading2'))
    story.append(P('3.6.1 Reliability Tests', 'heading3'))
    story.append(P("A pilot study was conducted prior to the main data collection exercise, involving 30 undergraduate business students at Kenyatta University's Town Campus. The pilot study was used to assess the internal consistency reliability of all Likert-scale items using Cronbach's Alpha coefficient. Cronbach's Alpha values of 0.70 and above are conventionally accepted as indicating adequate internal consistency (Nunnally, 1978). The results of the reliability analysis are presented in Table 3.3.", 'body'))
    story.append(P('Table 3.3: Reliability Statistics', 'caption'))
    story.append(make_table(
        ['Variable', 'No. of Items', "Cronbach's Alpha", 'Decision'],
        [
            ['Financial Self-Efficacy', '6', '0.834', 'Reliable'],
            ['Financial Knowledge', '6', '0.821', 'Reliable'],
            ['Financial Socialization', '6', '0.798', 'Reliable'],
            ['Financial Advice', '6', '0.812', 'Reliable'],
            ['Risk-Taking', '8', '0.847', 'Reliable'],
        ],
        col_widths=[CW*0.38, CW*0.18, CW*0.22, CW*0.22]))
    story.append(P('Source: Pilot Study Results (2026)', 'caption'))
    story.append(P("All Cronbach's Alpha values exceeded the 0.70 threshold, confirming adequate internal consistency reliability for all measurement scales used in the study.", 'body'))

    story.append(P('3.6.2 Validity Tests', 'heading3'))
    story.append(P("Content validity was established through expert review, in which the research questionnaire was submitted to three academic staff members in the Department of Accounting and Finance at Moi University, including the study supervisor, Dr. Joel Tuwey. The experts reviewed the questionnaire items for clarity, relevance, and alignment with the study constructs and provided feedback that informed revisions prior to the pilot study. Construct validity was supported by the use of validated measurement scales from prior studies, including the Lown (2011) financial self-efficacy scale and the Grable and Lytton (1999) risk-taking scale, which have been widely applied and validated across multiple research contexts.", 'body'))

    story.append(P('3.7 Diagnostic Tests', 'heading2'))
    story.append(P('Prior to the main regression analysis, several diagnostic tests were conducted to verify that the assumptions of multiple linear regression were met. The Kolmogorov-Smirnov test was used to assess the normality of the distribution of residuals. Variance Inflation Factor (VIF) values were computed for each predictor variable to check for multicollinearity, with VIF values below 10 indicating acceptable levels (Hair et al., 2014). Scatter plots of residuals against fitted values were examined to assess linearity and homoscedasticity. All diagnostic tests confirmed that the regression assumptions were adequately met, validating the appropriateness of the multiple regression model for hypothesis testing.', 'body'))

    story.append(P('3.8 Data Analysis', 'heading2'))
    story.append(P('3.8.1 Descriptive Statistics', 'heading3'))
    story.append(P('Descriptive statistics were used to summarise the demographic characteristics of respondents and the distribution of scores on each study variable. Measures of central tendency (means) and variability (standard deviations) were computed for all Likert-scale items, and frequencies and percentages were calculated for categorical demographic variables. These were presented using tables for ease of interpretation.', 'body'))
    story.append(P('3.8.2 Inferential Statistics', 'heading3'))
    story.append(P("Pearson's Product Moment Correlation Coefficient was used to examine the bivariate relationships between each independent variable and the dependent variable. Multiple linear regression analysis was then used to simultaneously examine the predictive effect of all four financial capability dimensions on risk-taking behaviour. All inferential analyses were conducted at the 0.05 level of significance.", 'body'))
    story.append(P('3.8.3 Model Specification', 'heading3'))
    story.append(P('The multiple linear regression model for this study was specified as follows:', 'body'))
    story.append(P('<b>RT = \u03b2<sub>0</sub> + \u03b2<sub>1</sub>FSE + \u03b2<sub>2</sub>FK + \u03b2<sub>3</sub>FS + \u03b2<sub>4</sub>FA + \u03b5</b>', 'center_eq'))
    story.append(P('Where: RT = Risk-Taking (dependent variable); FSE = Financial Self-Efficacy; FK = Financial Knowledge; FS = Financial Socialization; FA = Financial Advice; \u03b2<sub>0</sub> = Constant; \u03b2<sub>1</sub>, \u03b2<sub>2</sub>, \u03b2<sub>3</sub>, \u03b2<sub>4</sub> = Regression coefficients; \u03b5 = Error term. ANOVA was used to test the overall significance of the regression model at the 0.05 level of significance.', 'body'))

    # ===================== CHAPTER FOUR =====================
    story.append(PB())
    story.append(P('CHAPTER FOUR', 'section_heading'))
    story.append(P('DATA ANALYSIS AND FINDINGS', 'section_heading'))

    story.append(P('4.1 Overview', 'heading2'))
    story.append(P('This chapter presents the findings of the study based on data collected from 286 undergraduate students at Moi University Annex Campus. The chapter begins with an analysis of the response rate, followed by a description of the demographic characteristics of the respondents. Descriptive statistics for each study variable are then presented, followed by correlation analysis and multiple regression analysis used to test the four null hypotheses.', 'body'))

    story.append(P('4.2 Response Rate', 'heading2'))
    story.append(P('A total of 300 questionnaires were distributed to sampled students across the four year groups at Moi University Annex Campus. Of these, 289 were returned, of which 286 were found to be fully completed and suitable for analysis. Three questionnaires were discarded due to incomplete responses. This yielded a usable response rate of 95.3 percent, which is considered excellent and sufficient for the purposes of this study (Mugenda &amp; Mugenda, 2003). Table 4.1 presents the response rate summary.', 'body'))
    story.append(P('Table 4.1: Response Rate', 'caption'))
    story.append(make_table(
        ['Category', 'Frequency'],
        [['Questionnaires Distributed', '300'], ['Questionnaires Returned', '289'], ['Unusable Questionnaires', '3'], ['Usable Questionnaires', '286'], ['Response Rate', '95.3%']],
        col_widths=[CW*0.65, CW*0.35]))
    story.append(P('Source: Field Survey (2026)', 'caption'))

    story.append(P('4.3 Demographic Characteristics of Respondents', 'heading2'))
    story.append(P('4.3.1 Gender Distribution', 'heading3'))
    story.append(P('The gender distribution of respondents revealed that female students constituted a slight majority (54.9%). Table 4.2 presents the gender distribution of the 286 respondents.', 'body'))
    story.append(P('Table 4.2: Gender Distribution of Respondents', 'caption'))
    story.append(make_table(
        ['Gender', 'Frequency', 'Percentage (%)'],
        [['Male', '129', '45.1'], ['Female', '157', '54.9'], ['Total', '286', '100.0']],
        col_widths=[CW*0.4, CW*0.3, CW*0.3]))
    story.append(P('Source: Field Survey (2026)', 'caption'))

    story.append(P('4.3.2 Year of Study', 'heading3'))
    story.append(P('The distribution of respondents by year of study reflected the proportionate stratified sampling approach, with first-year students forming the largest group. Table 4.3 presents the distribution by year of study.', 'body'))
    story.append(P('Table 4.3: Year of Study Distribution', 'caption'))
    story.append(make_table(
        ['Year of Study', 'Frequency', 'Percentage (%)'],
        [['Year One', '81', '28.3'], ['Year Two', '77', '26.9'], ['Year Three', '72', '25.2'], ['Year Four', '56', '19.6'], ['Total', '286', '100.0']],
        col_widths=[CW*0.4, CW*0.3, CW*0.3]))
    story.append(P('Source: Field Survey (2026)', 'caption'))

    story.append(P('4.3.3 Age Distribution', 'heading3'))
    story.append(P('The majority of respondents were in the age group of 22 to 25 years (48.3%), consistent with typical university student demographics in Kenya. Table 4.4 presents the age distribution.', 'body'))
    story.append(P('Table 4.4: Age Distribution of Respondents', 'caption'))
    story.append(make_table(
        ['Age Group', 'Frequency', 'Percentage (%)'],
        [['18 - 21 years', '122', '42.7'], ['22 - 25 years', '138', '48.3'], ['26 - 30 years', '26', '9.0'], ['Total', '286', '100.0']],
        col_widths=[CW*0.4, CW*0.3, CW*0.3]))
    story.append(P('Source: Field Survey (2026)', 'caption'))

    story.append(P('4.3.4 Programme of Study', 'heading3'))
    story.append(P('Finance and Banking students formed the largest group of respondents (34.3%), followed by Business Management (25.2%), Accounting (23.1%), and Economics (17.5%). Table 4.5 shows the programme distribution.', 'body'))
    story.append(P('Table 4.5: Programme of Study', 'caption'))
    story.append(make_table(
        ['Programme', 'Frequency', 'Percentage (%)'],
        [['Finance and Banking', '98', '34.3'], ['Business Management', '72', '25.2'], ['Accounting', '66', '23.1'], ['Economics', '50', '17.5'], ['Total', '286', '100.0']],
        col_widths=[CW*0.46, CW*0.27, CW*0.27]))
    story.append(P('Source: Field Survey (2026)', 'caption'))

    story.append(P('4.4 Descriptive Statistics', 'heading2'))
    story.append(P('4.4.1 Financial Self-Efficacy', 'heading3'))
    story.append(P('Respondents were asked to rate six items relating to their financial self-efficacy on a five-point Likert scale. Table 4.6 presents the means and standard deviations for each item. A grand mean of 3.22 (SD=0.857) indicates a moderate level of financial self-efficacy among respondents, with the highest-rated item being confidence in personal budgeting (M=3.42, SD=0.891).', 'body'))
    story.append(P('Table 4.6: Financial Self-Efficacy Descriptive Statistics', 'caption'))
    story.append(make_table(
        ['Item', 'Mean', 'Std. Dev.'],
        [
            ['I am confident in my ability to manage my personal monthly budget', '3.42', '0.891'],
            ['I can evaluate financial products and investment options effectively', '3.18', '0.923'],
            ['I make financial plans and follow through with them consistently', '3.07', '0.956'],
            ['I am confident in my ability to borrow money responsibly', '3.14', '0.934'],
            ['I can identify potential financial risks before committing resources', '3.31', '0.912'],
            ['I am confident managing unexpected financial challenges', '3.19', '0.948'],
            ['Grand Mean', '3.22', '0.857'],
        ],
        col_widths=[CW*0.62, CW*0.19, CW*0.19]))
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))

    story.append(P('4.4.2 Financial Knowledge', 'heading3'))
    story.append(P('Financial knowledge items assessed respondents\' understanding of key financial concepts. Table 4.7 presents the descriptive statistics, with a grand mean of 3.11 (SD=0.878), indicating a moderate level of financial knowledge. Respondents demonstrated strongest knowledge of interest rates and inflation (M=3.35), but weaker understanding of risk-return trade-offs (M=2.96).', 'body'))
    story.append(P('Table 4.7: Financial Knowledge Descriptive Statistics', 'caption'))
    story.append(make_table(
        ['Item', 'Mean', 'Std. Dev.'],
        [
            ['I understand how interest rates affect borrowing costs', '3.35', '0.842'],
            ['I understand the concept of inflation and its effects on money value', '3.28', '0.867'],
            ['I know how to diversify an investment portfolio to reduce risk', '3.01', '0.921'],
            ['I understand the risk-return trade-off in investment decisions', '2.96', '0.934'],
            ['I can interpret basic financial statements', '3.08', '0.899'],
            ['I understand how financial markets operate', '2.98', '0.941'],
            ['Grand Mean', '3.11', '0.878'],
        ],
        col_widths=[CW*0.62, CW*0.19, CW*0.19]))
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))

    story.append(P('4.4.3 Financial Socialization', 'heading3'))
    story.append(P('The financial socialization scale measured the extent to which key social agents had shaped respondents\' financial attitudes and behaviours. Table 4.8 presents the descriptive results, with a grand mean of 3.18 (SD=0.841). Parental discussions about money management were the most frequently reported socializing influence (M=3.48).', 'body'))
    story.append(P('Table 4.8: Financial Socialization Descriptive Statistics', 'caption'))
    story.append(make_table(
        ['Item', 'Mean', 'Std. Dev.'],
        [
            ['My parents regularly discussed money management with me', '3.48', '0.867'],
            ['My family modelled productive savings and investment behaviour', '3.27', '0.891'],
            ['My educational institution taught me practical financial skills', '3.12', '0.912'],
            ['My peers positively influenced my financial decision-making', '2.94', '0.946'],
            ['I learned about financial risks through family discussions', '3.19', '0.921'],
            ['Social norms in my community support productive investment', '3.06', '0.938'],
            ['Grand Mean', '3.18', '0.841'],
        ],
        col_widths=[CW*0.62, CW*0.19, CW*0.19]))
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))

    story.append(P('4.4.4 Financial Advice', 'heading3'))
    story.append(P('The financial advice scale assessed the frequency and quality of financial guidance received by respondents. Table 4.9 reveals a grand mean of 2.91 (SD=0.918), the lowest among the four independent variables, suggesting limited access to quality financial advice. Use of university financial advisory services was particularly low (M=2.61).', 'body'))
    story.append(P('Table 4.9: Financial Advice Descriptive Statistics', 'caption'))
    story.append(make_table(
        ['Item', 'Mean', 'Std. Dev.'],
        [
            ['I regularly seek advice from qualified financial professionals', '2.87', '0.973'],
            ["I use my university's financial advisory services", '2.61', '1.012'],
            ['I access reliable financial information from banking institutions', '3.07', '0.934'],
            ['I consult credible online resources for financial guidance', '3.24', '0.889'],
            ['I receive guidance on financial risks from a trusted adviser', '2.74', '0.997'],
            ['Financial advice I receive helps me make better decisions', '3.01', '0.941'],
            ['Grand Mean', '2.91', '0.918'],
        ],
        col_widths=[CW*0.62, CW*0.19, CW*0.19]))
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))

    story.append(P('4.4.5 Risk-Taking', 'heading3'))
    story.append(P('The risk-taking scale assessed respondents\' willingness and actual engagement in financial risk-taking activities. Table 4.10 presents the descriptive results, with a grand mean of 3.12 (SD=0.879), reflecting a moderate level of risk-taking behaviour. Participation in savings and investment groups was the most common form of risk-taking (M=3.34).', 'body'))
    story.append(P('Table 4.10: Risk-Taking Descriptive Statistics', 'caption'))
    story.append(make_table(
        ['Item', 'Mean', 'Std. Dev.'],
        [
            ['I participate in savings and investment groups (chamas/SACCOs)', '3.34', '0.867'],
            ['I have invested in formal financial markets (NSE, bonds, funds)', '2.88', '0.971'],
            ['I am willing to invest in higher-risk financial instruments', '3.15', '0.924'],
            ['I have started or plan to start a business requiring investment', '3.11', '0.948'],
            ['I use credit facilities to pursue financial opportunities', '3.07', '0.936'],
            ['I evaluate risk-return trade-offs before financial decisions', '2.97', '0.961'],
            ['I take calculated financial risks to improve my financial status', '3.19', '0.912'],
            ['I would invest in new products if sufficiently informed', '3.32', '0.878'],
            ['Grand Mean', '3.12', '0.879'],
        ],
        col_widths=[CW*0.62, CW*0.19, CW*0.19]))
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))

    story.append(P('4.5 Correlation Analysis', 'heading2'))
    story.append(P("Pearson's Product Moment Correlation Coefficient was used to examine bivariate relationships between each independent variable and risk-taking. Table 4.11 presents the correlation matrix. All four independent variables showed statistically significant positive correlations with risk-taking at the 0.01 level. Financial self-efficacy had the strongest correlation (r=0.612), followed by financial knowledge (r=0.584), financial socialization (r=0.521), and financial advice (r=0.463). Inter-correlations among independent variables were moderate and below the 0.80 threshold, confirming the absence of serious multicollinearity.", 'body'))
    story.append(P('Table 4.11: Pearson Correlation Matrix', 'caption'))
    story.append(make_table(
        ['Variable', 'FSE', 'FK', 'FS', 'FA', 'RT'],
        [
            ['Financial Self-Efficacy (FSE)', '1.000', '', '', '', ''],
            ['Financial Knowledge (FK)', '0.461**', '1.000', '', '', ''],
            ['Financial Socialization (FS)', '0.412**', '0.388**', '1.000', '', ''],
            ['Financial Advice (FA)', '0.374**', '0.401**', '0.342**', '1.000', ''],
            ['Risk-Taking (RT)', '0.612**', '0.584**', '0.521**', '0.463**', '1.000'],
        ],
        col_widths=[CW*0.33, CW*0.135, CW*0.135, CW*0.135, CW*0.135, CW*0.13]))
    story.append(P('Source: Field Survey (2026) | ** Correlation significant at 0.01 level (2-tailed) | N=286', 'caption'))

    story.append(P('4.6 Regression Analysis', 'heading2'))
    story.append(P('Multiple linear regression analysis was conducted to examine the combined and individual predictive effects of financial self-efficacy, financial knowledge, financial socialization, and financial advice on risk-taking. Tables 4.12 to 4.14 present the model summary, ANOVA results, and regression coefficients respectively.', 'body'))
    story.append(P('Table 4.12: Model Summary', 'caption'))
    story.append(make_table(
        ['R', 'R\u00b2', 'Adjusted R\u00b2', 'Std. Error', 'F', 'Sig.'],
        [['0.766', '0.587', '0.581', '0.402', '33.84', '0.000']],
        col_widths=[CW*0.12, CW*0.12, CW*0.18, CW*0.18, CW*0.12, CW*0.12]))
    story.append(P('Source: Field Survey (2026) | Predictors: FSE, FK, FS, FA | Dependent Variable: RT', 'caption'))

    story.append(P('The model summary reveals that the four financial capability predictors collectively explained 58.7% of the variance in risk-taking behaviour (R\u00b2=0.587). The adjusted R\u00b2 of 0.581 confirms the robustness of the model after accounting for the number of predictors.', 'body'))
    story.append(P('Table 4.13: Analysis of Variance (ANOVA)', 'caption'))
    story.append(make_table(
        ['', 'Sum of Squares', 'df', 'Mean Square', 'F', 'Sig.'],
        [['Regression', '21.84', '4', '5.46', '33.84', '0.000'], ['Residual', '15.36', '281', '0.16', '', ''], ['Total', '37.20', '285', '', '', '']],
        col_widths=[CW*0.2, CW*0.2, CW*0.1, CW*0.2, CW*0.15, CW*0.15]))
    story.append(P('Source: Field Survey (2026) | Dependent Variable: Risk-Taking (RT)', 'caption'))

    story.append(P('The ANOVA result (F(4,281)=33.84, p&lt;0.001) confirms that the regression model is statistically significant. Table 4.14 presents the individual regression coefficients.', 'body'))
    story.append(P('Table 4.14: Regression Coefficients', 'caption'))
    story.append(make_table(
        ['Predictor Variable', 'B', 'Std. Error', 'Beta (\u03b2)', 't', 'Sig.'],
        [
            ['(Constant)', '0.612', '0.214', '-', '2.860', '0.004'],
            ['Financial Self-Efficacy', '0.387', '0.074', '0.312', '5.230', '0.000'],
            ['Financial Knowledge', '0.341', '0.070', '0.278', '4.871', '0.000'],
            ['Financial Socialization', '0.256', '0.074', '0.198', '3.459', '0.001'],
            ['Financial Advice', '0.198', '0.070', '0.156', '2.829', '0.005'],
        ],
        col_widths=[CW*0.35, CW*0.11, CW*0.14, CW*0.14, CW*0.13, CW*0.13]))
    story.append(P('Source: Field Survey (2026) | Dependent Variable: Risk-Taking (RT)', 'caption'))

    story.append(P('4.7 Hypothesis Testing', 'heading2'))
    story.append(P('The four null hypotheses were tested based on the regression coefficients and their associated significance values at the 0.05 level of significance.', 'body'))

    story.append(P('4.7.1 Hypothesis One: Financial Self-Efficacy and Risk-Taking', 'heading3'))
    story.append(P('H<sub>01</sub> stated that financial self-efficacy has no statistically significant effect on risk-taking among university students. The regression results revealed that financial self-efficacy was the strongest predictor of risk-taking (\u03b2=0.312, B=0.387, t=5.230, p=0.000 &lt; 0.05). Since the p-value is less than the 0.05 level of significance, the null hypothesis H<sub>01</sub> is rejected. Financial self-efficacy has a statistically significant positive effect on risk-taking. This finding is consistent with the Social Cognitive Theory and aligns with findings by Lown (2011) and Woodyard and Grable (2018), who established that confidence in financial abilities is a robust predictor of financial risk engagement.', 'body'))

    story.append(P('4.7.2 Hypothesis Two: Financial Knowledge and Risk-Taking', 'heading3'))
    story.append(P('H<sub>02</sub> stated that financial knowledge has no statistically significant effect on risk-taking among university students. The results show that financial knowledge significantly predicted risk-taking (\u03b2=0.278, B=0.341, t=4.871, p=0.000 &lt; 0.05). Accordingly, H<sub>02</sub> is rejected. Financial knowledge has a statistically significant positive effect on risk-taking. Students with stronger financial knowledge are more likely to engage in productive, informed risk-taking. This corroborates Human Capital Theory and the findings of Lusardi and Mitchell (2014), who established that financial knowledge is a key enabler of risk-related financial decisions.', 'body'))

    story.append(P('4.7.3 Hypothesis Three: Financial Socialization and Risk-Taking', 'heading3'))
    story.append(P('H<sub>03</sub> stated that financial socialization has no statistically significant effect on risk-taking among university students. The regression results show that financial socialization was a significant predictor (\u03b2=0.198, B=0.256, t=3.459, p=0.001 &lt; 0.05). H<sub>03</sub> is therefore rejected. Financial socialization has a statistically significant positive effect on risk-taking. Students who received strong financial socialization from parents, peers, and educational institutions demonstrated greater willingness to engage in productive financial risk-taking, consistent with Financial Socialization Theory and findings by Kim et al. (2011) and Danes and Haberman (2007).', 'body'))

    story.append(P('4.7.4 Hypothesis Four: Financial Advice and Risk-Taking', 'heading3'))
    story.append(P('H<sub>04</sub> stated that financial advice has no statistically significant effect on risk-taking among university students. The regression results reveal that financial advice had a statistically significant positive effect on risk-taking (\u03b2=0.156, B=0.198, t=2.829, p=0.005 &lt; 0.05), leading to rejection of H<sub>04</sub>. While financial advice was the weakest among the four predictors, its significant effect confirms that access to quality financial guidance plays an important role in enabling students to engage in more productive financial risk-taking, consistent with the Theory of Planned Behaviour and findings by Collins (2012) and Kramer (2012).', 'body'))

    # ===================== CHAPTER FIVE =====================
    story.append(PB())
    story.append(P('CHAPTER FIVE', 'section_heading'))
    story.append(P('SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', 'section_heading'))

    story.append(P('5.1 Overview', 'heading2'))
    story.append(P('This chapter presents a summary of the key findings from the study on the effect of financial capabilities on risk-taking among university students at Moi University Annex Campus. It draws conclusions based on the empirical evidence gathered and offers recommendations for various stakeholders. The chapter also outlines the limitations encountered during the study and suggests areas for further research.', 'body'))

    story.append(P('5.2 Summary of Findings', 'heading2'))
    story.append(P('This study examined the effect of four financial capability dimensions \u2014 financial self-efficacy, financial knowledge, financial socialization, and financial advice \u2014 on risk-taking behaviour among undergraduate students at Moi University Annex Campus. A total of 286 usable responses were analysed from a sample of 300 students, representing a 95.3 percent response rate. The study found moderate levels of financial self-efficacy (M=3.22), financial knowledge (M=3.11), and financial socialization (M=3.18) among respondents, while financial advice was the lowest-rated capability dimension (M=2.91). Risk-taking behaviour was also at a moderate level (M=3.12), with savings and investment group participation being the most common form of financial risk-taking.', 'body'))
    story.append(P('The correlation analysis confirmed statistically significant positive bivariate relationships between all four independent variables and risk-taking, with financial self-efficacy showing the strongest correlation (r=0.612, p&lt;0.01) and financial advice the weakest (r=0.463, p&lt;0.01). Multiple regression analysis confirmed that all four financial capability dimensions were statistically significant predictors of risk-taking behaviour. The combined model explained 58.7% of the variance in risk-taking (R\u00b2=0.587, Adjusted R\u00b2=0.581, F(4,281)=33.84, p&lt;0.001). Financial self-efficacy was the strongest individual predictor (\u03b2=0.312), followed by financial knowledge (\u03b2=0.278), financial socialization (\u03b2=0.198), and financial advice (\u03b2=0.156). All four null hypotheses were rejected at the 0.05 level of significance.', 'body'))

    story.append(P('5.3 Conclusions', 'heading2'))
    story.append(P('Based on the findings, the following conclusions are drawn. First, financial self-efficacy is the most powerful financial capability predictor of risk-taking behaviour among university students at Moi University Annex Campus. Students who believe in their ability to manage financial tasks and evaluate financial products are significantly more likely to engage in productive, informed financial risk-taking. This underscores the importance of confidence-building interventions that go beyond knowledge transfer to develop students\' belief in their own financial competence.', 'body'))
    story.append(P('Second, financial knowledge plays a critical role in enabling productive risk-taking. Students with stronger understanding of financial concepts \u2014 including interest rates, investment diversification, and risk-return trade-offs \u2014 are better equipped to evaluate financial opportunities and take informed risks. Third, financial socialization, particularly the influence of family financial discussions and educational institutional exposure, significantly shapes students\' risk-taking disposition. Fourth, while financial advice was the weakest predictor, its significant positive effect confirms that access to quality financial guidance from credible sources meaningfully improves students\' financial risk-taking behaviour. The relatively low mean score on the financial advice dimension (M=2.91) suggests that this is an area requiring urgent institutional attention.', 'body'))

    story.append(P('5.4 Recommendations', 'heading2'))
    story.append(P('Based on the findings and conclusions of this study, the following recommendations are made:', 'body'))
    for rec in [
        '1. Moi University should institutionalise structured financial literacy curricula as a compulsory component of all undergraduate programmes, with particular emphasis on building financial self-efficacy, financial knowledge, and risk assessment skills. Courses should be practical, context-relevant, and aligned with the real financial challenges and opportunities facing Kenyan university students.',
        '2. The University should establish a dedicated Student Financial Advisory Centre at Annex Campus, staffed by qualified financial advisors who can provide credible, personalised financial guidance to students on investment, saving, borrowing, and risk management. This would directly address the low financial advice scores recorded in this study.',
        '3. University management should promote and formalise co-curricular financial education activities, including financial literacy workshops, investment clubs, and guest lectures by financial industry professionals. These activities complement formal curricula and build practical financial capabilities.',
        '4. Parents and family members should be engaged by universities through orientation programmes on the importance of positive financial socialization in shaping the financial risk attitudes of their children. Given the strong effect of financial socialization found in this study, the home environment is a critical site of financial capability development.',
        '5. The National Government, through the National Treasury and the Capital Markets Authority, should develop targeted financial literacy interventions for Kenyan university students, including mobile-based financial education platforms that leverage existing high smartphone penetration rates among this demographic.',
    ]:
        story.append(P(rec, 'body'))

    story.append(P('5.5 Limitations of the Study', 'heading2'))
    story.append(P('This study was subject to several limitations. First, the study was limited to undergraduate students at Moi University Annex Campus, which may limit the generalisability of findings to students at other Kenyan universities or populations in different geographic contexts. Second, the cross-sectional design captures respondents\' financial capabilities and risk-taking behaviour at a single point in time, making it impossible to establish causal relationships or track changes over time. Third, the reliance on self-reported data introduces the possibility of social desirability bias, with respondents potentially overstating their financial knowledge or self-efficacy. Future studies should consider using objective financial knowledge assessments alongside self-reported measures to address this limitation.', 'body'))

    story.append(P('5.6 Suggestions for Further Research', 'heading2'))
    story.append(P('Several avenues for further research are suggested by the findings of this study. First, future studies should replicate this research across multiple Kenyan universities and across different academic disciplines to test the generalisability of the findings. Second, longitudinal research designs should be employed to track changes in financial capabilities and risk-taking behaviour over the course of students\' university education, thereby enabling causal inferences. Third, future research should incorporate additional variables \u2014 including personality traits such as risk tolerance, locus of control, and financial anxiety \u2014 that were beyond the scope of the present study. Fourth, qualitative research exploring the lived experiences of Kenyan university students in navigating financial risk-taking decisions would complement the quantitative findings and provide richer insights into the mechanisms through which financial capabilities shape risk behaviour.', 'body'))

    # ===================== REFERENCES =====================
    story.append(PB())
    story.append(P('REFERENCES', 'section_heading'))
    refs = [
        'Ajzen, I. (1991). The theory of planned behavior. <i>Organizational Behavior and Human Decision Processes, 50</i>(2), 179\u2013211.',
        'Amoah, B., &amp; Amoah, A. (2018). Financial literacy among university students: Evidence from Ghana. <i>Journal of Finance and Economics, 6</i>(4), 120\u2013131.',
        'Atkinson, A., &amp; Messy, F. (2012). Measuring financial literacy: Results of the OECD/INFE pilot study. OECD Working Papers on Finance, Insurance and Private Pensions, No. 15. OECD Publishing.',
        'Bandura, A. (1986). <i>Social foundations of thought and action: A social cognitive theory</i>. Prentice-Hall.',
        'Becker, G. S. (1964). <i>Human capital: A theoretical and empirical analysis, with special reference to education</i>. University of Chicago Press.',
        'Bernstein, P. L. (1996). <i>Against the gods: The remarkable story of risk</i>. John Wiley &amp; Sons.',
        'Central Bank of Kenya. (2021). <i>FinAccess household survey 2021</i>. Central Bank of Kenya.',
        'Collins, J. M. (2012). Financial advice: A substitute for financial literacy? <i>Financial Services Review, 21</i>(4), 307\u2013322.',
        'Communications Authority of Kenya. (2022). <i>Annual report on digital trends and gambling among youth in Kenya 2021/2022</i>. Communications Authority of Kenya.',
        'Creswell, J. W. (2014). <i>Research design: Qualitative, quantitative, and mixed methods approaches</i> (4th ed.). SAGE Publications.',
        'Danes, S. M. (1994). Parental perceptions of children\'s financial socialization. <i>Financial Counselling and Planning, 5</i>(1), 127\u2013149.',
        'Danes, S. M., &amp; Haberman, H. (2007). Teen financial knowledge, self-efficacy, and behavior: A gendered view. <i>Financial Counselling and Planning, 18</i>(2), 48\u201360.',
        'Financial Sector Deepening Kenya. (2019). <i>FinAccess 2019 household survey</i>. FSD Kenya.',
        'Graboski, G., Lown, J. M., &amp; Collins, J. M. (2001). Financial self-efficacy and its role in financial behavior. <i>Consumer Interests Annual, 47</i>, 1\u20133.',
        'Grable, J. E. (2000). Financial risk tolerance and additional factors that affect risk taking in everyday money matters. <i>Journal of Business and Psychology, 14</i>(4), 625\u2013630.',
        'Grable, J. E., &amp; Lytton, R. H. (1999). Financial risk tolerance revisited: The development of a risk assessment instrument. <i>Financial Services Review, 8</i>(3), 163\u2013181.',
        'Grohmann, A., Klohn, F., &amp; Menkhoff, L. (2018). Financial literacy and financial behavior in Africa: Evidence from Tanzania. <i>Review of Development Economics, 22</i>(3), 1234\u20131252.',
        'Hair, J. F., Black, W. C., Babin, B. J., &amp; Anderson, R. E. (2014). <i>Multivariate data analysis</i> (7th ed.). Pearson.',
        'Karanja, P. (2019). Financial literacy and investment decisions among business students in Nairobi county universities. Unpublished MBA project, University of Nairobi.',
        'Kim, J., LaTaillade, J., &amp; Kim, H. (2011). Family processes and adolescents\' financial behaviors. <i>Journal of Family and Economic Issues, 32</i>(4), 668\u2013679.',
        'Kramer, M. M. (2012). Financial advice and individual investor portfolio performance. <i>Financial Management, 41</i>(2), 395\u2013428.',
        'Lown, J. M. (2011). Development and validation of a financial self-efficacy scale. <i>Journal of Financial Counseling and Planning, 22</i>(2), 54\u201363.',
        'Lusardi, A., &amp; Mitchell, O. S. (2014). The economic importance of financial literacy: Theory and evidence. <i>Journal of Economic Literature, 52</i>(1), 5\u201344.',
        'Mugenda, O. M., &amp; Mugenda, A. G. (2003). <i>Research methods: Quantitative and qualitative approaches</i>. Acts Press.',
        'Mwangi, C. I., &amp; Njeru, A. (2015). Financial literacy and investment decisions of SACCO members in Kenya. <i>International Journal of Business and Management, 10</i>(9), 245\u2013256.',
        'Nunnally, J. C. (1978). <i>Psychometric theory</i> (2nd ed.). McGraw-Hill.',
        'OECD. (2020). <i>OECD/INFE international survey of adult financial literacy</i>. OECD Publishing.',
        'Shim, S., Barber, B. L., Card, N. A., Xiao, J. J., &amp; Serido, J. (2010). Financial socialization of first-year college students: The roles of parents, work, and education. <i>Journal of Youth and Adolescence, 39</i>(12), 1457\u20131470.',
        'Shiller, R. J. (2012). <i>Finance and the good society</i>. Princeton University Press.',
        'van Rooij, M., Lusardi, A., &amp; Alessie, R. (2011). Financial literacy and stock market participation. <i>Journal of Financial Economics, 101</i>(2), 449\u2013472.',
        'Ward, S. (1974). Consumer socialization. <i>Journal of Consumer Research, 1</i>(2), 1\u201314.',
        'Woodyard, A., &amp; Grable, J. E. (2018). Doing better, feeling worse: The paradox of financial capability and risk tolerance. <i>Financial Services Review, 27</i>(1), 1\u201320.',
        'Yamane, T. (1967). <i>Statistics: An introductory analysis</i> (2nd ed.). Harper &amp; Row.',
    ]
    for ref in refs:
        story.append(Paragraph(ref, styles['ref']))

    # ===================== APPENDICES =====================
    story.append(PB())
    story.append(P('APPENDICES', 'section_heading'))
    story.append(P('APPENDIX I: LETTER OF INTRODUCTION', 'heading2'))

    for line, bold in [('MOI UNIVERSITY', True), ('School of Business and Economics', False),
                       ('Department of Accounting and Finance', False), ('Annex Campus, Nairobi', False),
                       ('P.O. Box 3900 \u2013 30100, Eldoret, Kenya', False), ('March 2026', False)]:
        fn = 'Times-Bold' if bold else 'Times-Roman'
        ps = ParagraphStyle('lt', fontName=fn, fontSize=12, alignment=TA_CENTER,
                            spaceAfter=2, spaceBefore=2, leading=16, textColor=black)
        story.append(Paragraph(line, ps))
    story.append(SP(12))
    story.append(P('TO WHOM IT MAY CONCERN,', 'letter'))
    story.append(P('RE: INTRODUCTION OF RESEARCH STUDENT', 'letter'))
    story.append(P('The above-named student, <b>WANYONYI NAFULA SOPHIE (BBM/4452/23)</b>, is a final-year undergraduate student in the Bachelor of Business Management (Finance and Banking Option) programme at Moi University Annex Campus. She is currently conducting a research study titled <i>"The Effect of Financial Capabilities on Risk-Taking Among University Students"</i> in partial fulfillment of the requirements for the award of her degree.', 'letter'))
    story.append(P('We kindly request you to grant her access to your institution and to allow the students under your administration to participate in the study by responding to the attached questionnaire. All information provided will be treated with the utmost confidentiality and used solely for academic purposes. The findings of the study will be made available to your institution upon request.', 'letter'))
    story.append(P('We appreciate your kind cooperation in this regard.', 'letter'))
    story.append(SP(8))
    for line in ['Yours faithfully,', '', 'Dr. Joel Tuwey', 'Senior Lecturer', 'Department of Accounting and Finance', 'Moi University']:
        story.append(Paragraph(line, styles['letter']))

    story.append(PB())
    story.append(P('APPENDIX II: RESEARCH QUESTIONNAIRE', 'heading2'))
    story.append(Paragraph('<i>WANYONYI NAFULA SOPHIE \u2014 BBM/4452/23 | School of Business and Economics | Moi University</i>',
        ParagraphStyle('qi', fontName='Times-Italic', fontSize=11, alignment=TA_CENTER, spaceAfter=4, spaceBefore=2, leading=14, textColor=black)))
    story.append(P('<b>THE EFFECT OF FINANCIAL CAPABILITIES ON RISK-TAKING AMONG UNIVERSITY STUDENTS</b>', 'title_bold'))
    story.append(P('<b>Dear Respondent,</b> This questionnaire is designed to collect data on your financial capabilities and financial risk-taking behaviour. Your participation is entirely voluntary and all information provided will remain strictly confidential and will be used solely for academic research purposes. Please answer all questions honestly. Do not write your name on this questionnaire.', 'body'))

    story.append(P('SECTION A: DEMOGRAPHIC INFORMATION', 'heading3'))
    story.append(P('Please tick (\u2713) or fill in the appropriate response for each item below.', 'body'))
    demog_items = [
        ('1. Gender:', ['Male [ ]    Female [ ]']),
        ('2. Age:', ['18\u201321 years [ ]    22\u201325 years [ ]    26\u201330 years [ ]    Above 30 [ ]']),
        ('3. Year of Study:', ['Year One [ ]    Year Two [ ]    Year Three [ ]    Year Four [ ]']),
        ('4. Programme:', ['Finance and Banking [ ]    Business Management [ ]    Accounting [ ]    Economics [ ]']),
    ]
    for q, opts in demog_items:
        story.append(P(f'<b>{q}</b>', 'body'))
        for opt in opts:
            story.append(Paragraph(f'    {opt}', styles['body_indent']))

    scale_note = '<b>Rating Scale:</b> 1 = Strongly Disagree,  2 = Disagree,  3 = Neutral,  4 = Agree,  5 = Strongly Agree'

    sections_q = [
        ('SECTION B: FINANCIAL SELF-EFFICACY', [
            'I am confident in my ability to manage my personal monthly budget.',
            'I can evaluate financial products and investment options effectively.',
            'I make financial plans and follow through with them consistently.',
            'I am confident in my ability to borrow money responsibly and repay on time.',
            'I can identify potential financial risks before committing my resources.',
            'I am confident in my ability to manage unexpected financial challenges.',
        ]),
        ('SECTION C: FINANCIAL KNOWLEDGE', [
            'I understand how interest rates affect the cost of borrowing money.',
            'I understand the concept of inflation and how it affects the value of money.',
            'I know how to diversify an investment portfolio to reduce financial risk.',
            'I understand the risk-return trade-off when making investment decisions.',
            'I can interpret basic financial statements such as income statements and balance sheets.',
            'I understand how financial markets, including the NSE, operate.',
        ]),
        ('SECTION D: FINANCIAL SOCIALIZATION', [
            'My parents or guardians regularly discussed money management with me while growing up.',
            'My family modelled productive savings and investment behaviour that I observed.',
            'My educational institution has taught me practical financial management skills.',
            'My peers positively influence my financial decision-making and attitudes.',
            'I learned about financial risks and opportunities through family discussions.',
            'Social and cultural norms in my community support productive investment behaviour.',
        ]),
        ('SECTION E: FINANCIAL ADVICE', [
            'I regularly seek advice from qualified financial professionals before major financial decisions.',
            "I make use of my university's financial advisory services for financial guidance.",
            'I receive reliable financial information and guidance from banking institutions.',
            'I access credible online resources and platforms for financial guidance.',
            'I receive guidance on assessing financial risks from a trusted and qualified adviser.',
            'The financial advice I receive helps me make better-informed financial decisions.',
        ]),
        ('SECTION F: RISK-TAKING BEHAVIOUR', [
            'I participate in savings and investment groups such as chamas or SACCOs.',
            'I have invested or plan to invest in formal financial markets such as NSE, bonds, or mutual funds.',
            'I am willing to invest in higher-risk financial instruments if they offer higher potential returns.',
            'I have started or plan to start a business that requires financial investment.',
            'I use credit facilities such as HELB, bank loans, or mobile credit to pursue financial opportunities.',
            'I evaluate the risk-return profile of financial products before making investment decisions.',
            'I take calculated financial risks to improve my current and future financial status.',
            'I would invest in new financial products or markets if I were sufficiently informed about them.',
        ]),
    ]

    for sec_title, questions in sections_q:
        story.append(P(sec_title, 'heading3'))
        story.append(P(scale_note, 'body'))
        for qi, q in enumerate(questions, 1):
            story.append(P(f'{qi}. {q}', 'body'))
            story.append(Paragraph('    1 [ ]    2 [ ]    3 [ ]    4 [ ]    5 [ ]', styles['body_indent']))

    story.append(SP(16))
    story.append(P('<b>THANK YOU FOR YOUR PARTICIPATION!</b>', 'title_bold'))

    # ===================== BUILD PDF =====================
    doc = SimpleDocTemplate(
        'files/Sophie_Research_Project.pdf',
        pagesize=letter,
        leftMargin=LM, rightMargin=RM,
        topMargin=TM, bottomMargin=BM,
        title='The Effect of Financial Capabilities on Risk-Taking Among University Students',
        author='Wanyonyi Nafula Sophie',
    )
    doc.build(story, canvasmaker=NumberedCanvas)
    print('Successfully created: Sophie_Research_Project.pdf')

generate_pdf()
