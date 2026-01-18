import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Stock Dashboard",
    page_icon="📈",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.big-title {
    font-size: 35px;
    font-weight: 800;
    color: #00C853;
}
.small-title {
    font-size: 18px;
    font-weight: 600;
    color: #ffffff;
}
.kpi-card {
    background: #111827;
    padding: 18px;
    border-radius: 15px;
    text-align: center;
    color: white;
    box-shadow: 0px 4px 12px rgba(0,0,0,0.2);
}
.kpi-value {
    font-size: 28px;
    font-weight: 800;
    color: #00E676;
}
.kpi-label {
    font-size: 14px;
    color: #cbd5e1;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown('<div class="big-title">📊 Advanced Stock Market Dashboard</div>', unsafe_allow_html=True)
st.write("This dashboard shows **Adj Close trend, moving averages, returns, and volume analysis**.")

# ---------------- LOAD DATA ----------------
@st.cache_data
def load_data():
    df = pd.read_csv("AAPL (5).csv")   # <-- change your file name here
    df['Date'] = pd.to_datetime(df['Date'])
    df = df.sort_values("Date")
    return df

pj = load_data()

# ---------------- SIDEBAR FILTERS ----------------
st.sidebar.header("📌 Dashboard Filters")

start_date = st.sidebar.date_input("Start Date", pj["Date"].min().date())
end_date = st.sidebar.date_input("End Date", pj["Date"].max().date())

show_ma = st.sidebar.checkbox("Show Moving Averages (MA50 & MA200)", True)
show_returns = st.sidebar.checkbox("Show Daily Returns Chart", True)
show_volume = st.sidebar.checkbox("Show Volume Chart", True)

filtered = pj[(pj["Date"] >= pd.to_datetime(start_date)) & (pj["Date"] <= pd.to_datetime(end_date))]

# ---------------- FEATURE ENGINEERING ----------------
filtered["Daily Return"] = filtered["Adj Close"].pct_change()

filtered["MA50"] = filtered["Adj Close"].rolling(50).mean()
filtered["MA200"] = filtered["Adj Close"].rolling(200).mean()

latest_price = filtered["Adj Close"].iloc[-1]
max_price = filtered["Adj Close"].max()
min_price = filtered["Adj Close"].min()
avg_volume = int(filtered["Volume"].mean())

total_return = ((filtered["Adj Close"].iloc[-1] / filtered["Adj Close"].iloc[0]) - 1) * 100

# ---------------- KPI CARDS ----------------
st.subheader("📌 Key Performance Indicators (KPIs)")

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{latest_price:.2f}</div>
        <div class="kpi-label">Latest Adj Close</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{max_price:.2f}</div>
        <div class="kpi-label">Max Adj Close</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{min_price:.2f}</div>
        <div class="kpi-label">Min Adj Close</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{avg_volume:,}</div>
        <div class="kpi-label">Avg Volume</div>
    </div>
    """, unsafe_allow_html=True)

with col5:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-value">{total_return:.2f}%</div>
        <div class="kpi-label">Total Return</div>
    </div>
    """, unsafe_allow_html=True)

st.divider()

# ---------------- CHART 1: Adj Close Trend ----------------
st.subheader("📈 Adj Close Price Trend")

fig, ax = plt.subplots(figsize=(12,4))
ax.plot(filtered["Date"], filtered["Adj Close"], label="Adj Close")

if show_ma:
    ax.plot(filtered["Date"], filtered["MA50"], label="MA50")
    ax.plot(filtered["Date"], filtered["MA200"], label="MA200")

ax.set_xlabel("Date")
ax.set_ylabel("Price")
ax.grid(True)
ax.legend()
st.pyplot(fig)

# ---------------- CHART 2: Daily Returns ----------------
if show_returns:
    st.subheader("📉 Daily Returns Trend")
    fig2, ax2 = plt.subplots(figsize=(12,4))
    ax2.plot(filtered["Date"], filtered["Daily Return"])
    ax2.axhline(0, linestyle="--")
    ax2.set_xlabel("Date")
    ax2.set_ylabel("Daily Return")
    ax2.grid(True)
    st.pyplot(fig2)

# ---------------- CHART 3: Volume Chart ----------------
if show_volume:
    st.subheader("📊 Volume Over Time")
    fig3, ax3 = plt.subplots(figsize=(12,4))
    ax3.bar(filtered["Date"], filtered["Volume"])
    ax3.set_xlabel("Date")
    ax3.set_ylabel("Volume")
    ax3.grid(True)
    st.pyplot(fig3)

# ---------------- Volume vs Returns Scatter ----------------
st.subheader("🔍 Volume vs Daily Return Relationship")

fig4, ax4 = plt.subplots(figsize=(6,4))
ax4.scatter(filtered["Volume"], filtered["Daily Return"])
ax4.set_xlabel("Volume")
ax4.set_ylabel("Daily Return")
ax4.grid(True)
st.pyplot(fig4)

corr = filtered["Volume"].corr(filtered["Daily Return"])
st.write(f"📌 Correlation between Volume and Daily Return: **{corr:.4f}**")

# ---------------- DATA DOWNLOAD ----------------
st.subheader("⬇ Download Filtered Dataset")

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Download CSV",
    data=csv,
    file_name="filtered_stock_data.csv",
    mime="text/csv"
)

# ---------------- SHOW TABLE ----------------
st.subheader("📄 Filtered Data Preview")
st.dataframe(filtered.tail(10))


