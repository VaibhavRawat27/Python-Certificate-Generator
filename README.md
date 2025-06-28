
# 🎓 Python Certificate Generator (Streamlit)

This is a fully customizable, center-aligned certificate generator built with **Streamlit** and **ReportLab**. It allows you to generate beautiful PDF certificates with personalized details, styling options, and saves each certificate with a unique ID.

---

## ✨ Features

- 🎯 Center-aligned and margin-safe design
- 🧾 Customizable fonts, colors, and layout
- 🖼 Upload logo (top-left) and signature (bottom-right)
- 🧑‍🎓 Add authority name and position
- 🆔 Auto-generated unique Certificate ID (saved and displayed)
- 📂 Saves metadata to `certificates.csv`
- 📊 Live table view of all generated certificates
- 📥 One-click PDF download

---

## 🚀 How to Use

1. **Install dependencies**  
   Make sure you have Python and the required libraries installed:
   ```bash
   pip install streamlit reportlab pandas
   ```

2. **Run the app**
   ```bash
   streamlit run app.py
   ```

3. **Customize your certificate**  
   Fill in the recipient name, course title, summary, date, position, and authority in the sidebar.

4. **Style it your way**  
   Choose font, font sizes, colors, and optionally upload a logo and signature.

5. **Generate & Download**  
   Click the "🚀 Generate Beautiful Certificate" button and download the PDF instantly.

6. **Certificate Records**  
   Every certificate is saved in `certificates.csv` with ID, name, course, and date. You can view them in a live table inside the app.

---

## 📁 File Structure

```
📦 Python-Certificate-Generator/
 ┣ 📜 app.py
 ┣ 📜 certificates.csv  ← auto-generated
 ┗ 📄 README.md
```

---

## 🔒 Sample Certificate ID

Each certificate is assigned a unique ID like:

```
Certificate ID: 8F2A6B9C
```

This is helpful for verification, record-keeping, or issuing public certificates.

---

## 📌 Future Enhancements

- ✅ QR Code for Certificate ID
- ✅ Email delivery of certificates
- ✅ Batch generation from CSV input

---

## 📸 Demo

_(Add a screenshot of the UI or generated certificate here)_

---

## 📜 License

This project is licensed under the MIT License.
