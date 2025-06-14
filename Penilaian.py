import streamlit as st
from datetime import datetime
import pandas as pd
import os

# Konfigurasi halaman
st.set_page_config(page_title="Penilaian Kantor Ramah Lingkungan", layout="wide")
st.title("📄 Form Penilaian Kantor Ramah Lingkungan")

CSV_FILE = "penilaian.csv"

# Fungsi untuk memuat data dari CSV
def load_data():
    if os.path.exists(CSV_FILE) and os.path.getsize(CSV_FILE) > 0:
        return pd.read_csv(CSV_FILE).to_dict("records")
    return []

# Fungsi untuk menyimpan data ke CSV
def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)

# Inisialisasi data pada session_state
if "penilaian_data" not in st.session_state:
    st.session_state.penilaian_data = load_data()

# Komponen dan Sub-komponen penilaian
komponen = {
    "1. Area Kantor": ["Sampah dan gulma", "Tempat Sampah"],
    "2. Drainase": ["Sampah, gulma dan sedimen"],
    "3. RTH": [
        "Pohon peneduh berdasarkan sebaran",
        "Pohon peneduh berdasarkan fungsi",
        "Penghijauan"
    ],
    "4. Pelayanan Pengumpulan Sampah": [
        "Bangunan fisik dan pelayanan",
        "Kebersihan TPS"
    ],
    "5. Pemilahan Sampah": [
        "Sarana Pemilahan Sampah",
        "Proses Pemilahan Sampah"
    ],
    "6. Kegiatan Pengomposan": [
        "Sarana Pengolahan Sampah",
        "Proses Pengolahan Sampah",
        "Kapasitas",
        "Jumlah sampah untuk diolah",
        "Pemanfaatan"
    ],
    "7. Toilet": [
        "Kebersihan Toilet",
        "Air bersih di Toilet"
    ],
    "8. Kebersihan Ruangan": [
        "Debu, assesories ruangan (keset, bunga, dll)"
    ],
    "9. Ventilasi Ruangan": ["Jendela"],
    "10. Slogan/Himbauan/Etika": ["Plank nama, slogan/himbauan"],
    "11. Bank Sampah": [
        "Jumlah Bank Sampah/SK Bank Sampah",
        "Jumlah Bank Sampah yang sudah berjalan"
    ]
}

# Formulir input
with st.form("form_penilaian"):
    col1, col2 = st.columns(2)
    with col1:
        nama_instansi = st.text_input("Nama Instansi")
    with col2:
        nama_penilai = st.text_input("Nama Penilai")

    nilai_sub = {}
    total_nilai = 0

    # Loop semua komponen dan sub-komponen
    for judul, subkomponens in komponen.items():
        st.markdown(f"### {judul}")
        for sub in subkomponens:
            key = f"{judul} - {sub}"
            nilai = st.number_input(sub, min_value=0, max_value=100, step=10, key=key)
            nilai_sub[key] = nilai
            total_nilai += nilai

    # Tentukan kategori berdasarkan total nilai
    if total_nilai >= 81:
        kategori = "Sangat Baik"
    elif total_nilai >= 71:
        kategori = "Baik"
    elif total_nilai >= 61:
        kategori = "Sedang"
    elif total_nilai >= 46:
        kategori = "Jelek"
    elif total_nilai >= 30:
        kategori = "Sangat Jelek"
    else:
        kategori = "Belum Memadai"

    submitted = st.form_submit_button("Simpan Penilaian")

    if submitted and nama_instansi and nama_penilai:
        data_baru = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama Instansi": nama_instansi,
            "Nama Penilai": nama_penilai,
            "Total Nilai": total_nilai,
            "Kategori": kategori
        }
        data_baru.update(nilai_sub)

        st.session_state.penilaian_data.append(data_baru)
        save_data(st.session_state.penilaian_data)
        st.success("✅ Penilaian berhasil disimpan!")

# Tampilkan daftar penilaian
st.markdown("---")
st.subheader("📋 Daftar Penilaian Tersimpan")

if st.session_state.penilaian_data:
    for i, data in enumerate(st.session_state.penilaian_data):
        col1, col2 = st.columns([10, 1])
        with col1:
            st.markdown(f"""
            **{i+1}. {data['Nama Instansi']}**  
            🧑 Penilai: `{data['Nama Penilai']}`  
            📊 Nilai: `{data['Total Nilai']}`  
            🏅 Kategori: **{data['Kategori']}**  
            🕒 Waktu: {data['Waktu']}
            """)
        with col2:
            if st.button("🗑️ Hapus", key=f"hapus_{i}"):
                st.session_state.penilaian_data.pop(i)
                save_data(st.session_state.penilaian_data)
                st.experimental_rerun()
else:
    st.info("Belum ada data penilaian disimpan.")

# Tombol untuk mengunduh CSV
st.markdown("---")
st.download_button(
    label="⬇️ Unduh Semua Penilaian (CSV)",
    data=pd.DataFrame(st.session_state.penilaian_data).to_csv(index=False),
    file_name="penilaian.csv",
    mime="text/csv"
)
