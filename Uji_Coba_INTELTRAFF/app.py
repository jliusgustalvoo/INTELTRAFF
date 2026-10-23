import streamlit as st
import pandas as pd
import base64
import os
import time

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

# Fungsi untuk menghitung logika fuzzy buatan (TDS)
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

# Hitung data saat ini berdasarkan memori (Tanda kurung tutup ditambahkan di sini)
data_jalur, jalur_prioritas, waktu_hijau = hitung_tds_dan_waktu(
    st.session_state.utara, st.session_state.selatan, 
    st.session_state.timur, st.session_state.barat,
    st.session_state.min_hijau, st.session_state.max_hijau
)

def set_background(image_file, opacity=0.85):
    try:
        with open(image_file, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(
            f"""
            <style>
            [data-testid="stAppViewContainer"] {{
                background-image: linear-gradient(rgba(15, 23, 42, {opacity}), rgba(15, 23, 42, {opacity})), url("data:image/jpeg;base64,{b64}");
                background-size: cover; background-position: center; background-attachment: fixed;
            }}
            </style>
            """, unsafe_allow_html=True
        )
    except Exception:
        # Mengabaikan error jika gambar tidak ditemukan agar aplikasi tidak crash
        pass 

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
    set_background("Gemini_Generated_Image_208wzs208wzs208w.jfif", 0.7)
    
    st.markdown('<h1 style="text-align: center; color: white; font-weight: 900; letter-spacing: 2px;">🌍 INTELTRAFF CORE</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; color: #38bdf8; font-weight: 600;">Live AI Traffic Density Control Center</p>', unsafe_allow_html=True)
    
    # Tombol Jalankan Simulasi
    col_btn1, col_btn2, col_btn3 = st.columns([1, 1.5, 1])
    with col_btn2:
        mulai_simulasi = st.button("▶ JALANKAN SIKLUS SIMULASI (LIVE TIMER)", use_container_width=True, type="primary")
        
    st.markdown('<div style="height: 15px;"></div>', unsafe_allow_html=True)

    # Fungsi pembantu untuk menggambar kotak jalur di Control Room
    def render_card(jalur, is_hijau, waktu, antrean):
        status = "🟢 HIJAU (JALAN)" if is_hijau else "🔴 MERAH (BERHENTI)"
        badge_class = "badge-glowing-green" if is_hijau else "badge-red"
        border_color = "#10B981" if is_hijau else "rgba(239, 68, 68, 0.3)"
        return f'''
        <div class="glass-card" style="border-top: 5px solid {border_color};">
            <div class="jalur-title">{jalur}</div><div class="{badge_class}">{status}</div>
            <div class="label-teks">SISA WAKTU (DETIK)</div><div class="waktu-teks">{waktu}</div>
            <div class="antrean-teks">Antrean Kendaraan: <span class="highlight-antrean">{antrean}</span> 🚗</div>
        </div>
        '''
        
    layar_utama = st.empty()

    if mulai_simulasi:
        # URUTAN CERDAS: Diurutkan secara dinamis dari TDS tertinggi ke terendah
        urutan_siklus = sorted(data_jalur.keys(), key=lambda k: data_jalur[k]['tds'], reverse=True)
        urutan_teks = " ➡️ ".join([f"{j}" for j in urutan_siklus])
        
        # Eksekusi putaran lampu hijau per jalur
        for jalur_aktif in urutan_siklus:
            durasi_hijau = waktu_hijau[jalur_aktif]
            
            # Animasi Live Timer Mundur
            for sisa_waktu in range(durasi_hijau, -1, -1):
                with layar_utama.container():
                    st.info(f"🚦 **Siklus Cerdas Aktif!** Alur prioritas saat ini: **{urutan_teks}**")
                    
                    col_u_kosong, col_u, col_u_kosong2 = st.columns([1, 1.5, 1])
                    with col_u:
                        waktu_tampil = sisa_waktu if jalur_aktif == "UTARA" else waktu_hijau["UTARA"]
                        st.markdown(render_card("Jalur Utara", jalur_aktif == "UTARA", waktu_tampil, st.session_state.utara), unsafe_allow_html=True)
                        
                    col_b, col_tengah, col_t = st.columns([1.5, 0.5, 1.5])
                    with col_b:
                        waktu_tampil = sisa_waktu if jalur_aktif == "BARAT" else waktu_hijau["BARAT"]
                        st.markdown(render_card("Jalur Barat", jalur_aktif == "BARAT", waktu_tampil, st.session_state.barat), unsafe_allow_html=True)
                    with col_tengah:
                        st.markdown('<div style="text-align:center; padding-top:80px; opacity: 0.3;"><h1 style="font-size: 5rem; color:white;">+</h1></div>', unsafe_allow_html=True)
                    with col_t:
                        waktu_tampil = sisa_waktu if jalur_aktif == "TIMUR" else waktu_hijau["TIMUR"]
                        st.markdown(render_card("Jalur Timur", jalur_aktif == "TIMUR", waktu_tampil, st.session_state.timur), unsafe_allow_html=True)

                    col_s_kosong, col_s, col_s_kosong2 = st.columns([1, 1.5, 1])
                    with col_s:
                        waktu_tampil = sisa_waktu if jalur_aktif == "SELATAN" else waktu_hijau["SELATAN"]
                        st.markdown(render_card("Jalur Selatan", jalur_aktif == "SELATAN", waktu_tampil, st.session_state.selatan), unsafe_allow_html=True)
                time.sleep(1) # Berhenti 1 detik untuk membuat efek hitung mundur nyata
                
        st.success(f"✅ 1 Siklus Selesai! Urutan eksekusi: {urutan_teks}. Sistem terbukti memprioritaskan antrean terpanjang.")
    else:
        # Tampilan Statis sebelum tombol play ditekan
        with layar_utama.container():
            col_u_kosong, col_u, col_u_kosong2 = st.columns([1, 1.5, 1])
            with col_u: st.markdown(render_card("Jalur Utara", jalur_prioritas == "UTARA", waktu_hijau["UTARA"], st.session_state.utara), unsafe_allow_html=True)
            col_b, col_tengah, col_t = st.columns([1.5, 0.5, 1.5])
            with col_b: st.markdown(render_card("Jalur Barat", jalur_prioritas == "BARAT", waktu_hijau["BARAT"], st.session_state.barat), unsafe_allow_html=True)
            with col_tengah: st.markdown('<div style="text-align:center; padding-top:80px; opacity: 0.3;"><h1 style="font-size: 5rem; color:white;">+</h1></div>', unsafe_allow_html=True)
            with col_t: st.markdown(render_card("Jalur Timur", jalur_prioritas == "TIMUR", waktu_hijau["TIMUR"], st.session_state.timur), unsafe_allow_html=True)
            col_s_kosong, col_s, col_s_kosong2 = st.columns([1, 1.5, 1])
            with col_s: st.markdown(render_card("Jalur Selatan", jalur_prioritas == "SELATAN", waktu_hijau["SELATAN"], st.session_state.selatan), unsafe_allow_html=True)

elif menu == "2. Panel Input Kamera":
    set_background("Gemini_Generated_Image_c7d3v3c7d3v3c7d3.jfif", 0.6)
    
    st.markdown('<h2 style="color:white;">📷 Panel Input Kamera (Vision Layer)</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#cbd5e1;">Simulasi transmisi data antrean kendaraan (0-100) dari CCTV pintar lapangan ke Control Center.</p>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="glass-card"><h4 style="color:#38bdf8;">UTARA</h4>', unsafe_allow_html=True)
        st.session_state.utara = st.slider("", 0, 100, st.session_state.utara, key="su")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card"><h4 style="color:#38bdf8;">BARAT</h4>', unsafe_allow_html=True)
        st.session_state.barat = st.slider("", 0, 100, st.session_state.barat, key="sb")
        st.markdown('</div>', unsafe_allow_html=True)
    with col2:
        st.markdown('<div class="glass-card"><h4 style="color:#38bdf8;">SELATAN</h4>', unsafe_allow_html=True)
        st.session_state.selatan = st.slider("", 0, 100, st.session_state.selatan, key="ss")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="glass-card"><h4 style="color:#38bdf8;">TIMUR</h4>', unsafe_allow_html=True)
        st.session_state.timur = st.slider("", 0, 100, st.session_state.timur, key="st")
        st.markdown('</div>', unsafe_allow_html=True)

elif menu == "3. Analisis Logika (TDS)":
    set_background("Gemini_Generated_Image_bv9ofxbv9ofxbv9o.jfif", 0.75)
    
    st.markdown('<h2 style="color:white;">🧠 Decision Layer (Logika Inti)</h2>', unsafe_allow_html=True)
    st.markdown('''
    <div class="glass-card" style="text-align: left;">
        <h4 style="color: #38bdf8; margin-top: 0;">BAGAIMANA INTELTRAFF MENGAMBIL KEPUTUSAN?</h4>
        <ol style="color: #e2e8f0; font-size: 1.1rem; line-height: 1.6;">
            <li><b>Jumlah Kendaraan:</b> Sistem menghitung total mobil di semua arah.</li>
            <li><b>Traffic Density Score (TDS):</b> Sistem menghitung "porsi" kemacetan jalur (%). Jalur dengan TDS tertinggi akan otomatis menjadi Prioritas Utama pada awal siklus.</li>
            <li><b>Keputusan Hijau:</b> Durasi dihitung dinamis. Sangat padat = waktu maksimal. Sepi = dipotong ke batas minimum agar tidak ada ruang kosong.</li>
        </ol>
    </div>
    ''', unsafe_allow_html=True)
    
    df = pd.DataFrame({
        "JALUR": ["Utara", "Selatan", "Timur", "Barat"],
        "JUMLAH KENDARAAN": [st.session_state.utara, st.session_state.selatan, st.session_state.timur, st.session_state.barat],
        "TDS (%)": [f"{data_jalur['UTARA']['tds']:.1f}%", f"{data_jalur['SELATAN']['tds']:.1f}%", f"{data_jalur['TIMUR']['tds']:.1f}%", f"{data_jalur['BARAT']['tds']:.1f}%"],
        "DURASI HIJAU (Detik)": [waktu_hijau["UTARA"], waktu_hijau["SELATAN"], waktu_hijau["TIMUR"], waktu_hijau["BARAT"]]
    })
    st.table(df)

elif menu == "4. Perbandingan Kinerja":
    set_background("Lampu Hijau di Persimpangan Kota Basah.png", 0.7)
    
    st.markdown('<h2 style="color:white;">📊 Validasi Kinerja Sistem</h2>', unsafe_allow_html=True)
    
    waktu_konvensional = 40
    total_konvensional = waktu_konvensional * 4
    total_inteltraff = sum(waktu_hijau.values())
    hemat = total_konvensional - total_inteltraff
    
    df_chart = pd.DataFrame({
        "Jalur": ["Utara", "Selatan", "Timur", "Barat"],
        "Konvensional (Statis)": [waktu_konvensional] * 4,
        "INTELTRAFF (Adaptif)": [waktu_hijau["UTARA"], waktu_hijau["SELATAN"], waktu_hijau["TIMUR"], waktu_hijau["BARAT"]]
    })
    
    col1, col2 = st.columns([2, 1])
    with col1:
        st.bar_chart(df_chart.set_index("Jalur"), color=["#64748b", "#10b981"])
    with col2:
        st.markdown(f'''
        <div class="glass-card">
            <p style="color:#94a3b8; font-size:0.9rem; margin:0;">SIKLUS KONVENSIONAL</p>
            <h1 style="color:white; margin:0;">{total_konvensional}s</h1>
        </div>
        <div class="glass-card" style="border-left: 5px solid #10b981;">
            <p style="color:#10b981; font-size:0.9rem; margin:0;">SIKLUS INTELTRAFF</p>
            <h1 style="color:white; margin:0;">{total_inteltraff}s</h1>
            <p style="color:#38bdf8; margin:0;">Efisiensi Waktu: {hemat} Detik</p>
        </div>
        ''', unsafe_allow_html=True)

elif menu == "5. Pengaturan Sistem":
    set_background("Gemini_Generated_Image_ihrd8qihrd8qihrd.jpg", 0.8)
    
    st.markdown('<h2 style="color:white;">⚙️ Konfigurasi Keselamatan & Visi</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.number_input("Batas Minimum Lampu Hijau (Detik) - Jalur Sepi", value=15, min_value=10, max_value=30)
    with col2:
        st.number_input("Batas Maksimum Lampu Hijau (Detik) - Jalur Macet Total", value=60, min_value=40, max_value=120)
        
    st.markdown('''
    <div class="glass-card" style="text-align: left; background: rgba(15, 23, 42, 0.85); border-left: 5px solid #f59e0b; margin-top: 30px;">
        <h4 style="color: #f59e0b; letter-spacing: 1px; margin-top: 0;">MEMBAWA INOVASI MENUJU EKOSISTEM "SMART CITY"</h4>
        <p style="color: #e2e8f0; line-height: 1.8; text-align: justify;">
        INTELTRAFF bukan sekadar purwarupa pengatur lampu lalu lintas biasa. Gagasan ini lahir dari urgensi untuk menghadirkan keadilan dan efisiensi waktu di persimpangan jalan raya. Dengan memadukan potensi teknologi <i>Vision AI</i> (Pemrosesan Citra) dan algoritma <i>Fuzzy Logic</i>, kami menawarkan transisi dari sistem konvensional yang kaku menuju ekosistem <b>Smart City</b> yang dinamis dan adaptif.
        <br><br>
        Melalui pendekatan simulasi <i>Software-in-the-Loop</i> (SITL) pada purwarupa web interaktif ini, kami membuktikan secara kuantitatif bahwa kecerdasan buatan mampu menekan total waktu tunggu antrean secara signifikan tanpa mengabaikan aspek keselamatan berkendara. Inovasi ini merupakan wujud nyata komitmen mahasiswa <b>Institut Teknologi Sumatera (ITERA)</b> untuk berkontribusi dalam mengurai kemacetan, mereduksi emisi karbon gas buang akibat <i>idle</i> kendaraan, serta mendukung tercapainya <b>SDG 9: Industri, Inovasi, dan Infrastruktur</b>.
        </p>
    </div>
    ''', unsafe_allow_html=True)