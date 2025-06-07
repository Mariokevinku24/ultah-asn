import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO

def generate_surat(template_path, nama_perusahaan_list):
    output_doc = BytesIO()
    combined_doc = None

    for i, nama in enumerate(nama_perusahaan_list):
        tpl = DocxTemplate(template_path)
        context = {"Nama_Perusahaan": nama}
        tpl.render(context)
        
        temp_stream = BytesIO()
        tpl.save(temp_stream)
        temp_stream.seek(0)

        # Tambahkan ke dokumen gabungan
        if combined_doc is None:
            combined_doc = DocxTemplate(temp_stream)
        else:
            doc = DocxTemplate(temp_stream)
            for element in doc.docx.element.body:
                combined_doc.docx.element.body.append(element)
            combined_doc.docx.element.body.append(doc.docx.element.body[-1])  # Optional: tambah pemisah

    combined_doc.save(output_doc)
    output_doc.seek(0)
    return output_doc

st.title("Generator Surat CSR Format Rapi")

excel_file = st.file_uploader("Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("Upload Template Surat (Word .docx)", type="docx")

if excel_file and template_file:
    df = pd.read_excel(excel_file)
    nama_perusahaan = df.iloc[:, 0].dropna().tolist()

    if st.button("Buat Surat"):
        hasil = generate_surat(template_file, nama_perusahaan)
        st.download_button("Download Surat Gabungan", hasil, file_name="surat_csr.docx")

