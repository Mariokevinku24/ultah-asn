import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import date

EXCEL_FILE = "data_perusahaan.xlsx"
SHEET_NAME = "Data Perusahaan"

st.set_page_config(page_title="Input ke Excel + Download", layout="centered")
st.title("Form Input Data Perusahaan ke Excel")

# Form input
with st.form("form_perusahaan"):
    nama = st.text_input("Nama Perusahaan")
    direktur = st.text_input("Direktur Utama")
    bidang = st.text_input("Bidang Perusahaan")
    tanggal = st.date_input("Tanggal Perusahaan Berdiri", value=date.today())
    modal = st.number_input("Modal Tahun Berjalan (Rp)", min_value=0, step=1)

    submitted = st.form_submit_button("Simpan ke Excel")

    if submitted:
        # Data baru yang akan ditambahkan
        new_data = pd.DataFrame([{
            "Nama Perusahaan": nama,
            "Direktur Utama": direktur,
            "Bidang Perusahaan": bidang,
            "Tanggal Berdiri": tanggal.strftime("%d-%m-%Y"),
            "Modal (Rp)": f"{modal:,.0f}".replace(",", ".")
        }])

        # Cek apakah file Excel sudah ada
        if os.path.exists(EXCEL_FILE):
            existing_data = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            combined_data = new_data

        # Simpan gabungan ke Excel
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
            combined_data.to_excel(writer, index=False, sheet_name=SHEET_NAME)

        st.success("✅ Data berhasil ditambahkan ke Excel!")

# Tampilkan isi Excel saat ini jika ada
if os.path.exists(EXCEL_FILE):
    st.subheader("📁 Isi Excel Saat Ini")
    current_df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    st.dataframe(current_df, use_container_width=True)

    # Siapkan file untuk diunduh
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        current_df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    output.seek(0)

    st.download_button(
        label="📥 Unduh Excel Terbaru",
        data=output,
        file_name=EXCEL_FILE,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📂 Belum ada data disimpan ke Excel.")
