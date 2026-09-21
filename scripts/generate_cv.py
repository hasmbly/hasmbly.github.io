from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_RIGHT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    HRFlowable,
    Image,
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
PHOTO = ROOT / "assets" / "hasbi-cv-photo.jpg"

INK = colors.HexColor("#20242A")
MUTED = colors.HexColor("#5F6670")
ACCENT = colors.HexColor("#1E4F9A")
LINE = colors.HexColor("#C9CDD2")


def build_styles():
    base = getSampleStyleSheet()
    return {
        "name": ParagraphStyle(
            "Name", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=23, leading=25, textColor=INK, spaceAfter=2,
        ),
        "headline": ParagraphStyle(
            "Headline", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=10.2, leading=12.5, textColor=INK, spaceAfter=5,
        ),
        "contact": ParagraphStyle(
            "Contact", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.1, leading=11, textColor=MUTED,
        ),
        "section": ParagraphStyle(
            "Section", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.8, leading=10.5, textColor=INK,
            spaceBefore=7, spaceAfter=3,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.6, leading=11.3, textColor=INK, spaceAfter=3.5,
        ),
        "role": ParagraphStyle(
            "Role", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=9.8, leading=11.5, textColor=INK,
        ),
        "date": ParagraphStyle(
            "Date", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=7.6, leading=9.3, alignment=TA_RIGHT, textColor=MUTED,
        ),
        "company": ParagraphStyle(
            "Company", parent=base["Normal"], fontName="Helvetica-Bold",
            fontSize=8.2, leading=10, textColor=ACCENT, spaceAfter=2.5,
        ),
        "bullet": ParagraphStyle(
            "Bullet", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.25, leading=10.6, leftIndent=9, firstLineIndent=-6,
            bulletIndent=0, textColor=INK, spaceAfter=1.8,
        ),
        "skill_text": ParagraphStyle(
            "SkillText", parent=base["Normal"], fontName="Helvetica",
            fontSize=8.3, leading=10.5, textColor=INK,
        ),
    }


def section_heading(story, styles, text):
    story.append(Paragraph(text.upper(), styles["section"]))
    story.append(HRFlowable(width="100%", thickness=0.45, color=LINE, spaceAfter=4))


def dated_heading(styles, title, dates, title_width=116 * mm, date_width=60 * mm):
    table = Table(
        [[Paragraph(title, styles["role"]), Paragraph(dates, styles["date"])]],
        colWidths=[title_width, date_width],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("LEFTPADDING", (0, 0), (-1, -1), 0),
        ("RIGHTPADDING", (0, 0), (-1, -1), 0),
        ("TOPPADDING", (0, 0), (-1, -1), 0),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 0),
    ]))
    return table


def entry_block(styles, title, subtitle, dates, bullets, spacing=3):
    content = [
        dated_heading(styles, title, dates),
        Paragraph(subtitle, styles["company"]),
    ]
    content.extend(Paragraph(f"- {bullet}", styles["bullet"]) for bullet in bullets)
    content.append(Spacer(1, spacing))
    return KeepTogether(content)


def page_footer(canvas, document):
    canvas.saveState()
    canvas.setTitle("Hasbi - Full-Stack Software Engineer")
    canvas.setAuthor("Hasbi")
    canvas.setSubject("Curriculum Vitae")
    page_width, _ = A4
    canvas.setStrokeColor(LINE)
    canvas.setLineWidth(0.4)
    canvas.line(17 * mm, 13 * mm, page_width - 17 * mm, 13 * mm)
    canvas.setFillColor(MUTED)
    canvas.setFont("Helvetica", 7.1)
    canvas.drawString(17 * mm, 8.5 * mm, "Hasbi - Full-Stack Software Engineer")
    canvas.drawRightString(page_width - 17 * mm, 8.5 * mm, f"Page {document.page}")
    canvas.restoreState()


def header(styles):
    contact = Paragraph(
        '<link href="mailto:hasmbly@gmail.com" color="#1E4F9A">hasmbly@gmail.com</link>'
        '  |  <link href="https://github.com/hasmbly" color="#1E4F9A">github.com/hasmbly</link>'
        '  |  <link href="https://www.linkedin.com/in/justhasby/" color="#1E4F9A">linkedin.com/in/justhasby</link>',
        styles["contact"],
    )
    photo = Image(str(PHOTO), width=30 * mm, height=30 * mm)
    table = Table(
        [[[
            Paragraph("Hasbi", styles["name"]),
            Paragraph("FULL-STACK SOFTWARE ENGINEER", styles["headline"]),
            contact,
        ], photo]],
        colWidths=[139 * mm, 30 * mm],
    )
    table.setStyle(TableStyle([
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("LEFTPADDING", (0, 0), (0, 0), 0),
        ("RIGHTPADDING", (0, 0), (0, 0), 7),
        ("TOPPADDING", (0, 0), (0, 0), 0),
        ("BOTTOMPADDING", (0, 0), (0, 0), 0),
        ("LEFTPADDING", (1, 0), (1, 0), 0),
        ("RIGHTPADDING", (1, 0), (1, 0), 0),
        ("TOPPADDING", (1, 0), (1, 0), 0),
        ("BOTTOMPADDING", (1, 0), (1, 0), 0),
        ("BOX", (1, 0), (1, 0), 0.45, LINE),
    ]))
    return table


