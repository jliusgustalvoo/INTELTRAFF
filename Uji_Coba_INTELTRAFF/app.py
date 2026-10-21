import streamlit as st
import pandas as pd
import base64
import os

# Konfigurasi Halaman Dasar
st.set_page_config(page_title="INTELTRAFF - 5 Screen", page_icon="🚦", layout="wide")

# Custom CSS Premium & Animasi
st.markdown("""
<style>
    /* Desain Glassmorphism untuk Kartu Jalur */
    .glass-card {
        background: rgba(15, 23, 42, 0.65);
        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 20px;
        padding: 30px 20px;
        box-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.3);
        text-align: center;
        margin-bottom: 20px;
        transition: all 0.3s ease;
    }
    .glass-card:hover { transform: translateY(-5px); border-color: rgba(255, 255, 255, 0.3); }
    
    /* Indikator Menyala (Glowing Pulse) */
    .badge-glowing-green {
        background: rgba(16, 185, 129, 0.15);
        color: #10B981;
        border: 1px solid #10B981;
        box-shadow: 0 0 15px rgba(16, 185, 129, 0.5);
        padding: 8px 25px;
        border-radius: 30px;
        font-weight: 700;
        letter-spacing: 1.5px;
        font-size: 0.85em;
        text-transform: uppercase;
        animation: pulse-green 2s infinite;
        display: inline-block;
        margin-bottom: 20px;
    }
    @keyframes pulse-green {
        0% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0.7); }
        70% { box-shadow: 0 0 0 12px rgba(16, 185, 129, 0); }
        100% { box-shadow: 0 0 0 0 rgba(16, 185, 129, 0); }
    }
    
    /* Indikator Merah Elegan (Standby) */
    .badge-red {
        background: rgba(239, 68, 68, 0.05);
        color: #EF4444;
        border: 1px solid rgba(239, 68, 68, 0.3);
        padding: 8px 25px;
        border-radius: 30px;
        font-weight: 600;
        letter-spacing: 1.5px;
        font-size: 0.85em;
        text-transform: uppercase;
        display: inline-block;
        margin-bottom: 20px;
    }
    
    /* Tipografi Premium */
    .waktu-teks { font-size: 3.5rem; font-weight: 800; color: #ffffff; margin: 5px 0; line-height: 1; text-shadow: 0 2px 10px rgba(0,0,0,0.5); }
    .label-teks { font-size: 0.85rem; color: #94a3b8; text-transform: uppercase; letter-spacing: 1.5px; font-weight: 600; }
    .antrean-teks { font-size: 1.1rem; color: #cbd5e1; margin-top: 15px; font-weight: 500; }
    .highlight-antrean { color: #FBBF24; font-weight: 800; font-size: 1.2rem; }
    
    /* Mempercantik Judul Jalur */
    .jalur-title { font-size: 1.3rem; color: #38BDF8; font-weight: 800; letter-spacing: 2px; text-transform: uppercase; margin-bottom: 15px; }
</style>
""", unsafe_allow_html=True)

# Ini agar data angka kendaraan dan pengaturan tidak hilang saat kita pindah-pindah menu/halaman
if 'utara' not in st.session_state: st.session_state.utara = 45
if 'selatan' not in st.session_state: st.session_state.selatan = 12
if 'timur' not in st.session_state: st.session_state.timur = 8
if 'barat' not in st.session_state: st.session_state.barat = 25
if 'min_hijau' not in st.session_state: st.session_state.min_hijau = 15
if 'max_hijau' not in st.session_state: st.session_state.max_hijau = 60

# Fungsi untuk menghitung logika logika fuzzy buatan (TDS)
def hitung_tds_dan_waktu(u, s, t, b, min_h, max_h):
    total = max(u + s + t + b, 1) # Cegah error bagi 0
    data = {
        "UTARA": {"jumlah": u, "tds": (u/total)*100},
        "SELATAN": {"jumlah": s, "tds": (s/total)*100},
        "TIMUR": {"jumlah": t, "tds": (t/total)*100},
        "BARAT": {"jumlah": b, "tds": (b/total)*100}
    }
    prioritas = max(data, key=lambda k: data[k]["jumlah"])
    
    # Aturan Waktu Sederhana berdasarkan TDS
    waktu = {}
    for arah in data:
        jml = data[arah]["jumlah"]
        if jml < 15: w = min_h
        elif jml < 40: w = min_h + 15
        elif jml < 70: w = max_h - 15
        else: w = max_h
        waktu[arah] = w
        
    return data, prioritas, waktu

