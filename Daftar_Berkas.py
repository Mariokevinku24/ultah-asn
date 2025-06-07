import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO

st.set_page_config(page_title="Daftar Arsip & Berkas", layout="wide")
st.title("📁 Aplikasi Daftar Arsip dan Isi Berkas")

# Upload file Excel (opsional)
uploaded_file = st.file_uploader("📥 Upload Excel Daftar Berkas", type="xlsx")

# Contoh template form input
columns_form = [
    "Nomor Berkas", "Kode Klasifikasi", "Unit Pengolah", "Uraian Berkas",
    "Tahun", "Tingkat Perkembangan", "Jumlah", "Lokasi Simpan", "Status", "Keterangan"
]

# Jika file di-upload
if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.success("📄 File berhasil dibaca")
else:
    st.info("📌 Atau isi data daftar berkas secara manual di bawah ini")
    df = pd.DataFrame(columns=columns_form)
    new_row = {}
    for col in columns_form:
        new_row[col] = st.text_input(f"{col}", value="")

    if st.button("➕ Tambahkan ke Daftar"):
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)

# Tampilkan tabel
st.subheader("📋 Data Daftar Berkas")
edited_df = st.data_editor(df, num_rows="dynamic")

# Input identitas umum
st.subheader("🧾 Informasi Umum")
satker = st.text_input("Satuan Kerja", "Dinas Lingkungan Hidup")
unit_pengolah = st.text_input("Unit Pengolah", "Sekretariat")

# Upload template Word
template_file = st.file_uploader("📄 Upload Template Word Daftar Berkas", type="docx")

# Generate Word
if st.button("📄 Buat Dokumen Word"):
    if template_file is None:
        st.warning("Harap upload template Word terlebih dahulu.")
    else:
        context = {
            "Satuan_Kerja": satker,
            "Unit_Pengolah": unit_pengolah,
            "daftar_berkas": edited_df.to_dict(orient="records")
        }

        tpl = DocxTemplate(template_file)
        tpl.render(context)

        doc_io = BytesIO()
        tpl.save(doc_io)
        doc_io.seek(0)

        st.download_button(
            label="📥 Download Dokumen Word",
            data=doc_io,
            file_name="daftar_berkas.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )
