import streamlit as st
import pandas as pd
from docxtpl import DocxTemplate
from docx import Document
from io import BytesIO
from copy import deepcopy

st.set_page_config(
    page_title="Generator Perjanjian Kerja Petugas Keamanan DLH",
    page_icon="📄",
    layout="wide"
)

st.title("Generator Perjanjian Kerja Petugas Keamanan DLH")
st.caption(
    "Generator Perjanjian Kerja antara Kuasa Pengguna Anggaran "
    "Dinas Lingkungan Hidup Kabupaten Deli Serdang dengan "
    "Petugas Keamanan Kantor Tahun 2026"
)


# =========================================================
# UPLOAD FILE
# =========================================================

col1, col2 = st.columns(2)

with col1:
    excel_file = st.file_uploader(
        "📊 Upload Excel Data Petugas Keamanan",
        type=["xlsx"]
    )

with col2:
    template_file = st.file_uploader(
        "📄 Upload Template Perjanjian Kerja (.docx)",
        type=["docx"]
    )


# =========================================================
# MEMBERSIHKAN DATA
# =========================================================

def clean_value(value):
    """
    Membersihkan data hasil pembacaan Excel.
    """

    if pd.isna(value):
        return ""

    value = str(value).strip()

    # Menghilangkan .0 pada angka Excel
    # contoh NIK 1234567890.0
    if value.endswith(".0"):
        try:
            return str(int(float(value)))
        except ValueError:
            pass

    return value


# =========================================================
# MEMBUAT CONTEXT TEMPLATE WORD
# =========================================================

def create_context(row):
    """
    Mapping data Excel ke placeholder Word.

    Placeholder template:
    {{NOMOR}}
    {{NAMA}}
    {{NIK}}
    {{TTL}}
    {{PENDIDIKAN}}
    {{ALAMAT}}
    """

    return {
        "NOMOR": clean_value(row.get("NOMOR", "")),
        "NAMA": clean_value(row.get("NAMA", "")),
        "NIK": clean_value(row.get("NIK", "")),
        "TTL": clean_value(row.get("TTL", "")),
        "PENDIDIKAN": clean_value(row.get("PENDIDIKAN", "")),
        "ALAMAT": clean_value(row.get("ALAMAT", "")),
    }


# =========================================================
# MENGGABUNGKAN SEMUA SURAT
# =========================================================

def merge_documents(docs):
    """
    Menggabungkan hasil perjanjian kerja menjadi
    satu file Word.

    Setiap pegawai dimulai pada halaman baru.
    """

    if not docs:
        return None

    first_doc = Document(docs[0])

    for doc_stream in docs[1:]:

        # Halaman baru sebelum dokumen berikutnya
        first_doc.add_page_break()

        sub_doc = Document(doc_stream)

        for element in sub_doc.element.body:

            # sectPr tidak perlu dicopy karena dapat
            # menyebabkan section Word bertumpuk
            if element.tag.endswith("sectPr"):
                continue

            first_doc.element.body.append(
                deepcopy(element)
            )

    output = BytesIO()

    first_doc.save(output)

    output.seek(0)

    return output


# =========================================================
# MEMBUAT SELURUH PERJANJIAN
# =========================================================

def generate_single_docx(template_bytes, data_rows):

    rendered_docs = []

    for row in data_rows:

        tpl = DocxTemplate(
            BytesIO(template_bytes)
        )

        context = create_context(row)

        tpl.render(context)

        doc_io = BytesIO()

        tpl.save(doc_io)

        doc_io.seek(0)

        rendered_docs.append(
            BytesIO(doc_io.getvalue())
        )

    return merge_documents(rendered_docs)


# =========================================================
# PREVIEW TEXT
# =========================================================

def preview_docx_from_template(template_bytes, row):

    tpl = DocxTemplate(
        BytesIO(template_bytes)
    )

    context = create_context(row)

    tpl.render(context)

    temp = BytesIO()

    tpl.save(temp)

    temp.seek(0)

    doc = Document(temp)

    output_text = []

    # Paragraph biasa
    for paragraph in doc.paragraphs:

        if paragraph.text.strip():

            output_text.append(
                paragraph.text
            )


    # Isi tabel Word
    for table in doc.tables:

        for table_row in table.rows:

            cells = [
                cell.text.strip()
                for cell in table_row.cells
            ]

            if any(cells):

                output_text.append(
                    " | ".join(cells)
                )


    return "\n".join(output_text)


