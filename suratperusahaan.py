import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from docx import Document
from io import BytesIO
import zipfile
import re

st.title("Generator Banyak Surat Dinas (ZIP)")

# Upload file
excel_file = st.file_uploader("📄 Upload Excel (data kecamatan)", type="xlsx")
template_file = st.file_uploader("📄 Upload Template Surat (Word .docx)", type="docx")

# Fungsi membuat ZIP berisi surat-surat
def generate_zip(template_bytes, data_rows):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:

            tpl = DocxTemplate(BytesIO(template_bytes))

            context = {
                "Kecamatan": row.get("Kecamatan", ""),
                "Camat": row.get("Camat", ""),
                "Pangkat": row.get("Pangkat", ""),
                "Golongan": row.get("Golongan", ""),
                "NIP": row.get("NIP", ""),
                "Jlh_beras": row.get("Jlh_beras", ""),
                "terbilang_beras": row.get("terbilang_beras", ""),
                "Jlh_telur": row.get("Jlh_telur", ""),
                "terbilang_telur": row.get("terbilang_telur", ""),
                "Jlh_minyak": row.get("Jlh_minyak", ""),
                "terbilang_minyak": row.get("terbilang_minyak", ""),
                "Plt": row.get("Plt", "")
            }

            tpl.render(context)

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            # nama file berdasarkan kecamatan
            safe_kecamatan = re.sub(r"[^\w\s-]", "", context["Kecamatan"]).strip().replace(" ", "_")
            filename = f"BAST_Pasar_Murah_{safe_kecamatan}.docx"

            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer


# Fungsi preview surat
def preview_docx_from_template(template_bytes, context):

    tpl = DocxTemplate(BytesIO(template_bytes))
    tpl.render(context)

    doc_io = BytesIO()
    tpl.save(doc_io)
    doc_io.seek(0)

    doc = Document(doc_io)
    lines = [p.text for p in doc.paragraphs]

    return "\n".join(lines)


# Logika utama
if excel_file and template_file:

    df = pd.read_excel(excel_file).fillna("")

    required_columns = ["Kecamatan"]

    missing_cols = [col for col in required_columns if col not in df.columns]

    if missing_cols:
        st.error(f"Kolom berikut wajib ada di Excel: {', '.join(missing_cols)}")

    else:

        df_valid = df[df["Kecamatan"].str.strip() != ""]

        if df_valid.empty:
            st.error("Tidak ada data kecamatan yang valid. Kolom 'Kecamatan' wajib diisi.")

        else:

            data_rows = df_valid.to_dict(orient="records")
            template_bytes = template_file.read()

            # preview surat pertama
            st.subheader("📄 Preview Isi Surat Pertama:")

            preview_text = preview_docx_from_template(template_bytes, data_rows[0])

            st.text_area("Preview Surat", preview_text, height=500)

            # tombol generate
            if st.button("📝 Buat dan Unduh Semua Surat"):

                with st.spinner("Membuat semua surat..."):
                    hasil_zip = generate_zip(template_bytes, data_rows)

                st.download_button(
                    label="📦 Download Semua Surat (.zip)",
                    data=hasil_zip,
                    file_name="BAST_Pasar_Murah.zip",
                    mime="application/zip"
                )
