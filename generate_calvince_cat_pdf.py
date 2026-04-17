#!/usr/bin/env python3
"""
Generate formatted PDF for Calvince Odhiambo BBM 415 CAT
Moi University - Management of Financial Institutions
Font: Times New Roman 12pt, 1.5 line spacing
"""

from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, HRFlowable
)
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch, cm
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.lib import colors
from reportlab.platypus import Image as RLImage
from reportlab.lib.utils import ImageReader
import os
os.makedirs('files', exist_ok=True)

W, H = A4
FONT       = 'Times-Roman'
FONT_BOLD  = 'Times-Bold'
FONT_BI    = 'Times-BoldItalic'
FONT_IT    = 'Times-Italic'
SIZE       = 12
LEAD       = SIZE * 1.5      # 1.5 line spacing
LEAD_COVER = SIZE * 1.32     # cover page can be tighter


def mk_style(name, font=FONT, size=SIZE, leading=None, align=TA_JUSTIFY,
             space_before=0, space_after=6, left_indent=0, first_indent=0):
    return ParagraphStyle(
        name=name,
        fontName=font,
        fontSize=size,
        leading=leading or size * 1.5,
        alignment=align,
        spaceBefore=space_before,
        spaceAfter=space_after,
        leftIndent=left_indent,
        firstLineIndent=first_indent,
    )


# -------- Styles ---------
S = {
    'cover_uni':   mk_style('cover_uni',   FONT_BOLD, 16, 16*1.2, TA_CENTER, 4, 4),
    'cover_sub':   mk_style('cover_sub',   FONT_BOLD, 13, 13*1.2, TA_CENTER, 4, 4),
    'cover_detail':mk_style('cover_detail',FONT_BOLD, 12, 12*1.2, TA_LEFT,   4, 8),
    'q_head':      mk_style('q_head',      FONT_BOLD, 12, LEAD,   TA_LEFT,   14, 6),
    'q_text':      mk_style('q_text',      FONT_BI,   12, LEAD,   TA_JUSTIFY, 4, 8),
    'sub_head':    mk_style('sub_head',    FONT_BOLD, 12, LEAD,   TA_LEFT,   10, 4),
    'body':        mk_style('body',        FONT,      12, LEAD,   TA_JUSTIFY, 0, 6),
    'body_center': mk_style('body_center', FONT_BOLD, 12, LEAD,   TA_CENTER,  4, 4),
    'bullet':      mk_style('bullet',      FONT,      12, LEAD,   TA_JUSTIFY, 0, 4,
                            left_indent=18),
}


def P(text, style_key='body'):
    return Paragraph(text, S[style_key])


def SP(pts=6):
    return Spacer(1, pts)


def HR():
    return HRFlowable(width='100%', thickness=0.5, color=colors.black,
                      spaceAfter=4, spaceBefore=6)


def bullet(bold_label, text):
    return P(f'<b>{bold_label}</b> {text}', 'bullet')


