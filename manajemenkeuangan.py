import streamlit as st
import pandas as pd
import datetime
import os
from openpyxl.styles import numbers

FILE_PATH = "catatan_keuangan.xlsx"

# Fungsi untuk menyimpan dengan format tanggal
def save_data(df):
    with pd.ExcelWriter(FILE_PATH, engine='openpyxl') as writer:
        df.to_excel(writer, index=False)
        worksheet = writer.sheets['Sheet1']
        for cell in worksheet['A'][1:]:  # Format kolom tanggal
            cell.number_format = numbers.FORMAT_DATE_DDMMYYYY

# Fungsi untuk load dan validasi kolom
def load_data():
    kolom_default = ["Tanggal", "Keterangan", "Jumlah", "Uang di Tabungan", "Uang di Tangan"]
    if os.path.exists(FILE_PATH):
        df = pd.read_excel(FILE_PATH)
        for kolom in kolom_default:
            if kolom not in df.columns:
                df[kolom] = 0
        return df[kolom_default]
    else:
        df = pd.DataFrame(columns=kolom_default)
        save_data(df)
        return df

# Setup halaman & session
st.set_page_config(page_title="Manajemen Keuangan", layout="centered")
st.title("💰 Aplikasi Manajemen Keuangan Pribadi")

if "saldo_awal" not in st.session_state:
    st.session_state["saldo_awal"] = 0
if "hapus_index" not in st.session_state:
    st.session_state["hapus_index"] = None

# Sidebar saldo
st.sidebar.header("🔧 Pengaturan Awal")
saldo_awal = st.sidebar.number_input("Saldo Awal (Rp)", min_value=0, value=st.session_state["saldo_awal"])
st.session_state["saldo_awal"] = saldo_awal

# Form input
st.subheader("📝 Catat Pengeluaran")
with st.form("form_pengeluaran"):
    keterangan = st.text_input("Keterangan", placeholder="Contoh: Beli pulsa")
    jumlah = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0)
    tunai = st.number_input("Uang Disimpan di Tangan (Rp)", min_value=0)
    tanggal = st.date_input("Tanggal", value=datetime.date.today())
    submit = st.form_submit_button("💾 Simpan")

    if submit and (jumlah > 0 or tunai > 0):
        df = load_data()

        # Hitung tabungan: Saldo awal - jumlah - tunai
        total_pengeluaran = jumlah + tunai
        tabungan = max(saldo_awal - total_pengeluaran, 0)

        new_row = {
            "Tanggal": tanggal,
            "Keterangan": keterangan,
            "Jumlah": jumlah,
            "Uang di Tabungan": tabungan,
            "Uang di Tangan": tunai
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("✅ Data berhasil disimpan!")

# Load & konversi tanggal
df = load_data()
df["Tanggal"] = pd.to_datetime(df["Tanggal"]).dt.date

# Filter tanggal
st.subheader("📅 Lihat Pengeluaran per Tanggal")
tanggal_filter = st.date_input("Pilih tanggal:", value=datetime.date.today())
filtered_data = df[df["Tanggal"] == tanggal_filter]

# Tampilkan data
st.markdown(f"### 📋 Data pada {tanggal_filter.strftime('%d %B %Y')}")
if not filtered_data.empty:
    for idx, row in filtered_data.iterrows():
        st.markdown(f"""
        **{row['Keterangan']}**
        - Jumlah: Rp {row['Jumlah']:,.0f}
        - Tabungan: Rp {row['Uang di Tabungan']:,.0f}
        - Tunai: Rp {row['Uang di Tangan']:,.0f}
        """)
        if st.button("🗑 Hapus", key=f"hapus_{idx}"):
            st.session_state["hapus_index"] = df.index[df["Tanggal"] == tanggal_filter][idx]
            st.experimental_rerun()
else:
    st.info("Belum ada data untuk tanggal tersebut.")

# Hapus data
if st.session_state.get("hapus_index") is not None:
    df = df.drop(index=st.session_state["hapus_index"])
    df.reset_index(drop=True, inplace=True)
    save_data(df)
    st.session_state["hapus_index"] = None
    st.success("✅ Data berhasil dihapus.")
    st.experimental_rerun()

# Ringkasan
st.subheader("📊 Ringkasan Total")
total_pengeluaran = df["Jumlah"].sum()
total_tabungan = df["Uang di Tabungan"].sum()
total_tunai = df["Uang di Tangan"].sum()
sisa_saldo = saldo_awal - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col2.metric("Total Tabungan", f"Rp {total_tabungan:,.0f}")
col3.metric("Total Tunai", f"Rp {total_tunai:,.0f}")

st.success(f"💡 Sisa Saldo: Rp {sisa_saldo:,.0f}")

# Tombol unduh
st.subheader("⬇️ Unduh Rekap Keuangan")
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "rb") as f:
        st.download_button("📥 Download Excel", f, file_name="rekap_keuangan.xlsx")
else:
    st.info("Belum ada data untuk diunduh.")

