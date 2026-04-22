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

# --- 3. SIDEBAR NAVIGASI & LOGIN ---
with st.sidebar:
    # --- BAHAGIAN LOGO DENGAN JARAK YANG BETUL ---
    try:
        st.image("logo_pkd.jpg", use_container_width=True)
    except:
        st.info("🛡️ SMART DESK ICT")

    st.title("Menu Utama")
    # ... sambungan kod asal anda untuk menu dan login ...
    # Senarai menu asal untuk staf
    menu_pilihan = ["Borang Aduan Pengguna", "Semak Status Pengguna"]
    
    st.divider()
    st.subheader("🔒 Ruangan Admin")
    user_admin = st.text_input("Username")
    pass_admin = st.text_input("Password", type="password")
    
    # LOGIK LOGIN
    if user_admin == "adminict" and pass_admin == "lipis123":
        st.success("Log Masuk Berjaya!")
        menu_pilihan.append("Dashboard Admin ICT")
    elif user_admin != "" or pass_admin != "":
        st.error("Kredential Salah")

    st.divider()
    pilihan = st.radio("Navigasi Halaman:", menu_pilihan)
    
# --- 4. HALAMAN 1: BORANG ADUAN PENGGUNA ---
if pilihan == "Borang Aduan Pengguna":
    st.title("📝 Borang Aduan ICT")
    with st.form("form_aduan", clear_on_submit=True):
        nama = st.text_input("Nama Penuh")
        unit = st.selectbox("Unit",["Pejabat Kesihatan Daerah Lipis", "Klinik Kesihatan Benta", "Klinik Kesihatan Jerkoh", "Klinik Kesihatan Padang tengku",
                                                    "Klinik Kesihatan Chegar Perah", "Klinik Kesihatan Merapoh", "Klinik Kesihatan Bukit Betong", "Klinik Kesihatan Sungai Koyan",
                                                    "Klinik Kesihatan Betau", "Klinik Kesihatan Mela"])
        kategori = st.selectbox("Kategori", ["Hardware", "Software", "System", "Technical"])
        perincian = st.text_area("Masalah")
        submit = st.form_submit_button("HANTAR ADUAN")
        
        if submit:
            if nama and perincian:
                data_baru = {
                    "Nama": nama, "Unit": unit, "Kategori": kategori,
                    "Status": "Baru", "Tarikh": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                simpan_data(data_baru)
                st.success("Aduan berjaya dihantar!")
            else:
                st.error("Sila isi Nama dan Perincian.")

# --- 5. HALAMAN 2: SEMAK STATUS PENGGUNA ---
elif pilihan == "Semak Status Pengguna":
    st.title("🔍 Semak Status Aduan")
    nama_cari = st.text_input("Masukkan Nama Anda:")
    if nama_cari:
        if os.path.exists(DB_FILE):
            df = pd.read_excel(DB_FILE)
            hasil = df[df['Nama'].astype(str).str.contains(nama_cari, case=False, na=False)]
            if not hasil.empty:
                for index, row in hasil.iterrows():
                    with st.expander(f"Aduan: {row['Kategori']} ({row['Tarikh']})"):
                        st.write(f"Status: **{row['Status']}**")
            else:
                st.error("Rekod tidak dijumpai.")

# --- 6. HALAMAN 3: DASHBOARD ADMIN ICT (Hanya keluar kalau login betul) ---
elif pilihan == "Dashboard Admin ICT":
    st.title("📊 Dashboard Admin")
    if os.path.exists(DB_FILE):
        df = pd.read_excel(DB_FILE)
        st.write("Senarai Aduan Masuk:")
        st.dataframe(df)
        st.bar_chart(df['Kategori'].value_counts())
    else:
        st.warning("Tiada data.")