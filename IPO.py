import streamlit as st
import pandas as pd
from io import BytesIO
from datetime import date

st.set_page_config(page_title="Input Data Perusahaan", layout="centered")

st.title("Form Input Data Perusahaan")

# Inisialisasi session_state untuk menyimpan banyak data
if "data_perusahaan" not in st.session_state:
    st.session_state.data_perusahaan = []

# Form input
with st.form("form_perusahaan"):
    nama = st.text_input("Nama Perusahaan")
    direktur = st.text_input("Direktur Utama")
    bidang = st.text_input("Bidang Perusahaan")
    tanggal = st.date_input("Tanggal Perusahaan Berdiri", value=date.today())
    modal = st.number_input("Modal Tahun Berjalan (Rp)", min_value=0, step=1)

    submitted = st.form_submit_button("Tambah Data")

    if submitted:
        st.session_state.data_perusahaan.append({
            "Nama Perusahaan": nama,
            "Direktur Utama": direktur,
            "Bidang Perusahaan": bidang,
            "Tanggal Berdiri": tanggal.strftime("%d-%m-%Y"),
            "Modal (Rp)": f"{modal:,.0f}".replace(",", ".")
        })
        st.success("✅ Data berhasil ditambahkan!")

# Tampilkan tabel data
if st.session_state.data_perusahaan:
    df = pd.DataFrame(st.session_state.data_perusahaan)
    st.subheader("📊 Data Perusahaan Terkumpul")
    st.dataframe(df, use_container_width=True)

    # Export ke Excel
    output = BytesIO()
    with pd.ExcelWriter(output, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Data Perusahaan")
    output.seek(0)

    st.download_button(
        label="📥 Unduh Excel",
        data=output,
        file_name="Data_Perusahaan_Terkumpul.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("Belum ada data perusahaan yang dimasukkan.")

