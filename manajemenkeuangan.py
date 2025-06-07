import streamlit as st
import pandas as pd
import os
from io import BytesIO
from datetime import date

FILE_PATH = "catatan_keuangan.xlsx"
SHEET_NAME = "Data Keuangan"

# Atur halaman
st.set_page_config(page_title="Manajemen Keuangan", layout="centered")
st.title("💰 Aplikasi Manajemen Keuangan")

# Fungsi untuk load data
def load_data():
    if os.path.exists(FILE_PATH):
        try:
            df = pd.read_excel(FILE_PATH, sheet_name=SHEET_NAME)
        except Exception:
            df = pd.DataFrame(columns=["Tanggal", "Keterangan", "Jumlah", "Uang di Tabungan", "Uang di Tangan"])
    else:
        df = pd.DataFrame(columns=["Tanggal", "Keterangan", "Jumlah", "Uang di Tabungan", "Uang di Tangan"])
        with pd.ExcelWriter(FILE_PATH, engine="openpyxl") as writer:
            df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    return df

# Fungsi untuk simpan data
def save_data(df):
    with pd.ExcelWriter(FILE_PATH, engine="openpyxl", mode="w") as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET_NAME)

# Form Input
st.subheader("📝 Tambah Catatan Keuangan")
with st.form("form_input"):
    tanggal = st.date_input("Tanggal", value=date.today())
    keterangan = st.text_input("Keterangan")
    jumlah = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0, step=1)
    uang_di_tangan = st.number_input("Uang Disimpan di Tangan (Rp)", min_value=0, step=1)

    submitted = st.form_submit_button("💾 Simpan")

    if submitted and (jumlah > 0 or uang_di_tangan > 0):
        df = load_data()
        uang_di_tabungan = jumlah - uang_di_tangan
        uang_di_tabungan = max(uang_di_tabungan, 0)  # pastikan tidak negatif

        new_data = pd.DataFrame([{
            "Tanggal": tanggal,
            "Keterangan": keterangan,
            "Jumlah": jumlah,
            "Uang di Tabungan": uang_di_tabungan,
            "Uang di Tangan": uang_di_tangan
        }])

        df = pd.concat([df, new_data], ignore_index=True)
        save_data(df)
        st.success("✅ Data berhasil disimpan!")
        st.experimental_rerun()

# Tampilkan data
df = load_data()

if not df.empty:
    st.subheader("📋 Data Tersimpan")
    st.dataframe(df, use_container_width=True)

    # Ringkasan
    st.subheader("📊 Ringkasan")
    total_pengeluaran = df["Jumlah"].sum()
    total_tabungan = df["Uang di Tabungan"].sum()
    total_tunai = df["Uang di Tangan"].sum()
    st.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    st.metric("Total di Tabungan", f"Rp {total_tabungan:,.0f}")
    st.metric("Total di Tangan", f"Rp {total_tunai:,.0f}")

    # Hapus data
    with st.expander("🗑️ Hapus Catatan"):
        st.markdown("Centang baris yang ingin dihapus:")
        rows_to_delete = []
        for i, row in df.iterrows():
            label = f"{row['Tanggal']} - {row['Keterangan']} - Rp {row['Jumlah']:,.0f}"
            if st.checkbox(label, key=f"hapus_{i}"):
                rows_to_delete.append(i)

        if st.button("Hapus Terpilih"):
            if rows_to_delete:
                df = df.drop(index=rows_to_delete).reset_index(drop=True)
                save_data(df)
                st.success(f"✅ {len(rows_to_delete)} data berhasil dihapus.")
                st.experimental_rerun()
            else:
                st.warning("⚠️ Belum ada yang dipilih.")

    # Download
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name=SHEET_NAME)
    output.seek(0)
    st.download_button(
        label="⬇️ Download Excel",
        data=output,
        file_name=FILE_PATH,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
else:
    st.info("📂 Belum ada data yang disimpan.")
