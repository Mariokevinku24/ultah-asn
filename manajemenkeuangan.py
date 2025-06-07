import streamlit as st
import pandas as pd
import datetime
import os

FILE_PATH = "catatan_keuangan.xlsx"

# Load atau buat file data
def load_data():
    if os.path.exists(FILE_PATH):
        return pd.read_excel(FILE_PATH)
    else:
        df = pd.DataFrame(columns=["Tanggal", "Keterangan", "Jumlah", "Uang di Tabungan", "Uang di Tangan"])
        df.to_excel(FILE_PATH, index=False)
        return df

def save_data(df):
    df.to_excel(FILE_PATH, index=False)

# Inisialisasi
st.title("💰 Aplikasi Manajemen Keuangan Pribadi (Lanjutan)")

if "saldo_awal" not in st.session_state:
    st.session_state["saldo_awal"] = 0

# Sidebar: Saldo Awal
st.sidebar.header("🔧 Pengaturan Awal")
saldo_awal = st.sidebar.number_input("Masukkan Saldo Awal (Rp)", min_value=0, value=st.session_state["saldo_awal"])
st.session_state["saldo_awal"] = saldo_awal

# Form input data pengeluaran
st.subheader("📝 Tambah Pengeluaran")
with st.form("form_pengeluaran"):
    keterangan = st.text_input("Keterangan", placeholder="Contoh: Bensin")
    jumlah = st.number_input("Jumlah Pengeluaran (Rp)", min_value=0)
    tabungan = st.number_input("Uang yang Masuk ke Tabungan (Rp)", min_value=0)
    tunai = st.number_input("Uang yang Disimpan di Tangan (Rp)", min_value=0)
    tanggal = st.date_input("Tanggal Pengeluaran", value=datetime.date.today())
    submit = st.form_submit_button("💾 Simpan")

    if submit and (jumlah > 0 or tabungan > 0 or tunai > 0):
        df = load_data()
        new_row = {
            "Tanggal": tanggal,
            "Keterangan": keterangan,
            "Jumlah": jumlah,
            "Uang di Tabungan": tabungan,
            "Uang di Tangan": tunai
        }
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        save_data(df)
        st.success("Data berhasil ditambahkan!")

# Load data & konversi tanggal
df = load_data()
df["Tanggal"] = pd.to_datetime(df["Tanggal"]).dt.date

# Kalender filter
st.subheader("📅 Pilih Tanggal untuk Ditampilkan")
tanggal_filter = st.date_input("Filter tanggal:", value=datetime.date.today())
filtered_data = df[df["Tanggal"] == tanggal_filter]

# Tabel pengeluaran
st.subheader(f"📋 Data pada {tanggal_filter.strftime('%d %B %Y')}")
if not filtered_data.empty:
    for idx, row in filtered_data.iterrows():
        st.markdown(f"""
        **{row['Keterangan']}**
        - Jumlah: Rp {row['Jumlah']:,.0f}
        - Tabungan: Rp {row['Uang di Tabungan']:,.0f}
        - Tunai: Rp {row['Uang di Tangan']:,.0f}
        """)
        if st.button("🗑 Hapus", key=str(idx)):
            df = df.drop(index=idx)
            df.reset_index(drop=True, inplace=True)
            save_data(df)
            st.warning("Data berhasil dihapus.")
            st.experimental_rerun()
else:
    st.info("Tidak ada data untuk tanggal tersebut.")

# Ringkasan keuangan
st.subheader("📊 Ringkasan Total")
total_pengeluaran = df["Jumlah"].sum()
total_tabungan = df["Uang di Tabungan"].sum()
total_tunai = df["Uang di Tangan"].sum()
sisa_saldo = saldo_awal - total_pengeluaran

col1, col2, col3 = st.columns(3)
col1.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
col2.metric("Total Tabungan", f"Rp {total_tabungan:,.0f}")
col3.metric("Total Uang di Tangan", f"Rp {total_tunai:,.0f}")

st.write(f"**Sisa Saldo = Rp {sisa_saldo:,.0f}**")

# Tombol download
st.subheader("⬇️ Unduh Rekap Keuangan")
if os.path.exists(FILE_PATH):
    with open(FILE_PATH, "rb") as f:
        st.download_button("Download Excel", f, file_name="rekap_keuangan.xlsx")
else:
    st.info("Belum ada data untuk diunduh.")

    with open(FILE_PATH, "rb") as f:
        st.download_button("Download Excel", f, file_name="rekap_keuangan.xlsx")
else:
    st.info("Belum ada data untuk diunduh.")
