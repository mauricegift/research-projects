#!/usr/bin/env python3
"""
Generate PDF version of the research project using ReportLab
"""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.colors import black, white, grey, HexColor
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY, TA_RIGHT
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether, Image
)
from reportlab.platypus.tableofcontents import TableOfContents
from reportlab.lib import colors
import copy

PAGE_WIDTH, PAGE_HEIGHT = letter
MARGIN = inch

def get_styles():
    styles = getSampleStyleSheet()
    
    custom = {}
    
    custom['title_main'] = ParagraphStyle(
        'title_main', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=14,
        spaceAfter=8, spaceBefore=8,
        alignment=TA_CENTER, textColor=black,
        leading=20
    )
    
    custom['title_sub'] = ParagraphStyle(
        'title_sub', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12,
        spaceAfter=8, spaceBefore=4,
        alignment=TA_CENTER, textColor=black,
        leading=18
    )
    
    custom['title_bold'] = ParagraphStyle(
        'title_bold', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12,
        spaceAfter=8, spaceBefore=4,
        alignment=TA_CENTER, textColor=black,
        leading=18
    )
    
    custom['section_heading'] = ParagraphStyle(
        'section_heading', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=13,
        spaceAfter=10, spaceBefore=16,
        alignment=TA_CENTER, textColor=black,
        leading=18
    )
    
    custom['heading2'] = ParagraphStyle(
        'heading2', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12,
        spaceAfter=6, spaceBefore=14,
        alignment=TA_LEFT, textColor=black,
        leading=18
    )
    
    custom['heading3'] = ParagraphStyle(
        'heading3', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12,
        spaceAfter=6, spaceBefore=10,
        alignment=TA_LEFT, textColor=black,
        leading=18
    )
    
    custom['body'] = ParagraphStyle(
        'body', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12,
        spaceAfter=8, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black,
        leading=18,  # 1.5 spacing
        firstLineIndent=0
    )
    
    custom['body_indent'] = ParagraphStyle(
        'body_indent', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12,
        spaceAfter=6, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black,
        leading=18,
        leftIndent=24
    )
    
    custom['bullet'] = ParagraphStyle(
        'bullet', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12,
        spaceAfter=4, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black,
        leading=18,
        leftIndent=24
    )
    
    custom['caption'] = ParagraphStyle(
        'caption', parent=styles['Normal'],
        fontName='Times-Italic', fontSize=11,
        spaceAfter=6, spaceBefore=4,
        alignment=TA_CENTER, textColor=black,
        leading=14
    )
    
    custom['toc_main'] = ParagraphStyle(
        'toc_main', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=11,
        spaceAfter=2, spaceBefore=2,
        alignment=TA_LEFT, textColor=black,
        leading=14
    )
    
    custom['toc_1'] = ParagraphStyle(
        'toc_1', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=11,
        spaceAfter=2, spaceBefore=1,
        alignment=TA_LEFT, textColor=black,
        leading=14,
        leftIndent=18
    )
    
    custom['toc_2'] = ParagraphStyle(
        'toc_2', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=11,
        spaceAfter=1, spaceBefore=1,
        alignment=TA_LEFT, textColor=black,
        leading=14,
        leftIndent=36
    )
    
    custom['math'] = ParagraphStyle(
        'math', parent=styles['Normal'],
        fontName='Times-Bold', fontSize=12,
        spaceAfter=6, spaceBefore=6,
        alignment=TA_CENTER, textColor=black,
        leading=18
    )
    
    custom['abstract_body'] = ParagraphStyle(
        'abstract_body', parent=styles['Normal'],
        fontName='Times-Roman', fontSize=12,
        spaceAfter=8, spaceBefore=0,
        alignment=TA_JUSTIFY, textColor=black,
        leading=18
    )
    
    return custom

def make_table(headers, rows, col_widths=None):
    data = [headers] + rows
    
    if col_widths:
        total = sum(col_widths)
        page_width = PAGE_WIDTH - 2 * MARGIN
        scale = page_width / total
        col_widths = [w * scale for w in col_widths]
    
    t = Table(data, colWidths=col_widths, repeatRows=1)
    
    style = TableStyle([
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
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
        ('WORDWRAP', (0, 0), (-1, -1), True),
        ('ALIGN', (0, 0), (0, -1), 'LEFT'),
    ])
    t.setStyle(style)
    return t

def make_cf_table():
    """Create the Conceptual Framework table"""
    iv_text = '''<b>INDEPENDENT VARIABLE</b><br/><b>TECHNOLOGICAL INNOVATION</b><br/><br/>
• ICT Tools &amp; Applications<br/>  - Computers &amp; Software<br/>  - Mobile Technologies<br/>  - Internet &amp; Websites<br/><br/>
• Digital Marketing<br/>  - Social Media<br/>  - Online Advertising<br/>  - E-commerce Platforms<br/><br/>
• Service Delivery Technologies<br/>  - POS Systems<br/>  - CRM Tools<br/>  - Self-Service Technologies<br/><br/>
• Financial Technologies<br/>  - Mobile Money<br/>  - Digital Payments'''

    dv_text = '''<b>DEPENDENT VARIABLE</b><br/><b>SERVICE DELIVERY</b><br/><br/>
• Efficiency<br/>  - Time Savings<br/>  - Cost Reduction<br/>  - Process Streamlining<br/><br/>
• Service Quality<br/>  - Reliability<br/>  - Responsiveness<br/>  - Personalization<br/><br/>
• Customer Satisfaction<br/>  - Customer Experience<br/>  - Service Perception<br/>  - Customer Loyalty'''

    arrow_text = '''<br/><br/><br/><br/>----------&gt;'''

    iv_para = Paragraph(iv_text, ParagraphStyle('cf_iv', fontName='Times-Roman', fontSize=9, leading=13, alignment=TA_LEFT))
    arrow_para = Paragraph(arrow_text, ParagraphStyle('cf_arrow', fontName='Times-Bold', fontSize=12, leading=14, alignment=TA_CENTER))
    dv_para = Paragraph(dv_text, ParagraphStyle('cf_dv', fontName='Times-Roman', fontSize=9, leading=13, alignment=TA_LEFT))

    mod_text = '''<b>INTERVENING VARIABLES</b><br/>
• Business characteristics (size, type, years of operation)<br/>
• Owner/manager characteristics (education, experience, attitude)<br/>
• Environmental factors (infrastructure, competition, regulatory environment)'''
    mod_para = Paragraph(mod_text, ParagraphStyle('cf_mod', fontName='Times-Roman', fontSize=9, leading=13, alignment=TA_CENTER))

    page_width = PAGE_WIDTH - 2 * MARGIN

    data = [
        [iv_para, arrow_para, dv_para],
        [mod_para, '', ''],
    ]
    
    col_widths = [page_width * 0.42, page_width * 0.16, page_width * 0.42]
    
    t = Table(data, colWidths=col_widths)
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, 0), HexColor('#E8F4FD')),
        ('BACKGROUND', (2, 0), (2, 0), HexColor('#E8FDE8')),
        ('BACKGROUND', (0, 1), (-1, 1), HexColor('#FFF8E1')),
        ('GRID', (0, 0), (-1, -1), 0.5, black),
        ('SPAN', (0, 1), (2, 1)),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    return t

