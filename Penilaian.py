import streamlit as st

st.title("Form Penilaian Kantor Ramah Lingkungan")

# Input Nama Instansi dan Penilai
nama_instansi = st.text_input("Nama Instansi")
nama_penilai = st.text_input("Nama Penilai")

# Komponen dan Sub-komponen
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

st.markdown("---")
total_nilai = 0
nilai_komponen = {}

# Loop input untuk tiap sub-komponen
for k, sub_komponen in komponen.items():
    st.subheader(k)
    for sub in sub_komponen:
        nilai = st.number_input(
            f"Nilai untuk {sub}",
            min_value=0,
            max_value=10,
            step=1,
            key=f"{k}-{sub}"
        )
        nilai_komponen[f"{k} - {sub}"] = nilai
        total_nilai += nilai

# Hasil Total & Kategori
st.markdown("---")
st.subheader("Total Nilai")
st.write(f"**{total_nilai}**")

# Kategori akhir berdasarkan skor total
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

st.write(f"**Kategori: {kategori}**")

# Tampilkan informasi instansi dan penilai
st.markdown("---")
st.subheader("Informasi Penilaian")
st.write(f"**Nama Instansi:** {nama_instansi}")
st.write(f"**Nama Penilai:** {nama_penilai}")

