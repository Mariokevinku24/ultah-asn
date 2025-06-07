import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO
import zipfile
import mammoth  # Untuk preview surat sebagai HTML

st.title("Generator Banyak Surat CSR (ZIP + Preview)")

# Upload file
excel_file = st.file_uploader("Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("Upload Template Surat (Word .docx)", type="docx")

# Fungsi untuk generate ZIP
def generate_zip(template_file, data_rows):
    zip_buffer = BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:
            tpl = DocxTemplate(template_file)

            context = {
                "Nama_Perusahaan": row.get("Nama_Perusahaan", ""),
                "Nama_Direktur": row.get("Nama_Direktur", ""),
                "Jabatan_Direktur": row.get("Jabatan_Direktur", ""),
                "Kegiatan": row.get("Kegiatan", ""),
                "Lokasi": row.get("Lokasi", ""),
                "Jumlah_Sumbangan": row.get("Jumlah_Sumbangan", ""),
                "Jenis_Barang": row.get("Jenis_Barang", "")
            }

            try:
                tpl.render(context)
            except Exception as e:
                st.error(f"Gagal memproses surat untuk {context['Nama_Perusahaan']}: {e}")
                continue

            doc_io = BytesIO()
            tpl.save(doc_io)
            doc_io.seek(0)

            safe_nama = context["Nama_Perusahaan"].replace("/", "-").replace("\\", "-")
            filename = f"Surat_{safe_nama}.docx"
            zip_file.writestr(filename, doc_io.read())

    zip_buffer.seek(0)
    return zip_buffer

# Fungsi preview surat pertama sebagai HTML
def preview_surat_html(template_file, data):
    tpl = DocxTemplate(template_file)
    tpl.render(data)

    doc_io = BytesIO()
    tpl.save(doc_io)
    doc_io.seek(0)

    result = mammoth.convert_to_html(doc_io)
    return result.value

# Logika utama aplikasi
if excel_file and template_file:
    df = pd.read_excel(excel_file)
    df = df.fillna("")

    # Cek apakah semua kolom yang dibutuhkan ada
    required_columns = {"Nama_Perusahaan", "Nama_Direktur", "Jabatan_Direktur", "Kegiatan", "Lokasi", "Jumlah_Sumbangan", "Jenis_Barang"}
    if not required_columns.issubset(set(df.columns)):
        st.error(f"Kolom wajib tidak lengkap. Harus ada: {', '.join(required_columns)}")
    else:
        df_valid = df[df["Nama_Perusahaan"].str.strip() != ""]

        if df_valid.empty:
            st.error("Tidak ada data perusahaan yang valid. Kolom 'Nama_Perusahaan' wajib diisi.")
        else:
            data_rows = df_valid.to_dict(orient="records")

            st.write("✅ Ditemukan data untuk:", len(data_rows), "perusahaan.")
            st.dataframe(df_valid)

            # Tombol preview surat pertama
            if st.button("Preview Surat Pertama"):
                html_preview = preview_surat_html(template_file, data_rows[0])
                st.subheader("Preview Surat (Perusahaan Pertama):")
                st.markdown(html_preview, unsafe_allow_html=True)

            # Tombol buat surat & unduh ZIP
            if st.button("Buat Surat"):
                hasil_zip = generate_zip(template_file, data_rows)

                st.download_button(
                    label="Download Semua Surat (.zip)",
                    data=hasil_zip,
                    file_name="semua_surat_csr.zip",
                    mime="application/zip"
                )
