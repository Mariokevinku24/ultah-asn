import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from io import BytesIO
import zipfile
from num2words import num2words
import locale
from docx import Document

# Set locale ke Indonesia (tidak wajib)
try:
    locale.setlocale(locale.LC_ALL, 'id_ID.UTF-8')
except:
    pass

st.title("Generator Banyak Surat CSR (ZIP + Preview + Format Jumlah)")

# Upload file
excel_file = st.file_uploader("Upload Excel (daftar perusahaan)", type="xlsx")
template_file = st.file_uploader("Upload Template Surat (Word .docx)", type="docx")

# Fungsi untuk ubah DOCX ke teks (preview)
def docx_to_text(docx_bytes):
    doc = Document(docx_bytes)
    full_text = [para.text for para in doc.paragraphs]
    return "\n".join(full_text)

# Fungsi buat ZIP semua surat
def generate_zip(template_file, data_rows):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(zip_buffer, "w") as zip_file:
        for row in data_rows:
            tpl = DocxTemplate(template_file)

            jumlah = row.get("Jumlah_Sumbangan", 0)
            try:
                jumlah_float = float(jumlah)
            except:
                jumlah_float = 0.0

            jumlah_formatted = f"{jumlah_float:,.0f}".replace(",", ".")
            jumlah_terbilang = num2words(jumlah_float, lang='id').replace("koma nol", "").strip()

            context = {
                "Nama_Perusahaan": row.get("Nama_Perusahaan", ""),
                "Nama_Direktur": row.get("Nama_Direktur", ""),
                "Jabatan_Direktur": row.get("Jabatan_Direktur", ""),
                "Kegiatan": row.get("Kegiatan", ""),
                "Lokasi": row.get("Lokasi", ""),
                "Jumlah_Sumbangan": f"Rp. {jumlah_formatted},-",
                "Jumlah_Terbilang": jumlah_terbilang,
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

# Fungsi preview surat pertama sebagai teks
def preview_surat_text(template_file, data):
    tpl = DocxTemplate(template_file)

    jumlah = data.get("Jumlah_Sumbangan", 0)
    try:
        jumlah_float = float(jumlah)
    except:
        jumlah_float = 0.0

    jumlah_formatted = f"{jumlah_float:,.0f}".replace(",", ".")
    jumlah_terbilang = num2words(jumlah_float, lang='id').replace("koma nol", "").strip()

    context = {
        "Nama_Perusahaan": data.get("Nama_Perusahaan", ""),
        "Nama_Direktur": data.get("Nama_Direktur", ""),
        "Jabatan_Direktur": data.get("Jabatan_Direktur", ""),
        "Kegiatan": data.get("Kegiatan", ""),
        "Lokasi": data.get("Lokasi", ""),
        "Jumlah_Sumbangan": f"Rp. {jumlah_formatted},-",
        "Jumlah_Terbilang": jumlah_terbilang,
        "Jenis_Barang": data.get("Jenis_Barang", "")
    }

    tpl.render(context)
    doc_io = BytesIO()
    tpl.save(doc_io)
    doc_io.seek(0)
    return docx_to_text(doc_io)

# Logika utama
if excel_file and template_file:
    df = pd.read_excel(excel_file)
    df = df.fillna("")

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

            # Preview
            if st.button("Preview Surat Pertama"):
                preview_text = preview_surat_text(template_file, data_rows[0])
                st.subheader("📄 Preview Isi Surat Pertama:")
                st.text(preview_text)

            # Unduh
            if st.button("Buat Surat"):
                hasil_zip = generate_zip(template_file, data_rows)
                st.download_button(
                    label="Download Semua Surat (.zip)",
                    data=hasil_zip,
                    file_name="semua_surat_csr.zip",
                    mime="application/zip"
                )

