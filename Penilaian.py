import streamlit as st
import sqlite3
from datetime import datetime

DB_NAME = "penilaian.db"

# Inisialisasi database
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS penilaian (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            waktu TEXT,
            instansi TEXT,
            penilai TEXT,
            total_nilai INTEGER,
            kategori TEXT
        )
    """)
    conn.commit()
    conn.close()

# Simpan data
def simpan_penilaian(waktu, instansi, penilai, total_nilai, kategori):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO penilaian (waktu, instansi, penilai, total_nilai, kategori)
        VALUES (?, ?, ?, ?, ?)
    """, (waktu, instansi, penilai, total_nilai, kategori))
    conn.commit()
    conn.close()

# Ambil data
def get_data():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT id, waktu, instansi, penilai, total_nilai, kategori FROM penilaian")
    rows = cursor.fetchall()
    conn.close()
    return rows

# Hapus data
def hapus_data(id_):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM penilaian WHERE id = ?", (id_,))
    conn.commit()
    conn.close()

# Jalankan inisialisasi saat pertama
init_db()

st.title("Form Penilaian Kantor Ramah Lingkungan")

with st.form("penilaian_form"):
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
        "7. Toilet": ["Kebersihan Toilet", "Air bersih di Toilet"],
        "8. Kebersihan Ruangan": ["Debu, assesories ruangan"],
        "9. Ventilasi Ruangan": ["Jendela"],
        "10. Slogan/Himbauan/Etika": ["Plank nama, slogan/himbauan"],
        "11. Bank Sampah": [
            "Jumlah Bank Sampah/SK Bank Sampah",
            "Jumlah Bank Sampah yang sudah berjalan"
        ]
    }

    total_nilai = 0
    for k, sub_komponen in komponen.items():
        st.markdown(f"**{k}**")
        for sub in sub_komponen:
            nilai = st.number_input(f"{sub}", min_value=0, max_value=10, step=1, key=f"{k}-{sub}")
            total_nilai += nilai

    # Kategori
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

    submitted = st.form_submit_button("Simpan")

    if submitted and nama_instansi and nama_penilai:
        simpan_penilaian(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            nama_instansi,
            nama_penilai,
            total_nilai,
            kategori
        )
        st.success("✅ Penilaian berhasil disimpan!")

# Tampilkan data
st.markdown("---")
st.subheader("📋 Data Penilaian")

data = get_data()

if data:
    for row in data:
        id_, waktu, instansi, penilai, total, kategori = row
        col1, col2 = st.columns([10, 1])
        with col1:
            st.write(f"""
            **{instansi}**  
            Penilai: {penilai}  
            Nilai: {total} | Kategori: {kategori}  
            Waktu: {waktu}
            """)
        with col2:
            if st.button("Hapus", key=f"hapus_{id_}"):
                hapus_data(id_)
                st.experimental_rerun()
else:
    st.info("Belum ada data penilaian disimpan.")

