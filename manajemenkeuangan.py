import streamlit as st
import pandas as pd
import datetime
import os

# Nama file untuk menyimpan data
FILE_PATH = "catatan_keuangan.xlsx"

# Fungsi: Load data dari file Excel, atau buat file jika belum ada
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        df = pd.DataFrame(columns=["Tanggal", "Keterangan", "Jumlah"])
        df.to_excel(FILE_PATH, index=False)
        return df

# Fungsi: Simpan DataFrame ke file Excel
def save_data(df):
    df.to_excel(FILE_PATH, index=False)

# Judul aplikasi
st.title("💰 Aplikasi Manajemen Keuangan Pribadi")

# Sidebar untuk input saldo awal
st.sidebar.header("Set Saldo Awal")
if "saldo_awal" not in st.session_state:
    st.session_state["saldo_awal"] = 0

saldo_awal = st.sidebar.number_input(
    "Masukkan saldo awal (Rp)", min_value=0, value=st.session_state["saldo_awal"]
)
st.session_state["saldo_awal"] = saldo_awal

# Load data
data = load_data()

# Form untuk input pengeluaran
st.subheader("📝 Catat Pengeluaran Harian")
with st.form("form_pengeluaran"):
    keterangan = st.text_input("Keterangan", placeholder="Contoh: Makan siang")
    jumlah = st.number_input("Jumlah (Rp)", min_value=0)
    simpan = st.form_submit_button("Simpan Pengeluaran")

    if simpan and keterangan and jumlah > 0:
        new_row = {
            "Tanggal": datetime.date.today(),
            "Keterangan": keterangan,
            "Jumlah": jumlah
        }
        data = pd.concat([data, pd.DataFrame([new_row])], ignore_index=True)
        save_data(data)
        st.success("Pengeluaran berhasil dicatat!")

# Tampilkan pengeluaran hari ini
st.subheader("📅 Pengeluaran Hari Ini")
data["Tanggal"] = pd.to_datetime(data["Tanggal"]).dt.date
hari_ini = datetime.date.today()
pengeluaran_hari_ini = data[data["Tanggal"] == hari_ini]

if not pengeluaran_hari_ini.empty:
    st.table(pengeluaran_hari_ini[["Keterangan", "Jumlah"]])
else:
    st.info("Belum ada pengeluaran hari ini.")

# Hitung total dan sisa saldo
total_pengeluaran = data["Jumlah"].sum()
sisa_saldo = saldo_awal - total_pengeluaran

# Tampilkan ringkasan
st.subheader("📊 Ringkasan")
st.write(f"**Saldo Awal:** Rp {saldo_awal:,.0f}")
st.write(f"**Total Pengeluaran:** Rp {total_pengeluaran:,.0f}")
st.write(f"**Sisa Saldo:** Rp {sisa_saldo:,.0f}")

# Tombol download Excel
st.subheader("⬇️ Unduh Rekap Keuangan")
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "rb") as f:
        st.download_button("Download Excel", f, file_name="rekap_keuangan.xlsx")
else:
    st.info("Belum ada data untuk diunduh.")
