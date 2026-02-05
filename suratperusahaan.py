import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from docx import Document
from io import BytesIO
import zipfile
import re

st.title("Generator Banyak Surat SURAT DINAS (ZIP)")

# Upload file
excel_file = st.file_uploader("📄 Upload Excel (daftar nama)", type="xlsx")
template_file = st.file_uploader("📄 Upload Template Surat (Word .docx)", type="docx")

# Fungsi membuat ZIP berisi surat-surat
def generate_zip(template_bytes, data_rows):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:
            tpl = DocxTemplate(BytesIO(template_bytes))

            context = {
                "NAMA": row.get("NAMA", ""),
                "TTL": row.get("TTL", ""),
                "NIK": row.get("NIK", ""),
                "PENDIDIKAN": row.get("PENDIDIKAN", ""),
                "ALAMAT": row.get("ALAMAT", ""),
                "PENEMPATAN": row.get("PENEMPATAN", ""),
                "Jenis_Barang": row.get("Jenis_Barang", "")
            }

            tpl.render(context)

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            safe_nama = re.sub(r"[^\w\s-]", "", context["NAMA"]).strip().replace(" ", "_")
            filename = f"Surat-Kontrak_{safe_nama}.docx"
            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer

# Fungsi untuk preview isi surat pertama
def preview_docx_from_template(template_bytes, context):
    tpl = DocxTemplate(BytesIO(template_bytes))
    tpl.render(context)

    doc_io = BytesIO()
    tpl.save(doc_io)
    doc_io.seek(0)

    doc = Document(doc_io)
    lines = [p.text for p in doc.paragraphs]
    return "\n".join(lines)

# Logika utama aplikasi
if excel_file and template_file:
    df = pd.read_excel(excel_file).fillna("")
    
    required_columns = ["NAMA"]
    missing_cols = [col for col in required_columns if col not in df.columns]
    
    if missing_cols:
        st.error(f"Kolom berikut wajib ada di Excel: {', '.join(missing_cols)}")
    else:
        df_valid = df[df["NAMA"].str.strip() != ""]
        
        if df_valid.empty:
            st.error("Tidak ada data perusahaan yang valid. Kolom 'NAMA' wajib diisi.")
        else:
            data_rows = df_valid.to_dict(orient="records")
            template_bytes = template_file.read()

            # Tampilkan preview surat pertama
            st.subheader("📄 Preview Isi Surat Pertama:")
            preview_text = preview_docx_from_template(template_bytes, data_rows[0])
            st.text_area("Preview Surat", preview_text, height=500)

            # Tombol buat surat
            if st.button("📝 Buat dan Unduh Semua Surat"):
                with st.spinner("Membuat semua surat..."):
                    hasil_zip = generate_zip(template_bytes, data_rows)

                st.download_button(
                    label="📦 Download Semua Surat (.zip)",
                    data=hasil_zip,
                    file_name="semua_surat_kontrak.zip",
                    mime="application/zip"
                )
