import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from docx import Document
from io import BytesIO
import zipfile
import re


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
    "Membuat satu file Word untuk setiap petugas keamanan "
    "dan menggabungkan seluruh file ke dalam satu file ZIP."
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
# MEMBERSIHKAN NILAI DATA
# =========================================================
def clean_value(value):
    if value is None:
        return ""

    if pd.isna(value):
        return ""

    value = str(value).strip()

    # Menghilangkan .0 dari angka Excel
    if value.endswith(".0"):
        try:
            return str(int(float(value)))
        except ValueError:
            pass

    return value


# =========================================================
# MEMBERSIHKAN NAMA FILE
# =========================================================
def clean_filename(value):
    value = clean_value(value)

    # Karakter yang tidak boleh ada pada nama file
    value = re.sub(
        r'[\\/:*?"<>|]',
        "",
        value
    )

    # Ganti spasi berulang menjadi underscore
    value = re.sub(
        r"\s+",
        "_",
        value
    )

    return value.strip("_")


# =========================================================
# CONTEXT TEMPLATE
# =========================================================
def create_context(row):
    return {
        "NOMOR": clean_value(
            row.get("NOMOR", "")
        ),
        "NAMA": clean_value(
            row.get("NAMA", "")
        ),
        "NIK": clean_value(
            row.get("NIK", "")
        ),
        "TTL": clean_value(
            row.get("TTL", "")
        ),
        "PENDIDIKAN": clean_value(
            row.get("PENDIDIKAN", "")
        ),
        "ALAMAT": clean_value(
            row.get("ALAMAT", "")
        )
    }


# =========================================================
# GENERATE SATU FILE WORD
# =========================================================
def generate_one_docx(
    template_bytes,
    row
):
    tpl = DocxTemplate(
        BytesIO(template_bytes)
    )

    context = create_context(row)

    tpl.render(context)

    output = BytesIO()

    tpl.save(output)

    output.seek(0)

    return output


# =========================================================
# PREVIEW DOKUMEN
# =========================================================
def preview_document(
    template_bytes,
    row
):
    docx_stream = generate_one_docx(
        template_bytes,
        row
    )

    doc = Document(docx_stream)

    result = []

    # Paragraph biasa
    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()

        if text:
            result.append(text)

    # Isi tabel
    for table in doc.tables:
        for table_row in table.rows:

            cells = []

            for cell in table_row.cells:
                cell_text = (
                    cell.text.strip()
                )

                if cell_text:
                    cells.append(
                        cell_text
                    )

            if cells:
                result.append(
                    " | ".join(cells)
                )

    return "\n".join(result)


# =========================================================
# GENERATE ZIP
# =========================================================
def generate_zip(
    template_bytes,
    data_rows
):
    zip_buffer = BytesIO()

    with zipfile.ZipFile(
        zip_buffer,
        mode="w",
        compression=zipfile.ZIP_DEFLATED
    ) as zip_file:

        for index, row in enumerate(
            data_rows,
            start=1
        ):

            # Generate Word
            docx_file = generate_one_docx(
                template_bytes,
                row
            )

            nomor = clean_filename(
                row.get(
                    "NOMOR",
                    str(index)
                )
            )

            nama = clean_filename(
                row.get(
                    "NAMA",
                    "Tanpa_Nama"
                )
            )

            # Fallback apabila nomor kosong
            if not nomor:
                nomor = str(index).zfill(3)

            if not nama:
                nama = "Tanpa_Nama"

            file_name = (
                f"{nomor}_{nama}.docx"
            )

            zip_file.writestr(
                file_name,
                docx_file.getvalue()
            )

    zip_buffer.seek(0)

    return zip_buffer


