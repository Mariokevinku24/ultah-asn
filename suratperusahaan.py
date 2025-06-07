pip install python-docx
import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# Fungsi mengganti placeholder di template
def generate_surat(template_path, nama_perusahaan_list):
    # Load template
    doc_template = Document(template_path)
    
    # Simpan semua surat ke satu dokumen baru
    final_doc = Document()

    for nama in nama_perusahaan_list:
        # Clone isi template untuk setiap perusahaan
        temp_doc = Document(template_path)
        for para in temp_doc.paragraphs:
            if "{{Nama_Perusahaan}}" in para.text:
                para.text = para.text.replace("{{Nama_Perusahaan}}", nama)

        # Tambahkan ke dokumen akhir
        for element in temp_doc.element.body:
            final_doc.element.body.append(element)
        
        # Tambahkan page break jika bukan yang terakhir
        final_doc.add_page_break()

    return final_doc

st.title("Generator Surat CSR per Perusahaan")

# Upload file Excel
uploaded_excel = st.file_uploader("Upload file Excel dengan daftar perusahaan", type=['xlsx'])

# Upload template Word
uploaded_template = st.file_uploader("Upload Template Surat (.docx)", type=['docx'])

if uploaded_excel and uploaded_template:
    df = pd.read_excel(uploaded_excel)
    
    # Asumsikan kolom pertama berisi nama perusahaan
    nama_kolom = df.columns[0]
    daftar_perusahaan = df[nama_kolom].dropna().tolist()

    if st.button("Buat Surat"):
        hasil_doc = generate_surat(uploaded_template, daftar_perusahaan)

        buffer = BytesIO()
        hasil_doc.save(buffer)
        buffer.seek(0)

        st.download_button(
            label="Download File Word",
            data=buffer,
            file_name="surat_perusahaan_CSR.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
