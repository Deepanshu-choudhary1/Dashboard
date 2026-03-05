import streamlit as st
import pandas as pd
import plotly.express as px
import time

st.set_page_config(
    page_title="Retail Intelligence Dashboard",
    layout="wide",
    page_icon="📊"
)

# --------------------------------------------------
# Glassmorphism + SaaS Style CSS
# --------------------------------------------------

st.markdown("""
<style>

.stApp {
background: linear-gradient(135deg,#0f2027,#203a43,#2c5364);
color:white;
}

section[data-testid="stSidebar"] {
background: rgba(255,255,255,0.05);
backdrop-filter: blur(10px);
border-right:1px solid rgba(255,255,255,0.2);
}

.glass-card {
background: rgba(255,255,255,0.08);
border-radius:15px;
padding:20px;
backdrop-filter: blur(10px);
border:1px solid rgba(255,255,255,0.2);
box-shadow:0 8px 32px rgba(0,0,0,0.35);
text-align:center;
}

.metric-value {
font-size:32px;
font-weight:bold;
}

.metric-label {
font-size:14px;
opacity:0.8;
}

.chart-container {
background: rgba(255,255,255,0.06);
border-radius:15px;
padding:15px;
backdrop-filter: blur(10px);
border:1px solid rgba(255,255,255,0.15);
}

</style>
""", unsafe_allow_html=True)

# --------------------------------------------------
# Load Data
# --------------------------------------------------

@st.cache_data
def load_data():
    df = pd.read_csv("Superstore.csv", encoding="latin1")
    df["Order Date"] = pd.to_datetime(df["Order Date"])
    df["Year"] = df["Order Date"].dt.year
    df["Month"] = df["Order Date"].dt.strftime("%Y-%m")
    return df

df = load_data()

# --------------------------------------------------
# Sidebar Filters
# --------------------------------------------------

st.sidebar.title("Dashboard Filters")

region = st.sidebar.multiselect(
    "Region",
    df["Region"].unique(),
    default=df["Region"].unique()
)

category = st.sidebar.multiselect(
    "Category",
    df["Category"].unique(),
    default=df["Category"].unique()
)

year = st.sidebar.slider(
    "Year",
    int(df["Year"].min()),
    int(df["Year"].max()),
    (int(df["Year"].min()), int(df["Year"].max()))
)

filtered = df[
    (df["Region"].isin(region)) &
    (df["Category"].isin(category)) &
    (df["Year"].between(year[0], year[1]))
]

# --------------------------------------------------
# Title
# --------------------------------------------------

st.title("📊 Retail Intelligence Dashboard")

# --------------------------------------------------
# Animated KPI Function
# --------------------------------------------------

def animated_metric(label, value):

    placeholder = st.empty()

    for i in range(0, int(value), max(1,int(value/50))):
        placeholder.markdown(f"""
        <div class="glass-card">
            <div class="metric-value">{i}</div>
            <div class="metric-label">{label}</div>
        </div>
        """, unsafe_allow_html=True)
        time.sleep(0.01)

    placeholder.markdown(f"""
    <div class="glass-card">
        <div class="metric-value">{value:,}</div>
        <div class="metric-label">{label}</div>
    </div>
    """, unsafe_allow_html=True)

# --------------------------------------------------
# KPI Metrics
# --------------------------------------------------

sales = int(filtered["Sales"].sum())
profit = int(filtered["Profit"].sum())
orders = int(filtered["Order ID"].nunique())
units = int(filtered["Quantity"].sum())

c1,c2,c3,c4 = st.columns(4)

with c1:
    animated_metric("Total Sales ($)", sales)

with c2:
    animated_metric("Total Profit ($)", profit)

with c3:
    animated_metric("Total Orders", orders)

with c4:
    animated_metric("Units Sold", units)

st.write("")

# --------------------------------------------------
# Charts
# --------------------------------------------------

trend = filtered.groupby("Month")["Sales"].sum().reset_index()

fig1 = px.line(
    trend,
    x="Month",
    y="Sales",
    markers=True,
    title="Monthly Sales Trend",
)

fig2 = px.bar(
    filtered.groupby("Category")["Sales"].sum().reset_index(),
    x="Category",
    y="Sales",
    color="Category",
    title="Sales by Category"
)

fig3 = px.pie(
    filtered,
    names="Region",
    values="Sales",
    title="Sales Distribution by Region"
)

top = filtered.groupby("Sub-Category")["Sales"].sum().nlargest(10).reset_index()

fig4 = px.bar(
    top,
    x="Sales",
    y="Sub-Category",
    orientation="h",
    title="Top Products"
)

fig5 = px.scatter(
    filtered,
    x="Sales",
    y="Profit",
    size="Quantity",
    color="Category",
    hover_data=["Sub-Category"],
    title="Sales vs Profit"
)

# --------------------------------------------------
# Layout Charts
# --------------------------------------------------

col1,col2 = st.columns(2)

with col1:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig1, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig2, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

col3,col4 = st.columns(2)

with col3:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig3, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="chart-container">', unsafe_allow_html=True)
    st.plotly_chart(fig4, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="chart-container">', unsafe_allow_html=True)
st.plotly_chart(fig5, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)

# --------------------------------------------------
# Data Table
# --------------------------------------------------

st.subheader("Filtered Data")
st.dataframe(filtered)