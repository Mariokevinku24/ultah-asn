import streamlit as st
import graphviz

st.set_page_config(layout="wide")
st.title("📄 Flowchart SOP - Proses Verifikasi dan Keputusan")

# Inisialisasi Diagram
flowchart = graphviz.Digraph(format='png')
flowchart.attr(rankdir='TB', size='10')

# Bentuk-bentuk proses
flowchart.node('A', 'Verifikasi Berkas Administrasi', shape='box')
flowchart.node('B', 'Tinjauan Lapangan', shape='box')
flowchart.node('C', 'Lengkap?', shape='diamond')
flowchart.node('D1', 'Kembalikan ke Pemohon', shape='box')
flowchart.node('D2', 'Lanjutkan Penyusunan Izin', shape='parallelogram')
flowchart.node('E', 'Rancang Keputusan Izin', shape='box')

# Alur
flowchart.edge('A', 'B')
flowchart.edge('B', 'C')
flowchart.edge('C', 'D1', label='Tidak')
flowchart.edge('C', 'D2', label='Ya')
flowchart.edge('D2', 'E')

# Tampilkan diagram
st.graphviz_chart(flowchart)