# =========================================================
# LOGIKA UTAMA
# =========================================================
if (
    excel_file is not None
    and template_file is not None
):

    try:
        # =================================================
        # BACA EXCEL
        # =================================================
        df = pd.read_excel(
            excel_file,
            dtype=str
        ).fillna("")

        # Normalisasi nama kolom
        df.columns = [
            str(col)
            .strip()
            .upper()
            for col in df.columns
        ]


        # =================================================
        # VALIDASI KOLOM
        # =================================================
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
                "Kolom berikut tidak ditemukan "
                "di Excel: "
                + ", ".join(
                    missing_columns
                )
            )

            st.write(
                "Kolom yang ditemukan:"
            )

            st.code(
                "\n".join(
                    df.columns.tolist()
                )
            )

            st.stop()


        # =================================================
        # BERSIHKAN DATA
        # =================================================
        for col in required_columns:

            df[col] = (
                df[col]
                .astype(str)
                .str.strip()
            )


        # =================================================
        # FILTER DATA VALID
        # =================================================
        df_valid = df[
            df["NAMA"] != ""
        ].copy()

        if df_valid.empty:

            st.error(
                "Tidak ada data petugas "
                "yang valid."
            )

            st.stop()


        # =================================================
        # INFORMASI DATA
        # =================================================
        st.success(
            f"Berhasil membaca "
            f"{len(df_valid)} data petugas."
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


        # =================================================
        # TEMPLATE
        # =================================================
        template_bytes = (
            template_file.getvalue()
        )

        data_rows = (
            df_valid
            .to_dict(
                orient="records"
            )
        )


        # =================================================
        # PREVIEW
        # =================================================
        st.divider()

        st.subheader(
            "👁️ Preview Perjanjian Pertama"
        )

        try:

            preview_text = (
                preview_document(
                    template_bytes,
                    data_rows[0]
                )
            )

            st.text_area(
                "Preview Isi Dokumen",
                value=preview_text,
                height=500,
                disabled=True
            )

        except Exception as preview_error:

            st.warning(
                "Preview tidak dapat "
                "ditampilkan."
            )

            st.code(
                str(preview_error)
            )


        # =================================================
        # DOWNLOAD SATU DOKUMEN CONTOH
        # =================================================
        st.divider()

        st.subheader(
            "📄 Download Dokumen Pertama"
        )

        first_doc = generate_one_docx(
            template_bytes,
            data_rows[0]
        )

        first_nomor = clean_filename(
            data_rows[0].get(
                "NOMOR",
                "001"
            )
        )

        first_nama = clean_filename(
            data_rows[0].get(
                "NAMA",
                "Petugas"
            )
        )

        st.download_button(
            label=(
                "📄 Download "
                "Perjanjian Pertama"
            ),
            data=first_doc.getvalue(),
            file_name=(
                f"{first_nomor}_"
                f"{first_nama}.docx"
            ),
            mime=(
                "application/vnd.openxmlformats-"
                "officedocument.wordprocessingml."
                "document"
            ),
            use_container_width=True
        )


        # =================================================
        # GENERATE ZIP
        # =================================================
        st.divider()

        st.subheader(
            "📦 Download Semua Dokumen"
        )

        with st.spinner(
            "Sedang membuat seluruh "
            "Perjanjian Kerja..."
        ):

            zip_file = generate_zip(
                template_bytes,
                data_rows
            )


        st.success(
            f"{len(df_valid)} file Word "
            "berhasil dibuat."
        )


        # =================================================
        # DOWNLOAD ZIP
        # =================================================
        st.download_button(
            label=(
                f"📦 Download ZIP "
                f"({len(df_valid)} Perjanjian)"
            ),
            data=zip_file.getvalue(),
            file_name=(
                "Perjanjian_Kerja_"
                "Petugas_Keamanan_DLH_2026.zip"
            ),
            mime="application/zip",
            use_container_width=True
        )


    except Exception as e:

        st.error(
            "Terjadi kesalahan saat "
            "memproses file."
        )

        st.code(
            str(e)
        )


# =========================================================
# PETUNJUK FORMAT
# =========================================================
st.divider()

with st.expander(
    "ℹ️ Petunjuk Format Excel dan Template"
):

    st.write(
        "Kolom Excel:"
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
        "Placeholder Word:"
    )

    st.code(
        "{{NOMOR}}\n"
        "{{NAMA}}\n"
        "{{NIK}}\n"
        "{{TTL}}\n"
        "{{PENDIDIKAN}}\n"
        "{{ALAMAT}}"
    )
