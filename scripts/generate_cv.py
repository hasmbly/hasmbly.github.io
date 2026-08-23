from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT, TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    KeepTogether,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "output" / "pdf" / "hasbi-cv.pdf"

INK = colors.HexColor("#171B22")
MUTED = colors.HexColor("#5F6672")
ACCENT = colors.HexColor("#2459D3")
LINE = colors.HexColor("#D9DCD7")
SOFT = colors.HexColor("#F3F5FA")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=23,
            leading=26,
            textColor=INK,
            spaceAfter=2,
        ),
        "headline": ParagraphStyle(
            "Headline",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.5,
            leading=13,
            textColor=ACCENT,
            spaceAfter=5,
        ),
        "contact": ParagraphStyle(
            "Contact",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.1,
            leading=11,
            textColor=MUTED,
        ),
        "section": ParagraphStyle(
            "Section",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=9.2,
            leading=11,
            textColor=ACCENT,
            spaceBefore=8,
            spaceAfter=5,
            uppercase=True,
        ),
        "body": ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.6,
            leading=11.5,
            textColor=INK,
            spaceAfter=4,
        ),
        "role": ParagraphStyle(
            "Role",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=10.2,
            leading=12,
            textColor=INK,
        ),
        "date": ParagraphStyle(
            "Date",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.9,
            leading=10,
            alignment=TA_RIGHT,
            textColor=MUTED,
        ),
        "company": ParagraphStyle(
            "Company",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=8.2,
            leading=10,
            textColor=ACCENT,
            spaceAfter=3,
        ),
        "bullet": ParagraphStyle(
            "Bullet",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.35,
            leading=11,
            leftIndent=10,
            firstLineIndent=-7,
            bulletIndent=0,
            textColor=INK,
            spaceAfter=2.5,
        ),
        "label": ParagraphStyle(
            "Label",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=7.9,
            leading=10.5,
            textColor=INK,
        ),
        "small": ParagraphStyle(
            "Small",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7.9,
            leading=10.5,
            textColor=MUTED,
        ),
    }


def section_heading(story, styles, text):
    story.append(Paragraph(text.upper(), styles["section"]))
    story.append(HRFlowable(width="100%", thickness=0.45, color=LINE, spaceAfter=5))


def role_block(styles, role, company, dates, bullets):
    heading = Table(
        [[Paragraph(role, styles["role"]), Paragraph(dates, styles["date"])]],
        colWidths=[128 * mm, 45 * mm],
    )
    heading.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    content = [heading, Paragraph(company, styles["company"])]
    content.extend(Paragraph(f"- {bullet}", styles["bullet"]) for bullet in bullets)
    content.append(Spacer(1, 4))
    return KeepTogether(content)


def project_block(styles, name, client, dates, bullets):
    heading = Table(
        [[Paragraph(name, styles["role"]), Paragraph(dates, styles["date"])]],
        colWidths=[128 * mm, 45 * mm],
    )
    heading.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    content = [heading, Paragraph(client, styles["company"])]
    content.extend(Paragraph(f"- {bullet}", styles["bullet"]) for bullet in bullets)
    content.append(Spacer(1, 3))
    return KeepTogether(content)


def page_footer(canvas, document):
    canvas.saveState()
    canvas.setTitle("Hasbi - Full-Stack Software Engineer")
    canvas.setAuthor("Hasbi")
    canvas.setSubject("Curriculum Vitae")
    page_width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.45)
    canvas.line(18 * mm, 13 * mm, page_width - 18 * mm, 13 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.2)
    canvas.drawString(18 * mm, 8.5 * mm, "Hasbi - Full-Stack Software Engineer")
    canvas.drawRightString(page_width - 18 * mm, 8.5 * mm, f"Page {document.page}")
    canvas.restoreState()


