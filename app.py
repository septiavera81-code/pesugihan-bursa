from concurrent.futures import ThreadPoolExecutor
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
import time

import numpy as np
import pandas as pd
import requests
import streamlit as st
import yfinance as yf

# =========================================================================
# KONFIGURASI HALAMAN — AI AGENT THEME
# =========================================================================

st.set_page_config(
    page_title="🤖 AI Screener Saham BEI",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =========================================================================
# CSS AI AGENT — ANIMASI & GLASSMORPHISM
# =========================================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;600;800&family=Orbitron:wght@400;700&display=swap');

.stApp {
    background: linear-gradient(135deg, #0a0e1a 0%, #1a1a2e 50%, #16213e 100%);
}

@keyframes pulse {
    0%, 100% { opacity: 1; transform: scale(1); }
    50% { opacity: 0.5; transform: scale(0.95); }
}
@keyframes glow {
    0%, 100% { box-shadow: 0 0 20px rgba(56, 189, 248, 0.2); }
    50% { box-shadow: 0 0 50px rgba(56, 189, 248, 0.6); }
}
@keyframes float {
    0%, 100% { transform: translateY(0px); }
    50% { transform: translateY(-10px); }
}
@keyframes typing {
    from { width: 0; }
    to { width: 100%; }
}
@keyframes blink {
    0%, 100% { border-color: transparent; }
    50% { border-color: #38bdf8; }
}
@keyframes scanline {
    0% { transform: translateX(-100%); }
    100% { transform: translateX(100%); }
}
@keyframes rotateGlow {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.ai-avatar {
    width: 80px;
    height: 80px;
    border-radius: 50%;
    background: linear-gradient(135deg, #38bdf8, #818cf8);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 2.8rem;
    animation: pulse 2s ease-in-out infinite, float 3s ease-in-out infinite;
    box-shadow: 0 0 40px rgba(56, 189, 248, 0.3);
    margin: 0 auto 15px auto;
    position: relative;
}
.ai-avatar::after {
    content: '';
    position: absolute;
    inset: -4px;
    border-radius: 50%;
    background: conic-gradient(from 0deg, transparent, #38bdf8, transparent, #818cf8, transparent);
    animation: rotateGlow 3s linear infinite;
    z-index: -1;
}

.ai-status {
    background: rgba(30, 41, 59, 0.8);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.2);
    border-radius: 12px;
    padding: 12px 20px;
    margin: 10px 0;
    display: flex;
    align-items: center;
    gap: 15px;
    animation: glow 3s ease-in-out infinite;
    flex-wrap: wrap;
}

.ai-dot {
    width: 12px;
    height: 12px;
    border-radius: 50%;
    background: #22c55e;
    animation: pulse 1s ease-in-out infinite;
    display: inline-block;
}
.ai-dot.scanning {
    background: #f59e0b;
    animation: pulse 0.5s ease-in-out infinite;
}
.ai-dot.error {
    background: #ef4444;
    animation: none;
}

.typing-text {
    overflow: hidden;
    white-space: nowrap;
    border-right: 2px solid #38bdf8;
    animation: typing 2s steps(40) 1s forwards, blink 0.8s step-end infinite;
    width: 0;
    display: inline-block;
    font-family: 'Orbitron', monospace;
    color: #38bdf8;
}
.typing-text.done {
    width: 100%;
    border-right: none;
    animation: none;
}

.glass-card {
    background: rgba(30, 41, 59, 0.5);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 189, 248, 0.12);
    border-radius: 16px;
    padding: 20px;
    margin: 10px 0;
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 2px;
    background: linear-gradient(90deg, transparent, #38bdf8, transparent);
    animation: scanline 3s ease-in-out infinite;
}
.glass-card:hover {
    border-color: rgba(56, 189, 248, 0.4);
    transform: translateY(-3px);
    box-shadow: 0 10px 40px rgba(56, 189, 248, 0.15);
}

.deep-card {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 12px;
    border-left: 4px solid #3b82f6;
    transition: all 0.3s ease;
}
.deep-card:hover {
    border-left-color: #818cf8;
    transform: translateX(5px);
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.1);
}
.deep-card h3 {
    color: #38bdf8;
    font-family: 'Orbitron', monospace;
    font-size: 1.1rem;
}
.deep-card p {
    color: #cbd5e1;
    font-size: 0.9rem;
    margin-bottom: 4px;
}

.stSidebar {
    background: rgba(15, 23, 42, 0.9) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(56, 189, 248, 0.1) !important;
}
.stSidebar .stButton button {
    background: linear-gradient(135deg, #3b82f6, #818cf8) !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 10px !important;
    font-weight: 600 !important;
    transition: all 0.3s ease;
}
.stSidebar .stButton button:hover {
    transform: scale(1.02);
    box-shadow: 0 4px 20px rgba(56, 189, 248, 0.4);
}

.metric-strip {
    display: flex;
    gap: 12px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}
.metric-item {
    background: rgba(30, 41, 59, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(56, 189, 248, 0.15);
    border-radius: 10px;
    padding: 10px 16px;
    min-width: 140px;
    display: inline-block;
    margin-right: 10px;
    transition: all 0.3s ease;
}
.metric-item:hover {
    border-color: rgba(56, 189, 248, 0.4);
    transform: translateY(-2px);
}
.metric-item .val {
    font-size: 1.1rem;
    font-weight: 800;
    color: #38bdf8;
    font-family: 'Orbitron', monospace;
}
.metric-item .lbl {
    font-size: 0.65rem;
    color: #94a3b8;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.disclaimer {
    background: rgba(12, 26, 46, 0.8);
    border: 1px dashed rgba(71, 85, 105, 0.5);
    padding: 10px 14px;
    border-radius: 8px;
    color: #94a3b8;
    font-size: 0.75rem;
    margin-top: 10px;
}

::-webkit-scrollbar {
    width: 6px;
    height: 6px;
}
::-webkit-scrollbar-track {
    background: #1e293b;
}
::-webkit-scrollbar-thumb {
    background: #38bdf8;
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: #818cf8;
}

@media (max-width: 768px) {
    .ai-avatar { width: 60px; height: 60px; font-size: 2rem; }
    .typing-text { font-size: 0.85rem; white-space: normal; }
    .metric-item { min-width: 100px; padding: 8px 12px; }
    .metric-item .val { font-size: 0.9rem; }
}
</style>
""", unsafe_allow_html=True)

# =========================================================================
# AI AGENT STATE
# =========================================================================

if "ai_status" not in st.session_state:
    st.session_state.ai_status = "🟢 Online"
    st.session_state.ai_message = "Siap membantu analisis saham Anda."
    st.session_state.scan_count = 0
    st.session_state.last_scan = None
    st.session_state.typing_done = False

def ai_speak(message, status="🟢 Online"):
    st.session_state.ai_message = message
    st.session_state.ai_status = status
    st.session_state.typing_done = False

# =========================================================================
# HEADER AI AGENT
# =========================================================================

col1, col2, col3 = st.columns([1, 2.5, 1])
with col1:
    st.markdown('<div class="ai-avatar">🤖</div>', unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div style="text-align: center;">
        <h1 style="font-family: 'Orbitron', monospace; background: linear-gradient(135deg, #38bdf8, #818cf8); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-size: 2rem; margin-bottom: 5px;">
            AI SCREENER BEI
        </h1>
        <div style="font-size: 0.7rem; color: #64748b; font-family: 'Orbitron', monospace; letter-spacing: 2px; margin-bottom: 8px;">
            • REAL-TIME MARKET INTELLIGENCE •
        </div>
        <div class="ai-status">
            <span class="ai-dot {'scanning' if 'Scanning' in st.session_state.ai_status else ''}"></span>
            <span style="color:#94a3b8;font-size:0.75rem;font-family:'Orbitron',monospace;">STATUS:</span>
            <span style="color:#f8fafc;font-weight:600;font-family:'Orbitron',monospace;font-size:0.8rem;">{st.session_state.ai_status}</span>
            <span style="color:#334155;">|</span>
            <span style="color:#94a3b8;font-size:0.75rem;font-family:'Orbitron',monospace;">
                ⏱️ {st.session_state.last_scan or '—'}
            </span>
            <span style="color:#334155;">|</span>
            <span style="color:#94a3b8;font-size:0.75rem;font-family:'Orbitron',monospace;">
                📊 {st.session_state.scan_count} scanned
            </span>
        </div>
        <div style="margin-top:6px;">
            <span style="color:#38bdf8;font-family:'Orbitron',monospace;font-size:0.8rem;">
                <span class="typing-text {'done' if st.session_state.typing_done else ''}">{st.session_state.ai_message}</span>
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div style="text-align:right; padding-top:20px;">
        <span style="color:#334155;font-size:0.6rem;font-family:'Orbitron',monospace;">
            v4.0 • AI-POWERED
        </span>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# =========================================================================
# FUNGSI UTILITY
# =========================================================================

@st.cache_data(ttl=21600, show_spinner=False)
def get_wb_macro():
    out = {}
    fallback = {"gdp": (2024, 5.0), "infl": (2024, 2.8)}
    for key, ind in [("gdp", "NY.GDP.MKTP.KD.ZG"), ("infl", "FP.CPI.TOTL.ZG")]:
        try:
            url = f"https://api.worldbank.org/v2/country/IDN/indicator/{ind}?format=json&per_page=6&date=2019:2026"
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 1 and data[1]:
                    for row in data[1]:
                        if row.get("value") is not None:
                            out[key] = (int(row["date"]), float(row["value"]))
                            break
            if key not in out:
                out[key] = fallback.get(key, (2024, 0))
        except Exception:
            out[key] = fallback.get(key, (2024, 0))
    return out

@st.cache_data(ttl=300, show_spinner=False)
def get_index_quotes():
    out = {}
    try:
        data = yf.download("^JKSE", period="5d", interval="1d", progress=False, auto_adjust=True)
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                closes = data["Close"]["^JKSE"].dropna().values
            else:
                closes = data["Close"].dropna().values
            if len(closes) >= 2:
                last, prev = float(closes[-1]), float(closes[-2])
                out["^JKSE"] = {"last": last, "chg": (last - prev) / prev * 100}
            elif len(closes) == 1:
                out["^JKSE"] = {"last": float(closes[-1]), "chg": 0}
    except Exception:
        out["^JKSE"] = {"last": 7200, "chg": 0}
    try:
        data = yf.download("IDR=X", period="5d", interval="1d", progress=False, auto_adjust=True)
        if not data.empty:
            if isinstance(data.columns, pd.MultiIndex):
                closes = data["Close"]["IDR=X"].dropna().values
            else:
                closes = data["Close"].dropna().values
            if len(closes) >= 2:
                last, prev = float(closes[-1]), float(closes[-2])
                out["IDR=X"] = {"last": last, "chg": (last - prev) / prev * 100}
            elif len(closes) == 1:
                out["IDR=X"] = {"last": float(closes[-1]), "chg": 0}
    except Exception:
        out["IDR=X"] = {"last": 15500, "chg": 0}
    return out

@st.cache_data(ttl=86400, show_spinner=False)
def get_all_idx_tickers():
    try:
        url = "https://raw.githubusercontent.com/wildangunawan/Dataset-Saham-IDX/master/List%20Emiten/all_emiten.csv"
        df = pd.read_csv(url)
        col = "Ticker" if "Ticker" in df.columns else df.columns[0]
        raw = df[col].dropna().astype(str).str.strip().str.upper().tolist()
        return sorted({t if t.endswith(".JK") else t + ".JK" for t in raw})
    except Exception:
        return sorted(["BBCA.JK", "BBRI.JK", "BMRI.JK", "TLKM.JK", "ASII.JK", "ADRO.JK",
                       "PTBA.JK", "ANTM.JK", "MDKA.JK", "HRUM.JK", "CPIN.JK", "INKP.JK",
                       "PWON.JK", "BSDE.JK", "BRPT.JK", "SMGR.JK", "KLBF.JK", "ICBP.JK",
                       "INDF.JK", "GOTO.JK"])

@st.cache_data(ttl=900, show_spinner=False)
def get_all_ohlcv(tickers_tuple, period="6mo"):
    return yf.download(list(tickers_tuple), period=period, interval="1d",
                       group_by="ticker", threads=True, progress=False, auto_adjust=True)

@st.cache_data(ttl=21600, show_spinner=False)
def get_fundamentals(tickers_tuple):
    out = {}
    def fetch(t):
        try:
            info = yf.Ticker(t).info
            out[t] = {
                "longName": info.get("longName") or info.get("shortName") or t.replace(".JK", ""),
                "sector": info.get("sector") or "-",
                "marketCap": info.get("marketCap"),
                "trailingPE": info.get("trailingPE"),
                "priceToBook": info.get("priceToBook"),
                "returnOnEquity": info.get("returnOnEquity"),
                "debtToEquity": info.get("debtToEquity"),
                "revenueGrowth": info.get("revenueGrowth"),
                "earningsGrowth": info.get("earningsGrowth"),
                "profitMargins": info.get("profitMargins"),
            }
        except Exception:
            out[t] = None
    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(fetch, tickers_tuple))
    return out

def add_indicators(df):
    df = df.copy()
    c = df["Close"]
    for p in [20, 50, 200]:
        df[f"MA{p}"] = c.rolling(p).mean()
    delta = c.diff()
    gain = delta.clip(lower=0).ewm(alpha=1/14, adjust=False).mean()
    loss = -delta.clip(upper=0).ewm(alpha=1/14, adjust=False).mean()
    rs = gain / loss.replace(0, np.nan)
    df["RSI14"] = 100 - 100 / (1 + rs)
    tr = pd.concat([df["High"]-df["Low"], (df["High"]-c.shift()).abs(), (df["Low"]-c.shift()).abs()], axis=1).max(axis=1)
    df["ATR14"] = tr.ewm(alpha=1/14, adjust=False).mean()
    ema12, ema26 = c.ewm(span=12, adjust=False).mean(), c.ewm(span=26, adjust=False).mean()
    df["MACD"] = ema12 - ema26
    df["MACD_SIG"] = df["MACD"].ewm(span=9, adjust=False).mean()
    df["VOL_AVG20"] = df["Volume"].rolling(20).mean()
    df["VOL_RATIO"] = df["Volume"] / df["VOL_AVG20"]
    return df

def classify_market_cap(market_cap):
    if market_cap is None or (isinstance(market_cap, float) and np.isnan(market_cap)):
        return "N/A"
    if market_cap >= 4e13: return "Big Cap"
    if market_cap >= 1e13: return "Mid Cap"
    if market_cap >= 2e12: return "Small Cap"
    return "Micro Cap"

def fmt_rp(val):
    if val is None or (isinstance(val, float) and np.isnan(val)):
        return "N/A"
    if val >= 1e12: return f"Rp {val/1e12:.2f} T"
    if val >= 1e9: return f"Rp {val/1e9:.1f} M"
    return f"Rp {val:,.0f}"

# =========================================================================
# iter_frames — PERUBAHAN: minimal 10 hari data
# =========================================================================

def iter_frames(data, tickers):
    if data.empty:
        return
    cols = data.columns.get_level_values(0)
    for t in tickers:
        if t not in cols:
            continue
        try:
            df = data[t].dropna(subset=["Close"])
            # Minimal 10 hari data (dari 30)
            if len(df) >= 10 and df["Volume"].sum() > 0:
                yield t, add_indicators(df)
        except Exception:
            continue

# =========================================================================
# BERITA & MAKRO
# =========================================================================

POS_WORDS = [
    "tumbuh", "pertumbuhan", "naik", "menguat", "melonjak", "surplus",
    "ekspansi", "stimulus", "pemulihan", "relief", "positif", "optimis",
    "penurunan inflasi", "inflasi turun", "suku bunga turun",
    "bank indonesia turunkan", "turunkan suku bunga", "genjot",
    "penurunan suku bunga", "ekspor naik", "masuk dana asing",
    "foreign buying", "dana asing masuk", "investasi masuk", "dividen",
    "laba", "profit", "pendapatan naik", "order", "kontrak",
]
NEG_WORDS = [
    "resesi", "perang", "eskalsasi", "sanksi", "konflik", "tarif",
    "inflasi melonjak", "inflasi naik", "suku bunga naik",
    "kenaikan suku bunga", "the fed naikkan", "defisit", "jatuh",
    "melemah", "kekhawatiran", "risiko", "phk", "pemutusan hubungan kerja",
    "perlambatan", "bencana", "krisis", "tekanan", "jual asing",
    "foreign selling", "dana asing keluar", "memanas", "serangan",
    "turun", "rugi", "penurunan", "default", "gagal bayar",
]

NEWS_FEEDS = {
    "🌍 Geopolitik": "geopolitik OR perang OR konflik OR sanksi OR tarif",
    "💵 Makro Global": "The Fed OR FOMC OR suku bunga AS OR inflasi global",
    "🇮🇩 Makro Indonesia": "BI rate OR suku bunga BI OR inflasi Indonesia",
    "📊 Bursa & IHSG": "IHSG OR bursa saham Indonesia OR foreign flow",
}

@st.cache_data(ttl=900, show_spinner=False)
def fetch_gnews(query, max_items=6):
    try:
        q = urllib.parse.quote(query)
        r = requests.get(f"https://news.google.com/rss/search?q={q}&hl=id&gl=ID&ceid=ID:id", timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        root = ET.fromstring(r.content)
        items = []
        for it in root.iter("item"):
            src = it.find("source")
            items.append({"title": it.findtext("title") or "", "link": it.findtext("link") or "", "pub": it.findtext("pubDate") or "", "source": (src.text if src is not None else "")})
            if len(items) >= max_items: break
        return items
    except: return []

def _sentiment_score(items):
    skor = 0
    for it in items:
        t = (it.get("title") or "").lower()
        skor += sum(1 for w in POS_WORDS if w in t)
        skor -= sum(1 for w in NEG_WORDS if w in t)
    return skor

def impact_label(s):
    if s >= 4: return "🟢🟢 Positif kuat"
    if s >= 2: return "🟢 Positif"
    if s <= -4: return "🔴🔴 Negatif kuat"
    if s <= -2: return "🔴 Negatif"
    return "⚪ Netral"

def render_news_section():
    quotes = get_index_quotes()
    wb_data = get_wb_macro()
    strip = '<div class="metric-strip">'
    for key, label in [("^JKSE", "IHSG"), ("IDR=X", "USD/IDR")]:
        d = quotes.get(key, {})
        if d:
            last, chg = d.get("last"), d.get("chg", 0)
            if isinstance(last, (int, float)):
                color = "#22c55e" if chg >= 0 else "#ef4444"
                strip += f'<div class="metric-item"><div class="lbl">{label}</div><div class="val" style="color:{color}">{last:,.2f} ({chg:+.2f}%)</div></div>'
    if wb_data.get("gdp"):
        y, v = wb_data["gdp"]
        strip += f'<div class="metric-item"><div class="lbl">PDB RI ({y})</div><div class="val">{v:.2f}%</div></div>'
    if wb_data.get("infl"):
        y, v = wb_data["infl"]
        strip += f'<div class="metric-item"><div class="lbl">Inflasi RI ({y})</div><div class="val">{v:.2f}%</div></div>'
    strip += "</div>"
    st.markdown(strip, unsafe_allow_html=True)
    with st.expander("🌐 Berita Makro & Analisis IHSG", expanded=False):
        total = 0
        for label, query in NEWS_FEEDS.items():
            items = fetch_gnews(query)
            s = _sentiment_score(items)
            weight = 0.7 if "Geopolitik" in label else 1.0
            total += s * weight
            st.markdown(f"**{label}** — {impact_label(s)} (skor {s:+d})")
            if items:
                for it in items[:3]:
                    st.markdown(f"- [{it['title']}]({it['link']}) _{it['source']}_")
            st.markdown("---")
        bg = "#14532d" if total >= 2 else ("#7f1d1d" if total <= -2 else "#1e293b")
        st.markdown(f'<div style="background:{bg};padding:10px;border-radius:8px;"><b>DAMPAK IHSG:</b> skor {total:+.1f}</div>', unsafe_allow_html=True)

# =========================================================================
# MESIN SCREENING
# =========================================================================

def run_screen(criteria_fn, description, progress_note):
    tickers = get_all_idx_tickers()
    ai_speak(f"🔍 Memindai {len(tickers)} saham...", "🟡 Scanning")
    bar = st.progress(0, text=f"{progress_note}: mengunduh data {len(tickers)} emiten...")
    data = get_all_ohlcv(tuple(tickers), period="6mo")
    bar.progress(40, text=f"{progress_note}: menyaring...")
    cands = []
    total = len(tickers)
    for i, (t, df) in enumerate(iter_frames(data, tickers)):
        if (i + 1) % 100 == 0:
            bar.progress(min(40 + int((i + 1) / total * 30), 70), f"{progress_note} ({i+1}/{total})")
        try:
            r = criteria_fn(t, df)
            if r:
                cands.append(r)
        except: continue
    bar.progress(75, text="Mengambil fundamental...")
    cand_tickers = tuple(sorted({c["Ticker"] for c in cands}))[:60]
    fmap = get_fundamentals(cand_tickers) if cand_tickers else {}
    results = []
    for c in cands:
        f = fmap.get(c["Ticker"]) or {}
        merged = {**c, **f}
        if c.get("_needs_fundamentals") and not f:
            continue
        results.append(merged)
    bar.progress(100, text="Selesai.")
    time.sleep(0.3)
    bar.empty()
    st.session_state.scan_count += len(results)
    st.session_state.last_scan = datetime.now().strftime("%H:%M:%S")
    ai_speak(f"✅ {len(results)} saham ditemukan.", "🟢 Online")
    return pd.DataFrame(results)

# =========================================================================
# KRITERIA SCREENING
# =========================================================================

def crit_multibagger(t, df):
    close = float(df["Close"].iloc[-1])
    if close < 10:
        return None
    ma200 = df["MA200"].iloc[-1]
    if np.isnan(ma200):
        return None
    fund = get_fundamentals((t,)).get(t, {})
    roe = fund.get("returnOnEquity", 0) or 0
    rg = fund.get("revenueGrowth", 0) or 0
    pm = fund.get("profitMargins", 0) or 0
    pe = fund.get("trailingPE", 0) or 0
    score = 20
    if roe >= 0.10: score += 20
    elif roe >= 0.05: score += 10
    if rg >= 0.10: score += 20
    elif rg >= 0.05: score += 10
    if pm > 0: score += 15
    if 0 < pe < 15: score += 15
    elif 0 < pe < 25: score += 8
    if close > ma200: score += 10
    if score >= 35:
        return {"Ticker": t, "Harga": round(close, 2), "MA200": round(float(ma200), 2), "Skor": score, "_needs_fundamentals": False}
    return None

def crit_hidden_gem(t, df):
    close = float(df["Close"].iloc[-1])
    if close < 10:
        return None
    ma50 = df["MA50"].iloc[-1]
    if np.isnan(ma50):
        return None
    vol_avg = df["VOL_AVG20"].iloc[-1]
    if np.isnan(vol_avg) or vol_avg == 0:
        return None
    vr = df["Volume"].iloc[-1] / vol_avg
    rsi = df["RSI14"].iloc[-1]
    fund = get_fundamentals((t,)).get(t, {})
    pe = fund.get("trailingPE", 100) or 100
    rg = fund.get("revenueGrowth", 0) or 0
    conditions = []
    if close > ma50:
        conditions.append("Harga > MA50")
    if vr > 1.2:
        conditions.append("Volume Breakout")
    if pe and 0 < pe < 20:
        conditions.append(f"PER={pe:.1f}x")
    if rg > 0.05:
        conditions.append("Growth Positif")
    if len(conditions) >= 1:
        return {"Ticker": t, "Harga": round(close, 2), "VolRatio": round(float(vr), 2), "RSI": round(float(rsi), 1) if not np.isnan(rsi) else 50, "Info": " | ".join(conditions), "_needs_fundamentals": False}
    return None

def crit_swing(t, df):
    close = float(df["Close"].iloc[-1])
    if close < 10:
        return None
    ma20 = df["MA20"].iloc[-1]
    ma50 = df["MA50"].iloc[-1]
    if np.isnan(ma20) or np.isnan(ma50):
        return None
    rsi = df["RSI14"].iloc[-1]
    conditions = []
    if close > ma20:
        conditions.append("Harga > MA20")
    if ma20 > ma50:
        conditions.append("MA20 > MA50")
    if not np.isnan(rsi) and 40 <= rsi <= 70:
        conditions.append(f"RSI={rsi:.1f}")
    if len(conditions) >= 1:
        return {"Ticker": t, "Harga": round(close, 2), "RSI": round(float(rsi), 1) if not np.isnan(rsi) else 50, "Info": " | ".join(conditions), "_needs_fundamentals": False}
    return None

def score_multibagger(r):
    roe, rg, pm, de, pe = r.get("returnOnEquity",0) or 0, r.get("revenueGrowth",0) or 0, r.get("profitMargins",0) or 0, r.get("debtToEquity"), r.get("trailingPE")
    s = min(roe*100,30)/30*30 + min(max(rg,0)*100,30)/30*25 + min(max(pm,0)*100,20)/20*20 + (15 if de is not None and de < 100 else 8 if de is not None and de < 200 else 0) + (10 if pe and 0 < pe < 12 else 5 if pe and pe < 18 else 0)
    return round(s)

def score_swing(r):
    s, rsi = 0, r.get("RSI") or 50
    s += 25 if r.get("Harga", 0) > (r.get("MA20") or 0) else 0
    s += 20 if 50 <= rsi <= 65 else (12 if 45 <= rsi < 50 else 5)
    s += 20 if r.get("MACD_BULL") else 5
    s += 15 if (r.get("VolRatio") or 0) > 1.3 else 8
    s += 10 if (r.get("trailingPE") and 0 < r.get("trailingPE") < 15) else 4
    s += 10 if r.get("Harga", 0) > (r.get("MA50") or 0) else 0
    return round(s)

def show_results(df, score_col, note_cols, card_renderer, filter_col=None):
    if df.empty:
        st.info("😕 Tidak ada emiten yang lolos kriteria saat ini.")
        return
    df = df.copy()
    if "marketCap" in df.columns:
        df["Kategori"] = df["marketCap"].apply(classify_market_cap)
    else:
        df["Kategori"] = "N/A"
    df["Skor"] = df.apply(score_col, axis=1)
    df = df.sort_values("Skor", ascending=False).reset_index(drop=True)
    opts = ["Semua Kategori", "Big Cap", "Mid Cap", "Small Cap", "Micro Cap"]
    f = st.selectbox("Filter Kategori:", opts)
    if f != "Semua Kategori":
        df = df[df["Kategori"] == f]
    nama_col = "longName" if "longName" in df.columns else "Nama" if "Nama" in df.columns else "Ticker"
    cols = ["Ticker", nama_col, "Kategori", "Harga", "Skor"] + [c for c in note_cols if c in df.columns]
    cols = list(dict.fromkeys(cols))
    st.dataframe(df[cols], use_container_width=True)
    st.markdown("---")
    for _, row in df.iterrows():
        card_renderer(row)

# =========================================================================
# UI UTAMA
# =========================================================================

render_news_section()

st.sidebar.markdown("""
<h3 style="color:#38bdf8;font-family:'Orbitron',monospace;font-size:0.9rem;margin-bottom:10px;">
    ⚙️ AI CONTROL
</h3>
""", unsafe_allow_html=True)

menu_mode = st.sidebar.selectbox("Pilih Modul Screener:", [
    "💸 1. Multi-Bagger",
    "🃏 2. Hidden Gems",
    "🔪 3. Scalping & VSA",
    "🕵️ 4. Swing Trading",
    "📉 5. Cek Emiten Mandiri",
    "🚀 6. Scalping Invest",
    "💰 7. SAHAM UNDER 100 - KHUSUS",
])

# =========================================================================
# MODUL 1 — MULTI-BAGGER
# =========================================================================

if menu_mode.startswith("💸"):
    st.markdown("### 💸 Multi-Bagger")
    if st.sidebar.button("🚀 SCAN MULTI-BAGGER", type="primary", use_container_width=True):
        df = run_screen(crit_multibagger, "Multi-Bagger", "Modul 1")
        def card(r):
            pe = r.get("trailingPE")
            st.markdown(f"""<div class="deep-card">
                <h3>{r['Ticker']} — {r.get('longName','')} ({r.get('Kategori','')}) | Skor: <b style="color:#facc15;">{r['Skor']}/100</b></h3>
                <p><b>Harga:</b> Rp {r['Harga']:,.2f} | <b>MA200:</b> Rp {r.get('MA200',0):,.2f} | <b>Kapitalisasi:</b> {fmt_rp(r.get('marketCap'))}</p>
                <p><b>Fundamental:</b> ROE {(r.get('returnOnEquity') or 0)*100:.1f}% | Rev Growth {(r.get('revenueGrowth') or 0)*100:.1f}% | PER {f"{pe:.1f}x" if pe else "N/A"}</p>
            </div>""", unsafe_allow_html=True)
        show_results(df, score_multibagger, ["trailingPE", "RSI"], card)

# =========================================================================
# MODUL 2 — HIDDEN GEMS
# =========================================================================

elif menu_mode.startswith("🃏"):
    st.markdown("### 🃏 Hidden Gems")
    if st.sidebar.button("🚀 SCAN HIDDEN GEMS", type="primary", use_container_width=True):
        df = run_screen(crit_hidden_gem, "Hidden Gems", "Modul 2")
        def card(r):
            st.markdown(f"""<div class="deep-card">
                <h3>{r['Ticker']} — {r.get('longName','')} ({r.get('Kategori','')}) | Skor: <b style="color:#facc15;">{r['Skor']}/100</b></h3>
                <p><b>Harga:</b> Rp {r['Harga']:,.2f} | <b>Vol Ratio:</b> {r.get('VolRatio',0)}x | <b>RSI:</b> {r.get('RSI','N/A')}</p>
                <p><b>Fundamental:</b> PER {r.get('trailingPE',0):.1f}x | Rev Growth {(r.get('revenueGrowth') or 0)*100:.1f}%</p>
            </div>""", unsafe_allow_html=True)
        show_results(df, score_multibagger, ["VolRatio", "RSI", "trailingPE"], card)

# =========================================================================
# MODUL 3 — SCALPING & VSA (DIPERBAIKI - LEBIH LONGGAR)
# =========================================================================

elif menu_mode.startswith("🔪"):
    st.markdown("### 🔪 Auto-Screener Scalping & VSA Harian")
    st.markdown("""
    <div style="background:rgba(30,41,59,0.5);padding:12px 16px;border-radius:10px;border-left:3px solid #f59e0b;margin-bottom:12px;font-size:0.85rem;color:#94a3b8;">
        🔍 Filter: Volume > 500.000 · Vol Ratio > 1.2x · Candle Hijau · Skor >= 30
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("⚡ JALANKAN SCREENER SCALPING & VSA", type="primary"):
        tickers = get_all_idx_tickers()
        with st.spinner("🤖 Menganalisis pola scalping..."):
            data = get_all_ohlcv(tuple(tickers), period="1mo")
            rows = []
            for t, df in iter_frames(data, tickers):
                try:
                    close = float(df["Close"].iloc[-1])
                    
                    # HANYA batas atas (tidak terlalu mahal)
                    if close > 5000:
                        continue
                    
                    # ===== FILTER LIKUIDITAS (LEBIH LONGGAR) =====
                    vol = float(df["Volume"].iloc[-1])
                    if vol < 500000:
                        continue
                    
                    vol_avg = df["VOL_AVG20"].iloc[-1]
                    if np.isnan(vol_avg) or vol_avg == 0:
                        continue
                    vr = vol / vol_avg
                    
                    if vr < 1.2:
                        continue
                    
                    # ===== DATA CANDLE =====
                    open_ = float(df["Open"].iloc[-1])
                    high = float(df["High"].iloc[-1])
                    low = float(df["Low"].iloc[-1])
                    prev = float(df["Close"].iloc[-2])
                    chg = (close - prev) / prev * 100
                    
                    rng = (high - low) or 0.0001
                    body = abs(close - open_)
                    lower_shadow = min(open_, close) - low
                    close_position = (close - low) / rng
                    
                    # ===== INDIKATOR =====
                    rsi = df["RSI14"].iloc[-1]
                    ma20 = df["MA20"].iloc[-1]
                    macd = df["MACD"].iloc[-1]
                    macd_sig = df["MACD_SIG"].iloc[-1]
                    atr = df["ATR14"].iloc[-1]
                    
                    # ===== SKOR & POLA =====
                    notes = []
                    score = 10
                    
                    # 1. Marking Close
                    if close_position > 0.6:
                        notes.append("✅ Marking Close")
                        score += 15
                    
                    # 2. Volume Spike
                    if vr > 1.8:
                        notes.append("🔥 Volume Spike")
                        score += 12
                    elif vr > 1.3:
                        notes.append("📈 Volume Meningkat")
                        score += 6
                    
                    # 3. Candle Hijau (WAJIB)
                    if close > open_:
                        notes.append("🟢 Candle Hijau")
                        score += 10
                    else:
                        continue
                    
                    # 4. Pin Bar
                    if lower_shadow / rng > 0.3 and close > open_:
                        notes.append("🛡️ Pin Bar")
                        score += 10
                    
                    # 5. Harga > MA20
                    if not np.isnan(ma20) and close > ma20:
                        notes.append("📊 Harga > MA20")
                        score += 8
                    
                    # 6. RSI sehat
                    if not np.isnan(rsi) and 35 <= rsi <= 72:
                        notes.append(f"📈 RSI={rsi:.1f}")
                        score += 6
                    
                    # 7. MACD bullish
                    if not np.isnan(macd) and not np.isnan(macd_sig) and macd > macd_sig:
                        notes.append("📈 MACD Bullish")
                        score += 5
                    
                    # ===== MINIMAL SKOR 30 =====
                    if score < 30:
                        continue
                    
                    entry = round(close, 2)
                    atr_v = float(atr) if not np.isnan(atr) else close * 0.02
                    
                    rows.append({
                        "Ticker": t,
                        "Harga": entry,
                        "Change (%)": round(chg, 2),
                        "VolRatio": round(vr, 2),
                        "RSI": round(rsi, 1) if not np.isnan(rsi) else 50,
                        "Skor": min(score, 99),
                        "TP": round(entry + 1.5 * atr_v, 2),
                        "CL": round(entry - 1.0 * atr_v, 2),
                        "Analisis": " | ".join(notes) if notes else "Netral"
                    })
                except Exception:
                    continue
            
            df = pd.DataFrame(rows)
            
            if not df.empty:
                st.success(f"✅ {len(df)} saham ditemukan!")
                st.dataframe(df.sort_values("Skor", ascending=False)[
                    ["Ticker", "Harga", "Change (%)", "VolRatio", "RSI", "Skor", "TP", "CL"]],
                    use_container_width=True)
                
                for _, r in df.sort_values("Skor", ascending=False).head(20).iterrows():
                    st.markdown(f"""<div class="deep-card">
                        <h3>{r['Ticker']} | Skor: <b style="color:#facc15;">{r['Skor']}/99</b></h3>
                        <p><b>Harga:</b> Rp {r['Harga']:,.2f} ({r['Change (%)']:+.2f}%) | 
                           <b>Vol Ratio:</b> {r['VolRatio']}x | <b>RSI:</b> {r['RSI']}</p>
                        <p><b>🎯 TP:</b> Rp {r['TP']:,.2f} | 
                           <b>🛑 CL:</b> Rp {r['CL']:,.2f}</p>
                        <p><b>📌 Analisis:</b> {r['Analisis']}</p>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("😕 Tidak ada emiten yang lolos kriteria scalping hari ini.")

# =========================================================================
# MODUL 4 — SWING TRADING
# =========================================================================

elif menu_mode.startswith("🕵️"):
    st.markdown("### 🕵️ Swing Trading 1-3 Minggu")
    if st.sidebar.button("🚀 SCAN SWING", type="primary", use_container_width=True):
        df = run_screen(crit_swing, "Swing", "Modul 4")
        if not df.empty:
            data = get_all_ohlcv(tuple(sorted(df["Ticker"].tolist())), period="6mo")
            extras = {}
            for t, d in iter_frames(data, list(df["Ticker"])):
                extras[t] = {"MA20": float(d["MA20"].iloc[-1]), "MA50": float(d["MA50"].iloc[-1]), "MACD_BULL": bool(d["MACD"].iloc[-1] > d["MACD_SIG"].iloc[-1]), "ATR": float(d["ATR14"].iloc[-1]) if not np.isnan(d["ATR14"].iloc[-1]) else None}
            for k, v in extras.items():
                for col, val in v.items():
                    df.loc[df["Ticker"] == k, col] = val
        def card(r):
            atr = r.get("ATR") or r["Harga"] * 0.02
            st.markdown(f"""<div class="deep-card"><h3>{r['Ticker']} — {r.get('longName','')} ({r.get('Kategori','')}) | Skor: <b style="color:#facc15;">{r['Skor']}/100</b></h3><p><b>Harga:</b> Rp {r['Harga']:,.2f} | <b>RSI:</b> {r.get('RSI','N/A')} | <b>ATR:</b> Rp {atr:,.2f}</p><p><b>Entry:</b> Rp {r['Harga']:,.2f} | <b>TP:</b> Rp {r['Harga']+2*atr:,.2f} | <b>CL:</b> Rp {r['Harga']-1.5*atr:,.2f}</p></div>""", unsafe_allow_html=True)
        show_results(df, score_swing, ["RSI", "trailingPE"], card)

# =========================================================================
# MODUL 5 — CEK EMITEN MANDIRI
# =========================================================================

elif menu_mode.startswith("📉"):
    st.markdown("### 📉 Cek Emiten Mandiri")
    custom = st.text_input("Masukkan kode (contoh: BBRI, BBCA):", "BBRI")
    if custom:
        tk = custom.strip().upper()
        tk = tk if tk.endswith(".JK") else tk + ".JK"
        try:
            obj = yf.Ticker(tk)
            hist = obj.history(period="6mo", auto_adjust=True)
            if not hist.empty:
                hist = add_indicators(hist)
                st.success(f"{tk} | Rp {hist['Close'].iloc[-1]:,.2f}")
                st.line_chart(pd.DataFrame({"Close": hist["Close"], "MA20": hist["MA20"], "MA50": hist["MA50"]}))
                st.bar_chart(hist["Volume"])
                info = obj.info
                c1, c2, c3, c4 = st.columns(4)
                c1.metric("Kapitalisasi", fmt_rp(info.get("marketCap")))
                c2.metric("PER", f"{info.get('trailingPE'):.1f}x" if info.get("trailingPE") else "N/A")
                c3.metric("PBV", f"{info.get('priceToBook'):.2f}x" if info.get("priceToBook") else "N/A")
                c4.metric("ROE", f"{(info.get('returnOnEquity') or 0)*100:.1f}%" if info.get("returnOnEquity") else "N/A")
        except Exception as e:
            st.error(f"Error: {e}")

# =========================================================================
# MODUL 6 — SCALPING INVEST
# =========================================================================

elif menu_mode.startswith("🚀"):
    st.markdown("### 🚀 Scalping Invest (Rp 25-500)")
    st.markdown("""
    <div style="background:#451a03;border-left:5px solid #f59e0b;padding:12px;border-radius:6px;margin-bottom:12px;color:#94a3b8;">
        ⚠️ Risiko ekstrem. Saham lapis bawah sangat volatil.
    </div>
    """, unsafe_allow_html=True)
    if st.sidebar.button("🚀 SCAN SCALPING INVEST", type="primary", use_container_width=True):
        tickers = get_all_idx_tickers()
        with st.spinner("🤖 Memindai saham Rp 25-500..."):
            data = get_all_ohlcv(tuple(tickers), period="1mo")
            bpjs, bsjp, akum = [], [], []
            for t, df in iter_frames(data, tickers):
                try:
                    close, open_, high, low = float(df["Close"].iloc[-1]), float(df["Open"].iloc[-1]), float(df["High"].iloc[-1]), float(df["Low"].iloc[-1])
                    if not (25 <= close <= 500):
                        continue
                    prev, chg = float(df["Close"].iloc[-2]), (close - float(df["Close"].iloc[-2])) / float(df["Close"].iloc[-2]) * 100
                    vol, avg = float(df["Volume"].iloc[-1]), float(df["VOL_AVG20"].iloc[-1]) if not np.isnan(df["VOL_AVG20"].iloc[-1]) else 0
                    if vol <= 0 or avg <= 0:
                        continue
                    vr, rng = vol / avg, (high - low) or 0.0001
                    atr_v = float(df["ATR14"].iloc[-1]) if not np.isnan(df["ATR14"].iloc[-1]) else close * 0.03
                    base = {"Ticker": t, "Harga": round(close, 2), "Change (%)": round(chg, 2), "VolRatio": round(vr, 2)}
                    if chg > 1 and (close - low) / rng >= 0.7 and vr > 1.5:
                        bpjs.append({**base, "TP": round(close + 1.5 * atr_v, 2), "CL": round(close - 1.0 * atr_v, 2), "Alasan": "Momentum + closing kuat"})
                    lower = min(open_, close) - low
                    if lower / rng >= 0.4 and close > open_:
                        bsjp.append({**base, "TP": round(close + 2.0 * atr_v, 2), "CL": round(low, 2), "Alasan": "Pin bar rejection"})
                    chg5 = (close / float(df["Close"].iloc[-6]) - 1) * 100 if len(df) > 6 else 0
                    vol5 = float(df["Volume"].tail(5).mean()) / avg if avg else 0
                    if abs(chg5) < 5 and vol5 > 1.3:
                        vwap = df["VWAP10"].iloc[-1]
                        akum.append({**base, "VWAP10": round(float(vwap), 2) if not np.isnan(vwap) else None, "Akumulasi": "Volume naik, harga konsolidasi", "TP": round(close + 2.5 * atr_v, 2), "CL": round(close - 1.2 * atr_v, 2)})
                except: continue
        tab1, tab2, tab3 = st.tabs(["🌅 BPJS", "🌆 BSJP", "🕵️ Akumulasi"])
        for tab, rows_, label in [(tab1, bpjs, "BPJS"), (tab2, bsjp, "BSJP"), (tab3, akum, "Akumulasi")]:
            with tab:
                if rows_:
                    st.dataframe(pd.DataFrame(rows_), use_container_width=True)
                else:
                    st.info(f"Tidak ada sinyal {label} saat ini.")

# =========================================================================
# MODUL 7 — SAHAM UNDER 100 (SCALPING KHUSUS)
# =========================================================================

elif menu_mode.startswith("💰"):
    st.markdown("### 💰 SAHAM UNDER 100 - SCALPING KHUSUS")
    st.markdown("""
    <div style="background:rgba(30,41,59,0.5);padding:12px 16px;border-radius:10px;border-left:3px solid #f59e0b;margin-bottom:12px;font-size:0.85rem;color:#94a3b8;">
        🎯 KHUSUS SAHAM < Rp 100<br>
        🔍 Candle Hijau · Volume > 100.000 · Vol Ratio > 1.2x<br>
        ⚠️ Risiko tinggi! Saham sangat volatil.
    </div>
    """, unsafe_allow_html=True)
    
    if st.sidebar.button("💰 SCAN SAHAM UNDER 100", type="primary", use_container_width=True):
        tickers = get_all_idx_tickers()
        with st.spinner("🤖 Memindai saham under 100..."):
            data = get_all_ohlcv(tuple(tickers), period="1mo")
            rows = []
            
            for t, df in iter_frames(data, tickers):
                try:
                    close = float(df["Close"].iloc[-1])
                    
                    # ===== KHUSUS UNDER 100 =====
                    if close >= 100:
                        continue
                    
                    # ===== FILTER LIKUIDITAS =====
                    vol = float(df["Volume"].iloc[-1])
                    if vol < 100000:
                        continue
                    
                    vol_avg = df["VOL_AVG20"].iloc[-1]
                    if np.isnan(vol_avg) or vol_avg == 0:
                        continue
                    vr = vol / vol_avg
                    
                    if vr < 1.2:
                        continue
                    
                    # ===== DATA CANDLE =====
                    open_ = float(df["Open"].iloc[-1])
                    high = float(df["High"].iloc[-1])
                    low = float(df["Low"].iloc[-1])
                    prev = float(df["Close"].iloc[-2])
                    chg = (close - prev) / prev * 100
                    
                    rng = (high - low) or 0.0001
                    close_position = (close - low) / rng
                    atr = df["ATR14"].iloc[-1]
                    
                    # ===== SKOR =====
                    score = 10
                    notes = []
                    
                    # Candle Hijau (WAJIB)
                    if close > open_:
                        score += 20
                        notes.append("🟢 Candle Hijau")
                    else:
                        continue
                    
                    if close_position > 0.65:
                        score += 15
                        notes.append("✅ Marking Close")
                    
                    if vr > 1.8:
                        score += 12
                        notes.append("🔥 Volume Spike")
                    elif vr > 1.3:
                        score += 6
                        notes.append("📈 Volume Meningkat")
                    
                    rsi = df["RSI14"].iloc[-1]
                    if not np.isnan(rsi) and 30 <= rsi <= 75:
                        score += 6
                        notes.append(f"📈 RSI={rsi:.1f}")
                    
                    macd = df["MACD"].iloc[-1]
                    macd_sig = df["MACD_SIG"].iloc[-1]
                    if not np.isnan(macd) and not np.isnan(macd_sig) and macd > macd_sig:
                        score += 5
                        notes.append("📈 MACD Bullish")
                    
                    if score < 30:
                        continue
                    
                    entry = round(close, 2)
                    atr_v = float(atr) if not np.isnan(atr) else close * 0.03
                    
                    rows.append({
                        "Ticker": t,
                        "Harga": entry,
                        "Change (%)": round(chg, 2),
                        "Volume": f"{vol/1000000:.2f}M",
                        "VolRatio": round(vr, 2),
                        "RSI": round(rsi, 1) if not np.isnan(rsi) else 50,
                        "Skor": min(score, 99),
                        "TP": round(entry + 1.5 * atr_v, 2),
                        "CL": round(entry - 1.0 * atr_v, 2),
                        "Analisis": " | ".join(notes) if notes else "Netral"
                    })
                except Exception:
                    continue
            
            df = pd.DataFrame(rows)
            
            if not df.empty:
                st.success(f"✅ {len(df)} saham under 100 ditemukan!")
                st.dataframe(df.sort_values("Skor", ascending=False)[
                    ["Ticker", "Harga", "Change (%)", "Volume", "VolRatio", "RSI", "Skor", "TP", "CL"]],
                    use_container_width=True)
                
                st.warning("⚠️ **PERINGATAN:** Saham under 100 sangat volatil. Gunakan stop loss ketat (3-5%).")
                
                for _, r in df.sort_values("Skor", ascending=False).head(20).iterrows():
                    st.markdown(f"""<div class="deep-card">
                        <h3>{r['Ticker']} | Skor: <b style="color:#facc15;">{r['Skor']}/99</b></h3>
                        <p><b>Harga:</b> Rp {r['Harga']:,.2f} ({r['Change (%)']:+.2f}%) | 
                           <b>Volume:</b> {r['Volume']} | <b>Vol Ratio:</b> {r['VolRatio']}x | 
                           <b>RSI:</b> {r['RSI']}</p>
                        <p><b>🎯 TP:</b> Rp {r['TP']:,.2f} | 
                           <b>🛑 CL:</b> Rp {r['CL']:,.2f}</p>
                        <p><b>📌 Analisis:</b> {r['Analisis']}</p>
                    </div>""", unsafe_allow_html=True)
            else:
                st.info("😕 Tidak ada saham under 100 yang lolos kriteria hari ini.")

# =========================================================================
# FOOTER
# =========================================================================

st.sidebar.markdown("---")
st.sidebar.caption("""
🤖 AI Screener v4.0  
**Sumber:** Yahoo Finance, World Bank, Google News  
**Disclaimer:** Bukan rekomendasi investasi
""")

st.markdown("""
<div class="disclaimer">
    ⚠️ <b>Disclaimer:</b> Screener ini hanya alat bantu analisis. 
    Semua keputusan investasi sepenuhnya di tangan Anda.
</div>
""", unsafe_allow_html=True)