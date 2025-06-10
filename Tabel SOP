import streamlit as st
import graphviz

st.set_page_config(page_title="Flowchart Izin Pemanfaatan Air Limbah", layout="wide")

st.title("📄 Flowchart Penerbitan Izin Pemanfaatan Air Limbah untuk Aplikasi pada Tanah")

st.markdown("""
Diagram di bawah ini menggambarkan alur proses sesuai SOP.
""")

# Diagram menggunakan Graphviz
flowchart = graphviz.Digraph()

# Tambahkan node (tahapan proses)
flowchart.node("A", "1. Pemohon Ajukan Permohonan")
flowchart.node("B", "2. Meneruskan Surat")
flowchart.node("C", "3. Merancang Surat Persetujuan")
flowchart.node("D", "4. Menelaah & Menyetujui")
flowchart.node("E", "5. Permohonan Lanjutan (setelah penilaian)")
flowchart.node("F", "6. Verifikasi Dokumen & Tinjauan Lapangan")
flowchart.node("G", "7. Verifikasi Administratif Lanjutan")

# Hubungkan node
flowchart.edge("A", "B")
flowchart.edge("B", "C")
flowchart.edge("C", "D")
flowchart.edge("D", "E")
flowchart.edge("E", "F")
flowchart.edge("F", "G")

# Tampilkan diagram
st.graphviz_chart(flowchart)

st.caption("Sumber: SOP Dinas Lingkungan Hidup – Penerbitan Izin Aplikasi Air Limbah ke Tanah")