def generate_cv():
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    if not PHOTO.exists():
        raise FileNotFoundError(f"Portrait not found: {PHOTO}")

    styles = build_styles()
    document = SimpleDocTemplate(
        str(OUTPUT), pagesize=A4, rightMargin=17 * mm, leftMargin=17 * mm,
        topMargin=14 * mm, bottomMargin=18 * mm,
        title="Hasbi - Full-Stack Software Engineer", author="Hasbi",
        subject="Curriculum Vitae",
    )

    story = [
        header(styles), Spacer(1, 6),
        HRFlowable(width="100%", thickness=0.8, color=INK, spaceAfter=3),
    ]

    section_heading(story, styles, "Profile")
    story.append(Paragraph(
        "I have worked as a software engineer since 2019. I currently work as a Full-Stack Developer at "
        "PT Vioren Informatika Teknologi. I have a strong interest in clean architecture and technical work "
        "related to system performance and other system improvements. I enjoy digging "
        "into and solving complex technical problems.",
        styles["body"],
    ))

    section_heading(story, styles, "Current Tech Stack")
    story.append(Paragraph(
        ".NET 10, ASP.NET Core Web API, Microsoft SQL Server, Blazor, Azure DevOps, Azure Resources",
        styles["skill_text"],
    ))

    section_heading(story, styles, "Previous Tech Stack")
    story.append(Paragraph("Laravel, Go Echo, Angular", styles["skill_text"]))

    section_heading(story, styles, "Professional Experience")
    story.append(entry_block(
        styles, "Full-Stack Software Developer", "PT Vioren Informatika Teknologi",
        "February 2020 - Present",
        [
            "Develop enterprise software across web, desktop, services, infrastructure, and hardware-integrated environments.",
            "Contribute to solutions for energy, shipping, manufacturing, and mining clients.",
            "Apply clean architecture and investigate performance, security, and maintainability concerns.",
        ],
    ))
    story.append(entry_block(
        styles, "Electrical Engineer", "PT Intecs Teknikatama Industri",
        "December 2018 - May 2019",
        [
            "Worked on the AdaptFMS Fuel Management System project at BUMA Lati, Berau Coal, East Kalimantan.",
            "Project scope included RFID authorization for people and units, pulser and flowmeter measurement, tank gauging, motorized valves, and pump control.",
            "Installed low-voltage wiring for panel boxes and installed panel boxes on fuel trucks.",
        ],
    ))
    story.append(entry_block(
        styles, "System Engineer", "PT Netsource Global Technologies",
        "April 2014 - October 2018",
        [
            "Installed, configured, and troubleshot software, hardware, servers, and networks.",
            "Installed, configured, and troubleshot low-current electrical systems and CCTV.",
            "Helped with research and integrations between third-party hardware or systems and custom systems.",
            "Worked with clients including the Agriculture Department and Regional Police.",
        ],
    ))

    story.append(PageBreak())
    section_heading(story, styles, "Project Highlights")
    story.append(entry_block(
        styles, "Coal Weighing and Hauling Operations", "PT Adaro Minerals Indonesia Tbk",
        "December 2025 - August 2026",
        [
            "Developed a hybrid WPF-Blazor desktop application integrating RFID readers, weighbridges, and LED traffic-light relays.",
            "Built a concurrent .NET Linux service that consumes MQTT data and processes hauling transactions and trip data for RFID-tagged dump trucks.",
        ],
    ))
    story.append(entry_block(
        styles, "Investment Monitoring System / Project Monitoring on Return",
        "PT Pertamina International Shipping (Marine Logistics)",
        "Release 1: September 2024 - November 2024<br/>Release 2: May 2025 - December 2025",
        [
            "Monitors investments that have passed planning and reached the Final Investment Decision stage.",
            "Tracks monthly economic data from the execution stage through the on-stream stage.",
        ],
    ))
    story.append(entry_block(
        styles, "DevSecOps Implementation", "PT Pertamina Hulu Energi (Upstream)",
        "March 2024 - December 2024",
        [
            "Implemented DevSecOps using Azure DevOps and hybrid Azure and on-premises infrastructure.",
            "Used Azure Pipelines, on-premises agent servers, SonarQube for SAST, and IIS and Azure Web Apps for web hosting.",
        ],
    ))
    story.append(entry_block(
        styles, "MyDents Dental Clinic System", "Dental clinic information system",
        "October 2023 - December 2023",
        ["Developed an information system for dental clinics."],
    ))
    story.append(entry_block(
        styles, "Business Applications and Data Services",
        "Upfield / Flora Indonesia - Flora Food Groups",
        "January 2021 - February 2025",
        [
            "Worked on the Promotion and Claim Management System (PCMS).",
            "Worked on data retrieval services for distributor secondary sales from Accurate Online Indonesia.",
        ],
    ))
    story.append(entry_block(
        styles, "Fortifex", "Cryptocurrency portfolio platform", "February 2020",
        [
            "Software development platform for centralized and managed cryptocurrency portfolios across multiple exchanges and wallets.",
            "Designed to support safer cryptocurrency transactions and trading for businesses and individuals.",
        ],
    ))
    story.append(entry_block(
        styles, "SILADU - Sistem Layanan Aduan", "Social Affairs Agency",
        "July 2019 - December 2019",
        [
            "Handled back-end development for the Complaint Service System.",
            "The system helps Jakarta residents check their social-aid status and submit questions from home.",
        ],
    ))

    section_heading(story, styles, "Education")
    story.append(dated_heading(
        styles, "Universitas Indraprasta PGRI (UNINDRA)", "2014 - 2018",
    ))

    document.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(f"Created {OUTPUT}")


if __name__ == "__main__":
    generate_cv()
