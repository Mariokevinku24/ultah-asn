import streamlit as st

st.set_page_config(page_title="Struktur Organisasi", layout="wide")
st.title("📊 Struktur Organisasi Perusahaan")

st.graphviz_chart("""
digraph StrukturOrganisasi {
    node [shape=box, style=filled, color=lightblue];

    "Dewan Komisaris";
    "Komite Nominasi & Remunerasi";
    "Komite Audit";
    "Direktur Utama Nasreng";
    "Wakil Direktur Utama\\nKantil Wilisofi Himansyah";

    "Sekretaris Perusahaan\\nAhmad Afialt";
    "Legal Perusahaan\\nChristoporus Taufik";
    "Hubungan Investor\\nLuther Fidel Putra";
    "Audit Internal\\nRoy Shandy Duwila";

    "Direktur\\nHoris Baltas";
    "Direktur\\nLina P. Tanaya";
    "Direktur\\nValencia H. Tanderesetopo";
    "Direktur\\nDovi Tombaga";
    "Direktur\\nTitam Hermiawan";
    "Direktur\\nTatian Sumantara";

    "Dewan Komisaris" -> "Komite Nominasi & Remunerasi";
    "Dewan Komisaris" -> "Komite Audit";
    "Dewan Komisaris" -> "Direktur Utama Nasreng";

    "Direktur Utama Nasreng" -> "Wakil Direktur Utama\\nKantil Wilisofi Himansyah";
    "Direktur Utama Nasreng" -> "Sekretaris Perusahaan\\nAhmad Afialt";
    "Direktur Utama Nasreng" -> "Legal Perusahaan\\nChristoporus Taufik";
    "Direktur Utama Nasreng" -> "Hubungan Investor\\nLuther Fidel Putra";
    "Direktur Utama Nasreng" -> "Audit Internal\\nRoy Shandy Duwila";

    "Direktur Utama Nasreng" -> "Direktur\\nHoris Baltas";
    "Direktur Utama Nasreng" -> "Direktur\\nLina P. Tanaya";
    "Direktur Utama Nasreng" -> "Direktur\\nValencia H. Tanderesetopo";
    "Direktur Utama Nasreng" -> "Direktur\\nDovi Tombaga";
    "Direktur Utama Nasreng" -> "Direktur\\nTitam Hermiawan";
    "Direktur Utama Nasreng" -> "Direktur\\nTatian Sumantara";
}
""")