def generate_cat_pdf(output='files/Calvince_BBM_415_CAT.pdf'):
    doc = SimpleDocTemplate(
        output,
        pagesize=A4,
        leftMargin=1.25 * inch,
        rightMargin=inch,
        topMargin=inch,
        bottomMargin=inch,
    )

    story = []

    # ======================== COVER PAGE ========================
    # Logo
    logo_path = 'attached_assets/moi_logo_1773763714167.png'
    if os.path.exists(logo_path):
        img = RLImage(logo_path, width=1.4*inch, height=1.4*inch)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(SP(8))

    story.append(P('MOI UNIVERSITY', 'cover_uni'))
    story.append(P('ANNEX CAMPUS', 'cover_sub'))
    story.append(P('SCHOOL OF BUSINESS AND ECONOMICS', 'cover_sub'))
    story.append(SP(24))

    details = [
        ('COURSE CODE',  'BBM 415'),
        ('COURSE TITLE', 'MANAGEMENT OF FINANCIAL INSTITUTIONS'),
        ('NAME',         'ODHIAMBO CALVINCE'),
        ('REG NUMBER',   'BBM/1483/23'),
        ('TASK',         'CAT'),
        ('DATE',         '3RD APRIL 2026'),
        ('LECTURER',     'DR. JAPHET KOGEI'),
    ]
    for label, value in details:
        story.append(P(f'<b>{label:<16}</b>:  {value}', 'cover_detail'))

    story.append(PageBreak())

    # ======================== QUESTION ONE ========================
    story.append(P('QUESTION ONE', 'q_head'))
    story.append(P(
        'Financial institutions occupy a unique position in the economy due to their '
        'special characteristics and operational frameworks that distinguish them from '
        'non-financial enterprises.'))

    story.append(P(
        'a) Discuss the nature of financial institutions and explain why they are '
        'considered unique in terms of their operations and risk exposure. (5 Marks)',
        'q_text'))

    story.append(P(
        'Financial institutions are organizations that provide financial services for '
        'their clients or members. They differ significantly from non-financial enterprises '
        'like manufacturing or retail firms because their primary inventory is money and '
        'financial contracts rather than physical goods.'))
    story.append(P(
        'The fundamental nature of a financial institution is to act as a financial '
        'intermediary. They bridge the gap between "surplus units" (Savers/Investors) and '
        '"deficit units" (borrowers), ensuring the efficient allocation of capital within '
        'the economy.'))

    story.append(P('Reasons Why Financial Institutions are Unique', 'sub_head'))
    story.append(bullet(
        'i) Maturity Transformation:',
        'They borrow short term and lend long term. Depositors can withdraw funds on '
        'demand, but loans may be extended for years. This maturity mismatch creates '
        'significant liquidity risk.'))
    story.append(bullet(
        'ii) High Leverage:',
        'Financial institutions operate with high levels of debt relative to equity. '
        'Banks fund a significant portion of their operations using deposits and borrowed '
        'funds, making them more vulnerable to small shocks or adverse economic events.'))
    story.append(bullet(
        'iii) Risk Transformation:',
        'Financial institutions transform risky assets into less risky claims for savers. '
        'A bank may pool many risky individual loans but provide depositors with relatively '
        'safe and liquid claims on those pooled assets.'))

    story.append(P('Unique Risk Exposure', 'sub_head'))
    story.append(P(
        'Because of their specific operations, financial institutions face risks that are '
        'far more volatile than those of non-financial firms:'))
    story.append(bullet(
        'Interest Rate Risk:',
        'Because they deal in long-term assets and short-term liabilities, sudden changes '
        'in market interest rates can drastically impact their profit margins.'))
    story.append(bullet(
        'Credit/Default Risk:',
        'The primary risk is that borrowers will fail to repay their loans, directly '
        'affecting the financial institution\'s solvency and capital base.'))
    story.append(bullet(
        'Liquidity Risk:',
        'A sudden surge in depositor withdrawals can leave a bank unable to meet its '
        'short-term obligations, even if it is technically solvent.'))

    story.append(SP(8))
    story.append(P(
        'b) With reference to at least two different types of depository institutions '
        '(banks, insurance companies, or security firms), explain how their operational '
        'characteristics expose them to different types of risks. (5 Marks)',
        'q_text'))

    story.append(P(
        'The way a financial institution operates — what it takes in as liabilities and '
        'what it invests in as assets — determines the specific risks it faces. Two key '
        'types of financial institutions are examined below.'))

    story.append(P('i. Commercial Banks', 'sub_head'))
    story.append(P(
        'Banks take in deposits (savings and checking accounts) that customers can '
        'withdraw at any time, then use those deposits to issue long-term loans (mortgages '
        'and business loans). This business model exposes them to:'))
    story.append(bullet(
        'Liquidity Risk:',
        'Because liabilities are on demand but assets are locked in for years, a bank '
        'faces risk if too many depositors want their money back simultaneously (a '
        '"bank run").'))
    story.append(bullet(
        'Credit/Default Risk:',
        'The risk that borrowers will not repay their loans, leading to a loss of the '
        'bank\'s principal and interest income.'))
    story.append(bullet(
        'Interest Rate Risk:',
        'If market interest rates rise, the bank must pay more to retain depositors, '
        'but income from older, fixed-rate loans stays the same, squeezing profit margins.'))

    story.append(P('ii. Insurance Companies', 'sub_head'))
    story.append(P(
        'Insurance companies collect premiums in exchange for a promise to pay out if a '
        'specific event occurs (death, accident, fire). They invest these premiums in '
        'long-term, safe securities to ensure funds are available for future claims:'))
    story.append(bullet(
        'Underwriting Risk:',
        'The risk that actual claims paid out are much higher than the premiums collected — '
        'for example, due to a natural disaster or an unexpected spike in mortality rates.'))
    story.append(bullet(
        'Investment Risk:',
        'Since they hold long-duration assets, insurance companies are highly sensitive '
        'to market crashes or inflation that devalues their long-term bond holdings, '
        'reducing their ability to meet future claim obligations.'))

    story.append(PageBreak())

    # ======================== QUESTION TWO ========================
    story.append(P('QUESTION TWO', 'q_head'))
    story.append(P(
        'a) Define interest rate risk and explain the two primary sources of interest rate '
        'risk exposure in a bank\'s balance sheet. (5 Marks)',
        'q_text'))

    story.append(P(
        'Interest rate risk is the potential for a bank\'s financial condition — '
        'specifically its earnings (Net Interest Income) and the economic value of its '
        'equity — to be adversely affected by movements in market interest rates. It is '
        'one of the most significant financial risks facing depository institutions '
        'such as banks.'))

    story.append(P('Two Primary Sources of Interest Rate Risk', 'sub_head'))
    story.append(bullet(
        '1. Repricing Risk (Maturity Mismatch):',
        'This is the most common form of interest rate risk. It arises from timing '
        'differences in the maturity (for fixed-rate instruments) and repricing (for '
        'floating-rate instruments) of bank assets, liabilities, and off-balance sheet '
        'positions. For example, if a bank funds a long-term, fixed-rate mortgage with '
        'short-term certificates of deposit, and interest rates subsequently rise, the '
        'bank must pay more to retain depositors while income from the mortgage remains '
        'fixed, squeezing profit margins.'))
    story.append(bullet(
        '2. Basis Risk:',
        'This occurs when the interest rates on different instruments change by different '
        'amounts or at different times, even if they have similar repricing frequencies. '
        'A bank might have a loan priced on the prime rate but funded by deposits priced '
        'on LIBOR. If LIBOR-based deposit costs rise faster than prime-based loan income, '
        'the bank\'s net interest margin will decline.'))

    story.append(SP(8))
    story.append(P(
        'b) Discuss the concept of duration as a measure of interest rate sensitivity, and '
        'illustrate with a practical example how duration gap analysis helps a bank manage '
        'its interest rate risk exposure. (5 Marks)',
        'q_text'))

    story.append(P(
        'Duration is a comprehensive measure of the timing of the cash flows of a '
        'financial instrument. Unlike simple maturity, it accounts for the size and timing '
        'of all interest and principal payments, providing a more precise measure of '
        'interest rate sensitivity.'))

    story.append(P('Key Properties of Duration', 'sub_head'))
    story.append(bullet(
        'Sensitivity:',
        'Duration measures how much the price (or market value) of a financial asset or '
        'liability changes when interest rates change.'))
    story.append(bullet(
        'The Inverse Relationship:',
        'There is an inverse relationship between interest rates and the value of '
        'fixed-income instruments. If interest rates rise, the market value of the '
        'instrument falls.'))
    story.append(bullet(
        'The Rule of Thumb:',
        'A duration of 5 years implies that for every 1% increase in interest rates, '
        'the value of the instrument will decrease by approximately 5%.'))

    story.append(P('Duration Gap Analysis', 'sub_head'))
    story.append(P(
        'The Duration Gap (DGAP) measures the sensitivity of a bank\'s net worth to '
        'changes in interest rates and is calculated as:'))
    story.append(P('DGAP = D<sub rise="2">A</sub> \u2212 (L/A \u00d7 D<sub rise="2">L</sub>)',
                   'body_center'))
    for line in ['D<sub rise="2">A</sub> = Average duration of assets',
                 'D<sub rise="2">L</sub> = Average duration of liabilities',
                 'L/A = Ratio of total liabilities to total assets']:
        story.append(bullet('', line))

    story.append(P('Practical Example', 'sub_head'))
    story.append(P('Imagine a bank with the following balance sheet:'))
    for line in [
        'Assets (A): Ksh 100 million in long-term loans with a duration (D<sub rise="2">A</sub>) of 6 years.',
        'Liabilities (L): Ksh 90 million in short-term deposits with a duration (D<sub rise="2">L</sub>) of 1 year.',
        'Equity: Ksh 10 million.',
    ]:
        story.append(bullet('\u2022', line))

    story.append(P(
        'DGAP = 6 \u2212 (90/100 \u00d7 1) = 6 \u2212 0.9 = <b>5.1 years</b>',
        'body_center'))

    story.append(P(
        'This large positive DGAP means the bank\'s assets have a much longer duration '
        'than its liabilities. If interest rates rise by 1%:'))
    for line in [
        'The value of the Ksh 100 million assets would drop by roughly 6% (\u2212Ksh 6 million).',
        'The value of the Ksh 90 million liabilities would drop by only 1% (\u2212Ksh 0.9 million).',
        'The bank\'s equity would therefore decline by Ksh 5.1 million, wiping out over half of its capital.',
    ]:
        story.append(bullet('\u2022', line))

    story.append(P(
        'This analysis demonstrates that to manage interest rate risk, the bank should '
        'seek to reduce its DGAP — either by shortening the duration of its assets, '
        'extending the duration of its liabilities, or using interest rate derivatives '
        'such as swaps.'))

    story.append(PageBreak())

    # ======================== QUESTION THREE ========================
    story.append(P('QUESTION THREE', 'q_head'))
    story.append(P(
        'Credit risk remains a fundamental concern for all financial institutions engaged '
        'in lending activities.'))

    story.append(P(
        'a) Explain what credit risk is and discuss the key components that determine a '
        'borrower\'s creditworthiness when financial institutions evaluate loan '
        'applications. (5 Marks)',
        'q_text'))

    story.append(P(
        'Credit risk is the risk that a borrower or counterparty fails to meet contractual '
        'obligations (principal and/or interest), leading to default losses for the lender. '
        'It is the possibility of a loss resulting from a borrower\'s failure to repay a '
        'loan or meet contractual obligations.'))

    story.append(P('Key Components of Creditworthiness: The 5 Cs of Credit', 'sub_head'))
    story.append(P(
        'When financial institutions evaluate loan applications, they typically use the '
        '5 Cs of Credit framework:'))

    for label, text in [
        ('1) Character:', 'The borrower\'s reputation and track record for repaying debts. '
         'Lenders examine credit reports and credit scores to assess the applicant\'s '
         'reliability and honesty in handling past credit obligations.'),
        ('2) Capital:', 'The borrower\'s own investment in the project or overall net worth. '
         'A large down payment or significant savings indicate the borrower has "skin in '
         'the game," reducing the lender\'s risk.'),
        ('3) Collateral:', 'Assets (such as a house, car, or equipment) pledged as security '
         'for the loan. If the borrower defaults, the lender can seize and sell the '
         'collateral to recover losses.'),
        ('4) Capacity:', 'The borrower\'s ability to repay the loan, assessed via the '
         'debt-to-income (DTI) ratio, cash flow analysis, job stability, and other '
         'income sources.'),
        ('5) Conditions:', 'External factors affecting the borrower\'s ability to pay, '
         'including the purpose of the loan, the state of the broader economy, and '
         'prevailing interest rate conditions.'),
    ]:
        story.append(bullet(label, text))

    story.append(SP(8))
    story.append(P(
        'b) Discuss the various methods that financial institutions can employ to manage '
        'and mitigate credit risk exposure in their lending portfolios. Illustrate your '
        'answer with at least two practical examples. (5 Marks)',
        'q_text'))

    story.append(P(
        'To mitigate credit risk, financial institutions employ several strategies:'))

    story.append(bullet(
        'i) Credit Risk Assessment (5 Cs of Credit):',
        'Before lending, institutions evaluate a borrower\'s creditworthiness using the '
        '5 Cs framework — Character, Capacity, Capital, Collateral, and Conditions — '
        'ensuring only creditworthy borrowers receive loans.'))
    story.append(bullet(
        'ii) Portfolio Diversification:',
        'Institutions spread loans across different industries, geographic regions, and '
        'borrower types so that a downturn in one sector does not collapse the entire '
        'lending portfolio.'))
    story.append(bullet(
        'iii) Risk-Based Pricing:',
        'Riskier borrowers are charged higher interest rates. This "risk premium" '
        'compensates the bank for the higher probability of default.'))
    story.append(bullet(
        'iv) Collateralization:',
        'Requiring borrowers to pledge assets as security reduces potential losses in the '
        'event of default.'))

    story.append(P('Practical Examples', 'sub_head'))
    story.append(bullet(
        'Example 1 \u2014 Mortgage Lending (Collateralization):',
        'When a bank issues a home loan (mortgage), the house itself serves as collateral. '
        'If the homeowner stops making payments, the bank has the legal right to foreclose '
        'on the property. By selling the house, the bank recovers the outstanding loan '
        'amount, significantly reducing its credit risk exposure.'))
    story.append(bullet(
        'Example 2 \u2014 Small Business Loans (Diversification and Covenants):',
        'A commercial bank may lend to hundreds of different small businesses — from local '
        'restaurants to technology startups. By diversifying its portfolio, the bank ensures '
        'that struggles in one industry are offset by successes in another. Additionally, '
        'including a covenant requiring quarterly financial statements enables close '
        'monitoring of borrower financial health.'))

    story.append(PageBreak())

    # ======================== QUESTION FOUR ========================
    story.append(P('QUESTION FOUR', 'q_head'))
    story.append(P(
        'Capital adequacy and deposit insurance are two critical regulatory mechanisms '
        'designed to protect the stability of financial institutions and safeguard '
        'depositors.'))

    story.append(P(
        'a) Explain the concept of capital adequacy ratios and discuss why regulatory '
        'authorities impose minimum capital requirements on financial institutions. (5 Marks)',
        'q_text'))

    story.append(P(
        'The Capital Adequacy Ratio (CAR), also known as the Capital-to-Risk Weighted '
        'Assets Ratio (CRAR), is a measurement of a bank\'s available capital expressed '
        'as a percentage of its risk-weighted credit exposure. It is used to protect '
        'depositors and promote the stability and efficiency of financial systems '
        'around the world.'))
    story.append(P(
        'The Basel III framework requires banks to maintain a minimum CAR of 8%, with '
        'Tier 1 capital (core capital such as equity and retained earnings) forming the '
        'most critical component. In Kenya, the Central Bank of Kenya mandates a minimum '
        'CAR of 14.5% for commercial banks.'))

    story.append(P('Reasons Why Regulatory Authorities Impose Minimum Capital Requirements',
                   'sub_head'))
    for label, text in [
        ('i) Protection of Depositors:',
         'By ensuring a bank has enough of its own "skin in the game," regulators protect '
         'depositors\' money. If a bank fails, its capital absorbs losses before depositors '
         'lose their savings.'),
        ('ii) Restricting Excessive Risk-Taking:',
         'Requiring banks to hold more capital against riskier assets creates a financial '
         'disincentive for excessive risk-taking, encouraging more prudent lending and '
         'investment practices.'),
        ('iii) Promoting Financial Stability (Systemic Risk Mitigation):',
         'The failure of one large bank can trigger a "domino effect" across the entire '
         'economy. Minimum capital requirements reduce the likelihood of individual bank '
         'failures, protecting the broader financial system.'),
        ('iv) Maintaining Public Confidence:',
         'The banking system relies on trust. Knowing that banks are required to maintain '
         'a certain level of financial strength prevents bank runs, where many customers '
         'simultaneously withdraw funds out of fear of insolvency.'),
    ]:
        story.append(bullet(label, text))

    story.append(SP(8))
    story.append(P(
        'b) Discuss the role of deposit insurance as a liability guarantee mechanism, and '
        'explain how it protects depositors while also creating moral hazard issues that '
        'regulators must address. (5 Marks)',
        'q_text'))

    story.append(P(
        'Deposit insurance is a protective measure implemented in many countries to '
        'safeguard bank depositors, in full or in part, from losses caused by a bank\'s '
        'inability to pay its debts when due. It acts as a "safety net" for the banking '
        'system, underpinning public confidence in financial institutions.'))

    story.append(P('Role as a Liability Guarantee Mechanism', 'sub_head'))
    story.append(bullet(
        'Systemic Protection:',
        'Deposit insurance prevents a localized bank failure from spiraling into a '
        'systemic financial crisis by maintaining public trust in the banking sector.'))
    story.append(bullet(
        'Confidence and Stability:',
        'By guaranteeing that deposits are safe up to a prescribed limit, deposit insurance '
        'prevents bank runs where many customers withdraw funds simultaneously due to '
        'fear of bank insolvency.'))

    story.append(P('How Deposit Insurance Protects Depositors', 'sub_head'))
    story.append(bullet(
        'Direct Reimbursement:',
        'If a bank fails, the deposit insurance agency — for example, the FDIC in the '
        'United States or the Kenya Deposit Insurance Corporation (KDIC) in Kenya — pays '
        'out the insured amount directly to depositors.'))
    story.append(bullet(
        'Peace of Mind:',
        'Small depositors are not required to constantly monitor the bank\'s financial '
        'health, as their funds are guaranteed up to a certain limit. In Kenya, the KDIC '
        'currently protects deposits up to Ksh 500,000 per depositor per institution.'))

    story.append(P('Moral Hazard: The Key Challenge', 'sub_head'))
    story.append(P(
        'While beneficial, deposit insurance creates a moral hazard problem — a situation '
        'where parties take on more risk because they do not bear the full consequences '
        'of that risk:'))
    story.append(bullet(
        'For Banks:',
        'Because depositors are protected and less likely to withdraw funds in response '
        'to risky behaviour, bank management may be tempted to engage in higher-risk '
        'lending or investment strategies to seek higher profits, knowing the "safety '
        'net" exists if they fail.'))
    story.append(bullet(
        'For Depositors:',
        'Insured depositors have little incentive to monitor or discipline bank behaviour, '
        'removing a key check on excessive risk-taking.'))

    story.append(P('Regulatory Responses to Moral Hazard', 'sub_head'))
    story.append(P('To counter the moral hazard created by deposit insurance, regulators '
                   'implement the following strategies:'))
    for text in [
        '<b>Prudential Supervision</b> \u2014 Regular audits and examinations of banks by '
        'regulators to detect and address excessive risk-taking.',
        '<b>Risk-Based Premiums</b> \u2014 Banks that take on more risk pay higher deposit '
        'insurance premiums, aligning the cost of insurance with actual risk levels.',
        '<b>Coverage Limits</b> \u2014 Restricting the guarantee to a maximum amount (e.g., '
        'Ksh 500,000 in Kenya) preserves some depositor incentive to monitor bank health '
        'for amounts above the limit.',
        '<b>Capital Requirements</b> \u2014 Mandatory capital ratios (such as CAR) ensure '
        'banks maintain their own buffer against losses, reducing reliance on the '
        'insurance fund.',
    ]:
        story.append(bullet('\u2022', text))

    doc.build(story)
    print(f'PDF saved: {output}')
    return output


if __name__ == '__main__':
    generate_cat_pdf('files/Calvince_BBM_415_CAT.pdf')
