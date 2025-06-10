import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📄 SOP Penerbitan Izin Pemanfaatan Air Limbah untuk Aplikasi pada Tanah")

st.markdown("#### Tabel Proses SOP (Bagian 1 – Pengajuan dan Evaluasi)")

# Data kegiatan
data = [
    ["1", "Pemohon ajukan permohonan + dokumen lingkungan", "✅", "", "", "", "", "", "Surat Permohonan + UKL-UPL/AMDAL", "15 menit", "Tanda Terima"],
    ["2", "Meneruskan surat", "", "✅", "", "", "", "", "Surat dari Berkas", "15 menit", "-"],
    ["3", "Merancang surat persetujuan", "", "", "✅", "", "", "", "Draft", "2 hari", "Draft"],
    ["4", "Menelaah dan beri persetujuan", "", "", "", "✅", "", "", "Draft", "1 hari", "Surat Persetujuan"],
    ["5", "Pemohon ajukan permohonan pasca penilaian", "✅", "", "", "", "", "", "Surat Permohonan + Hasil Penilaian", "15 menit", "Disposisi"],
    ["6", "Verifikasi dokumen, tinjauan lapangan", "", "✅", "", "", "", "", "Surat permohonan & berkas", "3 hari", "Berita Acara"],
    ["7", "Verifikasi akhir permohonan", "✅", "", "", "", "", "", "Surat permohonan & berkas", "15 menit", "Tanda Terima"]
]

# Konversi ke DataFrame
columns = ["No", "Kegiatan", "Kasubbid Perizinan", "Kabid WASDAL", "Sekretaris", "Kaban", "Kabag Hukum", "Bupati", "Kelengkapan", "Waktu", "Output"]
df = pd.DataFrame(data, columns=columns)

# Tampilkan tabel dengan checkbox visual (HTML bisa ditambahkan juga jika diinginkan)
st.dataframe(df, use_container_width=True)

st.markdown("---")
st.markdown("#### Tabel Proses SOP (Bagian 2 – Penyusunan dan Penerbitan Izin)")

data2 = [
    ["10", "Membuat rancangan keputusan izin", "", "✅", "", "", "", "", "", "1 hari", "-"],
    ["11", "Koordinasi rancangan keputusan", "", "", "✅", "", "", "", "Draft", "2 hari", "Draft"],
    ["12", "Telaah dan tanda tangan izin", "", "", "", "✅", "", "", "Draft", "5 hari", "Draft"],
    ["13", "Teruskan ke Bupati untuk tanda tangan", "", "", "", "", "✅", "", "Draft", "1 hari", "Surat Izin"],
    ["14", "Serahkan izin ke Pemrakarsa", "✅", "", "", "", "", "", "Surat Izin", "15 menit", "Tanda Terima"]
]

df2 = pd.DataFrame(data2, columns=columns)
st.dataframe(df2, use_container_width=True)

st.caption("Sumber: SOP Dinas Lingkungan Hidup – Prosedur Penerbitan Izin Air Limbah ke Tanah")


