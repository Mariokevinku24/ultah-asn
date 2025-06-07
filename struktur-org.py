import streamlit as st

st.set_page_config(page_title="Struktur DLH Deli Serdang", layout="wide")
st.title("📊 Struktur Organisasi Dinas Lingkungan Hidup\nKabupaten Deli Serdang")

# Form input nama pejabat
st.sidebar.header("🖊️ Isi Nama Pejabat")
kadis = st.sidebar.text_input("Kepala Dinas", "Dinas Lingkungan Hidup")
sekretaris = st.sidebar.text_input("Sekretaris", "SEKRETARIAT")
sub_umum = st.sidebar.text_input("Sub Bagian Umum", "Sub Bagian Umum")
sub_keuangan = st.sidebar.text_input("Sub Bagian Keuangan", "Sub Bagian Keuangan")
sub_program = st.sidebar.text_input("Sub Bagian Program", "Sub Bagian Program")

# Graphviz untuk struktur organisasi
graph_code = f"""
digraph G {{
    node [shape=box, style="filled", fillcolor="#E0F7FA", fontname=Helvetica];

    "{kadis}";
    "{sekretaris}" -> "{sub_umum}";
    "{sekretaris}" -> "{sub_keuangan}";
    "{sekretaris}" -> "{sub_program}";
    "{kadis}" -> "{sekretaris}";
    "{kadis}" -> "Kelompok Jabatan\\nFungsional";

    "{kadis}" -> "Bidang Tata\\nLingkungan";
    "{kadis}" -> "Bidang Pengelolaan\\nSampah & Limbah B3";
    "{kadis}" -> "Bidang Pengendalian\\nPencemaran & Kerusakan";
    "{kadis}" -> "Bidang Penataan &\\nPeningkatan Kapasitas";

    "Bidang Tata\\nLingkungan" -> "Seksi Inventarisasi\\nRPPLH & KLHS";
    "Bidang Tata\\nLingkungan" -> "Seksi Kajian Dampak\\nLingkungan";
    "Bidang Tata\\nLingkungan" -> "Seksi Pemeliharaan\\nLingkungan Hidup";

    "Bidang Pengelolaan\\nSampah & Limbah B3" -> "Seksi Pengurangan\\nSampah";
    "Bidang Pengelolaan\\nSampah & Limbah B3" -> "Seksi Penanganan\\nSampah";
    "Bidang Pengelolaan\\nSampah & Limbah B3" -> "Seksi Limbah B3";

    "Bidang Pengendalian\\nPencemaran & Kerusakan" -> "Seksi Pemantauan\\nLingkungan";
    "Bidang Pengendalian\\nPencemaran & Kerusakan" -> "Seksi Pencemaran\\nLingkungan";
    "Bidang Pengendalian\\nPencemaran & Kerusakan" -> "Seksi Kerusakan\\nLingkungan";

    "Bidang Penataan &\\nPeningkatan Kapasitas" -> "Seksi Pengaduan &\\nPenyelesaian Sengketa";
    "Bidang Penataan &\\nPeningkatan Kapasitas" -> "Seksi Penegakan\\nHukum Lingkungan";
    "Bidang Penataan &\\nPeningkatan Kapasitas" -> "Seksi Peningkatan\\nKapasitas LH";

    "{kadis}" -> "UPT";
}}
"""

# Tampilkan struktur organisasi
st.subheader("📌 Struktur Organisasi DLH Deli Serdang")
st.graphviz_chart(graph_code)

