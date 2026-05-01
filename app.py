import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import datetime

# ── Page config ───────────────────────────────────────────────────
st.set_page_config(
    page_title="Metals AI Assistant",
    page_icon="🤖",
    layout="centered"
)

# ── CSS ───────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap');

html, body, .stApp { background: #0a0e1a !important; }

/* Robot container */
.robot-wrap {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin: 10px 0 20px 0;
}

/* Robot head */
.robot-head {
    width: 90px; height: 80px;
    background: linear-gradient(135deg, #1e3a5f, #0d2137);
    border-radius: 18px;
    border: 2px solid #00d4ff;
    position: relative;
    animation: float 3s ease-in-out infinite;
    box-shadow: 0 0 20px #00d4ff44;
}
@keyframes float {
    0%,100% { transform: translateY(0px); }
    50%      { transform: translateY(-8px); }
}

/* Eyes */
.robot-eye {
    width: 18px; height: 18px;
    background: #00d4ff;
    border-radius: 50%;
    position: absolute;
    top: 22px;
    animation: blink 4s ease-in-out infinite;
    box-shadow: 0 0 8px #00d4ff;
}
.robot-eye.left  { left: 18px; }
.robot-eye.right { right: 18px; }
@keyframes blink {
    0%,90%,100% { transform: scaleY(1); }
    95%          { transform: scaleY(0.1); }
}

/* Mouth */
.robot-mouth {
    width: 40px; height: 12px;
    border: 2px solid #00d4ff;
    border-radius: 0 0 20px 20px;
    border-top: none;
    position: absolute;
    bottom: 16px; left: 50%;
    transform: translateX(-50%);
    animation: smile 3s ease-in-out infinite;
}
@keyframes smile {
    0%,100% { width: 40px; }
    50%      { width: 50px; }
}

/* Antenna */
.robot-antenna {
    width: 4px; height: 20px;
    background: #00d4ff;
    margin: 0 auto;
    position: relative;
}
.robot-antenna::after {
    content: '';
    width: 10px; height: 10px;
    background: #00d4ff;
    border-radius: 50%;
    position: absolute;
    top: -10px; left: -3px;
    animation: pulse-dot 1.5s ease-in-out infinite;
    box-shadow: 0 0 10px #00d4ff;
}
@keyframes pulse-dot {
    0%,100% { transform: scale(1); opacity:1; }
    50%      { transform: scale(1.4); opacity:0.6; }
}

/* Body */
.robot-body {
    width: 70px; height: 55px;
    background: linear-gradient(135deg, #1e3a5f, #0d2137);
    border-radius: 12px;
    border: 2px solid #00d4ff44;
    margin-top: 4px;
    display: flex;
    align-items: center;
    justify-content: center;
    animation: float 3s ease-in-out infinite 0.5s;
}
.robot-chest {
    width: 30px; height: 20px;
    background: #00d4ff22;
    border: 1px solid #00d4ff;
    border-radius: 6px;
    animation: glow 2s ease-in-out infinite;
}
@keyframes glow {
    0%,100% { box-shadow: 0 0 5px #00d4ff; }
    50%      { box-shadow: 0 0 15px #00d4ff, 0 0 25px #00d4ff44; }
}

/* Robot name */
.robot-name {
    font-family: 'Orbitron', monospace;
    color: #00d4ff;
    font-size: 14px;
    font-weight: 700;
    margin-top: 8px;
    letter-spacing: 2px;
    text-shadow: 0 0 10px #00d4ff;
}
.robot-status {
    font-family: 'Rajdhani', sans-serif;
    color: #22c55e;
    font-size: 12px;
    margin-top: 3px;
}

/* Chat bubbles */
.bot-bubble {
    background: linear-gradient(135deg, #0d2137, #1e3a5f);
    border: 1px solid #00d4ff44;
    border-radius: 16px 16px 16px 4px;
    padding: 16px 20px;
    color: #e2f4ff !important;
    font-family: 'Rajdhani', sans-serif;
    font-size: 16px;
    line-height: 1.7;
    margin: 8px 0;
    box-shadow: 0 0 15px #00d4ff11;
}
.user-bubble {
    background: linear-gradient(135deg, #1a3a1a, #0d2137);
    border: 1px solid #22c55e44;
    border-radius: 16px 16px 4px 16px;
    padding: 12px 18px;
    color: #d1fae5 !important;
    font-family: 'Rajdhani', sans-serif;
    font-size: 15px;
    text-align: right;
    margin: 8px 0;
}

/* Price card */
.price-card {
    background: linear-gradient(135deg, #0d2137, #1e3a5f);
    border: 1px solid #00d4ff;
    border-radius: 16px;
    padding: 20px;
    text-align: center;
    margin: 12px 0;
    box-shadow: 0 0 20px #00d4ff22;
}
.price-val   { font-size:38px; font-weight:800; color:#00d4ff; font-family:'Orbitron',monospace; }
.price-label { font-size:13px; color:#8ab; margin-top:4px; font-family:'Rajdhani',sans-serif; }

/* Section headers */
.section-head {
    font-family: 'Orbitron', monospace;
    color: #00d4ff;
    font-size: 13px;
    letter-spacing: 2px;
    border-bottom: 1px solid #00d4ff33;
    padding-bottom: 6px;
    margin: 16px 0 10px 0;
}

/* News items */
.news-item {
    background: #0d213788;
    border-left: 3px solid #00d4ff;
    border-radius: 0 8px 8px 0;
    padding: 10px 14px;
    color: #cde !important;
    font-family: 'Rajdhani', sans-serif;
    font-size: 14px;
    margin: 6px 0;
    line-height: 1.5;
}

/* Title bar */
.title-bar {
    font-family: 'Orbitron', monospace;
    color: #00d4ff;
    font-size: 20px;
    font-weight: 700;
    text-align: center;
    letter-spacing: 3px;
    text-shadow: 0 0 20px #00d4ff;
    margin-bottom: 4px;
}
.title-sub {
    font-family: 'Rajdhani', sans-serif;
    color: #8ab;
    text-align: center;
    font-size: 13px;
    margin-bottom: 16px;
    letter-spacing: 1px;
}

/* Streamlit overrides */
div[data-testid="stChatMessage"] { display:none !important; }
.stButton button {
    background: linear-gradient(135deg, #0d2137, #1e3a5f) !important;
    color: #00d4ff !important;
    border: 1px solid #00d4ff !important;
    border-radius: 10px !important;
    font-family: 'Rajdhani', sans-serif !important;
    font-weight: 600 !important;
    letter-spacing: 1px !important;
    transition: all 0.2s !important;
}
.stButton button:hover {
    box-shadow: 0 0 15px #00d4ff55 !important;
    transform: translateY(-1px) !important;
}
</style>
""", unsafe_allow_html=True)

# ── Metal config ──────────────────────────────────────────────────
METALS = {
    "🥇 Gold":      {"ticker": "GC=F",  "unit": "USD / troy oz",   "color": "#f5c842"},
    "🥈 Silver":    {"ticker": "SI=F",  "unit": "USD / troy oz",   "color": "#c0c0c0"},
    "🔶 Copper":    {"ticker": "HG=F",  "unit": "USD / lb",        "color": "#b87333"},
    "⚙️ Aluminium": {"ticker": "ALI=F", "unit": "USD / contract",  "color": "#a8c4d4"},
}

# ── Session state ─────────────────────────────────────────────────
for k, v in {"step":"greet","selected":None,"greeted":False,"msgs":[],"show_ta":False}.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ── Helpers ───────────────────────────────────────────────────────
def add_msg(role, text):
    st.session_state.msgs.append({"role": role, "text": text})

def robot_html(talking=False):
    mouth_style = "border-radius: 0 0 20px 20px; border-top:none;" if not talking else "border-radius:20px;"
    return f"""
<div class="robot-wrap">
  <div class="robot-antenna"></div>
  <div class="robot-head">
    <div class="robot-eye left"></div>
    <div class="robot-eye right"></div>
    <div class="robot-mouth" style="{mouth_style}"></div>
  </div>
  <div class="robot-body"><div class="robot-chest"></div></div>
  <div class="robot-name">METAL·BOT</div>
  <div class="robot-status">● ONLINE — AI POWERED</div>
</div>"""

def fetch_data(ticker_symbol):
    try:
        t    = yf.Ticker(ticker_symbol)
        hist = t.history(period="3mo", interval="1d")
        if hist.empty:
            return None, [], None
        price  = round(hist["Close"].iloc[-1], 2)
        prev   = round(hist["Close"].iloc[-2], 2) if len(hist) > 1 else price
        change = round(price - prev, 2)
        pct    = round((change / prev) * 100, 2) if prev else 0
        # News
        news_titles = []
        try:
            for item in (t.news or [])[:5]:
                title = None
                content = item.get("content", {})
                if isinstance(content, dict):
                    title = content.get("title") or content.get("headline")
                if not title:
                    title = item.get("title") or item.get("headline")
                if title:
                    news_titles.append(title)
        except Exception:
            pass
        return {"price": price, "change": change, "pct": pct}, news_titles, hist
    except Exception:
        return None, [], None

def build_chart(hist, metal_name, show_ta=False):
    # Calculate indicators
    hist = hist.copy()
    hist["MA20"] = hist["Close"].rolling(20).mean()
    hist["MA50"] = hist["Close"].rolling(50).mean()
    # Bollinger Bands
    hist["BB_mid"] = hist["Close"].rolling(20).mean()
    std = hist["Close"].rolling(20).std()
    hist["BB_up"]  = hist["BB_mid"] + 2 * std
    hist["BB_dn"]  = hist["BB_mid"] - 2 * std
    # RSI
    delta = hist["Close"].diff()
    gain  = delta.clip(lower=0).rolling(14).mean()
    loss  = (-delta.clip(upper=0)).rolling(14).mean()
    rs    = gain / loss
    hist["RSI"] = 100 - (100 / (1 + rs))

    if show_ta:
        fig = make_subplots(
            rows=3, cols=1,
            shared_xaxes=True,
            row_heights=[0.55, 0.25, 0.20],
            vertical_spacing=0.04,
            subplot_titles=["Price + Bollinger Bands", "Volume", "RSI (14)"]
        )
    else:
        fig = make_subplots(rows=2, cols=1, shared_xaxes=True,
                            row_heights=[0.7, 0.3], vertical_spacing=0.04,
                            subplot_titles=["Price Chart", "Volume"])

    # Candlestick
    fig.add_trace(go.Candlestick(
        x=hist.index, open=hist["Open"], high=hist["High"],
        low=hist["Low"], close=hist["Close"],
        increasing_line_color="#22c55e", decreasing_line_color="#ef4444",
        name="Price"
    ), row=1, col=1)

    # MA lines
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA20"],
        line=dict(color="#f5c842", width=1.5), name="MA20"), row=1, col=1)
    fig.add_trace(go.Scatter(x=hist.index, y=hist["MA50"],
        line=dict(color="#a78bfa", width=1.5), name="MA50"), row=1, col=1)

    if show_ta:
        # Bollinger Bands
        fig.add_trace(go.Scatter(x=hist.index, y=hist["BB_up"],
            line=dict(color="#00d4ff", width=1, dash="dash"), name="BB Upper"), row=1, col=1)
        fig.add_trace(go.Scatter(x=hist.index, y=hist["BB_dn"],
            line=dict(color="#00d4ff", width=1, dash="dash"),
            fill="tonexty", fillcolor="rgba(0,212,255,0.05)", name="BB Lower"), row=1, col=1)

    # Volume
    colors = ["#22c55e" if c >= o else "#ef4444"
              for c, o in zip(hist["Close"], hist["Open"])]
    fig.add_trace(go.Bar(x=hist.index, y=hist["Volume"],
        marker_color=colors, name="Volume", showlegend=False), row=2, col=1)

    if show_ta:
        # RSI
        fig.add_trace(go.Scatter(x=hist.index, y=hist["RSI"],
            line=dict(color="#f97316", width=1.5), name="RSI"), row=3, col=1)
        fig.add_hline(y=70, line=dict(color="#ef4444", dash="dash", width=1), row=3, col=1)
        fig.add_hline(y=30, line=dict(color="#22c55e", dash="dash", width=1), row=3, col=1)

    fig.update_layout(
        plot_bgcolor="#0a0e1a", paper_bgcolor="#0a0e1a",
        font=dict(color="#8ab", family="Rajdhani"),
        xaxis_rangeslider_visible=False,
        height=550 if show_ta else 380,
        margin=dict(l=10, r=10, t=30, b=10),
        legend=dict(bgcolor="#0d2137",
                    font=dict(color="#cde", size=11)),
        title=dict(text=f"{metal_name} — Technical Analysis" if show_ta else f"{metal_name} — 90 Day Chart",
                   font=dict(color="#00d4ff", size=13))
    )
    for axis in ["xaxis","yaxis","xaxis2","yaxis2","xaxis3","yaxis3"]:
        fig.update_layout({axis: dict(gridcolor="#1e3a5f", zerolinecolor="#1e3a5f")})
    return fig

def get_ai_analysis(metal_name, price_data, hist_df):
    """Rule-based analysis using real market data — no API key needed"""
    try:
        price  = price_data["price"]
        change = price_data["change"]
        pct    = price_data["pct"]

        # ── Calculate indicators ──────────────────────────────────
        closes  = hist_df["Close"]
        ma20    = round(closes.rolling(20).mean().iloc[-1], 2)
        ma50    = round(closes.rolling(50).mean().iloc[-1], 2)
        high90  = round(hist_df["High"].max(), 2)
        low90   = round(hist_df["Low"].min(), 2)
        range90 = high90 - low90

        # RSI
        delta   = closes.diff()
        gain    = delta.clip(lower=0).rolling(14).mean()
        loss    = (-delta.clip(upper=0)).rolling(14).mean()
        rsi     = round((100 - (100 / (1 + gain/loss))).iloc[-1], 1)

        # Bollinger Bands
        bb_mid  = closes.rolling(20).mean().iloc[-1]
        bb_std  = closes.rolling(20).std().iloc[-1]
        bb_up   = round(bb_mid + 2*bb_std, 2)
        bb_low  = round(bb_mid - 2*bb_std, 2)

        # Position in 90d range (0=at low, 100=at high)
        pos_pct = round(((price - low90) / range90) * 100, 1) if range90 > 0 else 50

        # ── Trend analysis ────────────────────────────────────────
        if price > ma20 > ma50:
            trend_signal = "🟢 BULLISH"
            trend_text   = (f"{metal_name} is trading above both MA20 (${ma20:,}) and MA50 (${ma50:,}), "
                           f"confirming a bullish structure with higher highs forming.")
        elif price < ma20 < ma50:
            trend_signal = "🔴 BEARISH"
            trend_text   = (f"{metal_name} is trading below both MA20 (${ma20:,}) and MA50 (${ma50:,}), "
                           f"indicating a bearish trend with selling pressure dominating.")
        elif price > ma20 and price < ma50:
            trend_signal = "🟡 RECOVERING"
            trend_text   = (f"{metal_name} has reclaimed MA20 (${ma20:,}) but faces resistance at "
                           f"MA50 (${ma50:,}). A recovery attempt is underway — watch for confirmation.")
        else:
            trend_signal = "🟡 SIDEWAYS"
            trend_text   = (f"{metal_name} is consolidating near MA20 (${ma20:,}). "
                           f"The market is in a neutral phase — a breakout in either direction is possible.")

        # ── RSI signal ────────────────────────────────────────────
        if rsi > 70:
            rsi_text = f"RSI at {rsi} signals the market is **overbought** — momentum may slow or reverse soon. Watch for bearish divergence."
        elif rsi < 30:
            rsi_text = f"RSI at {rsi} signals the market is **oversold** — a potential bounce or reversal zone. Watch for buying interest."
        elif rsi > 55:
            rsi_text = f"RSI at {rsi} is in **bullish territory** — buyers are in control with moderate momentum."
        elif rsi < 45:
            rsi_text = f"RSI at {rsi} is in **bearish territory** — sellers have the upper hand with sustained pressure."
        else:
            rsi_text = f"RSI at {rsi} is in the **neutral zone (45–55)** — no clear momentum signal. Wait for RSI to break above 55 or below 45."

        # ── Key levels ────────────────────────────────────────────
        support    = round(low90 + range90 * 0.236, 2)   # Fibonacci 23.6%
        resistance = round(low90 + range90 * 0.618, 2)   # Fibonacci 61.8%
        levels_text = (f"Key **support** at ${support:,} (23.6% Fibonacci retracement). "
                      f"Key **resistance** at ${resistance:,} (61.8% Fibonacci level). "
                      f"Bollinger Bands range: ${bb_low:,} → ${bb_up:,}.")

        # ── Outlook ───────────────────────────────────────────────
        if pct > 1.5:
            outlook = (f"Strong positive momentum today (+{pct}%). "
                      f"Price at {pos_pct}% of its 90-day range. "
                      f"If bulls maintain above ${ma20:,}, further upside toward ${resistance:,} is likely.")
        elif pct < -1.5:
            outlook = (f"Significant selling pressure today ({pct}%). "
                      f"Price at {pos_pct}% of its 90-day range. "
                      f"A close below ${support:,} would confirm continued downside risk.")
        elif pos_pct > 75:
            outlook = (f"Price is trading near 90-day highs ({pos_pct}% of range). "
                      f"Strong long-term trend in place. Watch for consolidation before next leg up.")
        elif pos_pct < 25:
            outlook = (f"Price is near 90-day lows ({pos_pct}% of range). "
                      f"A value zone for long-term buyers. Watch RSI for oversold bounce signals.")
        else:
            outlook = (f"Price is mid-range ({pos_pct}% of 90-day range). "
                      f"Directional clarity will come from a break above ${resistance:,} or below ${support:,}.")

        return (f"**📊 Trend: {trend_signal}**<br>{trend_text}<br><br>"
                f"**📉 RSI Signal:**<br>{rsi_text}<br><br>"
                f"**🎯 Key Levels:**<br>{levels_text}<br><br>"
                f"**🔮 Short-term Outlook:**<br>{outlook}")

    except Exception as e:
        return f"⚠️ Analysis error: {str(e)}"

# ── Title ─────────────────────────────────────────────────────────
st.markdown('<div class="title-bar">⚡ METALS MARKET AI ⚡</div>', unsafe_allow_html=True)
st.markdown('<div class="title-sub">LIVE PRICES · AI ANALYSIS · TECHNICAL CHARTS</div>', unsafe_allow_html=True)

# ── Robot ─────────────────────────────────────────────────────────
st.markdown(robot_html(), unsafe_allow_html=True)

# ── Render chat history ───────────────────────────────────────────
for m in st.session_state.msgs:
    if m["role"] == "bot":
        st.markdown(f'<div class="bot-bubble">🤖 {m["text"]}</div>', unsafe_allow_html=True)
    else:
        st.markdown(f'<div class="user-bubble">{m["text"]} 👤</div>', unsafe_allow_html=True)

# ════════════════════════════════════════════════════════════════════
# STEP 1 — GREET
# ════════════════════════════════════════════════════════════════════
if st.session_state.step == "greet":
    if not st.session_state.greeted:
        h = datetime.datetime.now().hour
        g = "Good morning" if h < 12 else "Good afternoon" if h < 17 else "Good evening"
        add_msg("bot", f"{g}! I'm <b>Metal·Bot</b> — your AI-powered commodity market assistant.<br><br>"
                       "I provide <b>live prices, real-time news, technical charts, Bollinger Bands, RSI analysis</b> "
                       "and <b>AI-generated market insights</b>.<br><br>Which metal would you like to analyse today?")
        st.session_state.greeted = True
        st.rerun()

    st.markdown('<div class="bot-bubble">🤖 Choose a metal to get started:</div>', unsafe_allow_html=True)
    cols = st.columns(4)
    for i, metal in enumerate(METALS.keys()):
        if cols[i].button(metal, use_container_width=True, key=f"metal_{i}"):
            add_msg("user", f"Analyse {metal}")
            st.session_state.selected = metal
            st.session_state.step = "analyze"
            st.rerun()

# ════════════════════════════════════════════════════════════════════
# STEP 2 — ANALYZE
# ════════════════════════════════════════════════════════════════════
elif st.session_state.step == "analyze":
    metal = st.session_state.selected
    cfg   = METALS[metal]

    with st.spinner(f"⚡ Fetching live data for {metal}..."):
        price_data, news, hist = fetch_data(cfg["ticker"])

    if price_data is None:
        st.markdown('<div class="bot-bubble">⚠️ Could not fetch data — markets may be closed. Try another metal.</div>',
                    unsafe_allow_html=True)
    else:
        # Price card
        arrow = "▲" if price_data["change"] >= 0 else "▼"
        clr   = "#22c55e" if price_data["change"] >= 0 else "#ef4444"
        st.markdown(f"""
<div class="price-card">
  <div style="font-family:'Orbitron',monospace;color:#8ab;font-size:12px;letter-spacing:2px;margin-bottom:8px">
    {metal} — LIVE PRICE</div>
  <div class="price-val">${price_data['price']:,.2f}</div>
  <div class="price-label">{cfg['unit']}</div>
  <div style="font-size:16px;color:{clr};margin-top:8px;font-weight:700;font-family:'Rajdhani',sans-serif">
    {arrow} ${abs(price_data['change'])} &nbsp;({abs(price_data['pct'])}%) TODAY</div>
</div>""", unsafe_allow_html=True)

        # Chart
        st.markdown('<div class="section-head">📈 90-DAY PRICE CHART</div>', unsafe_allow_html=True)
        st.plotly_chart(build_chart(hist, metal, show_ta=False), use_container_width=True)

        # Technical Analysis toggle
        st.markdown('<div class="section-head">🔬 ADVANCED CHART ANALYSIS</div>', unsafe_allow_html=True)
        col1, col2 = st.columns([1,1])
        if col1.button("📊 Show Full Technical Analysis (RSI + Bollinger Bands + Volume)", use_container_width=True):
            st.session_state.show_ta = True
        if st.session_state.show_ta:
            st.plotly_chart(build_chart(hist, metal, show_ta=True), use_container_width=True)
            # RSI reading
            hist_copy = hist.copy()
            delta = hist_copy["Close"].diff()
            gain  = delta.clip(lower=0).rolling(14).mean()
            loss  = (-delta.clip(upper=0)).rolling(14).mean()
            rs    = gain / loss
            rsi_val = round((100 - (100 / (1 + rs))).iloc[-1], 1)
            rsi_signal = "🔴 OVERBOUGHT — potential reversal" if rsi_val > 70 else \
                         "🟢 OVERSOLD — potential bounce" if rsi_val < 30 else \
                         "🟡 NEUTRAL ZONE"
            st.markdown(f'<div class="bot-bubble">🤖 <b>RSI Reading: {rsi_val}</b> — {rsi_signal}<br>'
                        f'<br><b>How to read this chart:</b><br>'
                        f'• <b>Yellow line</b> = MA20 (short term trend)<br>'
                        f'• <b>Purple line</b> = MA50 (long term trend)<br>'
                        f'• <b>Blue dashed lines</b> = Bollinger Bands (volatility range)<br>'
                        f'• <b>RSI above 70</b> = overbought | <b>RSI below 30</b> = oversold</div>',
                        unsafe_allow_html=True)

        # AI Analysis
        st.markdown('<div class="section-head">🤖 AI-POWERED MARKET ANALYSIS</div>', unsafe_allow_html=True)
        with st.spinner("🧠 Claude AI generating analysis..."):
            analysis = get_ai_analysis(metal, price_data, hist)
        st.markdown(f'<div class="bot-bubble">🤖 {analysis.replace(chr(10),"<br>")}</div>',
                    unsafe_allow_html=True)

        # News
        st.markdown('<div class="section-head">📰 LIVE MARKET NEWS</div>', unsafe_allow_html=True)
        if news:
            for n in news:
                st.markdown(f'<div class="news-item">📌 {n}</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="news-item">No headlines at this moment — markets may be closed.</div>',
                        unsafe_allow_html=True)

    # Show next options INLINE — no rerun, no vanishing
    st.markdown("<hr style='border-color:#1e3a5f;margin:24px 0'>", unsafe_allow_html=True)
    st.markdown('<div class="bot-bubble">🤖 Analysis complete! Take your time exploring the charts above. When ready — what next?</div>', unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🔄 Check Another Metal", use_container_width=True, key="next_metal"):
        st.session_state.step     = "greet"
        st.session_state.selected = None
        st.session_state.show_ta  = False
        st.rerun()
    if c2.button("✅ Exit", use_container_width=True, key="exit_btn"):
        st.session_state.step = "exit"
        st.rerun()

# ════════════════════════════════════════════════════════════════════
# STEP 3 — END
# ════════════════════════════════════════════════════════════════════
elif st.session_state.step == "end":
    st.markdown('<div class="bot-bubble">🤖 Analysis complete! Would you like to check another metal?</div>',
                unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    if c1.button("🔄 Check Another Metal", use_container_width=True):
        add_msg("user", "Check another metal")
        st.session_state.step     = "greet"
        st.session_state.selected = None
        st.rerun()
    if c2.button("✅ Exit", use_container_width=True):
        add_msg("user", "Exit")
        st.session_state.step = "exit"
        st.rerun()

# ════════════════════════════════════════════════════════════════════
# STEP 4 — EXIT
# ════════════════════════════════════════════════════════════════════
elif st.session_state.step == "exit":
    st.markdown("""<div class="bot-bubble">🤖 Thank you for using <b>Metals Market AI</b>! 👋<br><br>
Stay informed and trade smart. Come back anytime for live prices and analysis.</div>""", unsafe_allow_html=True)
    if st.button("🔁 Start Over", use_container_width=True):
        for k in ["step","selected","greeted","msgs","show_ta"]:
            del st.session_state[k]
        st.rerun()
