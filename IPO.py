import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import date

EXCEL_FILE = "data_perusahaan.xlsx"
SHEET_NAME = "Data Perusahaan"

st.set_page_config(page_title="Input & Hapus Data Excel", layout="centered")
st.title("📝 Form Data Perusahaan")

# === FORM INPUT ===
with st.form("form_perusahaan"):
    st.subheader("➕ Tambah Data")
    nama = st.text_input("Nama Perusahaan")
    direktur = st.text_input("Direktur Utama")
    bidang = st.text_input("Bidang Perusahaan")
    tanggal = st.date_input("Tanggal Perusahaan Berdiri", value=date.today())
    modal = st.number_input("Modal Tahun Berjalan (Rp)", min_value=0, step=1)

    submitted = st.form_submit_button("Simpan ke Excel")

    if submitted:
        new_data = pd.DataFrame([{
            "Nama Perusahaan": nama,
            "Direktur Utama": direktur,
            "Bidang Perusahaan": bidang,
            "Tanggal Berdiri": tanggal.strftime("%d-%m-%Y"),
            "Modal (Rp)": f"{modal:,.0f}".replace(",", ".")
        }])

        if os.path.exists(EXCEL_FILE):
            existing_data = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            combined_data = new_data

        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
            combined_data.to_excel(writer, index=False, sheet_name=SHEET_NAME)

        st.success("✅ Data berhasil ditambahkan!")

# === TAMPILKAN DATA DAN DOWNLOAD ===
if os.path.exists(EXCEL_FILE):
    st.subheader("📋 Data Tersimpan")
    df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    st.dataframe(df, use_container_width=True)

    # Tombol Download Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    output.seek(0)

    st.download_button(
        label="📥 Unduh Excel Terbaru",
        data=output,
        file_name=EXCEL_FILE,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # === HAPUS DATA (pindah ke bawah) ===
    with st.expander("🗑️ Hapus Data Tidak Sesuai"):
        st.markdown("Centang data yang ingin dihapus:")
        rows_to_delete = []
        for i, row in df.iterrows():
            label = f"{row['Nama Perusahaan']} - {row['Direktur Utama']} - {row['Tanggal Berdiri']}"
            if st.checkbox(label, key=f"hapus_{i}"):
                rows_to_delete.append(i)

        if st.button("🗑️ Hapus Data Terpilih"):
            if rows_to_delete:
                df = df.drop(index=rows_to_delete).reset_index(drop=True)
                with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
                    df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
                st.success(f"✅ {len(rows_to_delete)} data berhasil dihapus!")
                st.experimental_rerun()
            else:
                st.warning("⚠️ Belum ada data yang dipilih untuk dihapus.")
else:
    st.info("📂 Belum ada data di Excel.")

