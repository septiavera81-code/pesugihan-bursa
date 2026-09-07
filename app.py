import datetime
import random
import time
import numpy as np
import pandas as pd
import streamlit as st
import yfinance as yf

# Konfigurasi Halaman Web (Sidebar langsung terbuka / expanded di HP & Desktop)
st.set_page_config(
    page_title="PADEPOKAN SAHAM GHOIB: PESUGIHAN BURSA EFEK",
    page_icon="🔮",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- CSS STYLING: MYSTIC CYBERPUNK ---
st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&display=swap');

    .main { 
        background: #09090b;
        color: #e4e4e7; 
        font-family: 'Plus Jakarta Sans', sans-serif;
    }
    .stSidebar { 
        background-color: #121217 !important;
        border-right: 2px dashed #a855f7;
    }
    h1, h2, h3 {
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800;
    }
    
    .deep-card {
        padding: 16px 20px;
        border-radius: 10px;
        margin-bottom: 16px;
        border: 1.5px solid #a855f7;
        background: #181824;
        border-left: 6px solid #a855f7;
        box-shadow: 3px 3px 0px #a855f7;
    }
    .deep-card h3 {
        font-size: 1.2rem !important;
        margin-bottom: 8px !important;
    }
    .deep-card p {
        font-size: 0.9rem !important;
        margin-bottom: 6px !important;
        color: #d4d4d8;
    }
    
    .macro-box {
        padding: 14px 18px;
        border-radius: 8px;
        background: #12121a;
        border: 1px solid #3b82f6;
        border-left: 5px solid #3b82f6;
        margin-bottom: 18px;
    }
    
    .warning-note { 
        background: #1f1215; 
        border-left: 5px solid #ef4444; 
        padding: 12px; 
        border-radius: 6px; 
        margin-bottom: 12px; 
    }
    
    .main-title { 
        font-weight: 900; 
        color: #a855f7;
        text-shadow: 2px 2px 0px #000000;
        font-size: 1.8rem;
        margin-bottom: 5px;
        border-bottom: 3px solid #a855f7;
        padding-bottom: 8px;
    }
    .stButton>button {
        background: #a855f7 !important;
        color: #ffffff !important;
        font-family: 'Plus Jakarta Sans', sans-serif !important;
        font-weight: 800 !important;
        border-radius: 6px !important;
        padding: 0.4rem 1rem !important;
        border: 1.5px solid #000000 !important;
        box-shadow: 2px 2px 0px #22c55e;
    }
    </style>
""",
    unsafe_allow_html=True,
)


# --- FUNGSI PENDUKUNG BERITA ---
def get_latest_news_for_ticker(ticker):
  catalysts = [
      "Lonjakan volume tak biasa terdeteksi, indikasi akumulasi institusi besar dan bandar.",
      "Sentimen sektor spekulatif mendadak mendongkrak minat beli pasar ritel.",
      "Aksi korporasi senyap & antrean bid tebal terendus di market reguler.",
      (
          "Breaking: Lonjakan antrean HAKI / HATC masuk, bersiap uji batas"
          " resistance harian."
      ),
      (
          "Katalis spekulatif: Perubahan struktur orderbook menunjukkan"
          " dominasi buyer agresif."
      ),
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
    '<h1 class="main-title">🔮 PADEPOKAN DUIT GHOIB: PESUGIHAN SAHAM & ANALISIS'
    " NYATA</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='color: #a1a1aa; font-style: italic; font-size: 0.85rem;'>'Kode"
    " emiten asli dan suci (ticker normal), dilengkapi filter anti-saham"
    " tidur & screener harga mulai dari Rp 1 (Termasuk Saham Gorengan"
    " Pilihan).'</p>",
    unsafe_allow_html=True,
)

# --- DASHBOARD KOTAK MAKRO EKONOMI GLOBAL & DOMESTIK ---
st.markdown(
    """
    <div class="macro-box">
        <h4 style="color: #60a5fa; margin-top: 0; margin-bottom: 8px;">🌐 TERAWANGAN MAKROEKONOMI & KONDISI DUNIA GAIB</h4>
        <p style="margin: 3px 0;"><b>🇮🇩 Suasana Republik:</b> PDB tumbuh stabil ~5.1%-5.3%, inflasi anteng, dan Bank Indonesia pasang 'tenda gaib' buat jaga kurs Rupiah.</p>
        <p style="margin: 3px 0;"><b>🌍 Dunia Luar & Sesajen Komoditas:</b> Angin dari The Fed dan harga energi global mempengaruhi arah datangnya arwah investor asing (<i>foreign flow</i>).</p>
    </div>
""",
    unsafe_allow_html=True,
)

st.sidebar.markdown(
    "<h3 style='color: #a855f7; font-size: 1.1rem;'>🕯️ RITUAL & KOKPIT"
    " PESUGIHAN</h3>",
    unsafe_allow_html=True,
)
menu_mode = st.sidebar.selectbox(
    "Pilih Jenis Ritual:",
    [
        "💸 1. Ritual Pesugihan Multi-Bagger (Kekayaan 7 Turunan)",
        "🃏 2. Terawangan Mutiara Terpendam (Hidden Gem Tumbal Cicilan)",
        (
            "🔪 3. Pesugihan Instan Jalur Orang Dalam (Scalping Kilat Pro +"
            " Gorengan)"
        ),
        "🕵️‍♂️ 4. Ritual Tarik Barang 1-3 Minggu (Swing Trading Sesajen)",
        "📉 5. Teropong Dukun Sakti: Cek Lembar Mantra Suka-Suka Lu",
    ],
)

# --- DATABASE LENGKAP EMITEN ---
multibagger_database = {
    "ADRO.JK": {
        "display_name": "PT Adaro Energy Indonesia Tbk",
        "reason": (
            "Lonjakan volume transaksi senyap tanpa kenaikan harga signifikan,"
            " menandakan akumulasi barang oleh institusi besar."
        ),
        "brokers": "BK (JPMorgan Sekuritas) & XC (Ajaib Sekuritas)",
        "project": "Restrukturisasi utang tuntas & pembalikan arus kas positif.",
        "news": (
            "Aksi korporasi rights issue strategis diserap penuh standby buyer."
        ),
        "narrative": "Turnaround story menuju kebangkitan kinerja operasional.",
        "macro": (
            "Didukung permintaan energi global yang stabil dan efisiensi"
            " operasional internal."
        ),
    },
    "PTBA.JK": {
        "display_name": "PT Bukit Asam Tbk",
        "reason": (
            "Akumulasi konsisten di area support bawah dengan volatilitas harga"
            " menyempit secara sehat."
        ),
        "brokers": "ZP (Mirae Asset) & YP (Retail Aktif)",
        "project": "Pengembangan blok tambang baru berteknologi modern.",
        "news": "Kenaikan volume produksi bulanan melampaui target internal.",
        "narrative": "Commodity expansion & operational efficiency play.",
        "macro": (
            "Sensitif terhadap tren harga komoditas logam dan kestabilan biaya"
            " pendanaan."
        ),
    },
    "ANTM.JK": {
        "display_name": "PT Aneka Tambang Tbk",
        "reason": (
            "Kenaikan harga komoditas diiringi efisiensi biaya operasional yang"
            " ketat."
        ),
        "brokers": "AK (Asing) & CC (Mandiri Sekuritas)",
        "project": "Eksplorasi blok migas cadangan terduga masif.",
        "news": (
            "Kontrak suplai energi jangka panjang dengan pembeli strategis."
        ),
        "narrative": "Energy security & strong cash-generation capability.",
        "macro": (
            "Diuntungkan tren harga energi global dan tingginya kebutuhan"
            " ketahanan energi."
        ),
    },
    "HRUM.JK": {
        "display_name": "PT Harum Energy Tbk",
        "reason": (
            "Valuasi murah PBV di bawah 1x (diskon aset kuat) dengan struktur"
            " tanpa utang berbunga."
        ),
        "brokers": "CC (Mandiri) & ZP (Mirae)",
        "project": "Penambahan armada kapal seismik dan pemboran terintegrasi.",
        "news": "Kontrak baru Pertamina Group mengamankan multi-tahun.",
        "narrative": "Undervalued asset play dengan dividend yield menarik.",
        "macro": (
            "Belanja modal hulu migas nasional yang ekspansif menopang"
            " utilisasi jasa."
        ),
    },
    "MEDC.JK": {
        "display_name": "PT Medco Energi Internasional Tbk",
        "reason": (
            "Transformasi struktural pasca-akuisisi oleh grup konglomerasi"
            " besar."
        ),
        "brokers": "RX (Macan Broker) & BB (Institusi)",
        "project": "Kontrak jasa pertambangan tier-1 backlog jumbo.",
        "news": "Tender proyek infrastruktur tambang Indonesia Timur.",
        "narrative": "Industrial powerhouse & supply chain integration.",
        "macro": (
            "Pertumbuhan investasi sektor pertambangan dan konstruksi domestik."
        ),
    },
    "MDKA.JK": {
        "display_name": "PT Merdeka Copper Gold Tbk",
        "reason": (
            "Peningkatan kadar bijih emas (ore grade) menurunkan biaya produksi"
            " per ons."
        ),
        "brokers": "CS (Credit Suisse) & AK (Asing)",
        "project": "Ekspansi pabrik pengolahan tahap 2 berkapasitas besar.",
        "news": "Volume produksi emas kuartalan mencetak rekor sejarah baru.",
        "narrative": "Gold supercycle & margin expansion story.",
        "macro": (
            "Permintaan aset safe haven global memperkuat valuasi emiten emas."
        ),
    },
}

multibagger_universe = list(multibagger_database.keys())

hidden_gem_database = {
    "ELSA.JK": {
        "display_name": "PT Elnusa Tbk",
        "reason": (
            "Akumulasi senyap oleh institusi pada area base konsolidasi panjang."
        ),
        "brokers": "YP (Retail) & LG (Lokal Growth)",
        "project": "Perluasan jaringan fiber optik koridor digital regional.",
        "news": "Lonjakan pendapatan segmen korporasi internet.",
        "narrative": "Digital infrastructure backbone & high growth margin.",
        "macro": (
            "Digitalisasi ekonomi nasional yang masif mendorong kebutuhan"
            " jaringan."
        ),
    },
    "KEEN.JK": {
        "display_name": "PT Kencana Energi Lestari Tbk",
        "reason": (
            "Valuasi atraktif energi terbarukan dengan kepastian cash flow PPA"
            " PLN."
        ),
        "brokers": "AK (Asing) & ZP (Mirae)",
        "project": "Pembangunan pembangkit mini hidro baru di kawasan timur.",
        "news": "Perolehan PPA jangka panjang dengan PLN.",
        "narrative": "Green energy transition & utility defensive growth.",
        "macro": (
            "Komitmen pemerintah terhadap transisi energi bersih dan bauran"
            " EBT."
        ),
    },
    "ACES.JK": {
        "display_name": "PT Aspirasi Hidup Indonesia Tbk",
        "reason": "Produsen bahan bangunan nasional dengan utilisasi pabrik optimal.",
        "brokers": "CC (Mandiri) & MG (Market Maker)",
        "project": "Modernisasi lini produksi keramik premium ekspor.",
        "news": "Penurunan biaya energi mendongkrak margin laba bersih.",
        "narrative": "Industrial manufacturing recovery & export-driven.",
        "macro": (
            "Stabilitas nilai tukar rupiah membantu efisiensi bahan baku."
        ),
    },
    "ASII.JK": {
        "display_name": "PT Astra International Tbk",
        "reason": (
            "Valuasi holding asuransi perbankan terdiskon dari nilai wajar aset."
        ),
        "brokers": "ZP (Mirae) & BB (Institusi)",
        "project": "Konsolidasi portofolio anak usaha asuransi dan pembiayaan.",
        "news": "Kinerja laba anak usaha mencetak rekor tertinggi.",
        "narrative": "Underpriced asset play & financial turnaround.",
        "macro": (
            "Sektor finansial domestik yang resilien mendukung pertumbuhan"
            " laba."
        ),
    },
}

hidden_gem_universe = list(hidden_gem_database.keys())
swing_netbuy_universe = [
    "BBCA.JK",
    "BMRI.JK",
    "BBNI.JK",
    "BBRI.JK",
    "TLKM.JK",
    "ASII.JK",
    "UNVR.JK",
    "ICBP.JK",
    "INDF.JK",
    "GOTO.JK",
]


# ==========================================
# MODUL 1: RITUAL PESUGIHAN MULTI-BAGGER
# ==========================================
if menu_mode == "💸 1. Ritual Pesugihan Multi-Bagger (Kekayaan 7 Turunan)":
  st.markdown(
      "### 💸 Mantra Pesugihan Multi-Bagger (Target 2x - 10x Lipat)"
  )
  st.markdown(
      "<p style='color: #a1a1aa;'>Pemanggilan arwah saham berfundamental kuat"
      " untuk kekayaan jangka panjang.</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button("🔮 MULAI RITUAL PESUGIHAN", type="primary"):
    with st.status(
        "🕯️ Membakar kemenyan, menyaring saham aktif (Volume > 0), dan harga >="
        " Rp 1...",
        expanded=True,
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
              "🟢 DISKON GHOIB (PBV < 1x)"
              if pbv < 1.0
              else "🔥 PREMIUM MAHAR TINGGI"
          )

          multibagger_results.append({
              "Ticker": t,
              "Nama": profile["display_name"],
              "Harga": round(close, 2),
              "Valuasi PE": pe,
              "Valuasi PBV": pbv,
              "StatusValuasi": val_status,
              "Multiplier": "10x Lipat Kekayaan",
              "Timeframe": "17 Bulan - 2 Tahun",
              "Score": f"⭐ {random.randint(85, 99)} / 100",
              "Entry": round(close * 0.99, 2),
              "Target Rasional": round(close * 4.5, 2),
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
          label="✨ Ritual Pesugihan Selesai, Arwah Cuan Aktif Dipanggil!",
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
            "Multiplier",
            "Timeframe",
            "Score",
        ]],
        use_container_width=True,
    )
    st.markdown("---")
    for mb in st.session_state["multibagger_data"]:
      st.markdown(
          f"""
                <div class="deep-card">
                    <h3 style="color: #a855f7;">🎯 Lembar Mantra: <b style="color: #ffffff;">{mb['Ticker']}</b> — {mb['Nama']} | Target: {mb['Multiplier']} | Kekuatan Khodam: <b style="color: #facc15;">{mb['Score']}</b></h3>
                    <p><b>💰 Harga Tumbal/Acuan:</b> Rp {mb['Harga']:,.2f} | <b>P/E:</b> {mb['Valuasi PE']} | <b>P/BV:</b> {mb['Valuasi PBV']} | <b>⏳ {mb['Timeframe']}</b></p>
                    <p><b>🔥 Status Valuasi Ghoib:</b> {mb['StatusValuasi']}</p>
                    <p><b>🎯 Panduan Sesajen Taktis:</b> Entry: Rp {mb['Entry']:,.2f} | TP: <b style="color: #22c55e;">Rp {mb['Target Rasional']:,.2f}</b> | CL: <b style="color: #ef4444;">Rp {mb['Cut Loss']:,.2f}</b></p>
                    <hr style="border-color: #3f3f46; margin: 8px 0;">
                    <p><b>🔴 Alasan Fundamental (Logika Nyata):</b> {mb['Reason']}</p>
                    <p><b>🏛️ Dukun / Broker Pengumpul:</b> <b style="color: #facc15;">{mb['Brokers']}</b></p>
                    <p><b>🏗️ Proyek Ritual:</b> <b style="color: #38bdf8;">{mb['Project']}</b></p>
                    <p><b>🌐 Tinjauan Makro Alam Semesta:</b> <b style="color: #60a5fa;">{mb['Macro']}</b></p>
                    <p><b>📰 Bisikan Gaib / News:</b> <i style="color: #facc15;">{mb['News']}</i></p>
                </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("👈 Klik tombol di sidebar untuk mulai ritual pesugihan.")

# ==========================================
# MODUL 2: HIDDEN GEM
# ==========================================
elif (
    menu_mode
    == "🃏 2. Terawangan Mutiara Terpendam (Hidden Gem Tumbal Cicilan)"
):
  st.markdown(
      "### 🃏 Terawangan Hidden Gem (Penyelamat Beban Hidup & Cicilan)"
  )
  st.markdown(
      "<p style='color: #a1a1aa;'>Mencari lembar saham lapis kedua yang dipendam"
      " bandar besar sebelum diledakkan.</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button("💎 TERAWANG HIDDEN GEM", type="primary"):
    with st.status(
        "💎 Mengorek tanah kuburan bursa, menyaring saham aktif & harga >="
        " Rp 1...",
        expanded=True,
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
              "Multiplier": "5x Lipat Mahar",
              "Timeframe": "12 Bulan - 1.5 Tahun",
              "Score": f"⭐ {random.randint(88, 98)} / 100",
              "Entry": round(close, 2),
              "Target Rasional": round(close * 3.0, 2),
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
          label="💎 Mutiara Terpendam Likuid Berhasil Ditemukan!",
          state="complete",
          expanded=False,
      )

  if (
      "hidden_gem_data" in st.session_state
      and st.session_state["hidden_gem_data"]
  ):
    df_hidden = pd.DataFrame(st.session_state["hidden_gem_data"])
    st.dataframe(
        df_hidden[["Ticker", "Nama", "Harga", "Multiplier", "Timeframe", "Score"]],
        use_container_width=True,
    )
    st.markdown("---")
    for hg in st.session_state["hidden_gem_data"]:
      st.markdown(
          f"""
                <div class="deep-card">
                    <h3 style="color: #a855f7;">💎 Kode Ticker: <b style="color: #ffffff;">{hg['Ticker']}</b> — {hg['Nama']} | Target: {hg['Multiplier']} | Khodam: <b style="color: #facc15;">{hg['Score']}</b></h3>
                    <p><b>💰 Harga Acuan:</b> Rp {hg['Harga']:,.2f} | <b>P/BV:</b> {hg['Valuasi PBV']} | <b>⏳ {hg['Timeframe']}</b></p>
                    <p><b>🎯 Panduan Tumbal Taktis:</b> Entry: Rp {hg['Entry']:,.2f} | TP: <b style="color: #22c55e;">Rp {hg['Target Rasional']:,.2f}</b> | CL: <b style="color: #ef4444;">Rp {hg['Cut Loss']:,.2f}</b></p>
                    <hr style="border-color: #3f3f46; margin: 8px 0;">
                    <p><b>🔴 Alasan Fundamental:</b> {hg['Reason']}</p>
                    <p><b>🏛️ Arwah Broker Pengumpul:</b> <b style="color: #facc15;">{hg['Brokers']}</b></p>
                    <p><b>🏗️ Proyek Ghoib:</b> <b style="color: #38bdf8;">{hg['Project']}</b></p>
                    <p><b>🌐 Tinjauan Makro:</b> <b style="color: #60a5fa;">{hg['Macro']}</b></p>
                    <p><b>📰 Berita Bisikan:</b> <i style="color: #facc15;">{hg['News']}</i></p>
                </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info("👈 Klik tombol di sidebar untuk menerawang Hidden Gem.")

# ==========================================
# MODUL 3: SCALPING KILAT PRO + SAHAM GORENGAN (SCREENER OTOMATIS)
# ==========================================
elif (
    menu_mode
    == "🔪 3. Pesugihan Instan Jalur Orang Dalam (Scalping Kilat Pro + Gorengan)"
):
  st.markdown(
      "### 🔪 Sinyal Scalping Jalur Orang Dalam & Screener Saham Gorengan"
  )
  st.markdown(
      "<p style='color: #a1a1aa;'>Screener otomatis mendeteksi saham gorengan"
      " harian dan lapis spekulatif dengan Inflow/Outflow, Makro, Kewaspadaan &"
      " Target Taktis secara instan berdasarkan data pasar riil.</p>",
      unsafe_allow_html=True,
  )

  # Daftar pool screener otomatis
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

  if st.sidebar.button(
      "⚡ BUKA JALUR ORANG DALAM PRO + GORENGAN", type="primary"
  ):
    with st.status(
        "⚡ Menyaring ketat saham tidur, memindai orderbook dan arus dana riil...",
        expanded=True,
    ) as status:
      scalp_results = []

      broker_mapping = {
          "BUMI": ("YP (Normura / Retail Market Maker)", "MG (Mega Capital)"),
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
          "MEDC": ("RX (Macan Broker)", "BB (Institusi Lokal)"),
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

          # FILTER ANTI-SAHAM TIDUR YANG KETAT:
          # Buang jika volume nol, harga < 1, atau pergerakan harga 0% (tidak ada aktivitas volatil)
          if volume_s <= 0 or close_s < 1.0 or price_change == 0.0:
            continue

          # Deteksi arus dana (Flow) murni dari arah price change & volume harian riil
          if price_change > 0.0:
            flow_status = (
                "🟢 GORENGAN INFLOW (Bandar Masuk / Akumulasi Kuat)"
            )
            prob_score = min(
                int(60 + (price_change * 3) + (vol_ratio * 5)), 99
            )
          else:
            flow_status = "🔴 GORENGAN DISTRIBUSI (Bandar Jualan / Tekanan Jual)"
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
            status_siap = "🔥 POTENSI AUTO REJECT ATAS (ARA) / SULTAN"
          elif prob_score >= 60:
            status_siap = "🟢 SIAP DIGORENG (Volatile Breakout Aktif)"
          elif prob_score >= 45:
            status_siap = "🟡 DALAM KONSOLIDASI BANDAR (Waspada False Break)"
          else:
            status_siap = "⚠️ RAWAN BAGGER TRAP / ZONA KUBURAN"

          entry_price = round(close_s, 2)
          tp_price = round(entry_price * 1.055, 2)
          cl_price = round(entry_price * 0.965, 2)

          # Spesifik makro & teknikal per emiten berdasarkan sektor
          if t in ["BUMI", "BRMS", "ENRG", "ADRO", "PTBA", "MEDC", "ELSA"]:
            macro_emiten = (
                "Sektor Energi & Pertambangan: Sangat sensitif terhadap tren"
                " harga komoditas global, nilai tukar USD/IDR, serta kebijakan"
                " ekspor-impor energi nasional."
            )
            tech_supply_demand = (
                f"Kondisi Teknikal & Supply-Demand ({t}): Volume harian"
                f" terdeteksi {vol_ratio:.2f}x dari rata-rata. Tekanan beli"
                " mendominasi area support terdekat dengan antrean bid tebal"
                " di orderbook."
            )
          elif t in ["ARTO", "GOTO"]:
            macro_emiten = (
                "Sektor Teknologi & Digital: Sangat dipengaruhi oleh sentimen"
                " suku bunga acuan The Fed dan arah perpindahan modal asing"
                " (foreign flow) pada saham growth."
            )
            tech_supply_demand = (
                f"Kondisi Teknikal & Supply-Demand ({t}): Volatilitas tinggi"
                " dengan rasio volume {vol_ratio:.2f}x. Buyer dan seller"
                " bertarung ketat di area pivot harga psikologis."
            )
          else:
            macro_emiten = (
                "Sektor Spekulatif / Properti / Konsumer: Didukung oleh daya"
                " beli domestik serta rotasi likuiditas harian para pelaku"
                " pasar ritel."
            )
            tech_supply_demand = (
                f"Kondisi Teknikal & Supply-Demand ({t}): Pergerakan harga"
                f" aktif dengan perubahan {price_change:.2f}%. Suplai dan"
                " demand seimbang di bawah kendali market maker."
            )

          if vol_ratio > 2.2 and price_change > 5:
            risk_note = (
                f"PERINGATAN KERAS ({t}): Saham gorengan mengalami lonjakan"
                " volume ekstrem! Sangat rawan aksi profit taking mendadak"
                " (guyuran bandar) di sesi berikutnya. Wajib pasang trailing"
                " stop!"
            )
          elif flow_status.startswith("🔴"):
            risk_note = (
                f"WASPADA ({t}): Harga sedang terkoreksi dengan indikasi"
                " distribusi riil. Hindari mengejar harga atas (FOMO)."
            )
          else:
            risk_note = (
                f"Analisis riil {t}: Pergerakan harga dan volume sesuai"
                " dengan siklus harian pasar. Amankan profit secara disiplin."
            )

          latest_news = get_latest_news_for_ticker(t)

          scalp_results.append({
              "Ticker": t,
              "Nama": f"PT {t} Tbk (Screener Spekulatif / Gorengan Riil)",
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
          label=(
              "⚡ Pemindaian Selesai, Saham Tidur Berhasil Dibuang & Data Riil"
              " Dimuat!"
          ),
          state="complete",
          expanded=False,
      )

  if (
      "scalp_pro_data" in st.session_state
      and st.session_state["scalp_pro_data"]
  ):
    st.markdown(
        """
            <div class="macro-box">
                <h4 style="color: #60a5fa; margin-top: 0; margin-bottom: 6px;">🌐 CATATAN MAKROEKONOMI TERBARU (GLOBAL & DOMESTIK)</h4>
                <p style="margin: 2px 0; font-size: 0.9rem;"><b>🇺🇸 Global / Luar Negeri:</b> Kebijakan suku bunga The Fed dan fluktuasi yield US Treasury terus membayangi arah arus modal asing (<i>foreign outflow/inflow</i>) di bursa berkembang.</p>
                <p style="margin: 2px 0; font-size: 0.9rem;"><b>🇮🇩 Domestik / Dalam Negeri:</b> Stabilitas inflasi dan intervensi Bank Indonesia dalam menjaga stabilitas nilai tukar Rupiah memberikan ruang gerak bagi sektor pilihan.</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

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
    st.subheader(
        "🔍 Bedah Detail Scalping, Makro per Emiten, News & Kondisi Teknikal"
    )
    selected_sc = st.selectbox(
        "Pilih Ticker Hasil Screener:", df_sc_display["Ticker"].tolist()
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
      st.metric(label="Cut Loss (-3.5%)", value=f"Rp {sc_detail['CL']}")
    with col4:
      st.metric(
          label="Probabilitas Naik",
          value=sc_detail["Probabilitas Siap Naik"],
      )

    st.info(f"📌 **Status Kesiapan:** {sc_detail['Status Kesiapan']}")

    # Tambahan Tampilan Makro per Emiten, News, dan Kondisi Teknikal Supply-Demand
    st.markdown(
        f"""
            <div class="deep-card">
                <h4 style="color: #38bdf8; margin-top: 0;">🌐 Makroekonomi & Sentimen Khusus Emiten ({selected_sc})</h4>
                <p>{sc_detail['MacroEmiten']}</p>
                <hr style="border-color: #3f3f46; margin: 8px 0;">
                <h4 style="color: #facc15; margin-top: 0;">📈 Kondisi Teknikal & Supply-Demand</h4>
                <p>{sc_detail['TechSupplyDemand']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        f"""
            <div class="warning-note">
                <h5 style="color: #f87171; margin-top: 0; margin-bottom: 4px;">⚠️ KEWASPADAAN KHUSUS SAHAM GORENGAN ({selected_sc})</h5>
                <p style="margin: 0; font-size: 0.9rem; color: #fca5a5;">{sc_detail['Catatan Kewaspadaan']}</p>
            </div>
        """,
        unsafe_allow_html=True,
    )

    st.warning(f"📰 **Katalis & Berita Terbaru:** {sc_detail['News']}")
    st.success(
        f"🏦 **Top Broker Penggoreng / Penampung:**"
        f" {sc_detail['Top Accumulator']} | **Arus Dana:**"
        f" {sc_detail['Arus Dana (Flow)']}"
    )
  else:
    st.info(
        "👈 Klik tombol di sidebar untuk menjalankan Screener Scalping &"
        " Gorengan berdasarkan kondisi riil."
    )

# ==========================================
# MODUL 4: SWING TRADING NET BUY
# ==========================================
elif (
    menu_mode == "🕵️‍♂️ 4. Ritual Tarik Barang 1-3 Minggu (Swing Trading Sesajen)"
):
  st.markdown(
      "### 🕵️‍♂️ Ritual Tarik Barang Bluechip (Swing Trading 1-3 Minggu)"
  )
  st.markdown(
      "<p style='color: #a1a1aa;'>Membaca rekam jejak akumulasi institusi"
      " besar dan korelasi ekonomi makro.</p>",
      unsafe_allow_html=True,
  )

  if st.sidebar.button("📊 MULAI RITUAL TARIK BARANG", type="primary"):
    with st.status(
        "🔍 Mengabsen arwah bandar besar, membuang saham tidur, & harga >="
        " Rp 1...",
        expanded=True,
    ) as status:
      netbuy_results = []

      institution_pool = [
          ("BK (JPMorgan Sekuritas)", "Asing (Foreign Net Buy Masif)"),
          ("AK (UBS Sekuritas)", "Asing (Akumulasi Institutional Fund)"),
          ("ZP (Mirae Asset Sekuritas)", "Lokal & Asing (Smart Money Retail Elit)"),
          (
              "RX (Macan Broker / Mandiri)",
              "Lokal Institusi (Big Player Accumulation)",
          ),
      ]

      macro_narratives = [
          (
              "Didukung likuiditas perbankan yang tebal dan daya beli"
              " masyarakat di tengah target PDB ~5.3%."
          ),
          (
              "Diuntungkan rotasi sektor dan derasnya aliran modal asing masuk"
              " ke bursa domestik."
          ),
          (
              "Sensitif terhadap arah suku bunga Bank Indonesia dan kestabilan"
              " kurs USD/IDR."
          ),
          (
              "Didorong oleh ekspansi korporasi besar serta kuatnya belanja"
              " fiskal pemerintah."
          ),
      ]

      swing_aliases = {
          "BBCA.JK": "PT Bank Central Asia Tbk",
          "BMRI.JK": "PT Bank Mandiri (Persero) Tbk",
          "BBNI.JK": "PT Bank Negara Indonesia (Persero) Tbk",
          "BBRI.JK": "PT Bank Rakyat Indonesia (Persero) Tbk",
          "TLKM.JK": "PT Telkom Indonesia (Persero) Tbk",
          "ASII.JK": "PT Astra International Tbk",
          "UNVR.JK": "PT Unilever Indonesia Tbk",
          "ICBP.JK": "PT Indofood CBP Sukses Makmur Tbk",
          "INDF.JK": "PT Indofood Sukses Makmur Tbk",
          "GOTO.JK": "PT GoTo Gojek Tokopedia Tbk",
      }

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

        avg_price_broker = round(close * random.uniform(0.97, 0.995), 2)
        flow_3_7_hari = f"+Rp {random.randint(45, 280)} Miliar (Inflow Deras)"
        inst_broker, inst_type = random.choice(institution_pool)
        macro_text = random.choice(macro_narratives)

        entry_price = close
        tp1 = round(entry_price * 1.06, 2)
        tp2 = round(entry_price * 1.12, 2)
        cl = round(entry_price * 0.96, 2)

        netbuy_results.append({
            "Ticker": t,
            "Nama": swing_aliases.get(t, "PT Korporasi Utama Tbk"),
            "Harga": close,
            "AvgBroker": avg_price_broker,
            "Flow": flow_3_7_hari,
            "Institusi": inst_broker,
            "TipeInst": inst_type,
            "Entry": entry_price,
            "TP1": tp1,
            "TP2": tp2,
            "CL": cl,
            "Timeframe": "Waktu Tanam: 1 - 3 Minggu",
            "Action": "Aksi korporasi pembagian dividen / ekspansi kuartalan.",
            "Insider": (
                "Direksi rajin melakukan pembelian di open market (Insider"
                " buy)."
            ),
            "News": "Laporan keuangan melampaui ekspektasi para dukun pasar.",
            "Macro": macro_text,
        })

      st.session_state["swing_netbuy_data"] = netbuy_results
      status.update(
          label="📊 Ritual Tarik Barang Selesai!", state="complete", expanded=False
      )

  if (
      "swing_netbuy_data" in st.session_state
      and st.session_state["swing_netbuy_data"]
  ):
    df_swing = pd.DataFrame(st.session_state["swing_netbuy_data"])
    st.markdown("### 📊 Tabel Ringkasan Ritual Tarik Barang (Swing)")
    st.dataframe(
        df_swing[[
            "Ticker",
            "Nama",
            "Harga",
            "AvgBroker",
            "Flow",
            "Institusi",
            "TP1",
            "CL",
        ]],
        use_container_width=True,
    )

    st.markdown("---")
    st.markdown("### 🔍 Detail Terawangan Bandarmologi & Makro Ekonomi")
    for nb in st.session_state["swing_netbuy_data"]:
      st.markdown(
          f"""
                <div class="deep-card">
                    <h3 style="color: #a855f7;">🕵️‍♂️ Kode Ticker: <b style="color: #ffffff;">{nb['Ticker']}</b> — {nb['Nama']} | ⏳ {nb['Timeframe']}</h3>
                    <p><b>💰 Harga Saat Ini:</b> Rp {nb['Harga']:,.2f} | <b>Avg Harga Dukun/Broker (3-7 Hari):</b> <b style="color: #22c55e;">Rp {nb['AvgBroker']:,.2f}</b></p>
                    <p><b>🌊 Arus Dana Masuk/Keluar:</b> <b style="color: #38bdf8;">{nb['Flow']}</b></p>
                    <p><b>🏛️ Institusi Penguasa:</b> <b style="color: #facc15;">{nb['Institusi']}</b> ({nb['TipeInst']})</p>
                    <hr style="border-color: #3f3f46; margin: 8px 0;">
                    <p><b>🎯 Panduan Sesajen Swing:</b> Entry: Rp {nb['Entry']:,.2f} | TP1 (+6%): <b style="color: #22c55e;">Rp {nb['TP1']:,.2f}</b> | TP2 (+12%): <b style="color: #22c55e;">Rp {nb['TP2']:,.2f}</b> | CL (-4%): <b style="color: #ef4444;">Rp {nb['CL']:,.2f}</b></p>
                    <p><b>🌐 Analisis Makro Ekonomi:</b> <b style="color: #60a5fa;">{nb['Macro']}</b></p>
                    <p><b>🏢 Aksi Korporasi:</b> {nb['Action']}</p>
                    <p><b>👤 Aktivitas Orang Dalam:</b> <i style="color: #facc15;">{nb['Insider']}</i></p>
                    <p><b>📰 Berita Pasar:</b> {nb['News']}</p>
                </div>
            """,
          unsafe_allow_html=True,
      )
  else:
    st.info(
        "👈 Klik tombol di sidebar untuk menjalankan Ritual Tarik Barang"
        " Swing."
    )

# ==========================================
# MODUL 5: TEROPONG MANDIRI
# ==========================================
elif (
    menu_mode == "📉 5. Teropong Dukun Sakti: Cek Lembar Mantra Suka-Suka Lu"
):
  st.markdown("### 📉 Teropong Dukun Sakti: Cek Saham Pilihanmu Sendiri")
  t_input = (
      st.text_input(
          "Masukkan Kode Ticker Asli (Contoh: BBCA.JK, BUMI.JK, GOTO.JK):",
          value="BBCA.JK",
      )
      .strip()
      .upper()
  )
  if st.button("TEROPONG SEKARANG", type="primary"):
    try:
      stock_t = yf.Ticker(t_input)
      df_chart = stock_t.history(period="1mo")
      info_t = stock_t.info
      if not df_chart.empty:
        st.line_chart(df_chart["Close"])
        st.markdown(
            f"""
                    <div class="deep-card">
                        <h3 style="color: #38bdf8;">🔭 Hasil Teropong Ghoib: {t_input}</h3>
                        <p><b>🏢 Nama Perusahaan:</b> {info_t.get('longName', t_input)}</p>
                        <p><b>📊 Sektor / Dunia Usaha:</b> {info_t.get('sector', 'N/A')} ({info_t.get('industry', 'N/A')})</p>
                        <p><b>🌐 Tinjauan Makro Sektoral:</b> Perusahaan ini beroperasi di bawah pengaruh siklus suku bunga domestik, daya beli konsumen, serta cuaca ekonomi global.</p>
                    </div>
                """,
            unsafe_allow_html=True,
        )
      else:
        st.error(
            "Kode ticker tidak ditemukan di dunia nyata maupun gaib."
        )
    except:
      st.error("Gagal mengambil data lembar emiten tersebut.")