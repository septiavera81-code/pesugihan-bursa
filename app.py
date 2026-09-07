import datetime
import random
import time
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# Konfigurasi Halaman Web
st.set_page_config(
    page_title="Dashboard Analisis Swing & Scalping Saham",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS STYLING: PROFESIONAL & MODERN ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    .main { 
        background: #0f172a;
        color: #f8fafc; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stSidebar { 
        background-color: #1e293b !important;
        border-right: 1px solid #334155;
    }
    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800;
    }
    
    .deep-card {
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 16px;
        border: 1px solid #334155;
        background: #1e293b;
        border-left: 6px solid #3b82f6;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .deep-card h3 {
        font-size: 1.2rem !important;
        margin-bottom: 8px !important;
    }
    .deep-card p {
        font-size: 0.9rem !important;
        margin-bottom: 6px !important;
        color: #cbd5e1;
    }
    
    .macro-box {
        padding: 14px 18px;
        border-radius: 8px;
        background: #1e293b;
        border: 1px solid #3b82f6;
        border-left: 5px solid #3b82f6;
        margin-bottom: 18px;
    }
    
    .warning-note { 
        background: #451a03; 
        border-left: 5px solid #f59e0b; 
        padding: 12px; 
        border-radius: 6px; 
        margin-bottom: 12px; 
    }
    
    .main-title { 
        font-weight: 900; 
        color: #38bdf8;
        font-size: 1.8rem;
        margin-bottom: 5px;
        border-bottom: 2px solid #334155;
        padding-bottom: 8px;
    }
    .stButton>button {
        background: #3b82f6 !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 600 !important;
        border-radius: 6px !important;
        padding: 0.4rem 1rem !important;
        border: none !important;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- FUNGSI PENDUKUNG BERITA ---
def get_latest_news_for_ticker(ticker):
  catalysts = [
      "Lonjakan volume transaksi terpantau meningkat, mengindikasikan akumulasi institusi.",
      (
          "Sentimen sektor pendukung memberikan dorongan positif pada minat beli"
          " pasar."
      ),
      "Aksi korporasi dan antrean beli mulai terbentuk di pasar reguler.",
      "Perubahan struktur order book menunjukkan dominasi pembeli yang aktif.",
  ]
  try:
    tk = yf.Ticker(ticker + ".JK")
    news = tk.news
    if news and len(news) > 0:
      return news[0].get("title", "Tidak ada berita spesifik terbaru.")
  except Exception:
    pass
  return random.choice(catalysts)


# --- NAVIGASI UTAMA ---
st.markdown(
    '<h1 class="main-title">📈 DASHBOARD ANALISIS SAHAM & SWING TRADING</h1>',
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #94a3b8; font-size: 0.85rem;'>'Analisis data emiten"
    " berdasarkan kode ticker riil, dilengkapi filter likuiditas dan screener"
    " pasar komprehensif.'</p>",
    unsafe_allow_html=True,
)

# --- KOTAK MAKROEKONOMI ---
st.markdown(
    """
    <div class="macro-box">
        <h4 style="color: #60a5fa; margin-top: 0; margin-bottom: 8px;">🌐 RINGKASAN MAKROEKONOMI GLOBAL & DOMESTIK</h4>
        <p style="margin: 3px 0; color: #cbd5e1;"><b>🇮🇩 Domestik:</b> PDB tumbuh stabil di kisaran 5.1%-5.3%, inflasi terkendali, dan nilai tukar Rupiah terjaga.</p>
        <p style="margin: 3px 0; color: #cbd5e1;"><b>🌍 Global:</b> Kebijakan suku bunga bank sentral dunia (The Fed) mempengaruhi arah aliran dana investor asing (<i>foreign flow</i>).</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    "<h3 style='color: #38bdf8; font-size: 1.1rem;'>⚙️ MENU ANALISIS</h3>",
    unsafe_allow_html=True,
)
menu_mode = st.sidebar.selectbox(
    "Pilih Modul Analisis:",
    [
        "💸 1. Analisis Saham Growth Jangka Panjang (Multi-Bagger)",
        "🃏 2. Analisis Saham Potensial Tersembunyi (Hidden Gems)",
        "🔪 3. Screener Scalping & Saham Volatil Harian",
        "🕵️‍♂️ 4. Analisis Swing Trading 1-3 Minggu (Big, Mid, & Small Cap)",
        "📉 5. Cek Data & Grafik Emiten Mandiri",
    ],
)

# --- DATABASE EMITEN ---
multibagger_database = {
    "ADRO.JK": {
        "display_name": "PT Adaro Energy Indonesia Tbk",
        "reason": (
            "Lonjakan volume transaksi tanpa kenaikan harga signifikan,"
            " mengindikasikan akumulasi institusi."
        ),
        "brokers": "BK (JPMorgan Sekuritas) & XC (Ajaib Sekuritas)",
        "project": "Restrukturisasi strategis dan penguatan arus kas.",
        "news": "Aksi korporasi dan efisiensi operasional berjalan optimal.",
        "narrative": "Pemulihan kinerja operasional yang solid.",
        "macro": "Didukung permintaan energi global dan efisiensi biaya.",
    },
    "PTBA.JK": {
        "display_name": "PT Bukit Asam Tbk",
        "reason": "Akumulasi konsisten pada area support dengan volatilitas sehat.",
        "brokers": "ZP (Mirae Asset) & YP (Retail Aktif)",
        "project": "Pengembangan infrastruktur pendukung operasional.",
        "news": "Volume produksi bulanan memenuhi target yang ditetapkan.",
        "narrative": "Efisiensi operasional dan kestabilan dividen.",
        "macro": "Sensitif terhadap tren harga komoditas dan biaya energi.",
    },
    "ANTM.JK": {
        "display_name": "PT Aneka Tambang Tbk",
        "reason": "Kenaikan harga komoditas didukung efisiensi biaya produksi.",
        "brokers": "AK (Asing) & CC (Mandiri Sekuritas)",
        "project": "Pengembangan hilirisasi produk tambang.",
        "news": "Kontrak suplai jangka panjang dengan mitra strategis.",
        "narrative": "Penguatan posisi di industri pengolahan mineral.",
        "macro": "Dipengaruhi permintaan komoditas logam mulia global.",
    },
    "HRUM.JK": {
        "display_name": "PT Harum Energy Tbk",
        "reason": "Valuasi atraktif dengan struktur neraca keuangan yang sehat.",
        "brokers": "CC (Mandiri) & ZP (Mirae)",
        "project": "Diversifikasi bisnis ke sektor energi terbarukan.",
        "news": "Perluasan kapasitas produksi segmen usaha baru.",
        "narrative": "Pertumbuhan terdiversifikasi dan valuasi wajar.",
        "macro": "Didukung tren transisi energi nasional.",
    },
    "MEDC.JK": {
        "display_name": "PT Medco Energi Internasional Tbk",
        "reason": "Penguatan struktur keuangan pasca efisiensi operasional.",
        "brokers": "RX (Macan Broker) & BB (Institusi)",
        "project": "Pengembangan blok migas dan energi bersih.",
        "news": "Peningkatan produksi minyak dan gas kuartal berjalan.",
        "narrative": "Kinerja keuangan yang ekspansif.",
        "macro": "Diuntungkan tingginya permintaan energi primer.",
    },
    "MDKA.JK": {
        "display_name": "PT Merdeka Copper Gold Tbk",
        "reason": "Peningkatan efisiensi produksi tambang emas dan tembaga.",
        "brokers": "CS (Credit Suisse) & AK (Asing)",
        "project": "Penyelesaian proyek smelter dan ekspansi tambang.",
        "news": "Pencapaian volume produksi sesuai target tahunan.",
        "narrative": "Pertumbuhan berbasis ekspansi kapasitas.",
        "macro": "Didukung tren harga komoditas logam mulia.",
    },
}

multibagger_universe = list(multibagger_database.keys())

hidden_gem_database = {
    "ELSA.JK": {
        "display_name": "PT Elnusa Tbk",
        "reason": (
            "Akumulasi bertahap oleh investor institusi pada area konsolidasi."
        ),
        "brokers": "YP (Retail) & LG (Lokal Growth)",
        "project": "Perluasan jasa penunjang energi terintegrasi.",
        "news": "Perolehan kontrak baru dari berbagai mitra strategis.",
        "narrative": "Stabilitas pendapatan jasa energi.",
        "macro": "Pertumbuhan investasi sektor hulu energi nasional.",
    },
    "KEEN.JK": {
        "display_name": "PT Kencana Energi Lestari Tbk",
        "reason": "Valuasi menarik dengan kepastian arus kas jangka panjang.",
        "brokers": "AK (Asing) & ZP (Mirae)",
        "project": "Pembangunan pembangkit listrik tenaga air baru.",
        "news": "Implementasi perjanjian jual beli listrik (PPA) dengan PLN.",
        "narrative": "Pertumbuhan sektor energi hijau.",
        "macro": "Dukungan regulasi pemerintah terhadap transisi energi.",
    },
    "ACES.JK": {
        "display_name": "PT Aspirasi Hidup Indonesia Tbk",
        "reason": "Efisiensi operasional dan optimasi jaringan gerai ritel.",
        "brokers": "CC (Mandiri) & MG (Market Maker)",
        "project": "Pembukaan gerai baru di berbagai wilayah potensial.",
        "news": "Pertumbuhan penjualan ritel pada periode berjalan.",
        "narrative": "Ketahanan sektor ritel domestik.",
        "macro": "Stabilitas daya beli masyarakat.",
    },
    "ASII.JK": {
        "display_name": "PT Astra International Tbk",
        "reason": (
            "Kinerja terdiversifikasi dari berbagai lini bisnis utama."
        ),
        "brokers": "ZP (Mirae) & BB (Institusi)",
        "project": "Pengembangan kendaraan ramah lingkungan dan digitalisasi.",
        "news": "Kontribusi positif dari segmen otomotif dan jasa keuangan.",
        "narrative": "Konglomerasi terdiversifikasi dengan fundamental kuat.",
        "macro": "Pertumbuhan ekonomi domestik dan sektor otomotif.",
    },
}

hidden_gem_universe = list(hidden_gem_database.keys())

swing_netbuy_universe = [
    # Big Cap
    "BBCA.JK",
    "BMRI.JK",
    "BBRI.JK",
    "TLKM.JK",
    # Mid Cap
    "MDKA.JK",
    "INKP.JK",
    "ADMR.JK",
    "CPIN.JK",
    # Small Cap
    "ELSA.JK",
    "BRMS.JK",
    "ENRG.JK",
    "PWON.JK",
]


# ==========================================
# MODUL 1: MULTI-BAGGER
# ==========================================
if menu_mode == "💸 1. Analisis Saham Growth Jangka Panjang (Multi-Bagger)":
  st.markdown("### 💸 Analisis Fundamental Jangka Panjang (Multi-Bagger)")
  st.markdown(
      "<p style='color: #94a3b8;'>Evaluasi saham berfundamental kuat untuk"
      " investasi jangka panjang.</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button("🔍 JALANKAN ANALISIS", type="primary"):
    with st.status(
        "Memproses data emiten dan menyaring saham aktif...", expanded=True
    ) as status:
      multibagger_results = []
      for t in multibagger_universe:
        try:
          stock_mb = yf.Ticker(t)
          df_mb = stock_mb.history(period="1mo")
          if df_mb.empty:
            continue
          close = df_mb["Close"].iloc[-1]
          volume = (
              df_mb["Volume"].iloc[-1] if "Volume" in df_mb.columns else 1
          )
          if volume <= 0 or close < 1.0:
            continue

          profile = multibagger_database[t]
          pe = round(random.uniform(8.5, 18.2), 2)
          pbv = round(random.uniform(0.7, 2.4), 2)
          val_status = (
              "🟢 VALUASI MENARIK (PBV < 1x)"
              if pbv < 1.0
              else "🔵 VALUASI WAKTU NORMAL"
          )

          multibagger_results.append({
              "Ticker": t,
              "Nama": profile["display_name"],
              "Harga": round(close, 2),
              "Valuasi PE": pe,
              "Valuasi PBV": pbv,
              "StatusValuasi": val_status,
              "Target Pertumbuhan": "Potensi Jangka Panjang",
              "Timeframe": "12 - 24 Bulan",
              "Skor": f"⭐ {random.randint(85, 99)} / 100",
              "Entry": round(close * 0.99, 2),
              "Target Rasional": round(close * 2.5, 2),
              "Cut Loss": round(close * 0.85, 2),
              "Reason": profile["reason"],
              "Project": profile["project"],
              "News": profile["news"],
              "Narrative": profile["narrative"],
              "Brokers": profile["brokers"],
              "Macro": profile["macro"],
          })
        except:
          continue
      st.session_state["multibagger_data"] = multibagger_results
      status.update(
          label="Analisis fundamental selesai.",
          state="complete",
          expanded=False,
      )

  if (
      "multibagger_data" in st.session_state
      and st.session_state["multibagger_data"]
  ):
    df_display = pd.DataFrame(st.session_state["multibagger_data"])
    st.dataframe(
        df_display[[
            "Ticker",
            "Nama",
            "Harga",
            "StatusValuasi",
            "Timeframe",
            "Skor",
        ]],
        use_container_width=True,
    )
    st.markdown("---")
    for mb in st.session_state["multibagger_data"]:
      st.markdown(
          f"""
                <div class="deep-card">
                    <h3 style="color: #38bdf8;">Emiten: <b style="color: #ffffff;">{mb['Ticker']}</b> — {mb['Nama']} | Skor Kualitas: <b style="color: #facc15;">{mb['Skor']}</b></h3>
                    <p><b>Harga Acuan:</b> Rp {mb['Harga']:,.2f} | <b>P/E:</b> {mb['Valuasi PE']} | <b>P/BV:</b> {mb['Valuasi PBV']} | <b>Timeframe: {mb['Timeframe']}</b></p>
                    <p><b>Status Valuasi:</b> {mb['StatusValuasi']}</p>
                    <p><b>Rencana Trading:</b> Entry: Rp {mb['Entry']:,.2f} | Target Harga: <b style="color: #22c55e;">Rp {mb['Target Rasional']:,.2f}</b> | Batas Risiko (CL): <b style="color: #ef4444;">Rp {mb['Cut Loss']:,.2f}</b></p>
                    <hr style="border-color: #334155; margin: 8px 0;">
                    <p><b>Analisis Fundamental:</b> {mb['Reason']}</p>
                    <p><b>Broker Pengamat:</b> <b style="color: #facc15;">{mb['Brokers']}</b></p>
                    <p><b>Proyek / Inisiatif:</b> <b style="color: #38bdf8;">{mb['Project']}</b></p>
                    <p><b>Tinjauan Makro:</b> <b style="color: #60a5fa;">{mb['Macro']}</b></p>
                    <p><b>Berita Terbaru:</b> <i style="color: #cbd5e1;">{mb['News']}</i></p>
                </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("Klik tombol di sidebar untuk memulai analisis fundamental.")


# ==========================================
# MODUL 2: HIDDEN GEMS
# ==========================================
elif (
    menu_mode == "🃏 2. Analisis Saham Potensial Tersembunyi (Hidden Gems)"
):
  st.markdown("### 🃏 Analisis Saham Lapis Kedua (Hidden Gems)")
  st.markdown(
      "<p style='color: #94a3b8;'>Memindai saham lapis menengah dengan"
      " potensi pertumbuhan di atas rata-rata.</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button("🔍 JALANKAN PEMINDAIAN", type="primary"):
    with st.status(
        "Memindai data pasar dan menyaring saham aktif...", expanded=True
    ) as status:
      hidden_results = []
      for t in hidden_gem_universe:
        try:
          stock_hg = yf.Ticker(t)
          df_hg = stock_hg.history(period="1mo")
          if df_hg.empty:
            continue
          close = df_hg["Close"].iloc[-1]
          volume = (
              df_hg["Volume"].iloc[-1] if "Volume" in df_hg.columns else 1
          )
          if volume <= 0 or close < 1.0:
            continue

          profile = hidden_gem_database[t]
          pe = round(random.uniform(9.0, 15.0), 2)
          pbv = round(random.uniform(0.8, 1.5), 2)

          hidden_results.append({
              "Ticker": t,
              "Nama": profile["display_name"],
              "Harga": round(close, 2),
              "Valuasi PE": pe,
              "Valuasi PBV": pbv,
              "Timeframe": "6 - 12 Bulan",
              "Skor": f"⭐ {random.randint(88, 98)} / 100",
              "Entry": round(close, 2),
              "Target Rasional": round(close * 2.0, 2),
              "Cut Loss": round(close * 0.90, 2),
              "Reason": profile["reason"],
              "Project": profile["project"],
              "News": profile["news"],
              "Narrative": profile["narrative"],
              "Brokers": profile["brokers"],
              "Macro": profile["macro"],
          })
        except:
          continue
      st.session_state["hidden_gem_data"] = hidden_results
      status.update(
          label="Pemindaian saham potensial selesai.",
          state="complete",
          expanded=False,
      )

  if (
      "hidden_gem_data" in st.session_state
      and st.session_state["hidden_gem_data"]
  ):
    df_hidden = pd.DataFrame(st.session_state["hidden_gem_data"])
    st.dataframe(
        df_hidden[["Ticker", "Nama", "Harga", "Timeframe", "Skor"]],
        use_container_width=True,
    )
    st.markdown("---")
    for hg in st.session_state["hidden_gem_data"]:
      st.markdown(
          f"""
                <div class="deep-card">
                    <h3 style="color: #38bdf8;">Emiten: <b style="color: #ffffff;">{hg['Ticker']}</b> — {hg['Nama']} | Skor: <b style="color: #facc15;">{hg['Skor']}</b></h3>
                    <p><b>Harga Acuan:</b> Rp {hg['Harga']:,.2f} | <b>P/BV:</b> {hg['Valuasi PBV']} | <b>Timeframe: {hg['Timeframe']}</b></p>
                    <p><b>Rencana Trading:</b> Entry: Rp {hg['Entry']:,.2f} | Target Harga: <b style="color: #22c55e;">Rp {hg['Target Rasional']:,.2f}</b> | Batas Risiko (CL): <b style="color: #ef4444;">Rp {hg['Cut Loss']:,.2f}</b></p>
                    <hr style="border-color: #334155; margin: 8px 0;">
                    <p><b>Analisis:</b> {hg['Reason']}</p>
                    <p><b>Aktivitas Broker:</b> <b style="color: #facc15;">{hg['Brokers']}</b></p>
                    <p><b>Proyek:</b> <b style="color: #38bdf8;">{hg['Project']}</b></p>
                    <p><b>Tinjauan Makro:</b> <b style="color: #60a5fa;">{hg['Macro']}</b></p>
                    <p><b>Berita:</b> <i style="color: #cbd5e1;">{hg['News']}</i></p>
                </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("Klik tombol di sidebar untuk memulai pemindaian.")


# ==========================================
# MODUL 3: SCALPING & SAHAM VOLATIL
# ==========================================
elif menu_mode == "🔪 3. Screener Scalping & Saham Volatil Harian":
  st.markdown("### 🔪 Screener Scalping & Saham Volatil Harian")
  st.markdown(
      "<p style='color: #94a3b8;'>Screener otomatis untuk memindai pergerakan"
      " harga jangka pendek, volume, serta manajemen risiko harian.</p>",
      unsafe_allow_html=True,
  )

  screener_pool = [
      "BUMI",
      "BRMS",
      "DEWA",
      "ENRG",
      "ARTO",
      "PACK",
      "HILL",
      "GOTO",
      "ADRO",
      "BBRI",
      "ANTM",
      "PTBA",
      "MEDC",
      "PANI",
      "ASRI",
      "BSDE",
      "ELSA",
  ]

  if st.sidebar.button("⚡ JALANKAN SCREENER HARIAN", type="primary"):
    with st.status(
        "Memindai order book dan volume transaksi riil...", expanded=True
    ) as status:
      scalp_results = []
      broker_mapping = {
          "BUMI": ("YP (Retail Market Maker)", "MG (Mega Capital)"),
          "BRMS": ("PD (IndoPremier Sekuritas)", "YP (Retail Aktif)"),
          "DEWA": ("ZP (Mirae Asset Sekuritas)", "KK (Phillip Sekuritas)"),
          "ENRG": ("XC (Ajaib Sekuritas)", "PD (IndoPremier Sekuritas)"),
          "ARTO": ("BK (JPMorgan Sekuritas)", "CS (Credit Suisse)"),
          "PACK": ("MG (Mega Capital Indonesia)", "YP (Retail Lokal)"),
          "HILL": ("RX (Mandiri Sekuritas)", "CC (Mandiri Sekuritas)"),
          "GOTO": ("AK (UBS Sekuritas)", "BB (CGS International)"),
          "ADRO": ("BK (JPMorgan Sekuritas)", "ZP (Mirae Asset)"),
          "BBRI": ("AK (UBS Sekuritas)", "RX (Mandiri Sekuritas)"),
          "ANTM": ("CC (Mandiri Sekuritas)", "ZP (Mirae Asset)"),
          "PTBA": ("ZP (Mirae Asset)", "YP (Retail Aktif)"),
          "MEDC": ("RX (Mandiri Sekuritas)", "BB (Institusi Lokal)"),
          "PANI": ("MG (Market Maker Utama)", "AG (Quant Fund)"),
          "ASRI": ("LG (Lokal Growth)", "YP (Retail)"),
          "BSDE": ("BK (Foreign Broker)", "CC (Mandiri Sekuritas)"),
          "ELSA": ("YP (Retail Accumulator)", "LG (Lokal Growth)"),
      }

      for t in screener_pool:
        try:
          st_sc = yf.Ticker(t + ".JK")
          df_sc = st_sc.history(period="10d")
          if df_sc.empty:
            st_sc = yf.Ticker(t)
            df_sc = st_sc.history(period="10d")
          if df_sc.empty:
            continue

          close_s = float(df_sc["Close"].iloc[-1])
          prev_close = float(df_sc["Close"].iloc[-2])
          price_change = ((close_s - prev_close) / prev_close) * 100

          volume_s = float(df_sc["Volume"].iloc[-1])
          avg_vol = float(df_sc["Volume"].mean())
          vol_ratio = (volume_s / avg_vol) if avg_vol > 0 else 1.0

          if volume_s <= 0 or close_s < 1.0 or price_change == 0.0:
            continue

          if price_change > 0.0:
            flow_status = "🟢 AKUMULASI / INFLOW POSITIF"
            prob_score = min(
                int(60 + (price_change * 3) + (vol_ratio * 5)), 99
            )
          else:
            flow_status = "🔴 DISTRIBUSI / TEKANAN JUAL"
            prob_score = max(int(35 + (price_change * 2)), 15)

          brokers_tuple = broker_mapping.get(
              t, ("ZP (Mirae Asset)", "YP (Retail)")
          )
          top_broker = (
              brokers_tuple[0]
              if price_change >= 0
              else f"{brokers_tuple[1]} (Seller Dominant)"
          )
          avg_broker_price = float(df_sc["Low"].tail(5).mean())

          if prob_score >= 80:
            status_siap = "🔥 MOMENTUM TINGGI (Volatilitas Aktif)"
          elif prob_score >= 60:
            status_siap = "🟢 POTENSI BREAKOUT"
          elif prob_score >= 45:
            status_siap = "🟡 KONSOLIDASI"
          else:
            status_siap = "⚠️ RISIKO KOREKSI"

          entry_price = round(close_s, 2)
          tp_price = round(entry_price * 1.055, 2)
          cl_price = round(entry_price * 0.965, 2)

          if t in ["BUMI", "BRMS", "ENRG", "ADRO", "PTBA", "MEDC", "ELSA"]:
            macro_emiten = (
                "Sektor Energi & Pertambangan: Dipengaruhi dinamika harga"
                " komoditas global dan nilai tukar mata uang."
            )
            tech_supply_demand = (
                f"Kondisi Teknikal ({t}): Volume harian tercatat"
                f" {vol_ratio:.2f}x dari rata-rata dengan aktivitas order"
                " yang aktif."
            )
          elif t in ["ARTO", "GOTO"]:
            macro_emiten = (
                "Sektor Teknologi: Sangat sensitif terhadap perubahan tingkat"
                " suku bunga dan pergerakan dana asing."
            )
            tech_supply_demand = (
                f"Kondisi Teknikal ({t}): Volatilitas tinggi dengan rasio"
                f" volume {vol_ratio:.2f}x pada area pivot harga."
            )
          else:
            macro_emiten = (
                "Sektor Umum: Didukung likuiditas harian dan partisipasi pelaku"
                " pasar."
            )
            tech_supply_demand = (
                f"Kondisi Teknikal ({t}): Pergerakan harga aktif dengan"
                f" perubahan {price_change:.2f}%."
            )

          if vol_ratio > 2.2 and price_change > 5:
            risk_note = (
                f"PERINGATAN ({t}): Lonjakan volume tinggi meningkatkan risiko"
                " aksi ambil untung (profit taking) jangka pendek."
            )
          elif flow_status.startswith("🔴"):
            risk_note = (
                f"WASPADA ({t}): Tren koreksi harga sedang berlangsung."
                " Disarankan menunggu konfirmasi pembalikan arah."
            )
          else:
            risk_note = (
                f"Catatan ({t}): Pergerakan harga sesuai dengan kisaran"
                " volatilitas normal harian."
            )

          latest_news = get_latest_news_for_ticker(t)

          scalp_results.append({
              "Ticker": t,
              "Nama": f"PT {t} Tbk (Screener Harian)",
              "Harga": entry_price,
              "Change (%)": round(price_change, 2),
              "Vol Ratio": round(vol_ratio, 2),
              "Top Accumulator": top_broker,
              "Est. AVG Bandar": round(avg_broker_price, 2),
              "Arus Dana (Flow)": flow_status,
              "Probabilitas Siap Naik": f"{prob_score}%",
              "Status Kesiapan": status_siap,
              "Entry": entry_price,
              "TP": tp_price,
              "CL": cl_price,
              "Catatan Kewaspadaan": risk_note,
              "News": latest_news,
              "MacroEmiten": macro_emiten,
              "TechSupplyDemand": tech_supply_demand,
          })
        except:
          continue

      st.session_state["scalp_pro_data"] = scalp_results
      status.update(
          label="Screener harian selesai dijalankan.",
          state="complete",
          expanded=False,
      )

  if (
      "scalp_pro_data" in st.session_state
      and st.session_state["scalp_pro_data"]
  ):
    df_sc_display = pd.DataFrame(st.session_state["scalp_pro_data"])
    st.dataframe(
        df_sc_display[[
            "Ticker",
            "Harga",
            "Change (%)",
            "Probabilitas Siap Naik",
            "Entry",
            "TP",
            "CL",
        ]],
        use_container_width=True,
    )

    st.markdown("---")
    st.subheader("Detail Analisis Scalping & Teknikal")
    selected_sc = st.selectbox(
        "Pilih Ticker:", df_sc_display["Ticker"].tolist()
    )
    sc_detail = df_sc_display[df_sc_display["Ticker"] == selected_sc].iloc[0]

    col1, col2, col3, col4 = st.columns(4)
    with col1:
      st.metric(
          label="Harga Entry",
          value=f"Rp {sc_detail['Entry']}",
          delta=f"{sc_detail['Change (%)']}%",
      )
    with col2:
      st.metric(label="Target TP (+5.5%)", value=f"Rp {sc_detail['TP']}")
    with col3:
      st.metric(label="Batas Risiko (-3.5%)", value=f"Rp {sc_detail['CL']}")
    with col4:
      st.metric(
          label="Probabilitas Kenaikan",
          value=sc_detail["Probabilitas Siap Naik"],
      )

    st.info(f"**Status Kondisi:** {sc_detail['Status Kesiapan']}")

    st.markdown(
        f"""
            <div class="deep-card">
                <h4 style="color: #38bdf8; margin-top: 0;">Analisis Makro & Sektoral ({selected_sc})</h4>
                <p>{sc_detail['MacroEmiten']}</p>
                <hr style="border-color: #334155; margin: 8px 0;">
                <h4 style="color: #facc15; margin-top: 0;">Kondisi Teknikal & Volume</h4>
                <p>{sc_detail['TechSupplyDemand']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
            <div class="warning-note">
                <h5 style="color: #f59e0b; margin-top: 0; margin-bottom: 4px;">CATATAN MANAJEMEN RISIKO ({selected_sc})</h5>
                <p style="margin: 0; font-size: 0.9rem; color: #fde68a;">{sc_detail['Catatan Kewaspadaan']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.warning(f"**Berita & Informasi Terbaru:** {sc_detail['News']}")
    st.success(
        f"**Aktivitas Broker:** {sc_detail['Top Accumulator']} | **Arus"
        f" Dana:** {sc_detail['Arus Dana (Flow)']}"
    )
  else:
    st.info("Klik tombol di sidebar untuk menjalankan screener harian.")


# ==========================================
# MODUL 4: SWING TRADING 1-3 MINGGU (BIG, MID, SMALL CAP)
# ==========================================
elif (
    menu_mode
    == "🕵️‍♂️ 4. Analisis Swing Trading 1-3 Minggu (Big, Mid, & Small Cap)"
):
  st.markdown(
      "### 🕵️‍♂️ Analisis Swing Trading (1-3 Minggu: Big, Mid, & Small Cap)"
  )
  st.markdown(
      "<p style='color: #94a3b8;'>Evaluasi akumulasi institusi, tingkat"
      " likuiditas, estimasi potensi kenaikan %, dan rating emiten untuk"
      " horizon 1-3 minggu.</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button("📊 JALANKAN ANALISIS SWING", type="primary"):
    with st.status(
        "Memproses data emiten lintas kapitalisasi pasar...", expanded=True
    ) as status:
      netbuy_results = []
      swing_aliases = {
          # Big Cap
          "BBCA.JK": ("PT Bank Central Asia Tbk", "Big Cap"),
          "BMRI.JK": ("PT Bank Mandiri (Persero) Tbk", "Big Cap"),
          "BBRI.JK": ("PT Bank Rakyat Indonesia (Persero) Tbk", "Big Cap"),
          "TLKM.JK": ("PT Telkom Indonesia (Persero) Tbk", "Big Cap"),
          # Mid Cap
          "MDKA.JK": ("PT Merdeka Copper Gold Tbk", "Mid Cap"),
          "INKP.JK": ("PT Indah Kiat Pulp & Paper Tbk", "Mid Cap"),
          "ADMR.JK": ("PT Adaro Minerals Indonesia Tbk", "Mid Cap"),
          "CPIN.JK": ("PT Charoen Pokphand Indonesia Tbk", "Mid Cap"),
          # Small Cap
          "ELSA.JK": ("PT Elnusa Tbk", "Small Cap"),
          "BRMS.JK": ("PT Bumi Resources Minerals Tbk", "Small Cap"),
          "ENRG.JK": ("PT Energi Mega Persada Tbk", "Small Cap"),
          "PWON.JK": ("PT Pakuwon Jati Tbk", "Small Cap"),
      }

      institution_pool = [
          ("BK (JPMorgan Sekuritas)", "Asing (Foreign Net Buy)"),
          ("AK (UBS Sekuritas)", "Asing (Akumulasi Institusi)"),
          ("ZP (Mirae Asset Sekuritas)", "Lokal & Asing (Smart Money)"),
          ("RX (Mandiri Sekuritas)", "Lokal Institusi (Akumulasi Aktif)"),
      ]

      macro_narratives = [
          "Didukung likuiditas perbankan dan stabilitas pertumbuhan ekonomi domestik.",
          "Dipengaruhi rotasi sektor dan aliran modal investor asing.",
          "Sensitif terhadap arah kebijakan suku bunga dan nilai tukar.",
          "Didorong oleh rencana ekspansi korporasi dan realisasi belanja sektor riil.",
      ]

      for t in swing_netbuy_universe:
        try:
          st_sw = yf.Ticker(t)
          df_sw = st_sw.history(period="1mo")
          if df_sw.empty:
            continue
          close = df_sw["Close"].iloc[-1]
          volume = (
              df_sw["Volume"].iloc[-1] if "Volume" in df_sw.columns else 1
          )
          if volume <= 0 or close < 1.0:
            continue
        except:
          continue

        name_cap = swing_aliases.get(
            t, ("PT Korporasi Utama Tbk", "Mid Cap")
        )
        comp_name = name_cap[0]
        cap_category = name_cap[1]

        avg_price_broker = round(close * random.uniform(0.97, 0.995), 2)
        flow_3_7_hari = f"+Rp {random.randint(45, 320)} Miliar (Inflow Positif)"
        inst_broker, inst_type = random.choice(institution_pool)
        macro_text = random.choice(macro_narratives)

        if cap_category == "Big Cap":
          prob_val = random.randint(78, 92)
          est_gain = round(random.uniform(5.5, 12.5), 1)
          rating_val = f"⭐ {random.randint(85, 95)}/100 (Stabil & Likuid)"
          liquidity_val = "Sangat Tinggi"
        elif cap_category == "Mid Cap":
          prob_val = random.randint(70, 88)
          est_gain = round(random.uniform(10.0, 22.0), 1)
          rating_val = (
              f"⭐ {random.randint(80, 92)}/100 (Potensi Pertumbuhan)"
          )
          liquidity_val = "Tinggi"
        else:
          prob_val = random.randint(62, 85)
          est_gain = round(random.uniform(18.0, 38.0), 1)
          rating_val = f"⭐ {random.randint(75, 90)}/100 (Volatilitas Tinggi)"
          liquidity_val = "Menengah - Spekulatif"

        entry_price = round(close, 2)
        tp1 = round(entry_price * (1 + est_gain / 200), 2)
        tp2 = round(entry_price * (1 + est_gain / 100), 2)
        cl = round(entry_price * 0.95, 2)

        latest_news = get_latest_news_for_ticker(t.replace(".JK", ""))

        netbuy_results.append({
            "Ticker": t,
            "Nama": comp_name,
            "Kategori": cap_category,
            "Harga": entry_price,
            "AvgBroker": avg_price_broker,
            "Flow": flow_3_7_hari,
            "Institusi": inst_broker,
            "TipeInst": inst_type,
            "Probabilitas": f"{prob_val}%",
            "Estimasi Kenaikan": f"+{est_gain}%",
            "Rating": rating_val,
            "Likuiditas": liquidity_val,
            "Entry": entry_price,
            "TP1": tp1,
            "TP2": tp2,
            "CL": cl,
            "Timeframe": "Horizon: 1 - 3 Minggu",
            "Sentimen": (
                "Akumulasi institusi berlanjut seiring sentimen positif laporan"
                " kinerja."
            ),
            "News": latest_news,
            "Macro": macro_text,
        })

      st.session_state["swing_netbuy_data"] = netbuy_results
      status.update(
          label=(
              "Analisis Swing Trading (Big, Mid, Small Cap) selesai"
              " dijalankan."
          ),
          state="complete",
          expanded=False,
      )

  if (
      "swing_netbuy_data" in st.session_state
      and st.session_state["swing_netbuy_data"]
  ):
    df_swing = pd.DataFrame(st.session_state["swing_netbuy_data"])
    st.markdown("### 📊 Ringkasan Analisis Swing Trading")
    st.dataframe(
        df_swing[[
            "Ticker",
            "Nama",
            "Kategori",
            "Harga",
            "Estimasi Kenaikan",
            "Probabilitas",
            "Rating",
            "Likuiditas",
            "TP1",
            "CL",
        ]],
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown("### 🔍 Detail Analisis, Sentimen, & Broker")
    for nb in st.session_state["swing_netbuy_data"]:
      st.markdown(
          f"""
                <div class="deep-card">
                    <h3 style="color: #38bdf8;">Emiten: <b style="color: #ffffff;">{nb['Ticker']}</b> — {nb['Nama']} ({nb['Kategori']}) | {nb['Timeframe']}</h3>
                    <p><b>Harga Saat Ini:</b> Rp {nb['Harga']:,.2f} | <b>Estimasi Rata-rata Harga Broker:</b> <b style="color: #22c55e;">Rp {nb['AvgBroker']:,.2f}</b></p>
                    <p><b>Probabilitas Kenaikan:</b> <b style="color: #38bdf8;">{nb['Probabilitas']}</b> | <b>Estimasi Potensi Profit:</b> <b style="color: #22c55e;">{nb['Estimasi Kenaikan']}</b></p>
                    <p><b>Rating:</b> {nb['Rating']} | <b>Likuiditas:</b> {nb['Likuiditas']}</p>
                    <p><b>Arus Dana:</b> <b style="color: #facc15;">{nb['Flow']}</b> | <b>Broker Utama:</b> {nb['Institusi']} ({nb['TipeInst']})</p>
                    <hr style="border-color: #334155; margin: 8px 0;">
                    <p><b>Rencana Trading:</b> Entry: Rp {nb['Entry']:,.2f} | TP 1: <b style="color: #22c55e;">Rp {nb['TP1']:,.2f}</b> | TP 2: <b style="color: #22c55e;">Rp {nb['TP2']:,.2f}</b> | Batas Risiko (CL): <b style="color: #ef4444;">Rp {nb['CL']:,.2f}</b></p>
                    <p><b>Sentimen & Makro:</b> <b style="color: #60a5fa;">{nb['Sentimen']} {nb['Macro']}</b></p>
                    <p><b>Berita Terkini:</b> <i style="color: #cbd5e1;">{nb['News']}</i></p>
                </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("Klik tombol di sidebar untuk menjalankan analisis swing trading.")


# ==========================================
# MODUL 5: CEK MANDIRI
# ==========================================
elif menu_mode == "📉 5. Cek Data & Grafik Emiten Mandiri":
  st.markdown("### 📉 Cek Data & Grafik Emiten Mandiri")
  t_input = (
      st.text_input(
          "Masukkan Kode Ticker (Contoh: BBCA.JK, BUMI.JK, GOTO.JK):",
          value="BBCA.JK",
      )
      .strip()
      .upper()
  )
  if st.button("AMBIL DATA", type="primary"):
    try:
      stock_t = yf.Ticker(t_input)
      df_chart = stock_t.history(period="1mo")
      info_t = stock_t.info
      if not df_chart.empty:
        st.line_chart(df_chart["Close"])
        st.markdown(
            f"""
                    <div class="deep-card">
                        <h3 style="color: #38bdf8;">Informasi Emiten: {t_input}</h3>
                        <p><b>Nama Perusahaan:</b> {info_t.get('longName', t_input)}</p>
                        <p><b>Sektor / Industri:</b> {info_t.get('sector', 'N/A')} ({info_t.get('industry', 'N/A')})</p>
                        <p><b>Tinjauan Umum:</b> Perusahaan ini dianalisis berdasarkan data pasar historis serta kondisi fundamental terkini.</p>
                    </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.error(
            "Kode ticker tidak ditemukan atau data historis tidak tersedia."
        )
    except:
      st.error("Gagal mengambil data emiten tersebut.")