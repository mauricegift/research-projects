#!/usr/bin/env python3
"""
Generate formatted PDF for Mourice Onyango BBM 453 CAT
Distributed Systems - Critical Analysis
"""

import os as _os, sys as _sys
_sys.path.insert(0, _os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))
_os.chdir(_os.path.dirname(_os.path.dirname(_os.path.abspath(__file__))))

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import Image as RLImage
import os

FONT      = 'Times-Roman'
FONT_BOLD = 'Times-Bold'
FONT_BI   = 'Times-BoldItalic'
FONT_IT   = 'Times-Italic'
SZ        = 12
LD        = SZ * 1.5


def sty(name, font=FONT, size=SZ, leading=None, align=TA_JUSTIFY,
        before=0, after=6, left=0, first=0):
    return ParagraphStyle(name, fontName=font, fontSize=size,
                          leading=leading or size * 1.5, alignment=align,
                          spaceBefore=before, spaceAfter=after,
                          leftIndent=left, firstLineIndent=first)


S = {
    'cover_uni':  sty('cu', FONT_BOLD, 16, 16*1.2, TA_CENTER, 4, 4),
    'cover_sub':  sty('cs', FONT_BOLD, 13, 13*1.2, TA_CENTER, 4, 4),
    'cover_dept': sty('cd', FONT_BOLD, 12, 12*1.2, TA_CENTER, 4, 4),
    'cover_det':  sty('cdt', FONT_BOLD, 12, 12*1.2, TA_LEFT,  2, 6),
    'heading':    sty('h2', FONT_BOLD, 12, LD,      TA_LEFT,  14, 6),
    'subhead':    sty('sh', FONT_BI,   12, LD,      TA_LEFT,  10, 4),
    'body':       sty('bd', FONT,      12, LD,      TA_JUSTIFY, 0, 6),
    'bullet':     sty('bl', FONT,      12, LD,      TA_JUSTIFY, 0, 4, left=18),
    'ref':        sty('rf', FONT,      12, LD,      TA_JUSTIFY, 0, 6, left=25, first=-25),
}


def P(text, s='body'):   return Paragraph(text, S[s])
def SP(n=6):             return Spacer(1, n)
def HR():
    return HRFlowable(width='100%', thickness=0.5, color=colors.black,
                      spaceAfter=4, spaceBefore=6)


def bullet(label, text):
    return P(f'<b>{label}</b>{text}', 'bullet')


