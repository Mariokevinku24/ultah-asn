import streamlit as st
import pandas as pd

st.set_page_config(layout="wide")
st.title("📋 SOP - Penerbitan Izin Pemanfaatan Air Limbah")

st.markdown("### Bagian Proses dan Pelaksana (dengan simbol visual sederhana)")

# Gunakan emoji atau simbol bentuk kotak 🔷 atau SVG inline
kotak = "🟦"
panah = "➡️"
diamond = "🔷"
dokumen = "📄"

data = [
    ["1", "Pemohon ajukan permohonan", kotak, "", "", "", "", "", "Dokumen Permohonan", "15 menit", "Tanda Terima"],
    ["2", "Meneruskan surat", "", kotak, "", "", "", "", "Surat", "15 menit", "-"],
    ["3", "Merancang surat persetujuan", "", "", kotak, "", "", "", "Draft", "2 hari", "Draft"],
    ["4", "Telaah dan beri persetujuan", "", "", "", kotak, "", "", "Draft", "1 hari", "Persetujuan"],
    ["5", "Verifikasi + Tinjauan Lapangan", "", kotak, "", "", "", "", "Form + Bukti Lapangan", "3 hari", "Berita Acara"],
    ["6", "Cek kelengkapan", kotak, "", "", "", "", "", "📄", "15 menit", "✔️ atau ❌"],
    ["7", "Keputusan Izin", "", kotak, "", "", diamond, "", "Naskah Izin", "1 hari", "Surat Izin"]
]

columns = ["No", "Kegiatan", "Kasubbid Perizinan", "Kabid WASDAL", "Sekretaris", "Kaban", "Kabag Hukum", "Bupati", "Kelengkapan", "Waktu", "Output"]
df = pd.DataFrame(data, columns=columns)

# Tampilkan tabel
st.markdown(df.to_html(escape=False, index=False), unsafe_allow_html=True)

