import streamlit as st
import pandas as pd
from datetime import datetime

# Data ulang tahun
data = [
    ("Sortauli Triana Manurung, ST", "1970-01-30"),
    ("Nurmi Nurani Mustika, ST, M.Si", "1970-01-31"),
    ("Debora Mandasari, ST", "1986-02-05"),
    ("Indra Soangkupon Siregar, SE", "1973-02-11"),
    ("Ronald MS Siburian, S.ST", "1981-02-15"),
    ("Erlita Lubis, S.Sos, MH", "1971-03-01"),
    ("Lamria Gultom, SE", "1971-03-29"),
    ("Elinasari Nasution, SP", "1972-03-30"),
    ("Mayanty Artauli Br. Simanjuntak, Amd", "1986-03-31"),
    ("Cristofel Limbong, S. Hut., M.Si.", "1978-04-14"),
    ("Posma R Batubara, ST, MM", "1978-04-25"),
    ("Misno Koko Handoko Silitonga, SH", "1979-05-07"),
    ("Rivan Silaen, ST, M.Si", "1972-05-09"),
    ("Abzuka Syukron, S.Si", "1994-05-31"),
    ("Ester Junita Tampubolon, SH, M.Kom", "1979-06-03"),
    ("Juniar Silalahi, SE", "1977-06-08"),
    ("Alexander Sipayung, SKM, MM", "1975-06-14"),
    ("Cristo Mori Romario M. ST", "1994-06-18"),
    ("Drs. Heady Habeahan", "1968-07-06"),
    ("Julius Karo Sekali, S.Sos", "1974-07-08"),
    ("Rizky Ananda S. Mat.", "1997-07-24"),
    ("Kevin Jeremy Dirgantara Pakpahan, S. Mat.", "2001-09-26"),
    ("Syahroni Harahap, ST", "1970-10-10"),
    ("Jamiah, S.Si, MM", "1980-10-10"),
    ("Noni Bahanoer, SE", "1983-10-13"),
    ("Rizky Dwi Ananda Ginting, S. T.", "1997-10-21"),
    ("Susanto, SH", "1971-11-11"),
    ("Eliyani Nasution, S.H, MM", "1972-11-24"),
    ("Saur Mangasi N Pangaribuan, SE, M.Si", "1971-11-28"),
    ("Ripin Panggabean, S. T", "1995-11-29"),
    ("Deasy Christine Natalia Doloksaribu, S.Pi", "1980-12-15"),
    ("Erika Natalia, SKM, MM", "1982-12-16"),
    ("Dr.Eng. Reza Darma Al Fariz, S. T., M. H", "1995-12-29"),
]

# Konversi ke DataFrame
df = pd.DataFrame(data, columns=["Nama", "Tanggal Lahir"])
df["Tanggal Lahir"] = pd.to_datetime(df["Tanggal Lahir"])
df["Ulang Tahun"] = df["Tanggal Lahir"].dt.strftime("%d %B")
df["Bulan"] = df["Tanggal Lahir"].dt.month
df["Hari"] = df["Tanggal Lahir"].dt.day

# Urutkan berdasarkan bulan dan hari
df_sorted = df.sort_values(by=["Bulan", "Hari"]).reset_index(drop=True)

# Header aplikasi
st.title("📅 Daftar Ulang Tahun Pegawai DLH")

# Cek siapa yang ulang tahun hari ini
today = datetime.today()
ulang_tahun_hari_ini = df_sorted[
    (df_sorted["Bulan"] == today.month) & (df_sorted["Hari"] == today.day)
]

if not ulang_tahun_hari_ini.empty:
    st.success("🎉 Hari ini ada yang berulang tahun!")
    st.table(ulang_tahun_hari_ini[["Nama", "Ulang Tahun"]])
else:
    st.info("Tidak ada ulang tahun hari ini.")

# Tampilkan semua jadwal ulang tahun
st.subheader("📋 Jadwal Lengkap")
st.table(df_sorted[["Nama", "Ulang Tahun"]])
