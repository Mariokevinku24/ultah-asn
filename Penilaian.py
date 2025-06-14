import streamlit as st
from datetime import datetime
import pandas as pd
import os

st.set_page_config(page_title="Penilaian Kantor Ramah Lingkungan", layout="wide")
st.title("📋 Form Penilaian Kantor Ramah Lingkungan")

CSV_FILE = "penilaian.csv"
DELETE_PASSWORD = "admin123"  # Ganti sesuai kebutuhan

def load_data():
    if os.path.exists(CSV_FILE):
        if os.path.getsize(CSV_FILE) == 0:
            return []
        try:
            return pd.read_csv(CSV_FILE).to_dict("records")
        except Exception as e:
            st.error(f"Gagal membaca CSV: {e}")
            return []
    return []

def save_data(data):
    df = pd.DataFrame(data)
    df.to_csv(CSV_FILE, index=False)

# Inisialisasi session state
if "penilaian_data" not in st.session_state:
    st.session_state.penilaian_data = load_data()

# Form penilaian
with st.form("form_penilaian"):
    col1, col2 = st.columns(2)
    with col1:
        nama_instansi = st.text_input("Nama Instansi")
    with col2:
        nama_penilai = st.text_input("Nama Penilai")

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

    total_nilai = 0
    for k, sub_komponen in komponen.items():
        st.markdown(f"### {k}")
        for sub in sub_komponen:
            nilai = st.number_input(
                sub,
                min_value=0,
                max_value=10,
                step=1,
                key=f"{k}-{sub}"
            )
            total_nilai += nilai

    # Penentuan kategori
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

    submitted = st.form_submit_button("💾 Simpan Penilaian")

    if submitted and nama_instansi and nama_penilai:
        data_baru = {
            "Waktu": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "Nama Instansi": nama_instansi,
            "Nama Penilai": nama_penilai,
            "Total Nilai": total_nilai,
            "Kategori": kategori
        }
        st.session_state.penilaian_data.append(data_baru)
        save_data(st.session_state.penilaian_data)
        st.success("✅ Penilaian berhasil disimpan!")

st.markdown("---")
st.subheader("📑 Daftar Penilaian Tersimpan")

# Tombol download
if st.session_state.penilaian_data:
    df_download = pd.DataFrame(st.session_state.penilaian_data)
    st.download_button(
        label="⬇️ Download CSV",
        data=df_download.to_csv(index=False).encode("utf-8"),
        file_name="data_penilaian.csv",
        mime="text/csv"
    )

# Tampilkan data
if st.session_state.penilaian_data:
    for i, data in enumerate(st.session_state.penilaian_data):
        with st.expander(f"📌 {i+1}. {data['Nama Instansi']} (oleh {data['Nama Penilai']})"):
            st.write(f"""
            **Total Nilai:** {data['Total Nilai']}  
            **Kategori:** {data['Kategori']}  
            **Waktu:** {data['Waktu']}
            """)

            with st.form(f"hapus_form_{i}"):
                password = st.text_input("Masukkan password untuk menghapus", type="password", key=f"pass_{i}")
                hapus = st.form_submit_button("🗑️ Hapus Data Ini")
                if hapus:
                    if password == DELETE_PASSWORD:
                        st.session_state.penilaian_data.pop(i)
                        save_data(st.session_state.penilaian_data)
                        st.success("✅ Data berhasil dihapus.")
                        st.experimental_rerun()
                    else:
                        st.error("❌ Password salah. Data tidak dihapus.")
else:
    st.info("Belum ada data penilaian disimpan.")
