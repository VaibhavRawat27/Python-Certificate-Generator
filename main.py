import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
from PIL import Image
import datetime

# Page setup
st.set_page_config(page_title="🎨 Custom Landscape Certificate", layout="centered")
st.title("🎨 Custom Landscape Certificate Generator")

# Sidebar input
st.sidebar.header("📝 Certificate Info")
recipient_name = st.sidebar.text_input("Recipient Name", "Vaibhav Rawat")
course_title = st.sidebar.text_input("Course Title", "AI Fundamentals")
summary_text = st.sidebar.text_area("Summary", "Awarded for outstanding performance in the course.")
position = st.sidebar.text_input("Position", "Top Scorer")
date = st.sidebar.date_input("Date", datetime.date.today())

# Font Options
st.sidebar.markdown("---")
st.sidebar.subheader("🖋 Font Settings")
font_color = st.sidebar.color_picker("Font Color", "#222222")
font_title_size = st.sidebar.slider("Title Font Size", 24, 40, 30)
font_name_size = st.sidebar.slider("Name Font Size", 18, 30, 22)
font_course_size = st.sidebar.slider("Course Font Size", 16, 28, 20)
font_summary_size = st.sidebar.slider("Summary Font Size", 12, 20, 14)

# Design Options
st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Design Settings")
bg_color = st.sidebar.color_picker("Background Color", "#FFF7F0")
add_border = st.sidebar.checkbox("Add Decorative Border", True)
add_separator_line = st.sidebar.checkbox("Add Line Below Title", True)

# Uploads
st.sidebar.markdown("---")
logo_file = st.sidebar.file_uploader("Upload Logo (optional)", type=["png", "jpg"])
sign_file = st.sidebar.file_uploader("Upload Signature (optional)", type=["png", "jpg"])

# Live preview
st.subheader("📄 Live Certificate Preview")
st.markdown(f"**Name:** {recipient_name}")
st.markdown(f"**Course:** {course_title}")
st.markdown(f"**Summary:** {summary_text}")
st.markdown(f"**Position:** {position}")
st.markdown(f"**Date:** {date.strftime('%d %B %Y')}")
st.markdown(f"**Font Color:** `{font_color}` | **Background:** `{bg_color}`")

if logo_file:
    st.image(logo_file, width=120, caption="Uploaded Logo")
if sign_file:
    st.image(sign_file, width=100, caption="Uploaded Signature")

st.markdown("---")
generate_btn = st.button("🎉 Generate Custom Certificate")

# PDF Generator
def create_certificate_pdf(name, course, summary, position, date, logo, sign, font_color, bg_color,
                           font_sizes, add_border, add_line):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(LETTER))
    width, height = landscape(LETTER)

    margin_x = 60
    center_x = width / 2

    # Background
    c.setFillColor(HexColor(bg_color))
    c.rect(0, 0, width, height, fill=1)

    # Optional border
    if add_border:
        c.setStrokeColorRGB(0.2, 0.2, 0.2)
        c.setLineWidth(3)
        c.rect(20, 20, width - 40, height - 40)

    # Font color
    c.setFillColor(HexColor(font_color))

    # Title
    c.setFont("Helvetica-Bold", font_sizes["title"])
    c.drawCentredString(center_x, height - 80, "🎓 Certificate of Completion")

    # Optional separator
    if add_line:
        c.setLineWidth(1)
        c.line(margin_x, height - 95, width - margin_x, height - 95)

    # Name
    c.setFont("Helvetica-Bold", font_sizes["name"])
    c.drawCentredString(center_x, height - 140, name)

    # Subtitle
    c.setFont("Helvetica", 14)
    c.drawCentredString(center_x, height - 175, "has successfully completed the course")

    # Course
    c.setFont("Helvetica-Bold", font_sizes["course"])
    c.drawCentredString(center_x, height - 210, course)

    # Summary
    c.setFont("Helvetica", font_sizes["summary"])
    c.drawCentredString(center_x, height - 245, summary)

    # Position
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(center_x, height - 275, f"Position: {position}")

    # Date at bottom-center
    c.setFont("Helvetica", 10)
    c.drawCentredString(center_x, 40, f"Date: {date.strftime('%d %B %Y')}")

    # Logo
    if logo:
        c.drawImage(ImageReader(logo), margin_x, height - 100, width=80, preserveAspectRatio=True, mask='auto')

    # Signature
    if sign:
        c.drawImage(ImageReader(sign), width - 140, 30, width=100, preserveAspectRatio=True, mask='auto')

    c.save()
    buffer.seek(0)
    return buffer

# Trigger generation
if generate_btn:
    pdf_data = create_certificate_pdf(
        name=recipient_name,
        course=course_title,
        summary=summary_text,
        position=position,
        date=date,
        logo=logo_file,
        sign=sign_file,
        font_color=font_color,
        bg_color=bg_color,
        font_sizes={
            "title": font_title_size,
            "name": font_name_size,
            "course": font_course_size,
            "summary": font_summary_size
        },
        add_border=add_border,
        add_line=add_separator_line
    )

    st.success("✅ Custom certificate generated!")
    st.download_button("📥 Download PDF", data=pdf_data, file_name=f"{recipient_name}_certificate.pdf", mime="application/pdf")
