import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from docx import Document
from io import BytesIO
from copy import deepcopy


# =========================================================
# KONFIGURASI HALAMAN
# =========================================================
st.set_page_config(
    page_title="Generator Perjanjian Kerja Petugas Keamanan DLH",
    page_icon="📄",
    layout="wide"
)

st.title("📄 Generator Perjanjian Kerja Petugas Keamanan DLH")
st.caption(
    "Membuat seluruh Perjanjian Kerja Petugas Keamanan "
    "Dinas Lingkungan Hidup Kabupaten Deli Serdang "
    "dalam satu file Word."
)


# =========================================================
# UPLOAD FILE
# =========================================================
col1, col2 = st.columns(2)

with col1:
    excel_file = st.file_uploader(
        "📊 Upload Excel Data Petugas",
        type=["xlsx"]
    )

with col2:
    template_file = st.file_uploader(
        "📄 Upload Template Perjanjian Kerja",
        type=["docx"]
    )


# =========================================================
# FUNGSI MEMBERSIHKAN NILAI
# =========================================================
def clean_value(value):
    if value is None:
        return ""

    if pd.isna(value):
        return ""

    value = str(value).strip()

    # Mencegah angka seperti 12345.0
    if value.endswith(".0"):
        try:
            return str(int(float(value)))
        except ValueError:
            pass

    return value


# =========================================================
# MEMBUAT CONTEXT UNTUK TEMPLATE WORD
# =========================================================
def create_context(row):
    return {
        "NOMOR": clean_value(row.get("NOMOR", "")),
        "NAMA": clean_value(row.get("NAMA", "")),
        "NIK": clean_value(row.get("NIK", "")),
        "TTL": clean_value(row.get("TTL", "")),
        "PENDIDIKAN": clean_value(row.get("PENDIDIKAN", "")),
        "ALAMAT": clean_value(row.get("ALAMAT", ""))
    }


# =========================================================
# RENDER SATU DOKUMEN
# =========================================================
def render_one_document(template_bytes, row):
    tpl = DocxTemplate(BytesIO(template_bytes))

    context = create_context(row)

    tpl.render(context)

    output = BytesIO()
    tpl.save(output)
    output.seek(0)

    return output


# =========================================================
# MERGE SEMUA DOKUMEN
# =========================================================
def merge_documents(document_streams):
    if not document_streams:
        return None

    # Gunakan dokumen pertama sebagai dokumen utama
    main_doc = Document(document_streams[0])

    # Tambahkan dokumen berikutnya
    for doc_stream in document_streams[1:]:
        main_doc.add_page_break()

        sub_doc = Document(doc_stream)

        for element in sub_doc.element.body:
            # Hindari duplikasi section properties
            if element.tag.endswith("sectPr"):
                continue

            main_doc.element.body.append(
                deepcopy(element)
            )

    output = BytesIO()
    main_doc.save(output)
    output.seek(0)

    return output


# =========================================================
# GENERATE SEMUA PERJANJIAN
# =========================================================
def generate_all_documents(template_bytes, data_rows):
    rendered_documents = []

    for row in data_rows:
        rendered = render_one_document(
            template_bytes,
            row
        )

        rendered_documents.append(rendered)

    return merge_documents(rendered_documents)


# =========================================================
# PREVIEW TEXT
# =========================================================
def preview_document(template_bytes, row):
    rendered = render_one_document(
        template_bytes,
        row
    )

    doc = Document(rendered)

    result = []

    # Ambil paragraf
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text:
            result.append(text)

    # Ambil isi tabel
    for table in doc.tables:
        for table_row in table.rows:
            cells = []

            for cell in table_row.cells:
                cell_text = cell.text.strip()

                if cell_text:
                    cells.append(cell_text)

            if cells:
                result.append(
                    " | ".join(cells)
                )

    return "\n".join(result)


