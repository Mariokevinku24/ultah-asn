import streamlit as st
import pandas as pd
import os
from datetime import date

EXCEL_FILE = "data_perusahaan.xlsx"
SHEET_NAME = "Data Perusahaan"

st.set_page_config(page_title="Input ke Excel Eksisting", layout="centered")
st.title("Form Input Data Perusahaan ke Excel")

# Input form
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

        # Cek apakah file sudah ada
        if os.path.exists(EXCEL_FILE):
            existing_data = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
            combined_data = pd.concat([existing_data, new_data], ignore_index=True)
        else:
            combined_data = new_data

        # Simpan ke Excel
        with pd.ExcelWriter(EXCEL_FILE, engine="openpyxl", mode="w") as writer:
            combined_data.to_excel(writer, index=False, sheet_name=SHEET_NAME)

        st.success(f"✅ Data berhasil ditambahkan ke '{EXCEL_FILE}'.")

# Tampilkan isi file jika sudah ada
if os.path.exists(EXCEL_FILE):
    st.subheader("📁 Isi Excel Saat Ini")
    current_df = pd.read_excel(EXCEL_FILE, sheet_name=SHEET_NAME)
    st.dataframe(current_df, use_container_width=True)