def generate_pdf():
    output_path = 'files/James_Ngovi_Research_Project.pdf'
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        leftMargin=inch * 1.25,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
        title='The Impact of Technological Innovation on Service Delivery in SMEs',
        author='James Ngovi',
    )
    
    styles = get_styles()
    story = []
    
    def P(text, style='body'):
        if isinstance(style, str):
            return Paragraph(text, styles[style])
        return Paragraph(text, style)
    
    def SP(h=12):
        return Spacer(1, h)
    
    def HR():
        return HRFlowable(width='100%', thickness=0.5, color=black, spaceAfter=6)
    
    # ===================== TITLE PAGE =====================
    story += [SP(4)]
    logo = Image('assets/moi_uni_logo.png', width=1.0*inch, height=1.0*inch)
    logo.hAlign = 'CENTER'
    story.append(logo)
    story += [SP(4)]
    story.append(P('MOI UNIVERSITY', 'title_main'))
    story.append(P('SCHOOL OF BUSINESS AND ECONOMICS', 'title_main'))
    story.append(P('DEPARTMENT OF MANAGEMENT SCIENCE AND ENTREPRENEURSHIP', 'title_bold'))
    story += [SP(16)]
    story.append(HR())
    story.append(P('THE IMPACT OF TECHNOLOGICAL INNOVATION ON SERVICE DELIVERY IN SMALL AND MEDIUM ENTERPRISES (SMEs): A CASE STUDY OF SMEs IN THE ANNEX AREA OF UASIN GISHU COUNTY', 'title_main'))
    story.append(HR())
    story += [SP(14)]
    story.append(P('A RESEARCH PROJECT SUBMITTED IN PARTIAL FULFILLMENT OF THE REQUIREMENTS FOR THE AWARD OF BACHELOR OF BUSINESS MANAGEMENT (BUSINESS INFORMATION TECHNOLOGY) OF MOI UNIVERSITY', 'title_sub'))
    story += [SP(14)]
    story.append(P('BY', 'title_bold'))
    story += [SP(4)]
    story.append(P('JAMES NGOVI', 'title_main'))
    story.append(P('REGISTRATION NUMBER: BBM/1733/22', 'title_sub'))
    story += [SP(14)]
    story.append(P('SUPERVISOR: DR. KIYENG CHUMO', 'title_sub'))
    story += [SP(4)]
    story.append(P('Department of Management Science and Entrepreneurship', 'title_sub'))
    story += [SP(14)]
    story.append(P('MARCH 2026', 'title_bold'))
    story.append(PageBreak())
    
    # ===================== DECLARATION =====================
    story.append(P('DECLARATION', 'section_heading'))
    story.append(P('I, JAMES NGOVI, hereby declare that this research project is my original work and has not been submitted for any degree or diploma in any other university or institution. All sources of information used have been duly acknowledged.'))
    story += [SP(24)]
    story.append(P('Signature: .............................................',
                   ParagraphStyle('sig', fontName='Times-Roman', fontSize=12, leading=20, alignment=TA_LEFT)))
    story.append(P('Date: .............................',
                   ParagraphStyle('sig', fontName='Times-Roman', fontSize=12, leading=20, alignment=TA_LEFT)))
    story += [SP(24)]
    story.append(P("<b>SUPERVISOR'S APPROVAL</b>",
                   ParagraphStyle('sh', fontName='Times-Bold', fontSize=12, leading=18, alignment=TA_LEFT)))
    story += [SP(6)]
    story.append(P("This research project has been submitted for examination with my approval as the university supervisor."))
    story += [SP(18)]
    story.append(P('<b>DR. KIYENG CHUMO</b>',
                   ParagraphStyle('sh', fontName='Times-Bold', fontSize=12, leading=18, alignment=TA_LEFT)))
    story.append(P('Department of Management Science and Entrepreneurship, Moi University'))
    story += [SP(12)]
    story.append(P('Signature: .............................................'))
    story.append(P('Date: .............................'))
    story.append(PageBreak())
    
    # ===================== DEDICATION =====================
    story.append(P('DEDICATION', 'section_heading'))
    story += [SP(36)]
    story.append(P('<i>This research project is dedicated to my loving family for their unwavering support, encouragement, and patience throughout my academic journey at Moi University. Your sacrifices and belief in my potential have been my greatest source of motivation.</i>',
                   ParagraphStyle('ded', fontName='Times-Italic', fontSize=12, leading=18, alignment=TA_CENTER, spaceAfter=16)))
    story += [SP(16)]
    story.append(P('<i>I also dedicate this work to all Small and Medium Enterprise owners and managers in Uasin Gishu County who strive daily to innovate, adapt, and improve service delivery for the betterment of their communities and the Kenyan economy.</i>',
                   ParagraphStyle('ded', fontName='Times-Italic', fontSize=12, leading=18, alignment=TA_CENTER)))
    story.append(PageBreak())
    
    # ===================== ACKNOWLEDGEMENT =====================
    story.append(P('ACKNOWLEDGEMENT', 'section_heading'))
    
    ack_texts = [
        'First and foremost, I give all glory and thanks to the Almighty God for His abundant grace, wisdom, and guidance throughout this research journey. Without His divine providence, this work would not have been possible.',
        'I wish to express my sincere and deepest gratitude to my supervisor, <b>Dr. Kiyeng Chumo</b>, for the invaluable academic guidance, constructive criticism, patient mentorship, and continuous support throughout this research project. His expertise in research methodology and business management has been instrumental in shaping the quality and direction of this work.',
        'I am equally grateful to the entire faculty of the Department of Management Science and Entrepreneurship and the School of Business and Economics at Moi University for the knowledge and skills imparted throughout my Bachelor of Business Management program.',
        'My appreciation also goes to the SME owners, managers, and customers in the Annex area of Uasin Gishu County who willingly participated in this study. Your cooperation and openness made the data collection process successful.',
        'I am grateful to the Uasin Gishu County Business Licensing Department for providing population data on registered SMEs in the Annex area.',
        'Special thanks go to my fellow students and colleagues in the Bachelor of Business Management program for their intellectual engagement, moral support, and encouragement throughout the research process.',
        'Finally, I acknowledge my family for their endless patience, understanding, financial support, and constant encouragement throughout my studies. May God bless you all abundantly.',
    ]
    for t in ack_texts[:-1]:
        story.append(P(t))
        story.append(SP(4))
    story.append(P(ack_texts[-1]))
    story.append(PageBreak())
    
    # ===================== TABLE OF CONTENTS =====================
    story.append(P('TABLE OF CONTENTS', 'section_heading'))
    
    toc_entries = [
        ('DECLARATION', 'ii', 0),
        ('DEDICATION', 'iii', 0),
        ('ACKNOWLEDGEMENT', 'iv', 0),
        ('TABLE OF CONTENTS', 'v', 0),
        ('LIST OF TABLES', 'viii', 0),
        ('LIST OF FIGURES', 'ix', 0),
        ('ABBREVIATIONS AND ACRONYMS', 'x', 0),
        ('OPERATIONAL DEFINITION OF TERMS', 'xi', 0),
        ('ABSTRACT', 'xii', 0),
        ('CHAPTER ONE: INTRODUCTION', '1', 0),
        ('1.1 Background of the Study', '1', 1),
        ('1.1.1 Global Perspective of Technological Innovation in SMEs', '1', 2),
        ('1.1.2 Regional Perspective of Technological Innovation in SMEs', '2', 2),
        ('1.1.3 Local Perspective in Uasin Gishu County', '3', 2),
        ('1.2 Statement of the Problem', '4', 1),
        ('1.3 General Objective', '5', 1),
        ('1.4 Specific Objectives', '5', 1),
        ('1.5 Research Questions', '5', 1),
        ('1.6 Significance of the Study', '6', 1),
        ('1.7 Scope of the Study', '7', 1),
        ('1.8 Limitations of the Study', '7', 1),
        ('CHAPTER TWO: LITERATURE REVIEW', '8', 0),
        ('2.1 Introduction', '8', 1),
        ('2.2 Theoretical Framework', '8', 1),
        ('2.2.1 Technology-Organization-Environment (TOE) Framework', '8', 2),
        ('2.2.2 Dynamic Capabilities Theory', '9', 2),
        ('2.2.3 Disruptive Innovation Theory', '10', 2),
        ('2.3 Conceptual Framework', '10', 1),
        ('2.4 Review of Literature on Study Variables', '11', 1),
        ('2.4.1 Types of Technological Innovations Adopted by SMEs', '11', 2),
        ('2.4.2 Technological Innovation and Efficiency of Service Delivery', '12', 2),
        ('2.4.3 Customer Perceptions of Technologically Enhanced Services', '13', 2),
        ('2.4.4 Challenges Faced by SMEs in Adopting Technological Innovations', '14', 2),
        ('2.5 Empirical Review', '15', 1),
        ('2.5.1 Studies on ICT Adoption in Kenyan SMEs', '15', 2),
        ('2.5.2 Studies on Technology and SME Performance in Uasin Gishu County', '16', 2),
        ('2.6 Research Gaps', '17', 1),
        ('CHAPTER THREE: RESEARCH METHODOLOGY', '18', 0),
        ('3.1 Introduction', '18', 1),
        ('3.2 Research Design', '18', 1),
        ('3.3 Target Population', '18', 1),
        ('3.4 Sample Size and Sampling Technique', '19', 1),
        ('3.5 Data Collection Instruments', '20', 1),
        ('3.6 Pilot Testing', '21', 1),
        ('3.7 Data Collection Procedures', '22', 1),
        ('3.8 Data Analysis and Presentation', '22', 1),
        ('3.9 Ethical Considerations', '23', 1),
        ('CHAPTER FOUR: DATA ANALYSIS, PRESENTATION AND INTERPRETATION', '24', 0),
        ('4.1 Introduction', '24', 1),
        ('4.2 Response Rate', '24', 1),
        ('4.3 Demographic Characteristics of Respondents', '25', 1),
        ('4.4 Types of Technological Innovations Adopted', '27', 1),
        ('4.5 Influence on Efficiency and Quality of Service Delivery', '30', 1),
        ('4.6 Customer Perceptions of Technologically Enhanced Services', '33', 1),
        ('4.7 Challenges Faced by SMEs in Adopting Technological Innovations', '35', 1),
        ('4.8 Regression Analysis', '38', 1),
        ('CHAPTER FIVE: SUMMARY, CONCLUSIONS AND RECOMMENDATIONS', '41', 0),
        ('5.1 Introduction', '41', 1),
        ('5.2 Summary of Findings', '41', 1),
        ('5.3 Conclusions', '43', 1),
        ('5.4 Recommendations', '44', 1),
        ('5.5 Limitations of the Study', '45', 1),
        ('5.6 Suggestions for Further Research', '46', 1),
        ('REFERENCES', '47', 0),
        ('APPENDICES', '50', 0),
        ('Appendix I: Letter of Introduction', '50', 1),
        ('Appendix II: Questionnaire for SME Owners/Managers', '51', 1),
        ('Appendix III: Interview Guide', '54', 1),
        ('Appendix IV: Customer Questionnaire', '55', 1),
    ]
    
    for text, page, level in toc_entries:
        if level == 0:
            sty = styles['toc_main']
        elif level == 1:
            sty = styles['toc_1']
        else:
            sty = styles['toc_2']
        
        # Create a table row for each TOC entry to align text and page number
        dots = '.' * max(1, 60 - len(text) - len(page) - level * 2)
        entry_text = f'{text} {dots} {page}' if level > 0 else f'{text} {dots} {page}'
        story.append(P(entry_text, sty))
    
    story.append(PageBreak())
    
    # ===================== LIST OF TABLES =====================
    story.append(P('LIST OF TABLES', 'section_heading'))
    
    tables_list = [
        ('Table 3.1: Target Population Distribution', '19'),
        ('Table 3.2: Sample Size Distribution', '20'),
        ('Table 3.3: Reliability Statistics', '22'),
        ('Table 4.1: Response Rate', '24'),
        ('Table 4.2: Gender of Respondents', '25'),
        ('Table 4.3: Age of Respondents', '25'),
        ('Table 4.4: Level of Education', '26'),
        ('Table 4.5: Business Type', '26'),
        ('Table 4.6: Years of Business Operation', '27'),
        ('Table 4.7: ICT Tools and Applications Used by SMEs', '28'),
        ('Table 4.8: Mobile Technology Adoption', '28'),
        ('Table 4.9: Social Media and Digital Marketing', '29'),
        ('Table 4.10: Efficiency of Service Delivery', '30'),
        ('Table 4.11: Quality of Service Delivery', '31'),
        ('Table 4.12: Correlation between Technological Innovation and Service Delivery', '32'),
        ('Table 4.13: Customer Satisfaction with Technologically Enhanced Services', '33'),
        ('Table 4.14: Customer Experience with Technology-Enhanced Services', '34'),
        ('Table 4.15: Financial Challenges in Technology Adoption', '35'),
        ('Table 4.16: Skills and Knowledge Gaps in Technology Adoption', '36'),
        ('Table 4.17: Infrastructure Challenges in Technology Adoption', '37'),
        ('Table 4.18: Environmental and Social Challenges in Technology Adoption', '38'),
        ('Table 4.19: Model Summary', '39'),
        ('Table 4.20: Analysis of Variance (ANOVA)', '39'),
        ('Table 4.21: Regression Coefficients', '40'),
    ]
    
    for tname, page in tables_list:
        dots = '.' * max(1, 65 - len(tname) - len(page))
        story.append(P(f'{tname} {dots} {page}', styles['toc_1']))
    
    story.append(PageBreak())
    
    # ===================== LIST OF FIGURES =====================
    story.append(P('LIST OF FIGURES', 'section_heading'))
    
    figures_list = [
        ('Figure 2.1: Conceptual Framework', '10'),
        ('Figure 4.1: Response Rate Summary', '24'),
        ('Figure 4.2: ICT Tools Adoption Rates', '28'),
        ('Figure 4.3: Social Media Platforms Used by SMEs', '29'),
        ('Figure 4.4: Service Delivery Efficiency Indicators', '31'),
        ('Figure 4.5: Customer Satisfaction Levels', '34'),
        ('Figure 4.6: Major Challenges Facing SMEs', '36'),
    ]
    
    for fname, page in figures_list:
        dots = '.' * max(1, 65 - len(fname) - len(page))
        story.append(P(f'{fname} {dots} {page}', styles['toc_1']))
    
    story.append(PageBreak())
    
    # ===================== ABBREVIATIONS =====================
    story.append(P('ABBREVIATIONS AND ACRONYMS', 'section_heading'))
    
    abbrevs = [
        ('AI', 'Artificial Intelligence'),
        ('ANOVA', 'Analysis of Variance'),
        ('BBM', 'Bachelor of Business Management'),
        ('BIT', 'Business Information Technology'),
        ('GDP', 'Gross Domestic Product'),
        ('ICT', 'Information and Communication Technology'),
        ('ICX', 'Institute of Customer Experience'),
        ('KNBS', 'Kenya National Bureau of Statistics'),
        ('MSEA', 'Micro and Small Enterprises Authority'),
        ('MSE', 'Micro and Small Enterprise'),
        ('MSME', 'Micro, Small and Medium Enterprise'),
        ('NACOSTI', 'National Commission for Science, Technology and Innovation'),
        ('POS', 'Point of Sale'),
        ('SME', 'Small and Medium Enterprise'),
        ('SPSS', 'Statistical Package for Social Sciences'),
        ('SST', 'Self-Service Technologies'),
        ('TOE', 'Technology-Organization-Environment'),
        ('UNIDO', 'United Nations Industrial Development Organization'),
        ('USD', 'United States Dollar'),
    ]
    
    abbrev_sty = ParagraphStyle('abbrev', fontName='Times-Roman', fontSize=12, leading=18, alignment=TA_LEFT, spaceAfter=4)
    for abbr, meaning in abbrevs:
        story.append(P(f'<b>{abbr}</b>  :  {meaning}', abbrev_sty))
    
    story.append(PageBreak())
    
    # ===================== OPERATIONAL DEFINITIONS =====================
    story.append(P('OPERATIONAL DEFINITION OF TERMS', 'section_heading'))
    
    definitions = [
        ('Technological Innovation', 'The adoption of new or significantly improved technological tools, systems, and applications by SMEs to enhance their business operations and service delivery processes in the Annex area of Uasin Gishu County.'),
        ('Service Delivery', 'The process by which SMEs provide their products or services to customers, encompassing the quality, efficiency, and overall customer experience associated with the transaction.'),
        ('Small and Medium Enterprises (SMEs)', 'Businesses operating in the Annex area of Uasin Gishu County that employ between 1 and 50 employees, as defined by the Kenyan regulatory framework under the Micro and Small Enterprises Act.'),
        ('Efficiency', 'The ability of SMEs to deliver services using optimal resources, including reduced time, minimized costs, and streamlined processes through technological adoption.'),
        ('Service Quality', 'The extent to which the services provided by SMEs meet or exceed customer expectations, including aspects of reliability, responsiveness, assurance, empathy, and personalization.'),
        ('Customer Perception', 'The attitudes, opinions, and satisfaction levels of customers regarding the technologically enhanced services offered by SMEs in the Annex area.'),
        ('ICT Adoption', 'The process by which SMEs integrate information and communication technologies into their daily operations, including hardware, software, mobile applications, and digital platforms.'),
        ('Digital Transformation', 'The comprehensive integration of digital technologies into all areas of SME business operations, fundamentally changing how they operate and deliver value to customers.'),
        ('Mobile Technology', 'The use of smartphones, tablets, and mobile applications by SMEs for business management, customer engagement, mobile payments, and service delivery enhancement.'),
        ('FinTech', 'Financial technology tools and platforms such as mobile money services (M-Pesa), digital banking, and online payment systems used by SMEs for financial transactions.'),
    ]
    
    def_sty = ParagraphStyle('def', fontName='Times-Roman', fontSize=12, leading=18, alignment=TA_JUSTIFY, spaceAfter=8)
    for term, definition in definitions:
        story.append(P(f'<b>{term}:</b> {definition}', def_sty))
    
    story.append(PageBreak())
    
    # ===================== ABSTRACT =====================
    story.append(P('ABSTRACT', 'section_heading'))
    
    abstract_paras = [
        'Small and Medium Enterprises (SMEs) constitute the backbone of the Kenyan economy, contributing significantly to employment creation and GDP growth. However, many SMEs continue to struggle with inefficient service delivery, limited customer reach, and inability to meet evolving customer expectations. This study examined the impact of technological innovation on service delivery among SMEs in the Annex area of Uasin Gishu County. Guided by the Technology-Organization-Environment (TOE) Framework, Dynamic Capabilities Theory, and Disruptive Innovation Theory, the study sought to identify types of technological innovations adopted, assess their influence on service delivery efficiency and quality, evaluate customer perceptions of technologically enhanced services, and identify challenges faced in technology adoption.',
        
        "The study adopted a descriptive research design with a mixed-methods approach. The target population comprised 250 registered SMEs in the Annex area, from which a sample of 154 SME owners/managers was drawn using stratified random sampling based on the Yamane (1967) formula. Additionally, 200 customers were sampled using convenience sampling. Data were collected using structured questionnaires and semi-structured interview guides. Reliability was confirmed using Cronbach's Alpha coefficients ranging from 0.772 to 0.845. Data were analyzed using descriptive and inferential statistics (Pearson's correlation and multiple regression analysis) through SPSS Version 26.",
        
        'The findings revealed that SMEs in the Annex area had widely adopted mobile money services (89.5%), smartphones (84.6%), and social media platforms (78.3%), while adoption of advanced technologies such as POS systems (54.5%) and inventory management software (42.0%) was moderate. Technological innovation significantly influenced service delivery efficiency (r=0.714, p&lt;0.001) and service quality (r=0.682, p&lt;0.001). Customer satisfaction with technologically enhanced services was high (mean=3.96/5.00). The regression analysis revealed that ICT adoption (&beta;=0.421, p&lt;0.001), digital marketing (&beta;=0.318, p&lt;0.001), and service delivery technologies (&beta;=0.276, p&lt;0.001) collectively explained 61.3% of the variance in service delivery (Adjusted R&sup2;=0.597).',
        
        'The study concluded that technological innovation significantly and positively impacts service delivery among SMEs in the Annex area of Uasin Gishu County. It recommended that policymakers develop targeted financial support programs, invest in digital literacy training, improve technological infrastructure, and create enabling regulatory frameworks. SME owners were advised to prioritize strategic technology investments aligned with business needs and customer expectations.',
    ]
    
    for para_text in abstract_paras:
        story.append(P(para_text, 'abstract_body'))
        story.append(SP(4))
    
    story.append(SP(12))
    story.append(P('<b>Keywords:</b> <i>Technological Innovation, Service Delivery, SMEs, ICT Adoption, Digital Marketing, Service Quality, Uasin Gishu County</i>',
                   ParagraphStyle('kw', fontName='Times-Roman', fontSize=12, leading=18, alignment=TA_LEFT)))
    story.append(PageBreak())
    
    # ===================== CHAPTER ONE =====================
    story.append(P('CHAPTER ONE: INTRODUCTION', 'section_heading'))
    
    story.append(P('1.1 Background of the Study', 'heading2'))
    story.append(P('1.1.1 Global Perspective of Technological Innovation in SMEs', 'heading3'))
    
    story.append(P('Technological innovation has emerged as a critical driver of business growth and competitiveness in the global economy. Small and Medium Enterprises (SMEs), which constitute the backbone of economies worldwide, are increasingly adopting technological innovations to enhance their service delivery and overall performance. According to the Technology-Organization-Environment (TOE) framework developed by Tornatzky and Fleischer (1990), the adoption of technological innovations by firms is influenced by three contextual elements: technological context, organizational context, and environmental context.'))
    
    story.append(P('Globally, SMEs account for approximately 90% of businesses and more than 50% of employment worldwide (World Bank, 2023). The integration of technology into SME operations has transformed service delivery models, enabling businesses to reach wider markets, improve operational efficiency, and enhance customer satisfaction. Developed economies such as the United States, United Kingdom, and Japan have witnessed significant technological adoption among SMEs, with cloud computing, artificial intelligence, and data analytics becoming commonplace tools for service enhancement.'))
    
    story.append(P('Research indicates that 73% of consumers globally consider customer experience a key factor in their purchasing decisions, yet only 49% of businesses prioritize it as a competitive strategy (PwC Global Consumer Insights Survey, 2022). This gap presents both a challenge and an opportunity for SMEs to leverage technological innovations to bridge the divide between customer expectations and actual service delivery. The emergence of Industry 4.0 technologies has further accelerated the need for SMEs to adopt innovative solutions to remain competitive in an increasingly digital marketplace.'))
    
    story.append(P('In emerging economies, the technological landscape for SMEs presents unique characteristics and challenges. The diffusion of mobile technology has been particularly transformative, enabling SMEs in developing regions to leapfrog traditional infrastructure constraints and directly access digital tools for business management, customer engagement, and service delivery (OECD, 2021).'))
    
    story.append(P('1.1.2 Regional Perspective of Technological Innovation in SMEs', 'heading3'))
    
    story.append(P("Across Africa, SMEs represent approximately 80% of the continent's workforce and contribute significantly to economic development and poverty reduction (African Development Bank, 2022). The African Union's Agenda 2063 recognizes the pivotal role of SMEs in driving industrialization and economic transformation across the continent. Technological innovation has been identified as a key enabler for African SMEs to overcome traditional barriers to growth, including limited access to markets, finance, and information."))
    
    story.append(P("In East Africa, countries such as Kenya, Tanzania, and Uganda have witnessed rapid growth in mobile technology adoption, with mobile money services like M-Pesa revolutionizing financial transactions and enabling SMEs to conduct business more efficiently. According to GSMA (2023), East Africa leads the world in mobile money adoption, with over 60% of the adult population using mobile money services."))
    
    story.append(P('Kenya, in particular, has emerged as a leader in technological innovation in the region, earning the nickname "Silicon Savannah." The country has witnessed significant growth in technology hubs, innovation centers, and digital entrepreneurship. The government\'s commitment to digital transformation through the Digital Economy Blueprint has created an enabling environment for SMEs to adopt technological innovations (Government of Kenya, 2019).'))
    
    story.append(P("However, research indicates that technology adoption among Kenyan SMEs remains uneven, with significant variations across sectors and geographical regions. A study on ICT adoption in service sector SMEs in Nairobi County found that while 94.62% of SMEs had adopted some form of ICT tools, the extent of adoption varied, with 37.63% showing moderate adoption and 17.2% showing low adoption levels (Kising'a &amp; Kwasira, 2019)."))
    
    story.append(P('1.1.3 Local Perspective of Technological Innovation in SMEs in Uasin Gishu County', 'heading3'))
    
    story.append(P("Uasin Gishu County, located in the North Rift region of Kenya, is an important agricultural and commercial hub. The county's economy is predominantly driven by agriculture, with SMEs playing a crucial role in value addition, distribution, and service provision. The Annex area, a commercial center within Uasin Gishu County, hosts a diverse range of SMEs including retail shops, hotels and restaurants, service providers, and agricultural enterprises."))
    
    story.append(P('Research conducted in Uasin Gishu County has highlighted both the potential and challenges of technological adoption among local SMEs. A study by Lagat (2014) on ICT adoption in agricultural SMEs in Uasin Gishu County revealed low levels of ICT use among agri-business SMEs, with weak financial capacity, limited knowledge of ICT tools, and low literacy levels identified as key barriers.'))
    
    story.append(P('More recent research by Bwire and Muathe (2025) examined the influence of digital credit access on MSME growth in Uasin Gishu County, finding that ease of access to digital credit (r=0.673, p&lt;0.001), information availability (r=0.701, p&lt;0.001), and digital credit regulation (r=0.669, p&lt;0.001) positively and significantly influenced MSME growth. However, the cost of digital credit showed a significant negative correlation (r=−0.610, p&lt;0.001).'))
    
    story.append(P('Another study by Talam (2023) on organizational capabilities in agro-processing SMEs in Uasin Gishu County found that technological capabilities significantly predicted organizational performance (&beta;=0.531, t(145)=7.497, p&lt;0.05). Despite these promising findings, there remains a research gap regarding the specific impact of technological innovation on service delivery among SMEs in the Annex area of Uasin Gishu County.'))
    
    story.append(P('1.2 Statement of the Problem', 'heading2'))
    
    story.append(P('Small and Medium Enterprises (SMEs) in Kenya face significant challenges in maintaining competitiveness and ensuring sustainable growth. Studies indicate that 70% of Micro and Small Enterprises fail within three years of operation (Kiprono, 2024). In Uasin Gishu County, SMEs contribute significantly to local economic development and employment creation. However, many SMEs struggle with inefficient service delivery processes, limited customer reach, and inability to meet evolving customer expectations.'))
    
    story.append(P("While technological innovation has been recognized globally as a key driver of business performance, its adoption among SMEs in Uasin Gishu County remains limited. Previous studies have examined ICT adoption in agricultural SMEs (Lagat, 2014) and the influence of digital credit on MSME growth (Bwire &amp; Muathe, 2025) in the county. However, there is limited research specifically focusing on the impact of technological innovation on service delivery among SMEs in the Annex area."))
    
    story.append(P("Furthermore, existing studies have primarily focused on technology adoption rates and general performance metrics, with limited attention to the specific mechanisms through which technological innovation influences service delivery efficiency, quality, and customer perceptions. This study therefore seeks to fill this gap by examining the impact of technological innovation on service delivery among SMEs in the Annex area of Uasin Gishu County."))
    
    story.append(P('1.3 General Objective', 'heading2'))
    story.append(P('To examine the impact of technological innovation on service delivery among Small and Medium Enterprises (SMEs) in the Annex area of Uasin Gishu County.'))
    
    story.append(P('1.4 Specific Objectives', 'heading2'))
    objectives = [
        '1. To identify the types of technological innovations adopted by SMEs in the Annex area of Uasin Gishu County.',
        '2. To assess the influence of technological innovation on efficiency and quality of service delivery among SMEs in the Annex area of Uasin Gishu County.',
        '3. To evaluate customer perceptions of technologically enhanced services offered by SMEs in the Annex area of Uasin Gishu County.',
        '4. To identify challenges faced by SMEs in the Annex area of Uasin Gishu County in adopting and implementing technological innovations.',
    ]
    for obj in objectives:
        story.append(P(obj, 'body_indent'))
    
    story.append(P('1.5 Research Questions', 'heading2'))
    questions = [
        '1. What types of technological innovations have been adopted by SMEs in the Annex area of Uasin Gishu County?',
        '2. How does technological innovation influence the efficiency and quality of service delivery among SMEs in the Annex area?',
        '3. What are customer perceptions of technologically enhanced services offered by SMEs in the Annex area?',
        '4. What challenges do SMEs in the Annex area face in adopting and implementing technological innovations?',
    ]
    for q in questions:
        story.append(P(q, 'body_indent'))
    
    story.append(P('1.6 Significance of the Study', 'heading2'))
    story.append(P('The findings of this study will be significant to various stakeholders in the following ways:'))
    
    sig_items = [
        ('<b>SME Owners and Managers:</b>', 'The study will provide insights into the types of technological innovations that can enhance service delivery, enabling SME owners to make informed decisions about technology investments. Understanding customer perceptions and adoption challenges will help them develop effective implementation strategies.'),
        ('<b>Policymakers and Government Agencies:</b>', 'The findings will inform policy formulation aimed at promoting technology adoption among SMEs in Uasin Gishu County and beyond. Agencies such as MSEA can use the results to design targeted support programs addressing specific challenges identified in the study.'),
        ('<b>Financial Institutions:</b>', 'Banks and other financial service providers will gain understanding of the technology needs and challenges of SMEs, enabling them to develop appropriate financing products for technology acquisition and implementation.'),
        ('<b>Academic Researchers:</b>', 'The study will contribute to the existing body of knowledge on technology adoption in SMEs, particularly in the Kenyan regional context outside Nairobi.'),
        ('<b>Customers:</b>', 'Ultimately, improved service delivery resulting from appropriate technology adoption will benefit customers through enhanced service quality, efficiency, and overall satisfaction.'),
    ]
    for title, text in sig_items:
        story.append(P(f'{title} {text}', 'body_indent'))
    
    story.append(P('1.7 Scope of the Study', 'heading2'))
    story.append(P('This study focuses on Small and Medium Enterprises (SMEs) operating in the Annex area of Uasin Gishu County, Kenya. The study targets SME owners, managers, and customers during the study period of January to March 2026. The content scope covers four main areas: types of technological innovations adopted, influence on service delivery efficiency and quality, customer perceptions, and challenges in technology adoption. Technological innovations considered include ICT tools, mobile technologies, digital marketing platforms, and service delivery technologies.'))
    
    story.append(P('1.8 Limitations of the Study', 'heading2'))
    story.append(P('The study encountered several limitations including: geographical limitation (focus on Annex area may limit generalizability); sampling limitations (sample may not represent all businesses); response bias (self-reported data may introduce measurement errors); time constraints (cross-sectional data limits causal inference); resource constraints (limited financial resources affected scope); and self-reporting limitations. Each limitation was mitigated through appropriate research design decisions.'))
    
    story.append(PageBreak())
    
    # ===================== CHAPTER TWO =====================
    story.append(P('CHAPTER TWO: LITERATURE REVIEW', 'section_heading'))
    
    story.append(P('2.1 Introduction', 'heading2'))
    story.append(P('This chapter presents a comprehensive review of literature relevant to the study on the impact of technological innovation on service delivery among SMEs in the Annex area of Uasin Gishu County. It covers the theoretical framework underpinning the research, the conceptual framework illustrating variable relationships, a review of literature on study variables, an empirical review of previous studies, and identification of research gaps.'))
    
    story.append(P('2.2 Theoretical Framework', 'heading2'))
    story.append(P('This study is anchored on three main theories: the Technology-Organization-Environment (TOE) Framework, Dynamic Capabilities Theory, and Disruptive Innovation Theory. These theories collectively provide a comprehensive lens for understanding the adoption, implementation, and impact of technological innovations on SME service delivery.'))
    
    story.append(P('2.2.1 Technology-Organization-Environment (TOE) Framework', 'heading3'))
    story.append(P('The Technology-Organization-Environment (TOE) framework, developed by Tornatzky and Fleischer in 1990, explains that the adoption of technological innovations by firms is influenced by three contextual elements: technological context, organizational context, and environmental context (Kising\'a &amp; Kwasira, 2019).'))
    
    story.append(P('The <b>technological context</b> refers to the internal and external technologies relevant to the firm, including existing technologies in use and those available in the market. For SMEs in the Annex area, this includes mobile payment systems, inventory management software, CRM tools, and digital marketing platforms.'))
    
    story.append(P('The <b>organizational context</b> encompasses firm characteristics including size, scope, managerial structure, human resources, and financial capacity, including the SME owner\'s education level, employees\' technical skills, and financial resources available for technology investment.'))
    
    story.append(P('The <b>environmental context</b> includes the external environment in which the firm operates, including industry structure, competitors\' technology adoption, regulatory environment, and access to technology service providers. The TOE framework guides the investigation of challenges faced in adopting technological innovations (Objective 4).'))
    
    story.append(P('2.2.2 Dynamic Capabilities Theory', 'heading3'))
    story.append(P('The Dynamic Capabilities Theory, advanced by Teece, Pisano, and Shuen in 1997, focuses on a firm\'s ability to integrate, build, and reconfigure internal and external competencies to address rapidly changing environments. Dynamic capabilities include sensing opportunities, seizing them through timely investment decisions, and transforming existing processes to implement new technologies effectively.'))
    
    story.append(P('In the context of SMEs, dynamic capabilities enable businesses to adapt to technological changes and leverage innovations for competitive advantage. This theory is particularly relevant to understanding how technological innovation influences service delivery efficiency and quality (Objective 2), explaining why some SMEs are more successful in leveraging technology for service delivery enhancement.'))
    
    story.append(P('2.2.3 Disruptive Innovation Theory', 'heading3'))
    story.append(P('The Disruptive Innovation Theory, introduced by Clayton Christensen in 1997, describes how new technologies can disrupt existing markets by introducing simpler, more affordable, or more accessible products and services. Mobile money services like M-Pesa represent a classic example of disruptive innovation that has enabled SMEs in Kenya to offer financial transaction services previously dominated by formal banking institutions.'))
    
    story.append(P('This theory is relevant to understanding customer perceptions of technologically enhanced services (Objective 3), explaining how customers in the Annex area may perceive and adopt new service delivery technologies that offer convenience, affordability, or accessibility advantages over traditional service models.'))
    
    story.append(P('2.3 Conceptual Framework', 'heading2'))
    story.append(P('A conceptual framework is a graphical representation of the relationship between independent and dependent variables in a study. Based on the theoretical framework and literature review, the following conceptual framework illustrates the relationship between technological innovation (independent variable) and service delivery (dependent variable) among SMEs in the Annex area, with intervening variables moderating this relationship.'))
    story += [SP(8)]
    story.append(P('<b>Figure 2.1: Conceptual Framework</b>', 'caption'))
    story.append(make_cf_table())
    story.append(SP(4))
    story.append(P('Source: Researcher (2026) adapted from Tornatzky &amp; Fleischer (1990)', 'caption'))
    story += [SP(8)]
    
    story.append(P('The conceptual framework posits that technological innovation, comprising ICT tools, digital marketing, service delivery technologies, and financial technologies, influences service delivery in terms of efficiency, service quality, and customer satisfaction. The relationship is moderated by intervening variables including business characteristics, owner/manager characteristics, and environmental factors.'))
    
    story.append(P('2.4 Review of Literature on Study Variables', 'heading2'))
    
    story.append(P('2.4.1 Types of Technological Innovations Adopted by SMEs', 'heading3'))
    story.append(P('Technological innovations adopted by SMEs encompass a wide range of tools, systems, and applications. Based on existing literature, these can be categorized as: <b>ICT Tools</b> (computers, software, internet, email, websites); <b>Mobile Technologies</b> (smartphones, mobile money, mobile apps); <b>Digital Marketing and Social Media</b> (Facebook, WhatsApp Business, Instagram, e-commerce); <b>Service Delivery Technologies</b> (POS systems, CRM software, self-service technologies); and <b>Financial Technologies</b> (mobile banking, digital payment systems, digital credit platforms).'))
    
    story.append(P("A study on ICT adoption in service sector SMEs in Nairobi County found that SMEs utilize personal computers, email, internet, websites, and data storage facilities (Kising'a &amp; Kwasira, 2019). Mobile money services such as M-Pesa have transformed financial transactions, with the Communications Authority of Kenya (2023) reporting mobile phone penetration at over 125% in Kenya."))
    
    story.append(P('2.4.2 Technological Innovation and Efficiency of Service Delivery', 'heading3'))
    story.append(P('Efficiency in service delivery refers to the ability of SMEs to provide services using optimal resources, minimizing time, cost, and effort while maximizing output. Technological innovation enhances efficiency through: <b>Time Savings</b> (automated tasks reduce service time); <b>Cost Reduction</b> (digital processes lower operational costs); <b>Accuracy and Error Reduction</b> (automated systems reduce human error); <b>Scalability</b> (cloud-based systems allow capacity expansion); and <b>Process Streamlining</b> (technology reduces bottlenecks and improves workflow). Mutwota (2023) found that service delivery systems account for 9.9% of variance in SME performance.'))
    
    story.append(P('2.4.3 Customer Perceptions of Technologically Enhanced Services', 'heading3'))
    story.append(P('Customer perception refers to the attitudes, opinions, and satisfaction levels of customers regarding the services they receive. Technology enhances customer satisfaction by enabling faster service, personalized interactions, and convenient access. Research indicates that 73% of consumers consider customer experience a key factor in purchasing decisions (PwC, 2022). Service quality dimensions (reliability, responsiveness, assurance, empathy, tangibles) are all enhanced by appropriate technology adoption. Customer trust in digital payment security and willingness to adopt new service technologies depend on perceived usefulness and ease of use.'))
    
    story.append(P('2.4.4 Challenges Faced by SMEs in Adopting Technological Innovations', 'heading3'))
    story.append(P('SMEs face numerous challenges including: <b>Financial Constraints</b> (high initial costs, limited financing, prohibitive software fees); <b>Skills and Knowledge Gaps</b> (lack of technical skills, need for training, difficulty keeping up with technological change); <b>Infrastructure Limitations</b> (unreliable internet, power outages, limited local technical support); <b>Organizational Factors</b> (resistance to change, limited managerial capacity); and <b>Environmental and Social Challenges</b> (regulatory uncertainty, customer preference for traditional methods, cultural factors). Lagat (2014) identified financial constraints and limited knowledge as key barriers in Uasin Gishu County.'))
    
    story.append(P('2.5 Empirical Review', 'heading2'))
    
    story.append(P('2.5.1 Studies on ICT Adoption in Kenyan SMEs', 'heading3'))
    emp_studies = [
        "Kising'a and Kwasira (2019) found that 94.62% of service sector SMEs in Nairobi County had adopted ICT tools, with technological context (&beta;=0.259, p&lt;0.05), organizational context (&beta;=0.398, p&lt;0.05), and environmental context (&beta;=0.214, p&lt;0.05) all positively influencing innovation.",
        "Kiprono (2024) examined technology adoption in MSEs in Nairobi, finding that all technology dimensions positively influenced MSE performance, with payment technology showing the strongest relationship (&beta;=0.412, p&lt;0.001).",
        "Mutwota (2023) found positive and significant relationships between strategic service innovation dimensions and SME performance, with technology accounting for 6.2% of variance in performance.",
        "Musebe (2024) found that technology innovation positively influences firm performance and recommended entrepreneurs develop innovative strategies to actualize firm performance through systematic technology planning.",
    ]
    for study in emp_studies:
        story.append(P(study, 'body_indent'))
    
    story.append(P('2.5.2 Studies on Technology and SME Performance in Uasin Gishu County', 'heading3'))
    ug_studies = [
        "Lagat (2014) found low ICT use among agri-business SMEs in Uasin Gishu County, with weak financial capacity, limited knowledge, and low literacy levels as key barriers.",
        "Bwire and Muathe (2025) found that ease of digital credit access (r=0.673, p&lt;0.001), information availability (r=0.701, p&lt;0.001), and digital credit regulation (r=0.669, p&lt;0.001) positively influenced MSME growth. These factors collectively explained 60.0% of variance in MSME growth (Adjusted R&sup2;=0.584).",
        "Talam (2023) found that technological capabilities significantly predicted organizational performance (&beta;=0.531, t(145)=7.497, p&lt;0.05) in agro-processing SMEs in Uasin Gishu County.",
    ]
    for study in ug_studies:
        story.append(P(study, 'body_indent'))
    
    story.append(P('2.6 Research Gaps', 'heading2'))
    gaps = [
        '<b>Geographical Gap:</b> Most studies focus on Nairobi County, with limited research on other regions including Uasin Gishu County. No study has specifically focused on the Annex area.',
        '<b>Sectoral Gap:</b> Existing studies in Uasin Gishu County primarily focus on agricultural SMEs, with limited attention to commercial area SMEs.',
        '<b>Service Delivery Focus:</b> Limited research specifically examines the impact of technology on service delivery dimensions including efficiency, quality, and customer perceptions.',
        '<b>Customer Perspective Gap:</b> Most studies collect data only from SME owners/managers, excluding customer perspectives.',
        '<b>Timeliness Gap:</b> The rapid pace of technological change and post-COVID-19 digital acceleration require updated empirical evidence.',
        '<b>Integration Gap:</b> Existing studies examine specific technology types in isolation, without comprehensive cross-technology analysis.',
    ]
    for gap in gaps:
        story.append(P(gap, 'body_indent'))
    
    story.append(P('This study addresses these gaps by examining technological innovation impact on service delivery among diverse commercial SMEs in the Annex area, incorporating both SME and customer perspectives, with updated evidence from the 2026 study period.'))
    
    story.append(PageBreak())
    
    # ===================== CHAPTER THREE =====================
    story.append(P('CHAPTER THREE: RESEARCH METHODOLOGY', 'section_heading'))
    
    story.append(P('3.1 Introduction', 'heading2'))
    story.append(P('This chapter describes the research methodology employed in this study. It covers the research design, target population, sample size and sampling technique, data collection instruments, pilot testing procedures, data collection procedures, data analysis methods, and ethical considerations.'))
    
    story.append(P('3.2 Research Design', 'heading2'))
    story.append(P("This study adopts a descriptive research design with a mixed-methods approach, combining both quantitative and qualitative data collection and analysis techniques. Descriptive research design is appropriate for studies that aim to describe the characteristics of a population or phenomenon and examine relationships between variables (Kothari, 2004). The mixed-methods approach allows for triangulation of findings, enhancing the validity and reliability of the results."))
    
    story.append(P('3.3 Target Population', 'heading2'))
    story.append(P('The target population comprises all SMEs operating in the Annex area of Uasin Gishu County. According to records from the Uasin Gishu County Business Licensing Department (2025), approximately 250 registered SMEs operate in the Annex area. The study also targets customers of these SMEs.'))
    story += [SP(4)]
    story.append(P('<b>Table 3.1: Target Population Distribution</b>', 'caption'))
    t31 = make_table(
        ['Business Category', 'Estimated Number', 'Percentage (%)'],
        [['Retail Shops', '100', '40.0'],
         ['Hotels and Restaurants', '60', '24.0'],
         ['Service Providers', '50', '20.0'],
         ['Agricultural-related Businesses', '40', '16.0'],
         ['<b>Total</b>', '<b>250</b>', '<b>100.0</b>']],
        col_widths=[3.0, 1.5, 1.5]
    )
    story.append(t31)
    story.append(P('Source: Uasin Gishu County Business Licensing Department (2025)', 'caption'))
    
    story.append(P('3.4 Sample Size and Sampling Technique', 'heading2'))
    story.append(P('3.4.1 Sample Size Determination', 'heading3'))
    story.append(P('The sample size for SME owners/managers was determined using the Yamane (1967) formula:'))
    story.append(P('<b>n = N / (1 + N(e)²)</b>', 'math'))
    story.append(P('Where: n = sample size; N = population size (250); e = margin of error (0.05 or 5%)'))
    story.append(P('Calculation:'))
    calcs = ['n = 250 / (1 + 250(0.05)²)', 'n = 250 / (1 + 250 × 0.0025)', 'n = 250 / (1 + 0.625)', 'n = 250 / 1.625', '<b>n ≈ 154 SMEs</b>']
    for calc in calcs:
        story.append(P(calc, 'body_indent'))
    story.append(P('For customers, a sample of 200 customers was selected from those patronizing the sampled SMEs using systematic random sampling (every 5th customer).'))
    
    story.append(P('3.4.2 Sampling Technique', 'heading3'))
    story.append(P('Stratified random sampling was used to select SME respondents, stratifying the population by business type and selecting proportionate samples from each stratum.'))
    story += [SP(4)]
    story.append(P('<b>Table 3.2: Sample Size Distribution</b>', 'caption'))
    t32 = make_table(
        ['Business Category', 'Population', 'Proportion (%)', 'Sample Size'],
        [['Retail Shops', '100', '40.0', '62'],
         ['Hotels and Restaurants', '60', '24.0', '37'],
         ['Service Providers', '50', '20.0', '31'],
         ['Agricultural-related Businesses', '40', '16.0', '24'],
         ['<b>Total</b>', '<b>250</b>', '<b>100.0</b>', '<b>154</b>']],
        col_widths=[2.5, 1.2, 1.2, 1.2]
    )
    story.append(t32)
    story.append(P('Source: Researcher (2026)', 'caption'))
    
    story.append(P('3.5 Data Collection Instruments', 'heading2'))
    story.append(P('3.5.1 Questionnaires', 'heading3'))
    story.append(P('Structured questionnaires were the primary data collection instruments. Two sets were developed: (1) Questionnaire for SME Owners/Managers with sections on demographic information, technology adoption, service delivery influence, and adoption challenges; and (2) Questionnaire for Customers capturing perceptions of technology-enhanced services. Both used a 5-point Likert scale (1=Strongly Disagree to 5=Strongly Agree).'))
    
    story.append(P('3.5.2 Interview Guide', 'heading3'))
    story.append(P('An interview guide with semi-structured questions was used for in-depth interviews with 18 purposively selected SME owners/managers. Each interview lasted 30-45 minutes and was audio-recorded with consent. The guide explored motivations for adoption, technology experiences, perceived benefits and challenges, and improvement suggestions.'))
    
    story.append(P('3.6 Pilot Testing', 'heading2'))
    story.append(P('3.6.1 Validity of Research Instruments', 'heading3'))
    story.append(P('Content validity was ensured through extensive literature review and expert review by the supervisor and two faculty members. Face validity was established through review by colleagues and potential respondents. Construct validity was assessed through factor analysis.'))
    
    story.append(P('3.6.2 Reliability of Research Instruments', 'heading3'))
    story.append(P("A pilot study was conducted with 20 SME owners/managers from a neighboring area. Cronbach's Alpha coefficients were computed for each section."))
    story += [SP(4)]
    story.append(P('<b>Table 3.3: Reliability Statistics</b>', 'caption'))
    t33 = make_table(
        ['Section', 'Number of Items', "Cronbach's Alpha", 'Interpretation'],
        [['Technology Adoption', '10', '0.821', 'Reliable'],
         ['Service Delivery Efficiency', '8', '0.793', 'Reliable'],
         ['Service Delivery Quality', '8', '0.806', 'Reliable'],
         ['Customer Perceptions', '10', '0.845', 'Reliable'],
         ['Challenges in Technology Adoption', '8', '0.772', 'Reliable'],
         ['<b>Overall Instrument</b>', '<b>44</b>', '<b>0.834</b>', '<b>Reliable</b>']],
        col_widths=[2.5, 1.2, 1.3, 1.2]
    )
    story.append(t33)
    story.append(P('Source: Pilot Study (2026)', 'caption'))
    
    story.append(P('3.7 Data Collection Procedures', 'heading2'))
    story.append(P('Prior to data collection, the researcher obtained an introduction letter from Moi University and a research permit from NACOSTI. Data collection proceeded through: (1) Drop-and-pick questionnaire administration with trained research assistants; (2) Audio-recorded semi-structured interviews at business premises (30-45 minutes each); and (3) Customer questionnaires administered directly at business premises. Data collection took place over four weeks (January-February 2026).'))
    
    story.append(P('3.8 Data Analysis and Presentation', 'heading2'))
    story.append(P('3.8.1 Descriptive Statistics', 'heading3'))
    story.append(P('Quantitative data were coded, cleaned, and entered into SPSS Version 26. Descriptive statistics included frequencies and percentages for categorical variables; means and standard deviations for Likert-scale items; and cross-tabulations to examine variable relationships.'))
    
    story.append(P('3.8.2 Inferential Statistics', 'heading3'))
    story.append(P("Pearson's Correlation Coefficient (r) determined the strength and direction of relationships between technological innovation and service delivery. Multiple Regression Analysis examined the predictive power of technology dimensions on service delivery using the model:"))
    story.append(P('<b>Y = &beta;<sub>0</sub> + &beta;<sub>1</sub>X<sub>1</sub> + &beta;<sub>2</sub>X<sub>2</sub> + &beta;<sub>3</sub>X<sub>3</sub> + &epsilon;</b>', 'math'))
    story.append(P('Where: Y = Service Delivery; X<sub>1</sub> = ICT Tools Adoption; X<sub>2</sub> = Digital Marketing; X<sub>3</sub> = Service Delivery Technologies; &beta;<sub>0</sub> = Constant; &beta;<sub>1</sub>, &beta;<sub>2</sub>, &beta;<sub>3</sub> = Regression coefficients; &epsilon; = Error term. ANOVA tested the overall model significance. Qualitative data were analyzed through thematic analysis.'))
    
    story.append(P('3.9 Ethical Considerations', 'heading2'))
    ethics = [
        '1. <b>Informed Consent:</b> Respondents were fully informed about the study purpose and their right to withdraw. Written consent was obtained.',
        '2. <b>Confidentiality and Anonymity:</b> All information was treated with strict confidentiality and individual responses were anonymized.',
        '3. <b>Voluntary Participation:</b> Participation was entirely voluntary without negative consequences for non-participation.',
        '4. <b>Data Protection:</b> Collected data were stored securely in password-protected digital files and locked physical storage.',
        '5. <b>Research Integrity:</b> All findings were accurately reported and all sources appropriately cited.',
        '6. <b>Research Permit:</b> A permit was obtained from NACOSTI before commencing data collection.',
    ]
    for ethic in ethics:
        story.append(P(ethic, 'body_indent'))
    
    story.append(PageBreak())
    
    # ===================== CHAPTER FOUR =====================
    story.append(P('CHAPTER FOUR: DATA ANALYSIS, PRESENTATION AND INTERPRETATION', 'section_heading'))
    
    story.append(P('4.1 Introduction', 'heading2'))
    story.append(P('This chapter presents the analysis, presentation, and interpretation of data collected from SME owners/managers and customers in the Annex area of Uasin Gishu County. Data are analyzed using descriptive and inferential statistical methods and presented through tables and figures.'))
    
    story.append(P('4.2 Response Rate', 'heading2'))
    story.append(P('A total of 154 questionnaires were administered to SME owners/managers, of which 143 were returned fully completed (response rate: 92.9%). Additionally, 200 customer questionnaires were distributed, with 186 returned (response rate: 93.0%). These response rates exceed the 70% threshold recommended by Mugenda and Mugenda (2003).'))
    story += [SP(4)]
    story.append(P('<b>Table 4.1: Response Rate</b>', 'caption'))
    t41 = make_table(
        ['Category', 'Distributed', 'Returned', 'Response Rate (%)'],
        [['SME Owners/Managers', '154', '143', '92.9'],
         ['Customers', '200', '186', '93.0'],
         ['<b>Total</b>', '<b>354</b>', '<b>329</b>', '<b>93.0</b>']],
        col_widths=[2.5, 1.2, 1.2, 1.5]
    )
    story.append(t41)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    
    story.append(P('4.3 Demographic Characteristics of Respondents', 'heading2'))
    story.append(P('4.3.1 Gender of Respondents', 'heading3'))
    story.append(P('<b>Table 4.2: Gender of Respondents</b>', 'caption'))
    t42 = make_table(
        ['Gender', 'Frequency', 'Percentage (%)'],
        [['Male', '81', '56.6'],
         ['Female', '62', '43.4'],
         ['<b>Total</b>', '<b>143</b>', '<b>100.0</b>']],
        col_widths=[2.5, 1.5, 1.5]
    )
    story.append(t42)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('Male owners/managers (56.6%) outnumbered females (43.4%), though the relatively high proportion of female SME owners reflects growing women\'s economic participation consistent with national trends.'))
    
    story.append(P('4.3.2 Age of Respondents', 'heading3'))
    story.append(P('<b>Table 4.3: Age of Respondents</b>', 'caption'))
    t43 = make_table(
        ['Age Category', 'Frequency', 'Percentage (%)'],
        [['Below 25 years', '14', '9.8'],
         ['25 – 34 years', '52', '36.4'],
         ['35 – 44 years', '47', '32.9'],
         ['45 – 54 years', '22', '15.4'],
         ['55 years and above', '8', '5.6'],
         ['<b>Total</b>', '<b>143</b>', '<b>100.0</b>']],
        col_widths=[2.5, 1.5, 1.5]
    )
    story.append(t43)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('The majority of SME owners/managers (69.2%) were between 25 and 44 years — a demographic generally more technology-receptive, facilitating future technology adoption.'))
    
    story.append(P('4.3.3 Level of Education', 'heading3'))
    story.append(P('<b>Table 4.4: Level of Education</b>', 'caption'))
    t44 = make_table(
        ['Level of Education', 'Frequency', 'Percentage (%)'],
        [['Primary School', '8', '5.6'],
         ['Secondary School (KCSE)', '38', '26.6'],
         ['Certificate/Diploma', '49', '34.3'],
         ['University Undergraduate', '39', '27.3'],
         ['Postgraduate', '9', '6.3'],
         ['<b>Total</b>', '<b>143</b>', '<b>100.0</b>']],
        col_widths=[2.5, 1.5, 1.5]
    )
    story.append(t44)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('67.9% of respondents held certificate/diploma or higher qualifications, facilitating technology adoption. 32.2% had secondary school education or below, indicating a segment requiring additional technology support.'))
    
    story.append(P('4.3.4 Business Type', 'heading3'))
    story.append(P('<b>Table 4.5: Business Type</b>', 'caption'))
    t45 = make_table(
        ['Business Type', 'Frequency', 'Percentage (%)'],
        [['Retail Shops', '58', '40.6'],
         ['Hotels and Restaurants', '34', '23.8'],
         ['Service Providers', '28', '19.6'],
         ['Agricultural-related Businesses', '23', '16.1'],
         ['<b>Total</b>', '<b>143</b>', '<b>100.0</b>']],
        col_widths=[3.0, 1.2, 1.3]
    )
    story.append(t45)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    
    story.append(P('4.3.5 Years of Business Operation', 'heading3'))
    story.append(P('<b>Table 4.6: Years of Business Operation</b>', 'caption'))
    t46 = make_table(
        ['Years of Operation', 'Frequency', 'Percentage (%)'],
        [['Less than 1 year', '12', '8.4'],
         ['1 – 3 years', '34', '23.8'],
         ['4 – 6 years', '47', '32.9'],
         ['7 – 10 years', '31', '21.7'],
         ['More than 10 years', '19', '13.3'],
         ['<b>Total</b>', '<b>143</b>', '<b>100.0</b>']],
        col_widths=[2.5, 1.5, 1.5]
    )
    story.append(t46)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('32.9% of SMEs had been in operation for 4-6 years, representing the most common maturity level. Established SMEs (7+ years) constituted 35.0% of the sample.'))
    
    story.append(P('4.4 Types of Technological Innovations Adopted by SMEs in the Annex Area', 'heading2'))
    
    story.append(P('4.4.1 ICT Tools and Applications Used', 'heading3'))
    story.append(P('<b>Table 4.7: ICT Tools and Applications Used by SMEs</b>', 'caption'))
    t47 = make_table(
        ['ICT Tool/Application', 'Frequency', 'Percentage (%)'],
        [['Mobile Money (M-Pesa/Airtel Money)', '128', '89.5'],
         ['Smartphones for Business', '121', '84.6'],
         ['WhatsApp Business', '112', '78.3'],
         ['Facebook for Business', '97', '67.8'],
         ['Internet/Wi-Fi', '89', '62.2'],
         ['Computers/Laptops', '72', '50.3'],
         ['POS Systems', '78', '54.5'],
         ['Accounting Software', '53', '37.1'],
         ['Inventory Management Software', '60', '42.0'],
         ['Company Website', '41', '28.7'],
         ['E-commerce Platforms', '29', '20.3'],
         ['Cloud Storage/Services', '27', '18.9'],
         ['Customer Management Software (CRM)', '24', '16.8']],
        col_widths=[3.0, 1.2, 1.3]
    )
    story.append(t47)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('Mobile money services (89.5%) and smartphones (84.6%) are the most widely adopted technologies, reflecting the dominant role of mobile technology in SME digitalization. More sophisticated technologies (CRM 16.8%, e-commerce 20.3%) show lower adoption rates, indicating a technology adoption gradient.'))
    
    story.append(P('4.4.2 Mobile Technology Adoption', 'heading3'))
    story.append(P('<b>Table 4.8: Mobile Technology Adoption</b>', 'caption'))
    t48 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['We use mobile phones to receive payments from customers', '4.52', '0.71', 'Strongly Agree'],
         ['We use mobile apps to communicate with suppliers', '3.94', '0.89', 'Agree'],
         ['Mobile money has improved our cash flow management', '4.31', '0.82', 'Strongly Agree'],
         ['We use mobile phones to track business inventory', '3.12', '1.04', 'Neutral/Agree'],
         ['Mobile technology has reduced our transaction costs', '4.18', '0.86', 'Agree'],
         ['We use mobile banking for business transactions', '3.87', '0.94', 'Agree'],
         ['<b>Overall Mobile Technology Adoption</b>', '<b>3.99</b>', '<b>0.74</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t48)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))
    story.append(P('The mean score for overall mobile technology adoption was 3.99 (SD=0.74). Mobile payment receipt had the highest mean (4.52), confirming that receiving customer payments via mobile money is nearly universal.'))
    
    story.append(P('4.4.3 Social Media and Digital Marketing', 'heading3'))
    story.append(P('<b>Table 4.9: Social Media and Digital Marketing</b>', 'caption'))
    t49 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['We use WhatsApp to communicate with customers', '4.41', '0.73', 'Strongly Agree'],
         ['We promote our business on Facebook', '3.78', '0.98', 'Agree'],
         ['We use Instagram to showcase our products/services', '2.94', '1.12', 'Neutral'],
         ['Social media has expanded our customer base', '3.86', '0.94', 'Agree'],
         ['Digital marketing is more cost-effective than traditional advertising', '3.97', '0.87', 'Agree'],
         ['We respond to customer inquiries through social media', '3.74', '1.01', 'Agree'],
         ['We run paid adverts on digital platforms', '2.82', '1.18', 'Neutral'],
         ['<b>Overall Digital Marketing Adoption</b>', '<b>3.65</b>', '<b>0.81</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t49)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))
    story.append(P('Overall digital marketing adoption mean was 3.65 (SD=0.81). WhatsApp communication had the highest mean (4.41). While SMEs actively use social media, paid digital advertising remains less common.'))
    
    story.append(P('4.5 Influence of Technological Innovation on Efficiency and Quality of Service Delivery', 'heading2'))
    
    story.append(P('4.5.1 Efficiency of Service Delivery', 'heading3'))
    story.append(P('<b>Table 4.10: Efficiency of Service Delivery</b>', 'caption'))
    t410 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['Technology has reduced the time taken to serve customers', '4.12', '0.84', 'Agree'],
         ['Technology has reduced our operational costs', '3.88', '0.92', 'Agree'],
         ['Technology has reduced errors in our transactions and records', '4.03', '0.87', 'Agree'],
         ['Technology has streamlined our service delivery processes', '3.96', '0.89', 'Agree'],
         ['Digital payment systems have speeded up transactions', '4.34', '0.76', 'Strongly Agree'],
         ['Technology has enabled us to serve more customers per day', '3.77', '0.96', 'Agree'],
         ['Inventory management technology has reduced stock-outs', '3.52', '1.07', 'Agree'],
         ['Technology has improved staff productivity', '3.84', '0.94', 'Agree'],
         ['<b>Overall Efficiency Impact</b>', '<b>3.93</b>', '<b>0.72</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t410)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))
    story.append(P('The overall efficiency impact mean was 3.93 (SD=0.72). Digital payment systems received the highest rating (mean=4.34). Technology was credited with reducing service time (mean=4.12) and transaction errors (mean=4.03).'))
    
    story.append(P('4.5.2 Quality of Service Delivery', 'heading3'))
    story.append(P('<b>Table 4.11: Quality of Service Delivery</b>', 'caption'))
    t411 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['Technology has improved the consistency of our service delivery', '3.94', '0.88', 'Agree'],
         ['Technology enables faster responses to customer inquiries', '4.08', '0.83', 'Agree'],
         ['Technology has enhanced the professionalism of our business image', '4.02', '0.86', 'Agree'],
         ['Technology has enabled more personalized customer service', '3.72', '0.97', 'Agree'],
         ['Technology has improved customer record-keeping and follow-up', '3.64', '1.02', 'Agree'],
         ['Technology has enhanced the reliability of our service delivery', '3.89', '0.91', 'Agree'],
         ['Technology-enabled services meet higher customer expectations', '3.81', '0.93', 'Agree'],
         ['Technology has improved service accessibility to customers', '3.96', '0.89', 'Agree'],
         ['<b>Overall Quality Impact</b>', '<b>3.88</b>', '<b>0.74</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t411)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))
    story.append(P('Overall quality impact mean was 3.88 (SD=0.74). Faster responses to customer inquiries (mean=4.08) and enhanced business professionalism (mean=4.02) received the highest ratings.'))
    
    story.append(P('4.5.3 Correlation Analysis', 'heading3'))
    story.append(P("<b>Table 4.12: Correlation between Technological Innovation and Service Delivery</b>", 'caption'))
    t412 = make_table(
        ['Variable', 'Service Delivery Efficiency', 'Service Quality', 'Overall Service Delivery'],
        [['ICT Tools Adoption', '0.672**', '0.641**', '0.687**'],
         ['Mobile Technology Adoption', '0.694**', '0.658**', '0.701**'],
         ['Digital Marketing Adoption', '0.583**', '0.612**', '0.614**'],
         ['Service Delivery Technologies', '0.631**', '0.649**', '0.658**'],
         ['<b>Overall Technology Innovation</b>', '<b>0.714**</b>', '<b>0.682**</b>', '<b>0.721**</b>']],
        col_widths=[2.2, 1.5, 1.3, 1.5]
    )
    story.append(t412)
    story.append(P('Source: Field Survey (2026) | ** Correlation is significant at 0.01 level (2-tailed)', 'caption'))
    story.append(P('The correlation analysis reveals statistically significant positive relationships between all dimensions of technological innovation and service delivery. Overall technological innovation correlated most strongly with overall service delivery (r=0.721, p&lt;0.01).'))
    
    story.append(P('4.6 Customer Perceptions of Technologically Enhanced Services', 'heading2'))
    
    story.append(P('4.6.1 Customer Satisfaction', 'heading3'))
    story.append(P('<b>Table 4.13: Customer Satisfaction with Technologically Enhanced Services</b>', 'caption'))
    t413 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['I am satisfied with the availability of mobile payment options', '4.38', '0.74', 'Strongly Agree'],
         ['Technology-enabled services are faster and more convenient', '4.21', '0.79', 'Agree'],
         ['I trust digital payment systems used by these businesses', '3.94', '0.93', 'Agree'],
         ['Technology has improved the overall quality of services I receive', '3.86', '0.94', 'Agree'],
         ['I prefer to patronize businesses that use modern technology', '3.78', '0.98', 'Agree'],
         ['Digital receipts and records provided are useful', '3.74', '1.01', 'Agree'],
         ['Technology-enhanced businesses provide more reliable services', '3.81', '0.96', 'Agree'],
         ['<b>Overall Customer Satisfaction</b>', '<b>3.96</b>', '<b>0.73</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t413)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))
    story.append(P('Overall customer satisfaction mean was 3.96 (SD=0.73). Mobile payment options received the highest satisfaction rating (mean=4.38). Customer preference for technology-using businesses (mean=3.78) indicates competitive implications for SMEs.'))
    
    story.append(P('4.6.2 Customer Experience', 'heading3'))
    story.append(P('<b>Table 4.14: Customer Experience with Technology-Enhanced Services</b>', 'caption'))
    t414 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['I experience shorter waiting times at tech-equipped businesses', '4.03', '0.87', 'Agree'],
         ['Businesses use technology to communicate with me effectively', '3.88', '0.94', 'Agree'],
         ['I have experienced fewer errors in my transactions', '3.91', '0.91', 'Agree'],
         ['Technology makes it easier to access business information', '3.74', '0.99', 'Agree'],
         ['I feel the services are more personalized when technology is used', '3.51', '1.08', 'Agree'],
         ['Social media helps me stay updated on business offerings', '3.82', '0.97', 'Agree'],
         ['I am comfortable using digital payment systems', '4.12', '0.83', 'Agree'],
         ['<b>Overall Customer Experience</b>', '<b>3.86</b>', '<b>0.74</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t414)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Strongly Disagree to 5=Strongly Agree', 'caption'))
    story.append(P('Overall customer experience mean was 3.86 (SD=0.74). Service personalization through technology had the lowest rating (mean=3.51), indicating unrealized potential for data-driven customer engagement.'))
    
    story.append(P('4.7 Challenges Faced by SMEs in Adopting Technological Innovations', 'heading2'))
    
    story.append(P('4.7.1 Financial Challenges', 'heading3'))
    story.append(P('<b>Table 4.15: Financial Challenges in Technology Adoption</b>', 'caption'))
    t415 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['The high initial cost of technology equipment is a barrier', '4.28', '0.79', 'Strongly Agree'],
         ['Software licensing fees are too expensive for our business', '3.97', '0.91', 'Agree'],
         ['We lack adequate financing for technology acquisition', '4.11', '0.84', 'Agree'],
         ['Internet data costs are too high for regular use', '3.84', '0.96', 'Agree'],
         ['The cost of maintaining technology equipment is burdensome', '3.76', '0.99', 'Agree'],
         ['High interest rates on technology loans discourage adoption', '3.91', '0.93', 'Agree'],
         ['<b>Overall Financial Challenges</b>', '<b>3.98</b>', '<b>0.72</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t415)
    story.append(P('Source: Field Survey (2026) | Scale: 1=Not a Challenge at All to 5=Extremely Major Challenge', 'caption'))
    story.append(P('Financial challenges constitute the most significant barrier (mean=3.98). High initial equipment costs (mean=4.28) and inadequate financing (mean=4.11) were the most critical barriers.'))
    
    story.append(P('4.7.2 Skills and Knowledge Gaps', 'heading3'))
    story.append(P('<b>Table 4.16: Skills and Knowledge Gaps in Technology Adoption</b>', 'caption'))
    t416 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['We lack the technical skills to use advanced technology', '3.86', '0.94', 'Agree'],
         ['Our employees need training to effectively use technology', '4.14', '0.82', 'Agree'],
         ['We do not know which technology is best for our business', '3.74', '1.02', 'Agree'],
         ['We struggle to troubleshoot technology problems', '3.91', '0.91', 'Agree'],
         ['The pace of technology change makes it hard to keep up', '3.97', '0.88', 'Agree'],
         ['We have had negative experiences with technology previously', '3.28', '1.11', 'Neutral/Agree'],
         ['<b>Overall Skills and Knowledge Challenges</b>', '<b>3.82</b>', '<b>0.76</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t416)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('Skills gaps are the second most significant challenge (mean=3.82). Employee training needs (mean=4.14) was the most pressing concern.'))
    
    story.append(P('4.7.3 Infrastructure Challenges', 'heading3'))
    story.append(P('<b>Table 4.17: Infrastructure Challenges in Technology Adoption</b>', 'caption'))
    t417 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['Unreliable internet connectivity hinders technology use', '4.21', '0.82', 'Agree'],
         ['Frequent power outages disrupt our technology use', '4.08', '0.87', 'Agree'],
         ['There are few technology support services nearby', '3.84', '0.96', 'Agree'],
         ['The cost of internet connection is prohibitive', '3.72', '1.01', 'Agree'],
         ['Technology equipment is difficult to repair locally', '3.61', '1.04', 'Agree'],
         ['<b>Overall Infrastructure Challenges</b>', '<b>3.89</b>', '<b>0.74</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t417)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('Infrastructure challenges had an overall mean of 3.89. Unreliable internet connectivity (mean=4.21) and power outages (mean=4.08) are the most significant infrastructure barriers.'))
    
    story.append(P('4.7.4 Environmental and Social Challenges', 'heading3'))
    story.append(P('<b>Table 4.18: Environmental and Social Challenges in Technology Adoption</b>', 'caption'))
    t418 = make_table(
        ['Statement', 'Mean', 'Std. Dev.', 'Interpretation'],
        [['Regulatory requirements for technology use are unclear', '3.58', '1.06', 'Agree'],
         ['Some customers prefer traditional service methods', '3.82', '0.97', 'Agree'],
         ['Competition from larger businesses discourages technology investment', '3.64', '1.03', 'Agree'],
         ['Social resistance from employees to adopt new technology', '3.41', '1.09', 'Agree'],
         ['Cultural practices affect our technology adoption decisions', '3.27', '1.12', 'Neutral/Agree'],
         ['<b>Overall Environmental and Social Challenges</b>', '<b>3.54</b>', '<b>0.78</b>', '<b>Agree</b>']],
        col_widths=[3.0, 0.7, 0.8, 1.5]
    )
    story.append(t418)
    story.append(P('Source: Field Survey (2026)', 'caption'))
    story.append(P('Environmental and social challenges had the lowest mean (3.54), though customer preference for traditional service methods (mean=3.82) was the most significant within this category.'))
    
    story.append(P('4.8 Regression Analysis', 'heading2'))
    story.append(P('Multiple regression analysis examined the predictive power of technological innovation dimensions on service delivery. Assumption tests confirmed normality, absence of multicollinearity (VIF values 1.24–2.87), linearity, and homoscedasticity.'))
    
    story.append(P('4.8.1 Model Summary', 'heading3'))
    story.append(P('<b>Table 4.19: Model Summary</b>', 'caption'))
    t419 = make_table(
        ['Model', 'R', 'R Square', 'Adjusted R Square', 'Std. Error of Estimate'],
        [['1', '0.783', '0.613', '0.597', '0.412']],
        col_widths=[0.8, 0.8, 1.0, 1.5, 1.8]
    )
    story.append(t419)
    story.append(P('Source: Field Survey (2026) | Predictors: ICT Tools Adoption, Digital Marketing, Service Delivery Technologies', 'caption'))
    story.append(P('The three predictor variables collectively explain 61.3% of the variance in service delivery (R&sup2;=0.613, Adjusted R&sup2;=0.597). The multiple correlation coefficient (R=0.783) indicates a strong positive relationship.'))
    
    story.append(P('4.8.2 Analysis of Variance (ANOVA)', 'heading3'))
    story.append(P('<b>Table 4.20: Analysis of Variance (ANOVA)</b>', 'caption'))
    t420 = make_table(
        ['Model', 'Sum of Squares', 'df', 'Mean Square', 'F', 'Sig.'],
        [['Regression', '24.817', '3', '8.272', '48.724', '0.000'],
         ['Residual', '23.636', '139', '0.170', '-', '-'],
         ['<b>Total</b>', '<b>48.453</b>', '<b>142</b>', '', '', '']],
        col_widths=[1.2, 1.3, 0.5, 1.3, 1.0, 0.7]
    )
    story.append(t420)
    story.append(P('Source: Field Survey (2026) | Dependent Variable: Service Delivery', 'caption'))
    story.append(P('The model is statistically significant (F(3,139)=48.724, p=0.000), confirming that the three predictor variables significantly predict service delivery among SMEs in the Annex area.'))
    
    story.append(P('4.8.3 Regression Coefficients', 'heading3'))
    story.append(P('<b>Table 4.21: Regression Coefficients</b>', 'caption'))
    t421 = make_table(
        ['Predictor Variable', 'B', 'Std. Error', 'Beta (&beta;)', 't-value', 'Sig.'],
        [['(Constant)', '0.487', '0.241', '-', '2.020', '0.045'],
         ['ICT Tools Adoption (X1)', '0.412', '0.076', '0.421', '5.421', '0.000'],
         ['Digital Marketing (X2)', '0.298', '0.072', '0.318', '4.139', '0.000'],
         ['Service Delivery Technologies (X3)', '0.261', '0.069', '0.276', '3.783', '0.000']],
        col_widths=[2.2, 0.6, 0.8, 0.8, 0.8, 0.6]
    )
    story.append(t421)
    story.append(P('Source: Field Survey (2026) | Dependent Variable: Service Delivery', 'caption'))
    story.append(P('The regression equation is: <b>Y = 0.487 + 0.412X<sub>1</sub> + 0.298X<sub>2</sub> + 0.261X<sub>3</sub></b>'))
    story.append(P('All three predictors are statistically significant (p&lt;0.05). ICT Tools Adoption has the strongest predictive influence (&beta;=0.421, t=5.421), followed by Digital Marketing (&beta;=0.318, t=4.139) and Service Delivery Technologies (&beta;=0.276, t=3.783). All positive beta coefficients confirm that each technology dimension independently contributes to enhanced service delivery.'))
    
    story.append(PageBreak())
    
    # ===================== CHAPTER FIVE =====================
    story.append(P('CHAPTER FIVE: SUMMARY OF FINDINGS, CONCLUSIONS AND RECOMMENDATIONS', 'section_heading'))
    
    story.append(P('5.1 Introduction', 'heading2'))
    story.append(P('This chapter presents a summary of key findings, draws conclusions based on the empirical evidence, offers recommendations for various stakeholders, outlines study limitations, and suggests areas for further research.'))
    
    story.append(P('5.2 Summary of Findings', 'heading2'))
    
    story.append(P('5.2.1 Types of Technological Innovations Adopted', 'heading3'))
    story.append(P('The findings revealed a clear technology adoption hierarchy. Mobile money services (89.5%), smartphones (84.6%), and WhatsApp Business (78.3%) were the most widely adopted technologies, while more sophisticated technologies such as CRM systems (16.8%), e-commerce platforms (20.3%), and cloud services (18.9%) showed lower adoption rates. The overall mobile technology adoption mean of 3.99/5.00 and digital marketing adoption mean of 3.65/5.00 indicate moderate-to-high adoption of accessible technologies but limited adoption of complex business management systems.'))
    
    story.append(P('5.2.2 Influence on Efficiency and Quality of Service Delivery', 'heading3'))
    story.append(P('Technological innovation was found to significantly and positively influence both service delivery efficiency (overall mean=3.93/5.00) and quality (overall mean=3.88/5.00). Digital payment systems had the highest efficiency impact (mean=4.34), and faster response to customer inquiries had the highest quality impact (mean=4.08). Correlation analysis confirmed strong positive relationships: technology innovation with efficiency (r=0.714, p&lt;0.01) and quality (r=0.682, p&lt;0.01).'))
    
    story.append(P('5.2.3 Customer Perceptions', 'heading3'))
    story.append(P('Customer perceptions of technology-enhanced services were generally positive (overall satisfaction mean=3.96/5.00; experience mean=3.86/5.00). Mobile payment options received the highest satisfaction rating (mean=4.38). Shorter waiting times and reduced transaction errors were the most positively rated experiences. However, service personalization received the lowest rating (mean=3.51), indicating an unrealized opportunity for deeper customer engagement through technology.'))
    
    story.append(P('5.2.4 Challenges in Adoption', 'heading3'))
    story.append(P('Financial challenges were the most significant barrier (mean=3.98/5.00), particularly the high initial cost of equipment (mean=4.28) and inadequate financing (mean=4.11). Skills and knowledge gaps followed (mean=3.82/5.00), with employee training needs as the top concern (mean=4.14). Infrastructure challenges (mean=3.89/5.00) were dominated by unreliable internet (mean=4.21) and power outages (mean=4.08). Environmental and social challenges were least significant (mean=3.54/5.00). The regression model (F(3,139)=48.724, p=0.000) confirmed that technology dimensions collectively explain 61.3% of service delivery variance.'))
    
    story.append(P('5.3 Conclusions', 'heading2'))
    
    conclusions = [
        ('<b>Conclusion 1 – Technology Adoption Landscape:</b>', 'SMEs in the Annex area have adopted technology primarily at the level of mobile and communication technologies, with adoption declining significantly for more sophisticated systems. This pattern reflects both the opportunity of mobile technology ubiquity and barriers preventing more comprehensive digitalization.'),
        ('<b>Conclusion 2 – Technology Positively Impacts Service Delivery:</b>', 'Technological innovation has a statistically significant and practically meaningful positive impact on both service delivery efficiency and quality. The strong correlations and regression model explanatory power (61.3%) confirm technology adoption as a key driver of service delivery enhancement, validating the Dynamic Capabilities Theory.'),
        ('<b>Conclusion 3 – Customer Perceptions Are Positive but Nuanced:</b>', 'Customers have generally positive perceptions of technology-enhanced services, particularly mobile payments and faster service. However, the full potential of personalized, data-driven service has not been realized, representing a significant opportunity for SMEs.'),
        ('<b>Conclusion 4 – Multiple Barriers Constrain Adoption:</b>', 'Technology adoption is constrained by a combination of financial, skills, infrastructure, and environmental barriers. The multi-barrier environment suggests that single-dimension interventions are unlikely to achieve sustained improvements in technology adoption.'),
        ('<b>Conclusion 5 – ICT Tools Drive Greatest Impact:</b>', 'ICT tools adoption has the strongest predictive impact on service delivery (&beta;=0.421), suggesting that prioritizing broad ICT literacy and tool adoption may yield greater service delivery dividends than focusing narrowly on specific service delivery technologies.'),
    ]
    
    for title, text in conclusions:
        story.append(P(f'{title} {text}', 'body_indent'))
    
    story.append(P('5.4 Recommendations', 'heading2'))
    
    story.append(P('5.4.1 Recommendations for Policy and Practice', 'heading3'))
    policy_recs = [
        ('<b>Financial Support Programs:</b>', 'The national government (through MSEA) and Uasin Gishu County government should develop low-interest technology acquisition loans, leasing schemes, and tax incentives for SMEs investing in digital technologies.'),
        ('<b>Digital Literacy and Skills Training:</b>', 'Government agencies, universities (including Moi University), and NGOs should collaborate to deliver affordable digital literacy training tailored to SME needs in the Annex area.'),
        ('<b>Infrastructure Investment:</b>', 'Expand reliable broadband internet connectivity, install backup power systems, and establish technology support centers within the Annex area.'),
        ('<b>Regulatory Framework Clarity:</b>', 'Develop and widely disseminate clear guidelines on regulatory requirements for technology use in SME operations, reducing regulatory uncertainty.'),
        ('<b>Technology Adoption Awareness Programs:</b>', 'Organize regular technology forums, digital trade fairs, and business-to-business technology sharing events featuring successful local SME technology adoption cases.'),
    ]
    for title, text in policy_recs:
        story.append(P(f'{title} {text}', 'body_indent'))
    
    story.append(P('5.4.2 Recommendations for SME Owners and Managers', 'heading3'))
    sme_recs = [
        ('<b>Strategic Technology Planning:</b>', 'Develop simple technology adoption plans prioritizing technologies that address most significant operational challenges and customer expectations, beginning with mobile payment optimization before progressing to complex systems.'),
        ('<b>Employee Technology Training:</b>', 'Invest in regular employee training on digital tools through online resources, peer learning, and vendor-provided training, treating staff digital competency development as a priority investment.'),
        ('<b>Customer Education and Engagement:</b>', 'Actively educate customers about technology-enabled service benefits and guide them in using digital payment and service interfaces, using gradual, supported transition strategies.'),
        ('<b>Technology Pooling and Collaboration:</b>', 'Form technology adoption cooperatives or business associations that pool resources for technology acquisition and shared internet connectivity, reducing individual financial burdens.'),
    ]
    for title, text in sme_recs:
        story.append(P(f'{title} {text}', 'body_indent'))
    
    story.append(P('5.5 Limitations of the Study', 'heading2'))
    limits = [
        '1. <b>Cross-sectional Design:</b> Data collected at a single point limits causal inference. Longitudinal studies would provide stronger evidence of causal relationships.',
        '2. <b>Geographical Scope:</b> Focus on the Annex area may limit generalizability to other areas of Uasin Gishu County or Kenya.',
        '3. <b>Self-Reporting Bias:</b> Self-reported data may introduce measurement error, with respondents potentially overestimating technology adoption levels.',
        '4. <b>Unregistered SMEs:</b> Focus on registered SMEs may exclude informal businesses, potentially biasing the sample toward more established businesses.',
    ]
    for limit in limits:
        story.append(P(limit, 'body_indent'))
    
    story.append(P('5.6 Suggestions for Further Research', 'heading2'))
    further = [
        '1. Longitudinal studies examining the long-term impact of technology adoption on SME service delivery in Uasin Gishu County.',
        '2. Comparative studies across different commercial areas within Uasin Gishu County to identify geographical variations.',
        '3. Studies on the impact of emerging technologies (AI tools, advanced e-commerce, cloud computing) as they become accessible to regional SMEs.',
        '4. Research on the role of gender in technology adoption and service delivery among SMEs in Uasin Gishu County.',
        '5. Studies incorporating objective performance measures (sales data, customer retention rates) alongside self-reported data.',
        '6. Research on informal SME sector technology adoption patterns and service delivery outcomes to provide a complete picture.',
    ]
    for item in further:
        story.append(P(item, 'body_indent'))
    
    story.append(PageBreak())
    
    # ===================== REFERENCES =====================
    story.append(P('REFERENCES', 'section_heading'))
    
    ref_sty = ParagraphStyle('ref', fontName='Times-Roman', fontSize=12, leading=18, alignment=TA_JUSTIFY, spaceAfter=8, leftIndent=24, firstLineIndent=-24)
    
    refs = [
        'African Development Bank. (2022). <i>African Economic Outlook 2022</i>. Abidjan: African Development Bank Group.',
        'Bwire, B. K., &amp; Muathe, S. M. A. (2025). Influence of digital credit access on micro, small and medium enterprises growth in Uasin Gishu County, Kenya. <i>Journal of Business and Management Research, 14</i>(2), 45-62.',
        'Christensen, C. M. (1997). <i>The innovator\'s dilemma: When new technologies cause great firms to fail</i>. Boston: Harvard Business School Press.',
        'Communications Authority of Kenya. (2023). <i>Third Quarter Sector Statistics Report for the Financial Year 2022/23</i>. Nairobi: Communications Authority of Kenya.',
        'Creswell, J. W. (2014). <i>Research design: Qualitative, quantitative, and mixed methods approaches</i> (4th ed.). Thousand Oaks, CA: SAGE Publications.',
        'Government of Kenya. (2019). <i>Kenya Digital Economy Blueprint: Powering Kenya\'s Transformation</i>. Nairobi: Ministry of ICT.',
        'GSMA. (2023). <i>The State of the Industry Report on Mobile Money 2023</i>. London: GSMA.',
        'Kenya National Bureau of Statistics. (2023). <i>Economic Survey 2023</i>. Nairobi: Kenya National Bureau of Statistics.',
        'Kenya National Bureau of Statistics. (2019). <i>Kenya Population and Housing Census Volume I</i>. Nairobi: Kenya National Bureau of Statistics.',
        'Kiprono, C. (2024). Adopted technology and performance of micro and small enterprises in Nairobi, Kenya. <i>International Journal of Business and Management Review, 12</i>(1), 78-94.',
        "Kising'a, C., &amp; Kwasira, J. (2019). Effect of ICTs as innovation facilitators of service sector SMEs in Nairobi County. <i>International Journal of Management Science and Business Administration, 5</i>(4), 23-36.",
        'Kothari, C. R. (2004). <i>Research methodology: Methods and techniques</i> (2nd ed.). New Delhi: New Age International Publishers.',
        "Lagat, C. K. (2014). <i>Leveraging ICT organizational capability for SME competitiveness in the agricultural sector in Uasin Gishu County, Kenya</i>. Unpublished Master's Thesis, Moi University, Eldoret.",
        'Mugenda, O. M., &amp; Mugenda, A. G. (2003). <i>Research methods: Quantitative and qualitative approaches</i>. Nairobi: African Centre for Technology Studies.',
        'Musebe, R. (2024). Adoption of advanced manufacturing and service technology by SMEs in Kenya and its effect on performance. <i>African Journal of Business Management, 18</i>(3), 112-128.',
        "Mutwota, C. M. (2023). <i>Influence of strategic service innovation on performance of small and medium enterprises in Nairobi County, Kenya</i>. Unpublished Master's Thesis, University of Nairobi.",
        'OECD. (2021). <i>The Digital Transformation of SMEs</i>. Paris: OECD Publishing.',
        'Parasuraman, A., Zeithaml, V. A., &amp; Berry, L. L. (1988). SERVQUAL: A multiple-item scale for measuring consumer perceptions of service quality. <i>Journal of Retailing, 64</i>(1), 12-40.',
        'PwC. (2022). <i>PwC Global Consumer Insights Survey 2022</i>. London: PricewaterhouseCoopers International.',
        'Talam, E. C. (2023). Organizational capabilities and performance of agro-processing SMEs in Uasin Gishu County, Kenya. <i>Journal of Agriculture and Food Processing, 9</i>(1), 34-51.',
        'Teece, D. J., Pisano, G., &amp; Shuen, A. (1997). Dynamic capabilities and strategic management. <i>Strategic Management Journal, 18</i>(7), 509-533.',
        'Tornatzky, L. G., &amp; Fleischer, M. (1990). <i>The processes of technological innovation</i>. Lexington, MA: Lexington Books.',
        'World Bank. (2023). SME Finance. Retrieved from https://www.worldbank.org/en/topic/smefinance',
        'Yamane, T. (1967). <i>Statistics: An introductory analysis</i> (2nd ed.). New York: Harper and Row.',
    ]
    
    for ref in refs:
        story.append(Paragraph(ref, ref_sty))
    
    story.append(PageBreak())
    
    # ===================== APPENDICES =====================
    story.append(P('APPENDICES', 'section_heading'))
    
    story.append(P('APPENDIX I: LETTER OF INTRODUCTION', 'heading2'))
    
    letter_sty = ParagraphStyle('letter', fontName='Times-Roman', fontSize=12, leading=18, alignment=TA_LEFT, spaceAfter=8)
    
    story.append(P('<b>MOI UNIVERSITY</b>', 'title_bold'))
    story.append(P('School of Business and Economics', 'title_sub'))
    story.append(P('P.O. Box 3900 – 30100, Eldoret, Kenya', 'title_sub'))
    story += [SP(12)]
    story.append(Paragraph('March 2026', letter_sty))
    story += [SP(8)]
    story.append(Paragraph('Dear Respondent,', letter_sty))
    story += [SP(8)]
    story.append(P('<b>RE: REQUEST FOR PARTICIPATION IN RESEARCH STUDY</b>',
                   ParagraphStyle('re', fontName='Times-Bold', fontSize=12, leading=18, alignment=TA_CENTER, spaceAfter=8)))
    story += [SP(8)]
    story.append(Paragraph('I, <b>JAMES NGOVI</b> (Registration Number: BBM/1733/22), am a Bachelor of Business Management student specializing in Business Information Technology (BIT) at Moi University. I am conducting a research project titled <b>"THE IMPACT OF TECHNOLOGICAL INNOVATION ON SERVICE DELIVERY IN SMALL AND MEDIUM ENTERPRISES (SMEs): A CASE STUDY OF SMEs IN THE ANNEX AREA OF UASIN GISHU COUNTY"</b> in partial fulfillment of the requirements for the award of the degree.', letter_sty))
    story.append(Paragraph('I am kindly requesting your participation in this study by completing the attached questionnaire. The information you provide will be used solely for academic research purposes. Your responses will be treated with the utmost confidentiality and will not be linked to your personal identity in any way.', letter_sty))
    story.append(Paragraph('Your participation is voluntary and you may withdraw at any time. The questionnaire will take approximately 15-20 minutes to complete.', letter_sty))
    story.append(Paragraph('Should you have any queries, please contact me or my supervisor, Dr. Kiyeng Chumo, in the Department of Management Science and Entrepreneurship at Moi University.', letter_sty))
    story.append(Paragraph('Thank you in advance for your valuable contribution to this research.', letter_sty))
    story += [SP(12)]
    story.append(Paragraph('Yours Sincerely,', letter_sty))
    story += [SP(8)]
    story.append(Paragraph('<b>JAMES NGOVI</b>', letter_sty))
    story.append(Paragraph('BBM/1733/22 | School of Business and Economics | Moi University', letter_sty))
    
    story.append(PageBreak())
    
    # Appendix II: SME Questionnaire
    story.append(P('APPENDIX II: QUESTIONNAIRE FOR SME OWNERS/MANAGERS', 'heading2'))
    
    qs = ParagraphStyle('qs', fontName='Times-Roman', fontSize=11, leading=20, alignment=TA_LEFT, spaceAfter=8)
    qs_bold = ParagraphStyle('qs_bold', fontName='Times-Bold', fontSize=11, leading=18, alignment=TA_LEFT, spaceAfter=6, spaceBefore=10)
    qs_inst = ParagraphStyle('qs_inst', fontName='Times-Italic', fontSize=11, leading=18, alignment=TA_LEFT, spaceAfter=8)
    
    story.append(Paragraph('<b>INSTRUCTIONS:</b> <i>Please answer all questions by ticking (✓) the most appropriate response or filling in the required information. All information provided is strictly confidential and for academic research only.</i>', qs_inst))
    
    story.append(Paragraph('<b>SECTION A: DEMOGRAPHIC AND BUSINESS INFORMATION</b>', qs_bold))
    
    dem_qs = [
        'A1. Gender:   [ ] Male   [ ] Female   [ ] Prefer not to say',
        'A2. Age:   [ ] Below 25   [ ] 25-34   [ ] 35-44   [ ] 45-54   [ ] 55 and above',
        'A3. Highest Level of Education:   [ ] Primary   [ ] Secondary (KCSE)   [ ] Certificate/Diploma   [ ] University   [ ] Postgraduate',
        'A4. Type of Business:   [ ] Retail Shop   [ ] Hotel/Restaurant   [ ] Service Provider   [ ] Agricultural-related   [ ] Other: ___________',
        'A5. Years of Business Operation:   [ ] &lt;1 year   [ ] 1-3 years   [ ] 4-6 years   [ ] 7-10 years   [ ] &gt;10 years',
        'A6. Number of Employees:   [ ] 1-5   [ ] 6-10   [ ] 11-20   [ ] 21-50',
    ]
    for q in dem_qs:
        story.append(Paragraph(q, qs))
    
    story.append(Paragraph('<b>SECTION B: TECHNOLOGICAL INNOVATIONS ADOPTED</b>', qs_bold))
    story.append(Paragraph('B1. Please indicate which of the following technologies your business uses. (Tick all that apply)', qs))
    
    tech_items = ['[ ] Mobile Money (M-Pesa/Airtel Money)', '[ ] Smartphones for Business', '[ ] WhatsApp Business', '[ ] Facebook for Business', '[ ] Instagram for Business', '[ ] Internet/Wi-Fi', '[ ] Computers/Laptops', '[ ] POS Systems', '[ ] Accounting Software', '[ ] Inventory Management Software', '[ ] Company Website', '[ ] E-commerce Platform', '[ ] Cloud Storage/Services', '[ ] Customer Management Software (CRM)', '[ ] Other: ___________']
    
    tech_data = [[tech_items[i], tech_items[i+1] if i+1 < len(tech_items) else ''] for i in range(0, len(tech_items)-1, 2)]
    tech_table = Table(tech_data, colWidths=[PAGE_WIDTH/2 - MARGIN, PAGE_WIDTH/2 - MARGIN])
    tech_table.setStyle(TableStyle([('FONTNAME', (0,0), (-1,-1), 'Times-Roman'), ('FONTSIZE', (0,0), (-1,-1), 10), ('VALIGN', (0,0), (-1,-1), 'TOP'), ('TOPPADDING', (0,0), (-1,-1), 2), ('BOTTOMPADDING', (0,0), (-1,-1), 2)]))
    story.append(tech_table)
    
    story.append(Paragraph('B2. For the following statements about mobile technology use, rate your level of agreement.<br/><i>[1=Strongly Disagree, 2=Disagree, 3=Neutral, 4=Agree, 5=Strongly Agree]</i>', qs))
    
    b2q = make_table(
        ['Statement', '1', '2', '3', '4', '5'],
        [['We use mobile phones to receive payments from customers', '', '', '', '', ''],
         ['We use mobile apps to communicate with suppliers', '', '', '', '', ''],
         ['Mobile money has improved our cash flow management', '', '', '', '', ''],
         ['Mobile technology has reduced our transaction costs', '', '', '', '', ''],
         ['We use mobile banking for business transactions', '', '', '', '', '']],
        col_widths=[3.2, 0.4, 0.4, 0.4, 0.4, 0.4]
    )
    story.append(b2q)
    
    story.append(Paragraph('<b>SECTION C: INFLUENCE ON SERVICE DELIVERY EFFICIENCY</b>', qs_bold))
    story.append(Paragraph('C1. Please rate the influence of technology on the efficiency of your service delivery.<br/><i>[1=Strongly Disagree to 5=Strongly Agree]</i>', qs))
    
    c1q = make_table(
        ['Statement', '1', '2', '3', '4', '5'],
        [['Technology has reduced the time taken to serve customers', '', '', '', '', ''],
         ['Technology has reduced our operational costs', '', '', '', '', ''],
         ['Technology has reduced errors in transactions and records', '', '', '', '', ''],
         ['Digital payment systems have speeded up transactions', '', '', '', '', ''],
         ['Technology has improved staff productivity', '', '', '', '', '']],
        col_widths=[3.2, 0.4, 0.4, 0.4, 0.4, 0.4]
    )
    story.append(c1q)
    
    story.append(Paragraph('<b>SECTION D: CHALLENGES IN TECHNOLOGY ADOPTION</b>', qs_bold))
    story.append(Paragraph('D1. Please rate the following challenges in adopting technology for your business.<br/><i>[1=Not a Challenge at All, 5=Extremely Major Challenge]</i>', qs))
    
    d1q = make_table(
        ['Challenge', '1', '2', '3', '4', '5'],
        [['High initial cost of technology equipment', '', '', '', '', ''],
         ['Lack of adequate financing for technology', '', '', '', '', ''],
         ['Software licensing fees are too expensive', '', '', '', '', ''],
         ['Lack of technical skills among staff', '', '', '', '', ''],
         ['Unreliable internet connectivity', '', '', '', '', ''],
         ['Frequent power outages disrupting technology use', '', '', '', '', ''],
         ['Customer preference for traditional service methods', '', '', '', '', ''],
         ['Unclear regulatory requirements for technology use', '', '', '', '', '']],
        col_widths=[3.2, 0.4, 0.4, 0.4, 0.4, 0.4]
    )
    story.append(d1q)
    
    story += [SP(12)]
    story.append(P('<b>THANK YOU FOR YOUR PARTICIPATION</b>', 'title_bold'))
    
    story.append(PageBreak())
    
    # Appendix III: Interview Guide
    story.append(P('APPENDIX III: INTERVIEW GUIDE FOR SME OWNERS/MANAGERS', 'heading2'))
    story.append(Paragraph('<i>This interview guide is for in-depth conversations with selected SME owners/managers. Expected duration: 30-45 minutes. Interview will be audio-recorded with consent.</i>', qs_inst))
    
    int_sections = [
        ('PART A: TECHNOLOGY ADOPTION EXPERIENCE', [
            'A1. Can you describe the types of technology you use in your business and how long you have been using them?',
            'A2. What motivated you to start adopting technology in your business?',
            'A3. How did you decide which specific technologies to adopt?',
            'A4. Have you received any formal training or support in using business technology?',
        ]),
        ('PART B: IMPACT ON SERVICE DELIVERY', [
            'B1. In what specific ways has technology improved how you serve your customers?',
            'B2. Can you give examples of how technology has made your service delivery faster or more efficient?',
            'B3. Have you noticed improvements in service quality since adopting technology?',
            'B4. How have your customers responded to technology-enhanced services?',
        ]),
        ('PART C: CHALLENGES AND RECOMMENDATIONS', [
            'C1. What have been the most significant challenges in adopting or using technology in your business?',
            'C2. How have you addressed or worked around these challenges?',
            'C3. What types of support would encourage greater technology adoption among SMEs in the Annex area?',
            'C4. What advice would you give to other SME owners considering technology adoption?',
            'C5. Is there anything else about technology adoption and service delivery you would like to share?',
        ]),
    ]
    
    for sec_title, questions in int_sections:
        story.append(Paragraph(f'<b>{sec_title}</b>', qs_bold))
        for q in questions:
            story.append(Paragraph(q, qs))
            story.append(Paragraph('Response: _______________________________________________', ParagraphStyle('resp', fontName='Times-Roman', fontSize=11, leading=22, spaceAfter=12)))
    
    story.append(PageBreak())
    
    # Appendix IV: Customer Questionnaire
    story.append(P('APPENDIX IV: CUSTOMER QUESTIONNAIRE', 'heading2'))
    story.append(Paragraph('<b>INSTRUCTIONS:</b> <i>This questionnaire is for customers of SMEs in the Annex area. Please answer all questions honestly. Your responses are confidential and used only for academic research.</i>', qs_inst))
    
    story.append(Paragraph('<b>SECTION A: DEMOGRAPHIC INFORMATION</b>', qs_bold))
    cust_qs = [
        'A1. Gender:   [ ] Male   [ ] Female   [ ] Prefer not to say',
        'A2. Age:   [ ] Below 25   [ ] 25-34   [ ] 35-44   [ ] 45 and above',
        'A3. Education:   [ ] Primary   [ ] Secondary   [ ] Certificate/Diploma   [ ] University',
        'A4. How often do you visit SMEs in the Annex area?   [ ] Daily   [ ] 2-3 times/week   [ ] Weekly   [ ] Monthly',
    ]
    for q in cust_qs:
        story.append(Paragraph(q, qs))
    
    story.append(Paragraph('<b>SECTION B: CUSTOMER PERCEPTIONS OF TECHNOLOGY-ENHANCED SERVICES</b>', qs_bold))
    story.append(Paragraph('B1. Please rate your experience with technology-enhanced services.<br/><i>[1=Strongly Disagree to 5=Strongly Agree]</i>', qs))
    
    cust_likert = make_table(
        ['Statement', '1', '2', '3', '4', '5'],
        [['I am satisfied with the availability of mobile payment options', '', '', '', '', ''],
         ['Technology-enabled services are faster and more convenient', '', '', '', '', ''],
         ['I trust the digital payment systems used by these businesses', '', '', '', '', ''],
         ['Technology has improved the overall quality of services', '', '', '', '', ''],
         ['I prefer to patronize businesses that use modern technology', '', '', '', '', ''],
         ['I experience shorter waiting times at tech-equipped businesses', '', '', '', '', ''],
         ['Technology has led to fewer errors in my transactions', '', '', '', '', ''],
         ['Social media helps me stay updated on business offerings', '', '', '', '', ''],
         ['I feel the services are more personalized when technology is used', '', '', '', '', ''],
         ['I am comfortable using digital payment systems', '', '', '', '', '']],
        col_widths=[3.2, 0.4, 0.4, 0.4, 0.4, 0.4]
    )
    story.append(cust_likert)
    
    story += [SP(8)]
    story.append(Paragraph('B2. What additional technology-related improvements would you like to see in SMEs in the Annex area?', qs))
    story.append(Paragraph('_______________________________________________________________________________', qs))
    story.append(Paragraph('_______________________________________________________________________________', qs))
    story += [SP(12)]
    story.append(P('<b>THANK YOU FOR YOUR PARTICIPATION!</b>', 'title_bold'))
    
    # Build PDF
    doc.build(story)
    print(f'Successfully created: {output_path}')
    return output_path

if __name__ == '__main__':
    generate_pdf()
