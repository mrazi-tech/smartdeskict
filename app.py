import streamlit as st
import pandas as pd
from datetime import datetime
import os

# --- 1. KONFIGURASI HALAMAN ---
st.set_page_config(page_title="e-Aduan ICT PKD Lipis", layout="wide", page_icon="🛡️")

# --- 2. FUNGSI DATABASE (EXCEL) ---
DB_FILE = 'database_aduan.xlsx'

def simpan_data(data):
    if not os.path.isfile(DB_FILE):
        df = pd.DataFrame([data])
        df.to_excel(DB_FILE, index=False)
    else:
        existing_df = pd.read_excel(DB_FILE)
        new_df = pd.concat([existing_df, pd.DataFrame([data])], ignore_index=True)
        new_df.to_excel(DB_FILE, index=False)

# --- 3. NAVIGASI SIDEBAR ---
with st.sidebar:
    st.title("Menu Utama")
    # Di sini kita tambah 3 pilihan navigasi
    pilihan = st.sidebar.radio("Navigasi:", 
                               ["Borang Aduan Pengguna", 
                                "Semak Status (Pengguna)", 
                                "Dashboard Admin ICT"])
    st.divider()
    st.info("UNIT ICT PKD Lipis")

# --- 4. HALAMAN 1: BORANG ADUAN PENGGUNA ---
if pilihan == "Borang Aduan Pengguna":
    st.title("🛡️ Borang Aduan ICT PKD Lipis")
    st.markdown("Sila isi butiran kerosakan di bawah.")
    
    with st.form("form_aduan", clear_on_submit=True):
        col1, col2 = st.columns(2)
        with col1:
            nama = st.text_input("Nama Penuh Kakitangan")
            unit = st.selectbox("Unit / Jabatan", ["Pejabat Kesihatan Daerah Lipis", "Klinik Kesihatan Benta", "Klinik Kesihatan Jerkoh", "Klinik Kesihatan Padang tengku",
                                                    "Klinik Kesihatan Chegar Perah", "Klinik Kesihatan Merapoh", "Klinik Kesihatan Bukit Betong", "Klinik Kesihatan Sungai Koyan",
                                                    "Klinik Kesihatan Betau", "Klinik Kesihatan Mela"])

        with col2:
            kategori = st.selectbox("Kategori Kerosakan", ["Hardware", "Software", "System", "Technical"])
            no_aset = st.text_input("No. Aset")

        perincian = st.text_area("Deskripsi Kerosakan")
        submit = st.form_submit_button("HANTAR ADUAN")

        if submit:
            if nama and perincian:
                data_baru = {
                    "Nama": nama, "Unit": unit, "Kategori": kategori,
                    "No_Aset": no_aset, "Perincian": perincian,
                    "Status": "Baru", "Tarikh": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                simpan_data(data_baru)
                st.success("Aduan berjaya dihantar!")
            else:
                st.error("Sila isi Nama dan Perincian.")

# --- 5. HALAMAN 2: SEMAK STATUS PENGGUNA (YANG ANDA MINTA) ---
elif pilihan == "Semak Status (Pengguna)":
    st.title("🔍 Semak Status Aduan")
    st.markdown("Masukkan nama anda untuk melihat perkembangan aduan secara 'Live'.")
    
    nama_cari = st.text_input("Masukkan Nama Penuh Anda:")
    
    if nama_cari:
        if os.path.exists(DB_FILE):
            df = pd.read_excel(DB_FILE)
            # Cari nama dalam database
            hasil = df[df['Nama'].astype(str).str.contains(nama_cari, case=False, na=False)]
            
            if not hasil.empty:
                for index, row in hasil.iterrows():
                    with st.expander(f"📌 Aduan: {row['Kategori']} ({row['Tarikh']})"):
                        status = row['Status']
                        # Logik warna status
                        if status == "Baru":
                            st.warning(f"🟡 Status: **{status}** (Menunggu ICT)")
                        elif status == "Dalam Tindakan":
                            st.info(f"🔵 Status: **{status}** (Juruteknik sedang bertugas)")
                        elif status == "Selesai":
                            st.success(f"🟢 Status: **{status}** (Selesai)")
                        
                        st.write(f"**Perincian:** {row['Perincian']}")
                        st.write(f"**No. Aset:** {row['No_Aset']}")
            else:
                st.error("Nama tidak dijumpai dalam rekod.")
        else:
            st.warning("Database belum wujud.")

# --- 6. HALAMAN 3: DASHBOARD ADMIN ICT ---
elif pilihan == "Dashboard Admin ICT":
    st.title("📊 Dashboard Admin")
    if os.path.exists(DB_FILE):
        df = pd.read_excel(DB_FILE)
        st.subheader("Data Keseluruhan Aduan")
        st.dataframe(df, use_container_width=True)
        
        # Grafik Ringkas
        st.bar_chart(df['Kategori'].value_counts())
    else:
        st.warning("Tiada data untuk dipaparkan.")