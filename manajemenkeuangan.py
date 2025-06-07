import streamlit as st
import pandas as pd
import os
from datetime import date
from io import BytesIO

FILE_PATH = "catatan_keuangan.xlsx"
SHEET_NAME = "Keuangan"

st.set_page_config(page_title="Manajemen Keuangan", layout="centered")
st.title("💰 Manajemen Keuangan Pribadi")

# Fungsi untuk memuat data
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
    else:
        return pd.DataFrame(columns=["Tanggal", "Keterangan", "Jumlah", "Uang di Tabungan", "Uang di Tangan"])

# Fungsi untuk menyimpan data
def save_data(df):
    with pd.ExcelWriter(FILE_PATH, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET_NAME)

# === FORM INPUT ===
st.subheader("➕ Tambah Pengeluaran")
with st.form("form_pengeluaran"):
    keterangan = st.text_input("Keterangan")
    jumlah = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0)
    tunai = st.number_input("Uang Disimpan di Tangan (Rp)", min_value=0)
    tanggal = st.date_input("Tanggal", value=date.today())
    simpan = st.form_submit_button("Simpan")

    if simpan and (jumlah > 0 or tunai > 0):
        tabungan = jumlah - tunai
        if tabungan < 0:
            tabungan = 0

        new_row = pd.DataFrame([{
            "Tanggal": tanggal,
            "Keterangan": keterangan,
            "Jumlah": jumlah,
            "Uang di Tabungan": tabungan,
            "Uang di Tangan": tunai
        }])

        df = load_data()
        df = pd.concat([df, new_row], ignore_index=True)
        save_data(df)
        st.success("✅ Data berhasil disimpan!")

# === TAMPILKAN DATA ===
if os.path.exists(FILE_PATH):
    st.subheader("📋 Riwayat Pengeluaran")
    df = load_data()
    st.dataframe(df, use_container_width=True)

    # Ringkasan
    st.subheader("📊 Ringkasan")
    total_pengeluaran = df["Jumlah"].sum()
    total_tabungan = df["Uang di Tabungan"].sum()
    total_tunai = df["Uang di Tangan"].sum()

    col1, col2, col3 = st.columns(3)
    col1.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    col2.metric("Total Tabungan", f"Rp {total_tabungan:,.0f}")
    col3.metric("Total Tunai", f"Rp {total_tunai:,.0f}")

    # Download
    st.subheader("⬇️ Unduh Data")
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    output.seek(0)

    st.download_button(
        label="📥 Unduh Rekap Excel",
        data=output,
        file_name=FILE_PATH,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

    # === HAPUS DATA ===
    with st.expander("🗑️ Hapus Pengeluaran"):
        st.markdown("Centang data yang ingin dihapus:")
        rows_to_delete = []
        for i, row in df.iterrows():
            label = f"{row['Tanggal']} - {row['Keterangan']} - Rp{row['Jumlah']:,.0f}"
            if st.checkbox(label, key=f"hapus_{i}"):
                rows_to_delete.append(i)

        if st.button("🗑️ Hapus Data Terpilih"):
            if rows_to_delete:
                df = df.drop(index=rows_to_delete).reset_index(drop=True)
                save_data(df)
                st.success(f"✅ {len(rows_to_delete)} data berhasil dihapus!")
                st.experimental_rerun()
            else:
                st.warning("⚠️ Belum ada data yang dipilih untuk dihapus.")
else:
    st.info("📂 Belum ada data keuangan.")

