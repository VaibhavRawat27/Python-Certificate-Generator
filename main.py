import streamlit as st
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER, landscape
from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import HexColor
from io import BytesIO
import datetime
import pandas as pd
import uuid
import os

# Constants
CERT_DB = "certificates.csv"
margin = 60  # Updated for bottom space

# Load certificate records
def load_data():
    if os.path.exists(CERT_DB):
        return pd.read_csv(CERT_DB)
    return pd.DataFrame(columns=["Certificate ID", "Recipient", "Course", "Date"])

# Save new certificate
def save_certificate(cert_id, name, course, date):
    df = load_data()
    new_entry = {
        "Certificate ID": cert_id,
        "Recipient": name,
        "Course": course,
        "Date": date.strftime("%d-%m-%Y")
    }
    df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
    df.to_csv(CERT_DB, index=False)

# Streamlit Setup
st.set_page_config(page_title="🎓 Certificate Generator", layout="wide")
st.title("📄 Pro Certificate Generator")

# Sidebar Inputs
st.sidebar.header("📝 Certificate Info")
recipient_name = st.sidebar.text_input("👤 Recipient Name", "Vaibhav Rawat")
course_title = st.sidebar.text_input("📘 Course Title", "AI Fundamentals")
summary_text = st.sidebar.text_area("📄 Summary", "Awarded for excellence in the course.")
position = st.sidebar.text_input("🏆 Position", "Top Scorer")
date = st.sidebar.date_input("📅 Date", datetime.date.today())
authority_name = st.sidebar.text_input("🖋 Authority Name", "John Doe, Director")

st.sidebar.markdown("---")
st.sidebar.subheader("🎨 Style Settings")
font_family = st.sidebar.selectbox("Font", ["Helvetica", "Helvetica-Bold", "Times-Roman", "Courier"])
font_color = st.sidebar.color_picker("Font Color", "#1F1F1F")
bg_color = st.sidebar.color_picker("Background Color", "#FFFDF6")
font_title_size = st.sidebar.slider("🎓 Title Size", 28, 50, 36)
font_name_size = st.sidebar.slider("👤 Name Size", 22, 36, 28)
font_course_size = st.sidebar.slider("📘 Course Size", 18, 32, 24)
font_summary_size = st.sidebar.slider("📄 Summary Size", 14, 24, 16)

st.sidebar.markdown("---")
logo_file = st.sidebar.file_uploader("🖼 Upload Logo (Top-Left)", type=["png", "jpg"])
sign_file = st.sidebar.file_uploader("✍️ Upload Signature", type=["png", "jpg"])

# Preview
st.subheader("📋 Certificate Preview")
st.markdown(f"**Name:** `{recipient_name}`")
st.markdown(f"**Course:** `{course_title}`")
st.markdown(f"**Summary:** `{summary_text}`")
st.markdown(f"**Position:** `{position}`")
st.markdown(f"**Date:** `{date.strftime('%d %B %Y')}`")
st.markdown(f"**Authority:** `{authority_name}`")

if logo_file:
    st.image(logo_file, width=120, caption="Logo (Top-Left)")
if sign_file:
    st.image(sign_file, width=100, caption="Signature (Bottom-Right)")

generate_btn = st.button("🚀 Generate Beautiful Certificate")

# PDF Generation Function
def create_certificate(name, course, summary, position, date, authority, logo, sign, font_color, bg_color, font_family, font_sizes):
    cert_id = str(uuid.uuid4())[:8].upper()
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=landscape(LETTER))
    width, height = landscape(LETTER)
    center_x = width / 2

    # Background
    c.setFillColor(HexColor(bg_color))
    c.rect(0, 0, width, height, fill=1)

    # Border
    c.setStrokeColor(HexColor("#444444"))
    c.setLineWidth(3)
    c.rect(margin, margin, width - 2 * margin, height - 2 * margin)

    # Font color
    c.setFillColor(HexColor(font_color))

    # Title
    c.setFont("Helvetica-Bold", font_sizes["title"])
    c.drawCentredString(center_x, height - 150, "Certificate of Achievement")

    # Separator Line
    c.setLineWidth(1)
    c.line(center_x - 200, height - 165, center_x + 200, height - 165)

    # Name
    c.setFont(font_family, font_sizes["name"])
    c.drawCentredString(center_x, height - 250, name)

    # Subtitle
    c.setFont("Helvetica", 14)
    c.drawCentredString(center_x, height - 280, "has successfully completed the course")

    # Course
    c.setFont(font_family, font_sizes["course"])
    c.drawCentredString(center_x, height - 315, course)

    # Summary
    c.setFont("Helvetica", font_sizes["summary"])
    c.drawCentredString(center_x, height - 355, summary)

    # Position
    c.setFont("Helvetica-Oblique", 12)
    c.drawCentredString(center_x, height - 375, f"Position: {position}")

    # Date (bottom-left)
    c.setFont("Helvetica", 10)
    c.drawString(margin + 10, margin + 10, f"Date: {date.strftime('%d %B %Y')}")

    # Authority (bottom-right)
    c.setFont("Helvetica", 10)
    c.drawRightString(width - margin - 10, margin + 10, authority)

    # Logo
    if logo:
        c.drawImage(ImageReader(logo), margin + 10, height - 100, width=80, preserveAspectRatio=True, mask='auto')

    # Signature
    if sign:
        c.drawImage(ImageReader(sign), width - 160, margin + 30, width=100, preserveAspectRatio=True, mask='auto')

    # Certificate ID (bottom center, just above margin)
    c.setFont("Helvetica", 8)
    c.drawCentredString(center_x, margin - 15, f"Certificate ID: {cert_id}")

    c.save()
    buffer.seek(0)
    return cert_id, buffer

# Generate & Show Download
if generate_btn:
    cert_id, pdf = create_certificate(
        name=recipient_name,
        course=course_title,
        summary=summary_text,
        position=position,
        date=date,
        authority=authority_name,
        logo=logo_file,
        sign=sign_file,
        font_color=font_color,
        bg_color=bg_color,
        font_family=font_family,
        font_sizes={
            "title": font_title_size,
            "name": font_name_size,
            "course": font_course_size,
            "summary": font_summary_size
        }
    )

    save_certificate(cert_id, recipient_name, course_title, date)

    st.success(f"✅ Certificate generated with ID: `{cert_id}`")
    st.download_button("📥 Download Certificate PDF", data=pdf, file_name=f"{recipient_name}_certificate.pdf", mime="application/pdf")

    # Show stored certificates
    with st.expander("📑 View All Certificates"):
        st.dataframe(load_data())
