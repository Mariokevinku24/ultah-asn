import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import datetime

# Judul aplikasi
st.title("Form Input Data Perusahaan ke Excel")

# Form input
nama_perusahaan = st.text_input("Nama Perusahaan")
direktur_utama = st.text_input("Direktur Utama")
bidang_perusahaan = st.text_input("Bidang Perusahaan")
tanggal_berdiri = st.date_input("Tanggal Perusahaan Berdiri")
modal_tahun_berjalan = st.number_input("Modal Tahun Berjalan (Rp)", min_value=0)

# Tombol Simpan
if st.button("Simpan ke Excel"):
    # Buat DataFrame dari input
    data = {
        "Nama Perusahaan": [nama_perusahaan],
        "Direktur Utama": [direktur_utama],
        "Bidang Perusahaan": [bidang_perusahaan],
        "Tanggal Berdiri": [tanggal_berdiri.strftime("%d-%m-%Y")],
        "Modal Tahun Berjalan (Rp)": [modal_tahun_berjalan]
    }
    df = pd.DataFrame(data)

    # Simpan ke Excel di memori
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name="Data Perusahaan")
    output.seek(0)

    # Unduh file Excel
    st.download_button(
        label="📥 Unduh File Excel",
        data=output,
        file_name=f"Data_Perusahaan_{nama_perusahaan.replace(' ', '_')}.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