# Hitung data saat ini berdasarkan memori
data_jalur, jalur_prioritas, waktu_hijau = hitung_tds_dan_waktu(
    st.session_state.utara, st.session_state.selatan, 
    st.session_state.timur, st.session_state.barat,
    st.session_state.min_hijau, st.session_state.max_hijau
)

st.sidebar.title("🚦 INTELTRAFF Menu")
menu = st.sidebar.radio("Pilih Layar (Screen):", [
    "1. Dashboard Utama", 
    "2. Panel Input Kamera", 
    "3. Analisis Logika (TDS)", 
    "4. Perbandingan Kinerja", 
    "5. Pengaturan Sistem"
])
st.sidebar.divider()
st.sidebar.caption("Simulasi PKM-KC / LITERA 2026")

if menu == "1. Dashboard Utama":
    # Menambahkan Background Image dengan pemanggil yang lebih kuat (data-testid)
    try:
        with open("Gemini_Generated_Image_208wzs208wzs208w.jfif", "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(rgba(15, 23, 42, 0.65), rgba(15, 23, 42, 0.85)), url("data:image/jpeg;base64,{b64}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("⚠️ File gambar 'Gemini_Generated_Image_208wzs208wzs208w.jfif' tidak ditemukan di folder yang sama dengan app.py")

    st.markdown('<h1 style="text-align: center; font-weight: 900; color: white; letter-spacing: 2px; margin-bottom: 0px; text-shadow: 0px 4px 15px rgba(0,0,0,0.6);">🌍 INTELTRAFF CORE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #38bdf8; font-size: 1.1rem; font-weight: 600; letter-spacing: 1px; margin-bottom: 40px;">Live AI Traffic Density Control Center</p>', unsafe_allow_html=True)
    
    # Fungsi pembantu untuk membuat Kartu Kaca (Glass Card) agar kode lebih rapi
    def render_card(jalur, is_prioritas, waktu, antrean):
        status = "🟢 ACTIVE" if is_prioritas else "🔴 STANDBY"
        badge_class = "badge-glowing-green" if is_prioritas else "badge-red"
        border_color = "#10B981" if is_prioritas else "rgba(255,255,255,0.1)"
        
        return f'''
        <div class="glass-card" style="border-top: 5px solid {border_color};">
            <div class="jalur-title">{jalur}</div>
            <div class="{badge_class}">{status}</div>
            <div class="label-teks">Durasi Lampu Hijau</div>
            <div class="waktu-teks">{waktu}s</div>
            <div class="antrean-teks">Antrean Kendaraan: <span class="highlight-antrean">{antrean}</span> 🚗</div>
        </div>
        '''
        
    col_u_kosong, col_u, col_u_kosong2 = st.columns([1, 1.5, 1])
    with col_u:
        st.markdown(render_card("Jalur Utara", jalur_prioritas == "UTARA", waktu_hijau["UTARA"], st.session_state.utara), unsafe_allow_html=True)
        
    col_b, col_tengah, col_t = st.columns([1.5, 0.5, 1.5])
    with col_b:
        st.markdown(render_card("Jalur Barat", jalur_prioritas == "BARAT", waktu_hijau["BARAT"], st.session_state.barat), unsafe_allow_html=True)
    with col_tengah:
        st.markdown('<div style="text-align:center; padding-top:80px; opacity: 0.3;"><h1 style="font-size: 5rem; margin:0; color:white;">+</h1></div>', unsafe_allow_html=True)
    with col_t:
        st.markdown(render_card("Jalur Timur", jalur_prioritas == "TIMUR", waktu_hijau["TIMUR"], st.session_state.timur), unsafe_allow_html=True)

    col_s_kosong, col_s, col_s_kosong2 = st.columns([1, 1.5, 1])
    with col_s:
        st.markdown(render_card("Jalur Selatan", jalur_prioritas == "SELATAN", waktu_hijau["SELATAN"], st.session_state.selatan), unsafe_allow_html=True)

elif menu == "2. Panel Input Kamera":
    # Menyiapkan Background Khusus Screen 2
    try:
        with open("Gemini_Generated_Image_c7d3v3c7d3v3c7d3.jfif", "rb") as f:
            data2 = f.read()
        b64_2 = base64.b64encode(data2).decode()
        st.markdown(
            f"""
            <style>
            /* Gradien dari kiri (gelap) ke kanan (bening) agar tiang lampu di kanan tetap terlihat */
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(to right, rgba(15, 23, 42, 0.95) 20%, rgba(15, 23, 42, 0.4) 100%), url("data:image/jpeg;base64,{b64_2}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Customisasi Slider agar lebih besar, tebal, dan premium (Glowing) */
            div.stSlider > div[data-baseweb="slider"] > div > div {{
                height: 12px !important; /* Jalur slider lebih tebal */
                border-radius: 10px;
            }}
            div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {{
                height: 26px !important; 
                width: 26px !important; 
                background-color: #38bdf8 !important; /* Warna biru cyan */
                border: 3px solid #ffffff !important;
                box-shadow: 0 0 15px rgba(56, 189, 248, 0.8) !important; /* Efek neon/menyala */
                cursor: grab;
            }}
            div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]:active {{
                cursor: grabbing;
                box-shadow: 0 0 25px rgba(56, 189, 248, 1) !important; /* Nyala lebih terang saat ditarik */
            }}
            
            /* Mempercantik kotak angka nilai (Value Box) saat digeser */
            div[data-testid="stThumbValue"] {{
                font-size: 1.1rem !important;
                font-weight: 800 !important;
                color: #10B981 !important; 
                background: rgba(15, 23, 42, 0.8) !important;
                padding: 4px 10px !important;
                border-radius: 8px !important;
                border: 1px solid #10B981 !important;
            }}
            
            /* Tipografi Judul Label Custom */
            .slider-label-custom {{
                font-size: 1.2rem;
                font-weight: 700;
                color: #f1f5f9;
                margin-bottom: -15px;
                letter-spacing: 1.5px;
                text-transform: uppercase;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("⚠️ File gambar 'Gemini_Generated_Image_c7d3v3c7d3v3c7d3.jfif' tidak ditemukan di folder yang sama.")

    st.markdown('<h1 style="color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">📷 Panel Input Kamera (Vision Layer)</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 40px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">Halaman ini menyimulasikan data kepadatan (0-100 kendaraan) yang dikirim dari sistem Vision AI lapangan ke <i>Control Center</i>.</p>', unsafe_allow_html=True)
    
    # Membuat layout agar slider terfokus di kiri dan tengah, membiarkan gambar kanan terlihat
    col1, col_gap, col2, col_kosong = st.columns([1, 0.1, 1, 0.5])
    
    with col1:
        st.markdown('<p class="slider-label-custom">🚙 Kepadatan Utara</p>', unsafe_allow_html=True)
        # label_visibility="collapsed" menyembunyikan label bawaan yang kecil
        st.session_state.utara = st.slider("Utara", 0, 100, st.session_state.utara, key="s_u", label_visibility="collapsed")
        
        st.write("") # Spasi
        st.write("")
        st.markdown('<p class="slider-label-custom">🚙 Kepadatan Barat</p>', unsafe_allow_html=True)
        st.session_state.barat = st.slider("Barat", 0, 100, st.session_state.barat, key="s_b", label_visibility="collapsed")
        
    with col2:
        st.markdown('<p class="slider-label-custom">🚙 Kepadatan Selatan</p>', unsafe_allow_html=True)
        st.session_state.selatan = st.slider("Selatan", 0, 100, st.session_state.selatan, key="s_s", label_visibility="collapsed")
        
        st.write("")
        st.write("")
        st.markdown('<p class="slider-label-custom">🚙 Kepadatan Timur</p>', unsafe_allow_html=True)
        st.session_state.timur = st.slider("Timur", 0, 100, st.session_state.timur, key="s_t", label_visibility="collapsed")
    
    st.markdown("""
    <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 15px; border-radius: 8px; margin-top: 50px; backdrop-filter: blur(5px);">
        <span style="color: #10B981; font-weight: bold; letter-spacing: 1px;">💡 INFO SISTEM:</span> 
        <span style="color: #cbd5e1; margin-left: 10px;">Setelah mengatur simulasi kepadatan di sini, silakan kembali ke menu <b>1. Dashboard Utama</b> untuk melihat algoritma INTELTRAFF mengambil keputusan pembagian lampu hijau secara <i>real-time</i>.</span>
    </div>
    """, unsafe_allow_html=True)

elif menu == "3. Analisis Logika (TDS)":
    st.title("🧠 Screen 3: Decision Layer (Logika Pengambilan Keputusan)")
    st.write("Menampilkan bagaimana sistem menghitung Traffic Density Score (TDS) dan menentukan jalur prioritas.")
    
    st.subheader(f"Jalur Prioritas Saat Ini: **{jalur_prioritas}**")
    
    # Menyiapkan data untuk tabel
    df_tds = pd.DataFrame({
        "Jalur": ["Utara", "Selatan", "Timur", "Barat"],
        "Jumlah Kendaraan": [st.session_state.utara, st.session_state.selatan, st.session_state.timur, st.session_state.barat],
        "TDS (%)": [f"{data_jalur['UTARA']['tds']:.1f}%", f"{data_jalur['SELATAN']['tds']:.1f}%", f"{data_jalur['TIMUR']['tds']:.1f}%", f"{data_jalur['BARAT']['tds']:.1f}%"],
        "Keputusan Lampu Hijau": [f"{waktu_hijau['UTARA']} Detik", f"{waktu_hijau['SELATAN']} Detik", f"{waktu_hijau['TIMUR']} Detik", f"{waktu_hijau['BARAT']} Detik"]
    })
    st.table(df_tds)
    
    with st.expander("Lihat Rumus TDS"):
        st.latex(r"TDS_i = \left( \frac{Kendaraan_i}{Total\_Kendaraan} \right) \times 100\%")

elif menu == "4. Perbandingan Kinerja":
    st.title("📊 Screen 4: Validasi & Perbandingan Kinerja")
    st.write("Membuktikan efisiensi sistem INTELTRAFF dibandingkan sistem lampu konvensional.")
    
    waktu_konvensional = 40 # Asumsi lampu biasa 40 detik tiap jalur (tetap)
    waktu_konvensional_total = waktu_konvensional * 4
    waktu_inteltraff_total = sum(waktu_hijau.values())
    
    col_chart, col_metrik = st.columns([2, 1])
    
    with col_chart:
        # Membuat Data Grafik Batang
        chart_data = pd.DataFrame(
            {
                "Durasi Hijau (Detik)": [waktu_konvensional, waktu_hijau["UTARA"], waktu_konvensional, waktu_hijau["SELATAN"], waktu_konvensional, waktu_hijau["TIMUR"], waktu_konvensional, waktu_hijau["BARAT"]],
                "Sistem": ["Konvensional", "INTELTRAFF", "Konvensional", "INTELTRAFF", "Konvensional", "INTELTRAFF", "Konvensional", "INTELTRAFF"],
                "Jalur": ["Utara", "Utara", "Selatan", "Selatan", "Timur", "Timur", "Barat", "Barat"]
            }
        )
        st.bar_chart(chart_data, x="Jalur", y="Durasi Hijau (Detik)", color="Sistem")
        
    with col_metrik:
        st.metric("Total Waktu Siklus (Konvensional)", f"{waktu_konvensional_total} Detik")
        st.metric("Total Waktu Siklus (INTELTRAFF)", f"{waktu_inteltraff_total} Detik", f"{waktu_konvensional_total - waktu_inteltraff_total} Detik Dihemat", delta_color="normal")
        if waktu_inteltraff_total < waktu_konvensional_total:
            st.success("Kesimpulan: INTELTRAFF berhasil menghemat waktu tunggu siklus persimpangan!")
        else:
            st.warning("Kesimpulan: Lalu lintas sedang sangat padat di seluruh jalur.")

elif menu == "5. Pengaturan Sistem":
    st.title("⚙️ Screen 5: Konfigurasi Parameter")
    st.write("Pengaturan batas keselamatan untuk mencegah durasi lampu yang tidak masuk akal.")
    
    st.session_state.min_hijau = st.number_input("Batas Minimum Lampu Hijau (Detik) - Jalur Sepi", min_value=5, max_value=30, value=st.session_state.min_hijau)
    st.session_state.max_hijau = st.number_input("Batas Maksimum Lampu Hijau (Detik) - Jalur Macet Total", min_value=45, max_value=120, value=st.session_state.max_hijau)
    
    st.info("Data ini akan langsung memperbarui kalkulasi di layar Analisis Logika.")