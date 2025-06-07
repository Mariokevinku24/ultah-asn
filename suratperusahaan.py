import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO
import zipfile

st.title("Generator Banyak Surat CSR (ZIP)")

excel_file = st.file_uploader("Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("Upload Template Surat (Word .docx)", type="docx")

def generate_zip(template_file, perusahaan_list):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for nama in perusahaan_list:
            tpl = DocxTemplate(template_file)
            context = {"Nama_Perusahaan": nama}
            tpl.render(context)

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            filename = f"Surat_{nama}.docx"
            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer

if excel_file and template_file:
    df = pd.read_excel(excel_file)
    nama_perusahaan = df.iloc[:, 0].dropna().tolist()

    if st.button("Buat Surat"):
        hasil_zip = generate_zip(template_file, nama_perusahaan)

        st.download_button("Download Semua Surat (.zip)", hasil_zip, file_name="semua_surat.zip")