def generate_cv():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    styles = build_styles()
    document = SimpleDocTemplate(
        str(OUTPUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=16 * mm,
        bottomMargin=18 * mm,
        title="Hasbi - Full-Stack Software Engineer",
        author="Hasbi",
        subject="Curriculum Vitae",
    )

    story = [
        Paragraph("Hasbi", styles["name"]),
        Paragraph("FULL-STACK SOFTWARE ENGINEER", styles["headline"]),
        Paragraph(
            '<link href="mailto:hasmbly@gmail.com" color="#2459D3">hasmbly@gmail.com</link>'
            '  |  <link href="https://github.com/hasmbly" color="#2459D3">github.com/hasmbly</link>'
            '  |  <link href="https://www.linkedin.com/in/justhasby/" color="#2459D3">linkedin.com/in/justhasby</link>',
            styles["contact"],
        ),
        Spacer(1, 7),
        HRFlowable(width="100%", thickness=1.2, color=INK, spaceAfter=4),
    ]

    section_heading(story, styles, "Professional Summary")
    story.append(
        Paragraph(
            "Full-stack software engineer with professional experience since 2019 across back-end services, "
            "web applications, desktop software, infrastructure, and hardware-integrated systems. Focused on "
            "clean architecture, performance, memory efficiency, security, and solving complex technical problems.",
            styles["body"],
        )
    )

    section_heading(story, styles, "Core Expertise")
    skills_table = Table(
        [
            [Paragraph("APPLICATIONS", styles["label"]), Paragraph(".NET 10, ASP.NET Core Web API, Blazor, WPF", styles["small"])],
            [Paragraph("DATA AND CLOUD", styles["label"]), Paragraph("Microsoft SQL Server, Azure DevOps, Azure Resources", styles["small"])],
            [Paragraph("ENGINEERING", styles["label"]), Paragraph("Clean architecture, performance, memory efficiency, security, concurrency", styles["small"])],
        ],
        colWidths=[34 * mm, 139 * mm],
    )
    skills_table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.45, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.extend([skills_table, Spacer(1, 3)])

    section_heading(story, styles, "Professional Experience")
    story.append(
        role_block(
            styles,
            "Full-Stack Software Developer",
            "PT Vioren Informatika Teknologi",
            "Feb 2020 - Present",
            [
                "Develop enterprise software across web, desktop, services, infrastructure, and hardware-integrated environments.",
                "Contribute to solutions for energy, shipping, manufacturing, and mining clients.",
                "Apply clean architecture and investigate performance, memory, security, and maintainability concerns.",
            ],
        )
    )
    story.append(
        role_block(
            styles,
            "Back-End Software Developer",
            "PUSDATIN - Social Affairs Agency",
            "Jul 2019 - Jan 2020",
            [
                "Contributed to back-end software at the Center for Data, Information, and Social Security.",
            ],
        )
    )

    section_heading(story, styles, "Selected Project Highlights")
    story.append(
        project_block(
            styles,
            "Coal Weighing and Hauling Operations",
            "PT Adaro Minerals Indonesia Tbk",
            "Dec 2025 - Aug 2026",
            [
                "Developed a hybrid WPF-Blazor desktop application integrating RFID readers, weighbridges, and LED traffic-light relays.",
                "Built a concurrent .NET Linux service that consumes MQTT data and processes hauling transactions and trip data for RFID-tagged dump trucks.",
            ],
        )
    )

    story.append(PageBreak())
    section_heading(story, styles, "Selected Project Highlights - Continued")
    story.append(
        project_block(
            styles,
            "InvestaSea - Phase I",
            "PT Pertamina International Shipping",
            "Sep 2024 - Nov 2024",
            [
                "Developed Project Monitoring on Return capabilities for investments that reached the Final Investment Decision milestone and monthly economic-indicator tracking.",
            ],
        )
    )
    story.append(
        project_block(
            styles,
            "InvestaSea - Phase II",
            "PT Pertamina International Shipping",
            "Jun 2025 - Dec 2025",
            [
                "Added later-phase features and integrated revenue and cost data from the third-party IMIS application.",
            ],
        )
    )
    story.append(
        project_block(
            styles,
            "DevSecOps Enablement",
            "PT Pertamina Hulu Energi",
            "Jun 2024 - Dec 2024",
            [
                "Implemented DevSecOps using Azure DevOps, SonarQube, and on-premise server agents, and contributed to refining the team's solution architecture.",
            ],
        )
    )
    story.append(
        project_block(
            styles,
            "PCMS Performance Improvements",
            "Upfield Indonesia (Flora Food Group)",
            "Jan 2024 - Feb 2024",
            [
                "Enhanced performance in the existing Promotion and Claim Management System.",
            ],
        )
    )
    story.append(
        project_block(
            styles,
            "Accurate Online Data Service",
            "Upfield Indonesia (Flora Food Group)",
            "Feb 2024 - Mar 2024",
            [
                "Improved a data-retrieval service integrating with Accurate Online accounting and business software.",
            ],
        )
    )

    section_heading(story, styles, "Additional Technical Skills")
    additional_skills = Table(
        [
            [Paragraph("EARLIER STACK", styles["label"]), Paragraph("Laravel, Go Echo, Angular", styles["small"])],
            [Paragraph("SYSTEMS", styles["label"]), Paragraph("Ubuntu Server administration, MikroTik network administration", styles["small"])],
            [Paragraph("HARDWARE", styles["label"]), Paragraph("Raspberry Pi, electrical installation, radio software configuration", styles["small"])],
        ],
        colWidths=[34 * mm, 139 * mm],
    )
    additional_skills.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), SOFT),
                ("BOX", (0, 0), (-1, -1), 0.45, LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.35, LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]
        )
    )
    story.append(additional_skills)

    section_heading(story, styles, "Education")
    education = Table(
        [[Paragraph("Universitas Indraprasta PGRI (UNINDRA)", styles["role"]), Paragraph("2014 - 2018", styles["date"])]],
        colWidths=[128 * mm, 45 * mm],
    )
    education.setStyle(
        TableStyle(
            [
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 0),
                ("RIGHTPADDING", (0, 0), (-1, -1), 0),
                ("TOPPADDING", (0, 0), (-1, -1), 0),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
            ]
        )
    )
    story.append(education)

    document.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    generate_cv()