def generate(output='files/Mourice_BBM_453_CAT.pdf'):
    doc = SimpleDocTemplate(output, pagesize=A4,
                            leftMargin=1.25*inch, rightMargin=inch,
                            topMargin=inch,       bottomMargin=inch)
    story = []

    # ─── COVER PAGE ───────────────────────────────────────────────
    logo = 'assets/moi_uni_logo.png'
    if os.path.exists(logo):
        img = RLImage(logo, width=1.4*inch, height=1.4*inch)
        img.hAlign = 'CENTER'
        story += [img, SP(8)]

    story.append(P('MOI UNIVERSITY',                                        'cover_uni'))
    story.append(P('ANNEX CAMPUS',                                          'cover_sub'))
    story.append(P('SCHOOL OF BUSINESS &amp; ECONOMICS',                   'cover_sub'))
    story.append(P('DEPARTMENT OF MANAGEMENT SCIENCE &amp; ENTREPRENEURSHIP',
                   'cover_dept'))
    story.append(SP(20))

    details = [
        ('PROGRAMME',        'BACHELOR OF BUSINESS MANAGEMENT'),
        ('ACADEMIC YEAR',    'YEAR 4'),
        ('COURSE CODE',      'BBM 453'),
        ('COURSE TITLE',     'DISTRIBUTED SYSTEMS'),
        ('SEMESTER',         '2025/26: SEM II'),
        ('ASSIGNMENT',       'RESEARCH (CAT)'),
        ('SUBMISSION DATE',  '10TH APRIL 2026'),
        ('MARKS',            '20 MARKS'),
        ('NAME',             'MOURICE ONYANGO'),
        ('REG NUMBER',       'BBM/1891/22'),
    ]
    for label, value in details:
        story.append(P(f'<b>{label:<18}</b>:  {value}', 'cover_det'))

    story.append(PageBreak())

    # ─── INTRODUCTION ─────────────────────────────────────────────
    story.append(P('1. INTRODUCTION', 'heading'))
    for t in [
        'Distributed systems represent one of the most transformative paradigms in modern '
        'computing. A distributed system is a collection of autonomous computing elements '
        'that appear to users as a single, coherent system (Tanenbaum &amp; Van Steen, 2017). '
        'Unlike centralized systems, distributed systems spread computation, data storage, '
        'and processing across multiple nodes connected via a network, enabling fault '
        'tolerance, scalability, and geographic flexibility.',
        'The current technological landscape is characterised by a convergence of several '
        'distributed computing trends: cloud computing, edge and fog computing, blockchain '
        'technology, microservices architecture, the Internet of Things (IoT), and real-time '
        'data streaming platforms. Together, these technologies are reshaping how institutions '
        'and enterprises deliver services, manage data, and respond to operational demands.',
        'In Kenya, the adoption of distributed systems has accelerated markedly over the past '
        'decade, driven by the growth of mobile internet penetration, government digitalization '
        'initiatives such as the Digital Superhighway program, and the emergence of a vibrant '
        'technology ecosystem centred around Nairobi\'s Silicon Savannah. The COVID-19 '
        'pandemic further accelerated digital transformation across all sectors, making '
        'distributed systems a critical enabler of continuity in healthcare, education, '
        'finance, security, and commerce.',
        'This paper critically analyses the current trends of distributed systems and '
        'evaluates their impact on five key sectors in Kenya: healthcare, finance and banking, '
        'education and academia, national security, and small and medium enterprises (SMEs). '
        'For each sector, a practical Kenyan example is provided to illustrate the tangible '
        'effects of distributed systems on service delivery and performance.',
    ]:
        story += [P(t), SP(4)]

    story.append(PageBreak())

    # ─── SECTION A ────────────────────────────────────────────────
    story.append(P('a) DISTRIBUTED SYSTEMS IN HEALTHCARE', 'heading'))
    story.append(P('Current Trends', 'subhead'))
    for t in [
        'The healthcare sector globally is undergoing a digital revolution anchored on '
        'distributed systems. Key trends include cloud-based Electronic Health Records (EHR) '
        'systems, telemedicine platforms, IoT-connected medical devices, and distributed '
        'data analytics for epidemiological surveillance. Edge computing is increasingly '
        'deployed to process medical sensor data in real time at the point of care, reducing '
        'latency and improving clinical decision-making.',
        'Interoperability between disparate health information systems — achieved through '
        'distributed middleware and Application Programming Interfaces (APIs) — is enabling '
        'the seamless exchange of patient information across hospitals, clinics, laboratories, '
        'and pharmacies. This interoperability is particularly significant in low-resource '
        'settings where fragmented data has historically hampered public health management.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact in Kenya', 'subhead'))
    for t in [
        'Kenya\'s Ministry of Health adopted the District Health Information System 2 (DHIS2), '
        'a distributed, open-source health information platform, as the national health '
        'management information system. DHIS2 aggregates health data from over 10,000 health '
        'facilities across the country, enabling the Ministry to track disease surveillance '
        'indicators, immunization coverage, maternal health outcomes, and resource utilization '
        'in near real time.',
        'Additionally, M-TIBA, a mobile-based healthcare financing platform developed by '
        'CarePay International and Safaricom, leverages distributed cloud architecture to '
        'connect patients, healthcare providers, and insurance funds. The platform enables '
        'Kenyans — including low-income households — to save for healthcare, receive health '
        'funds, and pay for medical services directly from their mobile phones.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Practical Example: DHIS2 and M-TIBA', 'subhead'))
    for t in [
        'During the COVID-19 pandemic, Kenya\'s Ministry of Health utilized DHIS2 as a '
        'real-time distributed data platform for tracking infections, hospitalisations, and '
        'vaccine administration. County health departments uploaded daily case data from '
        'tablets and smartphones across all 47 counties. The distributed architecture '
        'ensured that even in counties with intermittent internet connectivity, data could '
        'be entered offline and synchronized when connectivity was restored — a critical '
        'feature for remote areas.',
        'M-TIBA similarly demonstrated the power of distributed systems during the pandemic '
        'by facilitating cashless payment for COVID-19 testing and treatment services. By '
        'March 2021, M-TIBA had processed over 4 million health fund transactions and '
        'onboarded more than 1,500 healthcare providers across Kenya.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact on Service Delivery and Performance', 'subhead'))
    for label, text in [
        ('Improved Data Quality:  ',
         'Real-time, distributed data collection reduced reporting delays from weeks to hours, '
         'enabling faster policy responses to disease outbreaks.'),
        ('Enhanced Access:  ',
         'Telemedicine platforms powered by distributed cloud infrastructure extended '
         'specialist consultations to rural areas previously underserved by qualified doctors.'),
        ('Cost Reduction:  ',
         'M-TIBA\'s digital payment model reduced administrative costs for healthcare providers '
         'by eliminating paper-based billing and cash handling.'),
        ('Accountability:  ',
         'Distributed audit trails in DHIS2 improved accountability in health commodity supply '
         'chains, reducing stock-outs of essential medicines at facility level.'),
    ]:
        story.append(bullet(label, text))

    story.append(PageBreak())

    # ─── SECTION B ────────────────────────────────────────────────
    story.append(P('b) DISTRIBUTED SYSTEMS IN FINANCE AND BANKING', 'heading'))
    story.append(P('Current Trends', 'subhead'))
    for t in [
        'The financial sector has been among the earliest and most enthusiastic adopters of '
        'distributed systems technologies. Current trends include microservices-based core '
        'banking architectures, real-time payment processing networks, blockchain and '
        'distributed ledger technology (DLT) for transaction transparency, cloud-native '
        'banking platforms, and AI-driven distributed fraud detection systems.',
        'Open Banking — enabled by distributed APIs — is allowing third-party developers to '
        'build financial applications on top of bank infrastructure, democratizing access to '
        'financial services. Central Bank Digital Currencies (CBDCs), being explored by several '
        'African central banks, are also premised on distributed ledger architectures that '
        'ensure transparency and immutability of monetary transactions.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact in Kenya', 'subhead'))
    for t in [
        'Kenya\'s financial sector is globally recognised for its pioneering use of distributed '
        'mobile money systems. M-Pesa, launched by Safaricom in 2007 and built on a distributed '
        'transaction processing architecture, revolutionized financial inclusion in Kenya. The '
        'platform processes millions of transactions daily through a distributed network of '
        'agents, servers, and mobile nodes spread across the country.',
        'Equity Bank\'s Equitel platform and the PesaLink interbank payment system, operated '
        'by the Kenya Bankers Association (KBA), further exemplify the power of distributed '
        'systems in enabling real-time, interoperable financial transactions among competing '
        'financial institutions.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Practical Example: M-Pesa Distributed Architecture', 'subhead'))
    for t in [
        'M-Pesa\'s technical infrastructure is a distributed system comprising Safaricom\'s '
        'core transaction servers, a vast network of distributed agent terminals (over 250,000 '
        'agents nationwide), mobile subscriber endpoints, and integration gateways to banks, '
        'utilities, and government services. The system uses geographically redundant data '
        'centres to ensure 99.99% uptime, with automatic failover mechanisms that switch to '
        'backup nodes in the event of a primary node failure.',
        'The M-Pesa Global platform extended this distributed architecture across borders, '
        'enabling diaspora remittances from 14 countries to reach recipients in Kenya within '
        'seconds. PesaLink enables instant bank-to-bank transfers 24/7 — a capability '
        'unavailable under earlier centralised batch processing systems.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact on Service Delivery and Performance', 'subhead'))
    for label, text in [
        ('Financial Inclusion:  ',
         'M-Pesa has brought over 30 million Kenyans into the formal financial system, '
         'including unbanked populations in rural and peri-urban areas.'),
        ('Transaction Speed:  ',
         'Real-time distributed payment systems reduced settlement time from T+3 business '
         'days under traditional banking to near-instantaneous processing.'),
        ('Resilience:  ',
         'Geographically distributed data centres ensure continuity of financial services '
         'even during localised infrastructure failures or cyber attacks.'),
        ('Fraud Detection:  ',
         'Distributed machine learning models analysing transaction patterns across millions '
         'of nodes in real time have significantly reduced fraudulent transactions in '
         'mobile banking.'),
    ]:
        story.append(bullet(label, text))

    story.append(PageBreak())

    # ─── SECTION C ────────────────────────────────────────────────
    story.append(P('c) DISTRIBUTED SYSTEMS IN EDUCATION AND ACADEMIA', 'heading'))
    story.append(P('Current Trends', 'subhead'))
    for t in [
        'Education is experiencing a profound transformation through distributed learning '
        'management systems (LMS), cloud-hosted academic repositories, virtual classrooms, '
        'distributed video conferencing infrastructure, and peer-to-peer (P2P) collaborative '
        'platforms. Massive Open Online Courses (MOOCs), delivered via globally distributed '
        'content delivery networks (CDNs), have made quality education accessible to learners '
        'in remote and underserved regions.',
        'Edge computing is beginning to be deployed in educational institutions to support '
        'bandwidth-intensive applications such as virtual reality (VR) labs and real-time '
        'collaborative coding environments. Blockchain-based academic credential systems '
        'are emerging as a solution to certificate fraud by enabling verifiable, tamper-proof '
        'digital certificates on distributed ledgers.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact in Kenya', 'subhead'))
    for t in [
        'Kenya\'s transition to a competency-based curriculum and the government\'s Digital '
        'Literacy Programme (DLP) have been underpinned by distributed computing infrastructure. '
        'The Kenya Education Cloud (edCloud), managed by the Kenya Education Network (KENET), '
        'provides a distributed cloud hosting platform for universities and research '
        'institutions, supporting e-learning portals, digital libraries, and research '
        'data repositories.',
        'Moi University\'s online learning portal and the JKUAT virtual campus enabled '
        'continuity of learning during the COVID-19 school closures of 2020-2021, when all '
        'physical campuses were shut down by government directive.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Practical Example: KENET and BBM Annex', 'subhead'))
    for t in [
        'KENET operates a distributed research and education network connecting over 60 '
        'institutions of higher learning across Kenya through a high-speed fibre backbone '
        'and peering arrangements with regional and international networks. This distributed '
        'infrastructure supports video conferencing, remote access to academic journals, and '
        'high-performance computing resources for scientific research.',
        'At Moi University\'s Annex Campus, the student-developed BBM Annex platform '
        '(https://bbm.giftedtech.co.ke) exemplifies a grassroots distributed academic '
        'resource-sharing system. The platform aggregates lecture notes, past papers, and '
        'study guides uploaded by students across different academic years. Research by '
        'Onyango (2026) found that 71.8% of BBM students reported improved examination '
        'preparedness after accessing resources through the platform.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact on Service Delivery and Performance', 'subhead'))
    for label, text in [
        ('Continuity of Learning:  ',
         'Distributed e-learning platforms ensured that over 1 million university students '
         'in Kenya continued studies during COVID-19, preventing academic year loss.'),
        ('Resource Accessibility:  ',
         'KENET\'s distributed network gave students in remote campuses access to the same '
         'academic databases as students in Nairobi, reducing information inequality.'),
        ('Research Collaboration:  ',
         'Distributed cloud repositories enabled Kenyan researchers to collaborate with '
         'international counterparts, increasing research output and co-publications.'),
        ('Reduced Costs:  ',
         'Cloud-hosted LMS platforms eliminated expensive on-premise server infrastructure '
         'in individual institutions, lowering the cost of e-learning deployment.'),
    ]:
        story.append(bullet(label, text))

    story.append(PageBreak())

    # ─── SECTION D ────────────────────────────────────────────────
    story.append(P('d) DISTRIBUTED SYSTEMS IN NATIONAL SECURITY', 'heading'))
    story.append(P('Current Trends', 'subhead'))
    for t in [
        'Modern national security architectures are increasingly premised on distributed '
        'computing paradigms. Key trends include distributed surveillance networks integrating '
        'CCTV cameras, drones, and biometric terminals; distributed intelligence-sharing '
        'platforms connecting multiple security agencies; cloud-based command and control '
        'systems; and distributed cybersecurity infrastructure for real-time threat detection.',
        'Blockchain technology is being explored for securing sensitive government records '
        'and identity documents. The Zero Trust security model — which assumes no inherently '
        'trusted nodes in a distributed network — is gaining traction in government '
        'cybersecurity frameworks, requiring continuous verification of every user and device.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact in Kenya', 'subhead'))
    for t in [
        'The Government of Kenya has invested significantly in distributed security '
        'infrastructure. The National Integrated Identity Management System (NIIMS), known '
        'as Huduma Namba, is a distributed biometric identification system that consolidates '
        'citizen identity data from multiple government registries — including the National '
        'Registration Bureau, Kenya Revenue Authority, and Registrar of Persons — into a '
        'single interoperable platform.',
        'The Nairobi City Surveillance Project deployed over 1,800 networked CCTV cameras '
        'across the city, connected to a central command center via a distributed fibre and '
        'wireless network. This system has been expanded to Mombasa, Kisumu, and Eldoret as '
        'part of Kenya\'s Safe City initiative.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Practical Example: Huduma Namba and the Safe City CCTV Network',
                   'subhead'))
    for t in [
        'The Huduma Namba system exemplifies a large-scale distributed identity management '
        'deployment. Data is collected at distributed registration centers across all 47 '
        'counties using biometric enrollment devices and synchronized with a central '
        'cloud-hosted database managed by the State Department for Immigration. The '
        'distributed architecture allows for real-time identity verification at border '
        'checkpoints, airport immigration counters, and government service kiosks nationwide.',
        'The Nairobi Safe City CCTV network operates as a distributed surveillance system '
        'where video feeds from thousands of cameras are processed at edge nodes for '
        'preliminary analysis (number plate recognition, crowd monitoring) before being '
        'aggregated at the central command center. Edge processing reduces bandwidth '
        'requirements and enables faster incident response.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact on Service Delivery and Performance', 'subhead'))
    for label, text in [
        ('Crime Reduction:  ',
         'The Nairobi Safe City surveillance network contributed to a reported 46% reduction '
         'in crime in covered areas, demonstrating the deterrence effect of distributed '
         'video surveillance.'),
        ('Identity Verification:  ',
         'Huduma Namba has streamlined access to over 15 government services, reducing '
         'duplication of identity documents and enabling cross-agency real-time verification.'),
        ('Inter-Agency Coordination:  ',
         'Distributed intelligence-sharing platforms connecting NIS, Kenya Police Service, '
         'and KDF have improved coordination in counter-terrorism operations.'),
        ('Border Security:  ',
         'Distributed biometric verification at border points has strengthened immigration '
         'control, enabling real-time flagging of wanted persons and stolen documents.'),
    ]:
        story.append(bullet(label, text))

    story.append(PageBreak())

    # ─── SECTION E ────────────────────────────────────────────────
    story.append(P('e) DISTRIBUTED SYSTEMS IN SMALL AND MEDIUM ENTERPRISE (SME) BUSINESS',
                   'heading'))
    story.append(P('Current Trends', 'subhead'))
    for t in [
        'Small and medium enterprises worldwide are leveraging distributed systems to compete '
        'effectively in digital markets previously accessible only to large corporations. The '
        'democratization of cloud computing has been particularly transformative: SMEs can now '
        'access enterprise-grade distributed computing resources — databases, analytics '
        'platforms, AI tools, and global content delivery networks — on a pay-as-you-use basis '
        'with minimal upfront capital expenditure.',
        'Current trends driving SME adoption include cloud-based ERP systems, mobile POS '
        'terminals integrated with cloud inventory management, e-commerce platforms on globally '
        'distributed infrastructure, distributed supply chain management systems, and mobile '
        'payment APIs connecting SME businesses to millions of mobile money users.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact in Kenya', 'subhead'))
    for t in [
        'Kenya\'s SME sector — accounting for approximately 98% of all businesses, 30% of GDP, '
        'and 80% of employment (KNBS, 2021) — has been significantly transformed by distributed '
        'systems. The integration of M-Pesa\'s Lipa Na M-Pesa Till and Paybill APIs into SME '
        'operations has enabled even small roadside kiosks to accept cashless payments and '
        'reconcile sales data through cloud-connected terminals.',
        'Platforms such as Jumia Kenya, Copia Global, and Twiga Foods have deployed distributed '
        'supply chain and e-commerce systems connecting small-scale retailers, farmers, and '
        'manufacturers across Kenya\'s diverse geography, enabling them to access markets, '
        'source inputs, and receive payments through a unified digital infrastructure.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Practical Example: Twiga Foods Distributed Supply Chain Platform',
                   'subhead'))
    for t in [
        'Twiga Foods is a Nairobi-based agri-tech company that operates a distributed supply '
        'chain management platform connecting smallholder farmers upcountry with informal food '
        'vendors (mama mbogas) in urban areas. Vendors place orders via USSD or a smartphone '
        'app; orders are aggregated by a cloud-based platform, matched to the nearest '
        'fulfilment center, and dispatched via a distributed network of contracted delivery '
        'vehicles tracked in real time through GPS-connected tablets.',
        'Copia Global similarly operates a distributed last-mile e-commerce platform targeting '
        'low-income consumers in peri-urban and rural Kenya. The platform uses a network of '
        'distributed agents — small shop owners who act as order collection points — connected '
        'to a central cloud platform, enabling customers without smartphones to order products '
        'digitally through their local agent.',
    ]:
        story += [P(t), SP(4)]

    story.append(P('Impact on Service Delivery and Performance', 'subhead'))
    for label, text in [
        ('Market Reach:  ',
         'Distributed e-commerce platforms have enabled Kenyan SMEs to reach customers beyond '
         'their immediate geographic areas, with some micro-enterprises reporting a doubling '
         'of their customer base within 12 months of joining digital marketplaces.'),
        ('Supply Chain Efficiency:  ',
         'Twiga Foods\' distributed platform reduced post-harvest food losses by up to 30% '
         'by optimising supply-demand matching and eliminating inefficient middlemen.'),
        ('Financial Access:  ',
         'SMEs transacting through distributed mobile payment platforms build a digital '
         'credit history that enables access to micro-loans from M-Shwari, KCB M-Pesa, '
         'and Tala, facilitating business expansion.'),
        ('Operational Efficiency:  ',
         'Cloud-based distributed ERP and POS systems have reduced SME administrative '
         'overhead by automating inventory, sales reconciliation, and tax reporting.'),
    ]:
        story.append(bullet(label, text))

    story.append(PageBreak())

    # ─── CONCLUSION ───────────────────────────────────────────────
    story.append(P('2. CONCLUSION', 'heading'))
    for t in [
        'This paper has critically examined the current trends of distributed systems and their '
        'impact across five key sectors in Kenya. The analysis demonstrates that distributed '
        'computing is not merely a technical advancement but a fundamental enabler of '
        'socio-economic transformation. From DHIS2\'s distributed health data platform '
        'improving pandemic response, to M-Pesa\'s distributed transaction network '
        'revolutionising financial inclusion, to Twiga Foods\' distributed supply chain '
        'reducing food insecurity — distributed systems are at the heart of Kenya\'s digital '
        'development story.',
        'Across all five sectors examined, a consistent pattern emerges: distributed systems '
        'improve service delivery by enhancing scalability, resilience, and real-time '
        'responsiveness; they improve performance by enabling data-driven decision-making, '
        'automating repetitive processes, and connecting previously isolated stakeholders '
        'into collaborative digital ecosystems. The geographic flexibility of distributed '
        'architectures is particularly significant in the Kenyan context, where infrastructure '
        'quality varies enormously between urban centres and rural areas.',
        'However, the benefits of distributed systems are not without challenges. Cybersecurity '
        'risks increase as the attack surface expands across multiple distributed nodes. Data '
        'privacy concerns arise when personal health, financial, and identity data is processed '
        'across geographically dispersed servers. Connectivity inequalities risk creating a '
        'two-tier digital economy where the gains of distributed systems are concentrated in '
        'well-connected urban areas while rural communities remain excluded.',
        'To maximise the transformative potential of distributed systems in Kenya, stakeholders '
        '— government, private sector, academia, and civil society — must collaborate to invest '
        'in digital infrastructure, strengthen data governance frameworks, build local technical '
        'capacity, and design inclusive distributed systems that serve all Kenyans regardless '
        'of location or income level.',
    ]:
        story += [P(t), SP(4)]

    story.append(PageBreak())

    # ─── REFERENCES ───────────────────────────────────────────────
    story.append(P('REFERENCES', 'heading'))
    refs = [
        'Buyya, R., Yeo, C. S., Venugopal, S., Broberg, J., &amp; Brandic, I. (2009). Cloud '
        'computing and emerging IT platforms: Vision, hype, and reality for delivering '
        'computing as the 5th utility. <i>Future Generation Computer Systems, 25</i>(6), '
        '599-616.',
        'Chetty, K., Qigui, L., Gcora, N., Josie, J., Sheng, L., &amp; Fang, C. (2018). '
        'Bridging the digital divide: Measuring digital literacy. <i>Economics, 12</i>(1), '
        '1-20.',
        'Government of Kenya. (2022). <i>Kenya National Digital Master Plan 2022-2032.</i> '
        'Ministry of ICT, Innovation and Youth Affairs. Nairobi: Government Printer.',
        'Hashem, I. A. T., Yaqoob, I., Anuar, N. B., Mokhtar, S., Gani, A., &amp; Khan, S. U. '
        '(2015). The rise of "big data" on cloud computing: Review and open research issues. '
        '<i>Information Systems, 47</i>, 98-115.',
        'Kenya National Bureau of Statistics. (2021). <i>Economic Survey 2021.</i> Nairobi: KNBS.',
        'Lomas, E. (2017). Cyber security: Ensuring confidentiality, integrity and availability '
        'of information. <i>Records Management Journal, 27</i>(3), 264-278.',
        'Maitland, C., &amp; Alamgir, H. (2019). Distributed systems and humanitarian '
        'information management: Implications for design. <i>The Electronic Journal of '
        'Information Systems in Developing Countries, 85</i>(5), e12093.',
        'Onyango, M. (2026). <i>Effectiveness of software development on Moi University '
        'students\' learning behaviour: A case study of BBM Annex.</i> Bachelor of Business '
        'Management Research Project. Moi University.',
        'Safaricom PLC. (2023). <i>Integrated Report and Financial Statements 2023.</i> '
        'Nairobi: Safaricom PLC.',
        'Tanenbaum, A. S., &amp; Van Steen, M. (2017). <i>Distributed systems: Principles '
        'and paradigms</i> (3rd ed.). Prentice Hall.',
        'World Bank. (2022). <i>Kenya Digital Economy Assessment.</i> Washington DC: '
        'World Bank Group.',
        'Zuboff, S. (2019). <i>The age of surveillance capitalism: The fight for a human '
        'future at the new frontier of power.</i> Public Affairs.',
    ]
    for r in refs:
        story.append(P(r, 'ref'))

    doc.build(story)
    print(f'PDF saved: {output}')


if __name__ == '__main__':
    generate('files/Mourice_BBM_453_CAT.pdf')
