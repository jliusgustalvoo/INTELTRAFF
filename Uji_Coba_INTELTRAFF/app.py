import streamlit as st
import pandas as pd

# Konfigurasi Halaman Dasar
st.set_page_config(page_title="INTELTRAFF - 5 Screen", page_icon="🚦", layout="wide")

# Custom CSS untuk mempercantik tampilan visual
st.markdown("""
<style>
    .status-badge-hijau { background-color: #10B981; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    .status-badge-merah { background-color: #EF4444; color: white; padding: 5px 15px; border-radius: 20px; font-weight: bold; }
    .kartu-jalur { background-color: #1e222a; padding: 20px; border-radius: 12px; text-align: center; margin-bottom: 15px;}
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
st.sidebar.caption("Simulasi INTELTRAFF - Sistem Kendali Lampu Lalu Lintas Cerdas Berbasis Vision AI & Logika Fuzzy")

if menu == "1. Dashboard Utama":
    st.title("🖥️ Screen 1: Dashboard Kendali Utama")
    st.write("Pemantauan visual persimpangan lalu lintas secara _real-time_.")
    
    col_u_kosong, col_u, col_u_kosong2 = st.columns([1,2,1])
    with col_u:
        status_u = "🟢 HIJAU AKTIF" if jalur_prioritas == "UTARA" else "🔴 MERAH"
        css_class = "status-badge-hijau" if jalur_prioritas == "UTARA" else "status-badge-merah"
        st.markdown(f'<div class="kartu-jalur" style="border-top: 5px solid #3b82f6;"><h3>⬆️ UTARA</h3><p><span class="{css_class}">{status_u}</span></p><h2>⏱️ {waktu_hijau["UTARA"]} Detik</h2><p>Antrean: {st.session_state.utara} 🚗</p></div>', unsafe_allow_html=True)
        
    col_b, col_tengah, col_t = st.columns([2,1,2])
    with col_b:
        status_b = "🟢 HIJAU AKTIF" if jalur_prioritas == "BARAT" else "🔴 MERAH"
        css_class = "status-badge-hijau" if jalur_prioritas == "BARAT" else "status-badge-merah"
        st.markdown(f'<div class="kartu-jalur" style="border-left: 5px solid #3b82f6;"><h3>⬅️ BARAT</h3><p><span class="{css_class}">{status_b}</span></p><h2>⏱️ {waktu_hijau["BARAT"]} Detik</h2><p>Antrean: {st.session_state.barat} 🚗</p></div>', unsafe_allow_html=True)
    with col_tengah:
        st.markdown('<div style="text-align:center; padding-top:40px;"><h2>🚥</h2><p><b>INTELTRAFF CORE</b></p></div>', unsafe_allow_html=True)
    with col_t:
        status_t = "🟢 HIJAU AKTIF" if jalur_prioritas == "TIMUR" else "🔴 MERAH"
        css_class = "status-badge-hijau" if jalur_prioritas == "TIMUR" else "status-badge-merah"
        st.markdown(f'<div class="kartu-jalur" style="border-right: 5px solid #3b82f6;"><h3>➡️ TIMUR</h3><p><span class="{css_class}">{status_t}</span></p><h2>⏱️ {waktu_hijau["TIMUR"]} Detik</h2><p>Antrean: {st.session_state.timur} 🚗</p></div>', unsafe_allow_html=True)

    col_s_kosong, col_s, col_s_kosong2 = st.columns([1,2,1])
    with col_s:
        status_s = "🟢 HIJAU AKTIF" if jalur_prioritas == "SELATAN" else "🔴 MERAH"
        css_class = "status-badge-hijau" if jalur_prioritas == "SELATAN" else "status-badge-merah"
        st.markdown(f'<div class="kartu-jalur" style="border-bottom: 5px solid #3b82f6;"><h3>⬇️ SELATAN</h3><p><span class="{css_class}">{status_s}</span></p><h2>⏱️ {waktu_hijau["SELATAN"]} Detik</h2><p>Antrean: {st.session_state.selatan} 🚗</p></div>', unsafe_allow_html=True)

elif menu == "2. Panel Input Kamera":
    st.title("📷 Screen 2: Simulator Vision AI")
    st.write("Halaman ini menyimulasikan data yang masuk dari kamera pendeteksi kendaraan (Vision Layer).")
    
    col1, col2 = st.columns(2)
    with col1:
        st.session_state.utara = st.slider("🚗 Kendaraan Jalur UTARA", 0, 100, st.session_state.utara)
        st.session_state.barat = st.slider("🚗 Kendaraan Jalur BARAT", 0, 100, st.session_state.barat)
    with col2:
        st.session_state.selatan = st.slider("🚗 Kendaraan Jalur SELATAN", 0, 100, st.session_state.selatan)
        st.session_state.timur = st.slider("🚗 Kendaraan Jalur TIMUR", 0, 100, st.session_state.timur)
    
    st.info("💡 Setelah mengubah nilai di sini, silakan kembali ke **1. Dashboard Utama** untuk melihat perubahan lampu secara instan.")

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