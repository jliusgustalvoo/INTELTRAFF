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
                background-image: linear-gradient(to right, rgba(15, 23, 42, 0.95) 20%, rgba(15, 23, 42, 0.3) 100%), url("data:image/jpeg;base64,{b64_2}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* 1. KOTAK MODUL SLIDER (Membungkus Slider agar rapi) */
            div.stSlider {{
                background: linear-gradient(145deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
                padding: 25px 25px 20px 25px;
                border-radius: 0 16px 16px 16px;
                border: 1px solid rgba(56, 189, 248, 0.2);
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                margin-top: -5px; /* Menempel dengan label tab di atasnya */
                margin-bottom: 25px;
            }}

            /* 2. JALUR SLIDER (Track) */
            div.stSlider > div[data-baseweb="slider"] > div > div {{
                height: 10px !important; 
                background-color: rgba(255, 255, 255, 0.08) !important;
                border-radius: 10px;
                box-shadow: inset 0 2px 5px rgba(0,0,0,0.5) !important;
            }}

            /* 3. TOMBOL GESER (Thumb) bergaya Kenop Canggih */
            div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"] {{
                height: 28px !important; 
                width: 28px !important; 
                background: radial-gradient(circle, #38bdf8 30%, #0284c7 100%) !important; 
                border: 2px solid #e0f2fe !important;
                box-shadow: 0 0 15px rgba(56, 189, 248, 0.6), inset 0 0 5px rgba(255, 255, 255, 0.9) !important; 
                cursor: grab;
                transition: transform 0.15s ease, box-shadow 0.15s ease;
            }}
            /* Efek saat cursor di atas tombol */
            div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]:hover {{
                transform: scale(1.15);
                box-shadow: 0 0 25px rgba(56, 189, 248, 0.9) !important; 
            }}
            /* Efek saat tombol ditarik */
            div.stSlider > div[data-baseweb="slider"] > div > div > div[role="slider"]:active {{
                cursor: grabbing;
                transform: scale(0.95);
                box-shadow: 0 0 35px rgba(56, 189, 248, 1) !important; 
            }}
            
            /* 4. ANGKA POP-UP (LED Display Style) */
            div[data-testid="stThumbValue"] {{
                font-family: 'Courier New', Courier, monospace !important;
                font-size: 1.2rem !important;
                font-weight: 900 !important;
                color: #0f172a !important; 
                background: #38bdf8 !important;
                padding: 6px 14px !important;
                border-radius: 8px !important;
                box-shadow: 0 5px 15px rgba(56, 189, 248, 0.4) !important;
                border: none !important;
                margin-bottom: 8px !important;
            }}
            
            /* 5. TAB LABEL CUSTOM */
            .slider-label-custom {{
                font-size: 0.9rem;
                font-weight: 800;
                color: #38bdf8;
                background: linear-gradient(145deg, rgba(30, 41, 59, 0.9), rgba(15, 23, 42, 1));
                padding: 10px 25px;
                border-radius: 12px 12px 0 0;
                margin-bottom: 0px;
                letter-spacing: 2px;
                text-transform: uppercase;
                border: 1px solid rgba(56, 189, 248, 0.2);
                border-bottom: none;
                display: inline-block;
                box-shadow: 0 -5px 15px rgba(0,0,0,0.2);
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("⚠️ File gambar 'Gemini_Generated_Image_c7d3v3c7d3v3c7d3.jfif' tidak ditemukan di folder yang sama.")

    st.markdown('<h1 style="color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">📷 Panel Input Kamera (Vision Layer)</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">Simulasi pengiriman data kepadatan kendaraan (0-100) dari CCTV pintar lapangan ke <i>Control Center</i>.</p>', unsafe_allow_html=True)
    
    col1, col_gap, col2, col_kosong = st.columns([1, 0.1, 1, 0.5])
    
    with col1:
        st.markdown('<div class="slider-label-custom">🚙 FEED KAMERA UTARA</div>', unsafe_allow_html=True)
        st.session_state.utara = st.slider("Utara", 0, 100, st.session_state.utara, key="s_u", label_visibility="collapsed")
        
        st.markdown('<div class="slider-label-custom">🚙 FEED KAMERA BARAT</div>', unsafe_allow_html=True)
        st.session_state.barat = st.slider("Barat", 0, 100, st.session_state.barat, key="s_b", label_visibility="collapsed")
        
    with col2:
        st.markdown('<div class="slider-label-custom">🚙 FEED KAMERA SELATAN</div>', unsafe_allow_html=True)
        st.session_state.selatan = st.slider("Selatan", 0, 100, st.session_state.selatan, key="s_s", label_visibility="collapsed")
        
        st.markdown('<div class="slider-label-custom">🚙 FEED KAMERA TIMUR</div>', unsafe_allow_html=True)
        st.session_state.timur = st.slider("Timur", 0, 100, st.session_state.timur, key="s_t", label_visibility="collapsed")
    
    st.markdown("""
    <div style="background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; padding: 15px; border-radius: 8px; margin-top: 30px; backdrop-filter: blur(5px);">
        <span style="color: #38bdf8; font-weight: bold; letter-spacing: 1px;">💡 SISTEM AKTIF:</span> 
        <span style="color: #cbd5e1; margin-left: 10px;">Perubahan data pada panel ini akan langsung ditransmisikan dan diproses oleh algoritma Fuzzy di <b>1. Dashboard Utama</b>.</span>
    </div>
    """, unsafe_allow_html=True)

elif menu == "3. Analisis Logika (TDS)":
    try:
        with open("Gemini_Generated_Image_bv9ofxbv9ofxbv9o.jfif", "rb") as f:
            data3 = f.read()
        b64_3 = base64.b64encode(data3).decode()
        st.markdown(
            f"""
            <style>
            /* Latar belakang dengan gradasi agar teks di kiri terbaca, lampu di kanan tetap bersinar */
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(to right, rgba(15, 23, 42, 0.95) 40%, rgba(15, 23, 42, 0.4) 100%), url("data:image/jpeg;base64,{b64_3}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Desain Kotak Penjelasan (Panel Kaca) */
            .info-panel {{
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
                border-left: 5px solid #38bdf8;
                border-radius: 12px;
                padding: 25px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(10px);
                margin-bottom: 30px;
                color: #cbd5e1;
            }}
            .info-title {{
                color: #38bdf8;
                font-size: 1.2rem;
                font-weight: 800;
                margin-bottom: 15px;
                letter-spacing: 1px;
                text-transform: uppercase;
            }}
            .info-highlight {{
                color: #10B981;
                font-weight: bold;
            }}
            
            /* Kustomisasi Tabel */
            [data-testid="stTable"] {{
                background-color: rgba(15, 23, 42, 0.7);
                border-radius: 10px;
                overflow: hidden;
            }}
            th {{ background-color: rgba(56, 189, 248, 0.2) !important; color: #38bdf8 !important; font-size: 1.1rem !important; text-align: center !important; }}
            td {{ color: #ffffff !important; font-size: 1.1rem !important; text-align: center !important; font-weight: 500; }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("⚠️ File gambar 'Gemini_Generated_Image_bv9ofxbv9ofxbv9o.jfif' tidak ditemukan.")

    st.markdown('<h1 style="color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">🧠 Decision Layer (Logika Inti)</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="info-panel">
        <div class="info-title">Bagaimana INTELTRAFF Mengambil Keputusan?</div>
        <p style="font-size: 1.05rem; line-height: 1.6;">
            Sistem ini tidak hanya melihat "jumlah", tetapi menggunakan <b>Traffic Density Score (TDS)</b> untuk mengukur keadilan. Berikut adalah alur kerjanya:
        </p>
        <ol style="font-size: 1.05rem; line-height: 1.8; margin-left: 20px;">
            <li><b>Jumlah Kendaraan (Data Masuk):</b> Sistem menghitung total mobil di semua arah (Utara + Selatan + Timur + Barat).</li>
            <li><b>TDS (Kalkulasi Persentase):</b> Sistem menghitung seberapa besar "porsi" kemacetan suatu jalur dibandingkan total kemacetan simpang. <br><i>(Contoh: Jika di Utara ada 50 mobil dari total 100 mobil di simpang, maka TDS Utara = 50%).</i> Jalur dengan TDS tertinggi akan menjadi <span class="info-highlight">Jalur Prioritas</span>.</li>
            <li><b>Keputusan Waktu Hijau (Eksekusi):</b> Setelah jalur diprioritaskan, sistem memberikan durasi detiknya secara dinamis. Jika sangat padat, durasi bisa menyentuh batas maksimum. Jika sepi, dipotong ke batas minimum agar tidak ada antrean kosong.</li>
        </ol>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'''
        <div style="background: rgba(16, 185, 129, 0.15); border: 1px solid #10B981; padding: 15px; border-radius: 10px; text-align: center; margin-bottom: 25px;">
            <span style="color: #cbd5e1; font-size: 1.1rem;">Status Saat Ini: Jalur Prioritas diberikan kepada </span>
            <strong style="color: #10B981; font-size: 1.3rem; letter-spacing: 2px;">{jalur_prioritas}</strong>
        </div>
    ''', unsafe_allow_html=True)
    
    # Menyiapkan data untuk tabel
    df_tds = pd.DataFrame({
        "JALUR": ["Utara", "Selatan", "Timur", "Barat"],
        "JUMLAH KENDARAAN": [st.session_state.utara, st.session_state.selatan, st.session_state.timur, st.session_state.barat],
        "TDS (%)": [f"{data_jalur['UTARA']['tds']:.1f}%", f"{data_jalur['SELATAN']['tds']:.1f}%", f"{data_jalur['TIMUR']['tds']:.1f}%", f"{data_jalur['BARAT']['tds']:.1f}%"],
        "DURASI LAMPU HIJAU": [f"{waktu_hijau['UTARA']} Detik", f"{waktu_hijau['SELATAN']} Detik", f"{waktu_hijau['TIMUR']} Detik", f"{waktu_hijau['BARAT']} Detik"]
    })
    
    # Menampilkan Tabel yang sudah dikustomisasi melalui CSS di atas
    st.table(df_tds)
    
    with st.expander("Klik untuk melihat Rumus Matematis TDS", expanded=False):
        st.latex(r"TDS_i = \left( \frac{Kendaraan_i}{\sum_{j=1}^{4} Kendaraan_j} \right) \times 100\%")
        st.info("Keterangan: TDS dari jalur ke-i adalah jumlah kendaraan di jalur tersebut dibagi dengan total seluruh kendaraan di simpang, dikali 100 persen.")

elif menu == "4. Perbandingan Kinerja":
    try:
        with open("Lampu Hijau di Persimpangan Kota Basah.png", "rb") as f:
            data4 = f.read()
        b64_4 = base64.b64encode(data4).decode()
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(to right, rgba(15, 23, 42, 0.95) 30%, rgba(15, 23, 42, 0.4) 100%), url("data:image/png;base64,{b64_4}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            /* Custom Card untuk Metrik Kinerja */
            .metric-card {{
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.8), rgba(15, 23, 42, 0.9));
                border-top: 4px solid #38bdf8;
                border-radius: 12px;
                padding: 20px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.5);
                backdrop-filter: blur(10px);
                text-align: center;
                margin-bottom: 20px;
            }}
            .metric-title {{ color: #94a3b8; font-size: 0.9rem; text-transform: uppercase; letter-spacing: 1px; margin-bottom: 10px; font-weight: 700; }}
            .metric-value {{ color: #ffffff; font-size: 2.5rem; font-weight: 900; margin-bottom: 5px; text-shadow: 0 2px 10px rgba(0,0,0,0.3); }}
            .metric-delta {{ color: #10B981; font-size: 1.1rem; font-weight: 700; background: rgba(16, 185, 129, 0.15); padding: 5px 15px; border-radius: 20px; display: inline-block; }}
            .metric-delta-negative {{ color: #EF4444; font-size: 1.1rem; font-weight: 700; background: rgba(239, 68, 68, 0.15); padding: 5px 15px; border-radius: 20px; display: inline-block; }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("⚠️ File gambar 'Lampu Hijau di Persimpangan Kota Basah.png' tidak ditemukan.")

    st.markdown('<h1 style="color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">📊 Validasi Kinerja Sistem</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">Membuktikan efisiensi algoritma INTELTRAFF dibandingkan sistem lampu lalu lintas konvensional (waktu tetap) berdasarkan total waktu tunggu siklus.</p>', unsafe_allow_html=True)
    
    waktu_konvensional = 40 # Asumsi lampu biasa 40 detik tiap jalur (tetap)
    waktu_konvensional_total = waktu_konvensional * 4
    waktu_inteltraff_total = sum(waktu_hijau.values())
    penghematan = waktu_konvensional_total - waktu_inteltraff_total
    
    col_chart, col_gap, col_metrik = st.columns([2.2, 0.1, 1])
    
    with col_chart:
        # Membungkus grafik dalam panel kaca agar rapi
        st.markdown('<div style="background: rgba(15, 23, 42, 0.7); padding: 20px; border-radius: 12px; border: 1px solid rgba(255,255,255,0.05); backdrop-filter: blur(10px);">', unsafe_allow_html=True)
        
        # Menyiapkan Data
        chart_data = pd.DataFrame({
            "Jalur": ["Utara", "Utara", "Selatan", "Selatan", "Timur", "Timur", "Barat", "Barat"],
            "Sistem": ["Konvensional", "INTELTRAFF", "Konvensional", "INTELTRAFF", "Konvensional", "INTELTRAFF", "Konvensional", "INTELTRAFF"],
            "Durasi Hijau (Detik)": [waktu_konvensional, waktu_hijau["UTARA"], waktu_konvensional, waktu_hijau["SELATAN"], waktu_konvensional, waktu_hijau["TIMUR"], waktu_konvensional, waktu_hijau["BARAT"]]
        })
        
        # Membuat Grafik Profesional dengan Altair
        import altair as alt
        bars = alt.Chart(chart_data).mark_bar(
            cornerRadiusTopLeft=6, 
            cornerRadiusTopRight=6,
            size=30 # Lebar batang
        ).encode(
            x=alt.X('Jalur:N', title=None, axis=alt.Axis(labelAngle=0, labelColor='#cbd5e1', labelFontSize=13, labelPadding=10)),
            y=alt.Y('Durasi Hijau (Detik):Q', title='Durasi Hijau (Detik)', axis=alt.Axis(gridColor='rgba(255,255,255,0.05)', titleColor='#94a3b8', labelColor='#cbd5e1')),
            color=alt.Color('Sistem:N', 
                            scale=alt.Scale(domain=['Konvensional', 'INTELTRAFF'], range=['#64748b', '#10B981']),
                            legend=alt.Legend(title=None, labelColor='#cbd5e1', orient='top', symbolType='circle', labelFontSize=12)),
            xOffset='Sistem:N', # Memisahkan batang agar bersebelahan (Grouped Bar Chart)
            tooltip=['Jalur', 'Sistem', 'Durasi Hijau (Detik)']
        ).properties(
            height=400,
            background='transparent'
        ).configure_view(strokeWidth=0) # Menghilangkan garis tepi kotak grafik
        
        st.altair_chart(bars, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col_metrik:
        # Kartu Metrik Sistem Lama
        st.markdown(f'''
        <div class="metric-card" style="border-top-color: #64748b;">
            <div class="metric-title">Siklus Konvensional</div>
            <div class="metric-value">{waktu_konvensional_total}s</div>
            <div style="color: #94a3b8; font-size: 0.85rem; margin-top: 5px;">Waktu tunggu tetap (40s/jalur)</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Menghitung gaya teks dinamis untuk penghematan
        delta_class = "metric-delta" if penghematan > 0 else ("metric-delta" if penghematan == 0 else "metric-delta-negative")
        delta_text = f"↓ Hemat {abs(penghematan)} Detik" if penghematan > 0 else (f"Sama Persis" if penghematan == 0 else f"↑ Ekstra {abs(penghematan)} Detik")
        
        # Kartu Metrik Sistem INTELTRAFF
        st.markdown(f'''
        <div class="metric-card" style="border-top-color: #10B981;">
            <div class="metric-title">Siklus INTELTRAFF</div>
            <div class="metric-value" style="color: #10B981;">{waktu_inteltraff_total}s</div>
            <div class="{delta_class}">{delta_text}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Kesimpulan Otomatis (AI Insight)
        if penghematan > 0:
            st.markdown(f'''
            <div style="background: rgba(16, 185, 129, 0.1); border-left: 4px solid #10B981; padding: 15px; border-radius: 8px; color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                <span style="color: #10B981; font-weight: bold;">✔ Kesimpulan:</span> Algoritma terbukti <b>mengurangi waktu tunggu siklus hingga {penghematan} detik</b>. Sangat efisien dalam mengurai kemacetan tanpa membuang waktu di jalur yang kosong.
            </div>
            ''', unsafe_allow_html=True)
        elif penghematan == 0:
             st.markdown('''
            <div style="background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; padding: 15px; border-radius: 8px; color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                <span style="color: #38bdf8; font-weight: bold;">⚖️ Kesimpulan:</span> Kepadatan lalu lintas terpantau seimbang di semua jalur. Sistem berjalan normal layaknya waktu konvensional.
            </div>
            ''', unsafe_allow_html=True)
        else:
            st.markdown(f'''
            <div style="background: rgba(245, 158, 11, 0.1); border-left: 4px solid #F59E0B; padding: 15px; border-radius: 8px; color: #cbd5e1; font-size: 0.95rem; line-height: 1.5;">
                <span style="color: #F59E0B; font-weight: bold;">⚠️ Status Ekstrem:</span> Volume kendaraan sangat padat merata. Sistem mengalokasikan waktu ekstra <b>{abs(penghematan)} detik</b> demi keselamatan dan penguraian antrean panjang.
            </div>
            ''', unsafe_allow_html=True)

elif menu == "5. Pengaturan Sistem":
    try:
        with open("Gemini_Generated_Image_ihrd8qihrd8qihrd.png", "rb") as f:
            data5 = f.read()
        b64_5 = base64.b64encode(data5).decode()
        
        st.markdown(
            f"""
            <style>
            /* Latar belakang dengan gradasi gelap agar teks dan panel penutup terlihat mewah */
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(to right, rgba(15, 23, 42, 0.95) 40%, rgba(15, 23, 42, 0.5) 100%), url("data:image/jpeg;base64,{b64_5}");
                background-size: cover;
                background-position: center;
                background-attachment: fixed;
            }}
            
            /* Kustomisasi Input Angka (Number Input) */
            .stNumberInput > div > div > input {{
                color: #ffffff !important;
                background-color: rgba(30, 41, 59, 0.8) !important;
                border: 1px solid #38bdf8 !important;
                border-radius: 8px !important;
                font-size: 1.1rem !important;
            }}
            .stNumberInput label {{
                color: #cbd5e1 !important;
                font-weight: 600 !important;
                letter-spacing: 1px !important;
            }}
            
            /* Panel Penutup (Closing Statement Card) */
            .closing-panel {{
                background: linear-gradient(135deg, rgba(30, 41, 59, 0.85), rgba(15, 23, 42, 0.95));
                border-left: 5px solid #F59E0B;
                border-radius: 12px;
                padding: 30px;
                box-shadow: 0 10px 30px rgba(0, 0, 0, 0.6);
                backdrop-filter: blur(12px);
                margin-top: 40px;
                color: #e2e8f0;
                border-top: 1px solid rgba(255,255,255,0.05);
            }}
            .closing-title {{
                color: #F59E0B;
                font-size: 1.4rem;
                font-weight: 800;
                margin-bottom: 20px;
                letter-spacing: 1.5px;
                text-transform: uppercase;
                border-bottom: 1px solid rgba(245, 158, 11, 0.3);
                padding-bottom: 10px;
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    except FileNotFoundError:
        st.error("⚠️ File gambar 'Gemini_Generated_Image_ihrd8qihrd8qihrd.jpg' tidak ditemukan.")

    st.markdown('<h1 style="color: white; text-shadow: 0 2px 10px rgba(0,0,0,0.5);">⚙️ Konfigurasi Keselamatan & Visi</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: #94a3b8; font-size: 1.1rem; margin-bottom: 30px; border-bottom: 1px solid rgba(255,255,255,0.1); padding-bottom: 15px;">Pengaturan batas aman <i>(Safety Constraints)</i> untuk mencegah durasi lampu hijau yang terlalu singkat atau terlalu lama.</p>', unsafe_allow_html=True)
    
    col_set1, col_set_gap, col_set2 = st.columns([1, 0.1, 1])
    
    with col_set1:
        st.session_state.min_hijau = st.number_input("Batas Minimum Lampu Hijau (Detik) - Jalur Sepi", min_value=5, max_value=30, value=st.session_state.min_hijau)
    with col_set2:
        st.session_state.max_hijau = st.number_input("Batas Maksimum Lampu Hijau (Detik) - Jalur Macet Total", min_value=45, max_value=120, value=st.session_state.max_hijau)
        
    st.markdown('''
    <div style="background: rgba(56, 189, 248, 0.1); border-left: 4px solid #38bdf8; padding: 15px; border-radius: 8px; color: #cbd5e1; font-size: 0.95rem; margin-top: 10px;">
        <span style="color: #38bdf8; font-weight: bold;">💡 Info Real-Time:</span> Data parameter ini terhubung langsung dengan Otak Sistem di <b>Screen 3 (Analisis Logika)</b>. Perubahan di sini akan otomatis memperbarui kalkulasi algoritma seketika.
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('''
    <div class="closing-panel">
        <div class="closing-title">Membawa Inovasi Menuju Ekosistem "Smart City"</div>
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify;">
            <strong>INTELTRAFF</strong> bukan sekadar purwarupa pengatur lampu lalu lintas biasa. Gagasan ini lahir dari urgensi untuk menghadirkan keadilan dan efisiensi waktu di persimpangan jalan raya. Dengan memadukan potensi teknologi <i>Vision AI</i> (Pemrosesan Citra) dan algoritma <i>Fuzzy Logic</i>, kami menawarkan transisi dari sistem konvensional yang kaku menuju ekosistem <strong>Smart City</strong> yang dinamis dan adaptif.
        </p>
        <p style="font-size: 1.1rem; line-height: 1.8; text-align: justify; margin-top: 15px;">
            Melalui pendekatan simulasi <i>Software-in-the-Loop</i> (SITL) pada purwarupa web interaktif ini, kami membuktikan secara kuantitatif bahwa kecerdasan buatan mampu menekan total waktu tunggu antrean secara signifikan tanpa mengabaikan aspek keselamatan berkendara. Inovasi ini merupakan wujud nyata komitmen mahasiswa <strong>Institut Teknologi Sumatera (ITERA)</strong> untuk berkontribusi dalam mengurai kemacetan, mereduksi emisi karbon gas buang akibat idel kendaraan, serta mendukung tercapainya <strong>SDG 9: Industri, Inovasi, dan Infrastruktur</strong>.
        </p>
    </div>
    ''', unsafe_allow_html=True)