# =========================================================
# LOGIKA UTAMA
# =========================================================

if excel_file is not None and template_file is not None:

    try:

        # =================================================
        # BACA EXCEL
        # =================================================

        df = pd.read_excel(
            excel_file,
            dtype=str
        ).fillna("")


        # Bersihkan nama kolom
        df.columns = [
            str(col).strip().upper()
            for col in df.columns
        ]


        # =================================================
        # KOLOM WAJIB
        # =================================================

        required_columns = [
            "NOMOR",
            "NAMA",
            "NIK",
            "TTL",
            "PENDIDIKAN",
            "ALAMAT"
        ]


        missing_cols = [

            col

            for col in required_columns

            if col not in df.columns

        ]


        if missing_cols:

            st.error(
                "Kolom Excel berikut belum tersedia: "
                + ", ".join(missing_cols)
            )

            st.write(
                "Kolom yang ditemukan di Excel:"
            )

            st.code(
                "\n".join(df.columns.tolist())
            )

            st.stop()


        # =================================================
        # FILTER DATA VALID
        # =================================================

        df["NAMA"] = (
            df["NAMA"]
            .astype(str)
            .str.strip()
        )


        df_valid = df[
            df["NAMA"] != ""
        ].copy()


        if df_valid.empty:

            st.error(
                "Tidak terdapat data petugas keamanan "
                "yang valid."
            )

            st.stop()


        # =================================================
        # INFORMASI DATA
        # =================================================

        st.success(
            f"{len(df_valid)} data petugas keamanan "
            "berhasil dibaca."
        )


        with st.expander(
            "👥 Lihat Data Petugas Keamanan"
        ):

            st.dataframe(
                df_valid,
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
        # PREVIEW DATA PERTAMA
        # =================================================

        st.divider()

        st.subheader(
            "👁️ Preview Perjanjian Pertama"
        )


        try:

            preview_text = (
                preview_docx_from_template(
                    template_bytes,
                    data_rows[0]
                )
            )


            st.text_area(
                "Preview Isi Perjanjian",
                value=preview_text,
                height=600,
                disabled=True
            )


        except Exception as e:

            st.warning(
                f"Preview tidak dapat ditampilkan: {e}"
            )


        # =================================================
        # GENERATE FILE
        # =================================================

        st.divider()

        st.subheader(
            "📥 Download Perjanjian Kerja"
        )


        with st.spinner(
            "Sedang membuat semua perjanjian kerja..."
        ):

            final_doc = (
                generate_single_docx(
                    template_bytes,
                    data_rows
                )
            )


        if final_doc:

            st.download_button(
                label=(
                    f"📥 Download Semua Perjanjian "
                    f"({len(df_valid)} Petugas)"
                ),
                data=final_doc.getvalue(),
                file_name=(
                    "Perjanjian_Kerja_"
                    "Petugas_Keamanan_DLH_2026.docx"
                ),
                mime=(
                    "application/vnd.openxmlformats-"
                    "officedocument.wordprocessingml.document"
                ),
                use_container_width=True
            )


    except Exception as e:

        st.error(
            f"Terjadi kesalahan: {e}"
        )


# =========================================================
# PETUNJUK FORMAT EXCEL
# =========================================================

with st.expander(
    "ℹ️ Format Excel dan Placeholder Word"
):

    st.markdown(
        """
### Kolom Excel

File Excel harus memiliki kolom:

| NOMOR | NAMA | NIK | TTL | PENDIDIKAN | ALAMAT |
|---|---|---|---|---|---|
| 001 | Budi Santoso | 1271xxxxxxxxxxxx | Medan, 10 Januari 1990 | SMA | Deli Serdang |
| 002 | Andi Saputra | 1271xxxxxxxxxxxx | Lubuk Pakam, 5 Mei 1992 | SMA | Lubuk Pakam |

### Placeholder pada Word

Gunakan:

```text
{{NOMOR}}
{{NAMA}}
{{NIK}}
{{TTL}}
{{PENDIDIKAN}}
{{ALAMAT}}
