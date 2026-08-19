from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Table,
    TableStyle
)
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
import os
from datetime import datetime


def generate_security_report(
    input_data,
    result,
    confidence
):

    # Create reports folder
    os.makedirs("reports", exist_ok=True)

    # Create unique filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    filename = (
        f"reports/AI_Phishing_Report_{timestamp}.pdf"
    )

    # --------------------------------------------------------
    # Determine risk
    # --------------------------------------------------------

    result_lower = str(result).lower()

    if (
        "phishing" in result_lower
        or "suspicious" in result_lower
        or "malicious" in result_lower
    ):

        if confidence >= 80:
            risk_level = "HIGH"

        elif confidence >= 50:
            risk_level = "MEDIUM"

        else:
            risk_level = "LOW"

    else:

        risk_level = "LOW"


    # --------------------------------------------------------
    # Determine attack type
    # --------------------------------------------------------

    if "email" in result_lower:

        attack_type = "Email Phishing / Social Engineering"

    elif (
        "phishing" in result_lower
        or "suspicious" in result_lower
    ):

        attack_type = "URL Phishing / Credential Phishing"

    else:

        attack_type = "No major phishing attack detected"


    # --------------------------------------------------------
    # Create PDF
    # --------------------------------------------------------

    document = SimpleDocTemplate(
        filename,
        pagesize=A4,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()


    title_style = ParagraphStyle(
        "TitleStyle",
        parent=styles["Title"],
        fontSize=24,
        alignment=TA_CENTER,
        spaceAfter=20
    )


    heading_style = ParagraphStyle(
        "HeadingStyle",
        parent=styles["Heading2"],
        fontSize=16,
        spaceBefore=18,
        spaceAfter=10
    )


    normal_style = ParagraphStyle(
        "NormalStyle",
        parent=styles["Normal"],
        fontSize=11,
        leading=16
    )


    story = []


    # --------------------------------------------------------
    # TITLE
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "AI PHISHING DETECTION",
            title_style
        )
    )

    story.append(
        Paragraph(
            "SECURITY ANALYSIS REPORT",
            title_style
        )
    )

    story.append(
        Paragraph(
            "Generated: "
            + datetime.now().strftime(
                "%d-%m-%Y %H:%M:%S"
            ),
            normal_style
        )
    )

    story.append(
        Spacer(1, 20)
    )


    # --------------------------------------------------------
    # SCAN INFORMATION
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "1. Scan Information",
            heading_style
        )
    )


    scan_data = [

        ["Input / Target", str(input_data)],

        ["Detection Result", str(result)],

        ["Confidence", f"{confidence:.2f}%"],

        ["Risk Level", risk_level],

        ["Possible Attack Type", attack_type],

    ]


    table = Table(
        scan_data,
        colWidths=[
            2 * inch,
            4 * inch
        ]
    )


    table.setStyle(
        TableStyle([

            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.lightgrey
            ),

            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.5,
                colors.grey
            ),

            (
                "FONTNAME",
                (0, 0),
                (0, -1),
                "Helvetica-Bold"
            ),

            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),

            (
                "PADDING",
                (0, 0),
                (-1, -1),
                8
            )

        ])
    )


    story.append(table)


    # --------------------------------------------------------
    # RISK ASSESSMENT
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "2. Risk Assessment",
            heading_style
        )
    )


    story.append(
        Paragraph(
            f"The AI system assigned a confidence score of "
            f"<b>{confidence:.2f}%</b> to the detected result.",
            normal_style
        )
    )


    story.append(
        Spacer(1, 8)
    )


    story.append(
        Paragraph(
            f"<b>Overall Risk Level:</b> {risk_level}",
            normal_style
        )
    )


    # --------------------------------------------------------
    # POSSIBLE ATTACK
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "3. Possible Phishing Attack",
            heading_style
        )
    )


    story.append(
        Paragraph(
            f"<b>Possible attack type:</b> {attack_type}",
            normal_style
        )
    )


    story.append(
        Paragraph(
            "Attackers may use phishing techniques to "
            "trick users into revealing passwords, OTPs, "
            "financial information or other sensitive data.",
            normal_style
        )
    )


    # --------------------------------------------------------
    # POSSIBLE RISKS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "4. Possible Risks",
            heading_style
        )
    )


    risks = [

        "Credential theft",

        "Account takeover",

        "Identity theft",

        "Financial loss",

        "Malware infection",

        "Loss of sensitive information",

        "Privacy compromise"

    ]


    for risk in risks:

        story.append(
            Paragraph(
                f"• {risk}",
                normal_style
            )
        )


    # --------------------------------------------------------
    # WHAT TO DO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "5. What You Should Do",
            heading_style
        )
    )


    recommendations = [

        "Verify the sender or website through an official source.",

        "Check the domain name carefully.",

        "Do not enter passwords on suspicious websites.",

        "Enable Multi-Factor Authentication (MFA).",

        "Change your password if credentials may have been exposed.",

        "Report suspicious emails or websites.",

        "Keep your browser and operating system updated."

    ]


    for item in recommendations:

        story.append(
            Paragraph(
                f"✓ {item}",
                normal_style
            )
        )


    # --------------------------------------------------------
    # WHAT NOT TO DO
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "6. What You Should NOT Do",
            heading_style
        )
    )


    warnings = [

        "Do not enter your password into suspicious websites.",

        "Do not provide OTPs or verification codes.",

        "Do not provide banking or card information.",

        "Do not download unknown attachments.",

        "Do not click suspicious links.",

        "Do not ignore browser or email security warnings."

    ]


    for item in warnings:

        story.append(
            Paragraph(
                f"✗ {item}",
                normal_style
            )
        )


    # --------------------------------------------------------
    # SECURITY RECOMMENDATIONS
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "7. Security Recommendations",
            heading_style
        )
    )


    recommendations2 = [

        "Use strong and unique passwords.",

        "Enable MFA on important accounts.",

        "Keep security software updated.",

        "Check URLs before entering sensitive information.",

        "Avoid links from unknown senders.",

        "Monitor accounts for unusual activity."

    ]


    for item in recommendations2:

        story.append(
            Paragraph(
                f"• {item}",
                normal_style
            )
        )


    # --------------------------------------------------------
    # DISCLAIMER
    # --------------------------------------------------------

    story.append(
        Paragraph(
            "8. Important Note",
            heading_style
        )
    )


    story.append(
        Paragraph(
            "This report is generated using an AI/ML-based "
            "phishing detection system. The confidence score "
            "represents the model's prediction and should not "
            "be considered absolute proof. Further investigation "
            "may be required before making a final security decision.",
            normal_style
        )
    )


    # --------------------------------------------------------
    # BUILD PDF
    # --------------------------------------------------------

    document.build(story)


    return filename