# =========================================================
# LOGIKA UTAMA
# =========================================================
if excel_file is not None and template_file is not None:

    try:
        # -------------------------------------------------
        # MEMBACA EXCEL
        # -------------------------------------------------
        df = pd.read_excel(
            excel_file,
            dtype=str
        ).fillna("")

        # Normalisasi nama kolom
        df.columns = [
            str(col).strip().upper()
            for col in df.columns
        ]

        # -------------------------------------------------
        # KOLOM WAJIB
        # -------------------------------------------------
        required_columns = [
            "NOMOR",
            "NAMA",
            "NIK",
            "TTL",
            "PENDIDIKAN",
            "ALAMAT"
        ]

        missing_columns = [
            col
            for col in required_columns
            if col not in df.columns
        ]

        if missing_columns:
            st.error(
                "Kolom berikut tidak ditemukan di Excel: "
                + ", ".join(missing_columns)
            )

            st.info(
                "Pastikan nama kolom Excel sama persis dengan format yang diperlukan."
            )

            st.write("Kolom yang ditemukan:")

            st.code(
                "\n".join(df.columns.tolist())
            )

            st.stop()

        # -------------------------------------------------
        # MEMBERSIHKAN DATA
        # -------------------------------------------------
        for col in required_columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )

        # -------------------------------------------------
        # FILTER BARIS VALID
        # -------------------------------------------------
        df_valid = df[
            df["NAMA"] != ""
        ].copy()

        if df_valid.empty:
            st.error(
                "Tidak ada data petugas yang valid. "
                "Kolom NAMA tidak boleh kosong."
            )
            st.stop()

        # -------------------------------------------------
        # TAMPILKAN DATA
        # -------------------------------------------------
        st.success(
            f"Berhasil membaca {len(df_valid)} data petugas."
        )

        with st.expander(
            "👥 Lihat Data Petugas"
        ):
            st.dataframe(
                df_valid[
                    required_columns
                ],
                use_container_width=True,
                hide_index=True
            )

        # -------------------------------------------------
        # AMBIL TEMPLATE
        # -------------------------------------------------
        template_bytes = template_file.getvalue()

        data_rows = df_valid.to_dict(
            orient="records"
        )

        # -------------------------------------------------
        # PREVIEW DATA PERTAMA
        # -------------------------------------------------
        st.divider()

        st.subheader(
            "👁️ Preview Perjanjian Pertama"
        )

        try:
            preview_text = preview_document(
                template_bytes,
                data_rows[0]
            )

            st.text_area(
                "Preview Isi Dokumen",
                value=preview_text,
                height=550,
                disabled=True
            )

        except Exception as preview_error:
            st.warning(
                "Preview tidak dapat ditampilkan."
            )

            st.code(
                str(preview_error)
            )

        # -------------------------------------------------
        # GENERATE SEMUA DOKUMEN
        # -------------------------------------------------
        st.divider()

        st.subheader(
            "📥 Generate Dokumen"
        )

        with st.spinner(
            "Sedang membuat seluruh Perjanjian Kerja..."
        ):
            final_document = generate_all_documents(
                template_bytes,
                data_rows
            )

        # -------------------------------------------------
        # DOWNLOAD
        # -------------------------------------------------
        if final_document is not None:
            st.success(
                f"Dokumen berhasil dibuat untuk "
                f"{len(df_valid)} petugas."
            )

            st.download_button(
                label=(
                    f"📥 Download Semua Perjanjian "
                    f"({len(df_valid)} Petugas)"
                ),
                data=final_document.getvalue(),
                file_name=(
                    "Perjanjian_Kerja_Petugas_"
                    "Keamanan_DLH_2026.docx"
                ),
                mime=(
                    "application/vnd.openxmlformats-officedocument."
                    "wordprocessingml.document"
                ),
                use_container_width=True
            )

    except Exception as e:
        st.error(
            "Terjadi kesalahan saat memproses file."
        )

        st.code(
            str(e)
        )


# =========================================================
# PETUNJUK FORMAT
# =========================================================
st.divider()

with st.expander(
    "ℹ️ Petunjuk Format Excel dan Template Word"
):

    st.write(
        "Kolom Excel yang harus tersedia:"
    )

    st.code(
        "NOMOR\n"
        "NAMA\n"
        "NIK\n"
        "TTL\n"
        "PENDIDIKAN\n"
        "ALAMAT"
    )

    st.write(
        "Placeholder pada template Word:"
    )

    st.code(
        "{{NOMOR}}\n"
        "{{NAMA}}\n"
        "{{NIK}}\n"
        "{{TTL}}\n"
        "{{PENDIDIKAN}}\n"
        "{{ALAMAT}}"
    )

    st.write(
        "Contoh penggunaan dalam template Word:"
    )

    st.code(
        "NOMOR: {{NOMOR}} TAHUN 2026\n\n"
        "II. Nama            : {{NAMA}}\n"
        "    NIK             : {{NIK}}\n"
        "    Tempat/tgl lahir: {{TTL}}\n"
        "    Pendidikan      : {{PENDIDIKAN}}\n"
        "    Alamat          : {{ALAMAT}}"
    )
