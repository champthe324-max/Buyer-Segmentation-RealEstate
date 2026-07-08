import streamlit as st
import pandas as pd
import plotly.express as px


# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="Buyer Segmentation Dashboard",
    page_icon="🏠",
    layout="wide"
)

# ==========================================
# Load Dataset
# ==========================================

buyer_df = pd.read_csv("data/processed/final_buyer_dataset.csv")

# ==========================================
# Sidebar Filters
# ==========================================

st.sidebar.header("🔍 Filters")

# Country Filter
country = st.sidebar.selectbox(
    "Select Country",
    ["All"] + sorted(buyer_df["country"].unique().tolist())
)

# Region Filter
region = st.sidebar.selectbox(
    "Select Region",
    ["All"] + sorted(buyer_df["region"].unique().tolist())
)

# Buyer Persona Filter
buyer_persona = st.sidebar.selectbox(
    "Buyer Persona",
    ["All"] + sorted(buyer_df["Buyer_Persona"].unique().tolist())
)

# Loan Applied Filter
loan = st.sidebar.selectbox(
    "Loan Applied",
    ["All"] + sorted(buyer_df["loan_applied"].unique().tolist())
)

# ==========================================
# Apply Filters
# ==========================================

filtered_df = buyer_df.copy()

if country != "All":
    filtered_df = filtered_df[
        filtered_df["country"] == country
    ]

if region != "All":
    filtered_df = filtered_df[
        filtered_df["region"] == region
    ]

if buyer_persona != "All":
    filtered_df = filtered_df[
        filtered_df["Buyer_Persona"] == buyer_persona
    ]

if loan != "All":
    filtered_df = filtered_df[
        filtered_df["loan_applied"] == loan
    ]

# ==========================================
# Title
# ==========================================

st.title("🏠 Buyer Segmentation & Investment Profiling")
st.markdown("### Real Estate Market Intelligence Dashboard")

# ==========================================
# Success Message
# ==========================================

st.success("Dataset Loaded Successfully!")

# ==========================================
# KPI Metrics
# ==========================================
total_buyers = filtered_df.shape[0]

total_properties = filtered_df["total_properties"].sum()

total_investment = filtered_df["total_investment"].sum()

avg_satisfaction = filtered_df["satisfaction_score"].mean()

col1, col2, col3, col4 = st.columns(4)
col1.metric("👥 Total Buyers", f"{total_buyers:,}")
col2.metric("🏠 Total Properties", f"{int(total_properties):,}")
col3.metric("💰 Total Investment", f"${total_investment:,.0f}")
col4.metric("⭐ Avg Satisfaction", f"{avg_satisfaction:.2f}")

# ==========================================
# Buyer Persona Distribution
# ==========================================

st.subheader("📊 Buyer Persona Distribution")

persona_count = (
    filtered_df["Buyer_Persona"]
    .value_counts()
    .reset_index()
)

persona_count.columns = [
    "Buyer Persona",
    "Count"
]

fig = px.bar(
    persona_count,
    x="Buyer Persona",
    y="Count",
    color="Buyer Persona",
    text="Count",
    title="Buyer Persona Distribution"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Buyer Persona",
    yaxis_title="Number of Buyers",
    title_x=0.3
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Loan Applied Distribution
# ==========================================

st.subheader("🏦 Loan Applied Distribution")

loan_data = (
    filtered_df["loan_applied"]
    .value_counts()
    .reset_index()
)

loan_data.columns = [
    "Loan Applied",
    "Count"
]

fig = px.pie(
    loan_data,
    names="Loan Applied",
    values="Count",
    hole=0.45,
    title="Loan Applied Distribution"
)

fig.update_layout(
    template="plotly_white",
    height=450
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Buyers by Country
# ==========================================

st.subheader("🌍 Buyers by Country")

country_data = (
    filtered_df["country"]
    .value_counts()
    .reset_index()
)

country_data.columns = [
    "Country",
    "Number of Buyers"
]

fig = px.bar(
    country_data,
    x="Country",
    y="Number of Buyers",
    color="Country",
    text="Number of Buyers",
    title="Number of Buyers by Country"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    template="plotly_white",
    height=500,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)




# ==========================================
# Buyers by Region
# ==========================================

st.subheader("🗺️ Buyers by Region")

region_data = (
    filtered_df["region"]
    .value_counts()
    .reset_index()
)

region_data.columns = [
    "Region",
    "Number of Buyers"
]

fig = px.bar(
    region_data,
    x="Region",
    y="Number of Buyers",
    color="Region",
    text="Number of Buyers",
    title="Number of Buyers by Region"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    template="plotly_white",
    height=500,
    showlegend=False,
    xaxis_title="Region",
    yaxis_title="Buyers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Total Investment by Buyer Persona
# ==========================================

st.subheader("💰 Total Investment by Buyer Persona")

investment_data = (
    filtered_df
    .groupby("Buyer_Persona")["total_investment"]
    .sum()
    .reset_index()
)

fig = px.bar(
    investment_data,
    x="Buyer_Persona",
    y="total_investment",
    color="Buyer_Persona",
    text="total_investment",
    title="Total Investment by Buyer Persona"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Buyer Persona",
    yaxis_title="Total Investment ($)",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Age Distribution
# ==========================================

st.subheader("📈 Buyer Age Distribution")

fig = px.histogram(
    filtered_df,
    x="age",
    nbins=20,
    color_discrete_sequence=["#00CC96"],
    title="Distribution of Buyer Age"
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Age",
    yaxis_title="Number of Buyers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Average Satisfaction by Buyer Persona
# ==========================================

st.subheader("⭐ Average Satisfaction by Buyer Persona")

satisfaction_data = (
    filtered_df
    .groupby("Buyer_Persona")["satisfaction_score"]
    .mean()
    .reset_index()
)

fig = px.bar(
    satisfaction_data,
    x="Buyer_Persona",
    y="satisfaction_score",
    color="Buyer_Persona",
    text="satisfaction_score",
    title="Average Satisfaction Score by Buyer Persona"
)

fig.update_traces(
    texttemplate="%{text:.2f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Buyer Persona",
    yaxis_title="Average Satisfaction Score",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Referral Channel Analysis
# ==========================================

st.subheader("📢 Referral Channel Analysis")

referral_data = (
    filtered_df["referral_channel"]
    .value_counts()
    .reset_index()
)

referral_data.columns = [
    "Referral Channel",
    "Number of Buyers"
]

fig = px.bar(
    referral_data,
    x="Referral Channel",
    y="Number of Buyers",
    color="Referral Channel",
    text="Number of Buyers",
    title="Buyer Acquisition by Referral Channel"
)

fig.update_traces(textposition="outside")

fig.update_layout(
    template="plotly_dark",
    height=500,
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Investment by Country
# ==========================================

st.subheader("💰 Total Investment by Country")

investment_data = (
    filtered_df
    .groupby("country")["total_investment"]
    .sum()
    .reset_index()
)

fig = px.bar(
    investment_data,
    x="country",
    y="total_investment",
    color="country",
    text="total_investment",
    title="Total Investment by Country"
)

fig.update_traces(
    texttemplate="$%{text:,.0f}",
    textposition="outside"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Country",
    yaxis_title="Total Investment ($)",
    showlegend=False
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Age Distribution
# ==========================================

st.subheader("📈 Buyer Age Distribution")

fig = px.histogram(
    filtered_df,
    x="age",
    nbins=15,
    color_discrete_sequence=["#3B82F6"],
    title="Buyer Age Distribution"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Age",
    yaxis_title="Number of Buyers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Satisfaction Score Distribution
# ==========================================

st.subheader("⭐ Satisfaction Score Distribution")

fig = px.histogram(
    filtered_df,
    x="satisfaction_score",
    nbins=10,
    color_discrete_sequence=["#10B981"],
    title="Customer Satisfaction Score Distribution"
)

fig.update_layout(
    template="plotly_white",
    height=500,
    xaxis_title="Satisfaction Score",
    yaxis_title="Number of Buyers"
)

st.plotly_chart(fig, use_container_width=True)

# ==========================================
# Download Filtered Dataset
# ==========================================

st.download_button(
    label="📥 Download Filtered Dataset",
    data=filtered_df.to_csv(index=False),
    file_name="filtered_buyer_dataset.csv",
    mime="text/csv"
)

# ==========================================
# Business Insights
# ==========================================

st.subheader("💡 Business Insights")

highest_country = (
    filtered_df.groupby("country")["total_investment"]
    .sum()
    .idxmax()
)

highest_investment = (
    filtered_df.groupby("country")["total_investment"]
    .sum()
    .max()
)

top_persona = (
    filtered_df["Buyer_Persona"]
    .mode()[0]
)

loan_rate = (
    (filtered_df["loan_applied"] == "Yes").mean() * 100
)

avg_age = filtered_df["age"].mean()

avg_properties = filtered_df["total_properties"].mean()

st.info(f"""
🏆 **Highest Investment Country:** {highest_country}

💰 **Highest Investment:** ${highest_investment:,.0f}

👥 **Most Common Buyer Persona:** {top_persona}

🏠 **Average Properties Owned:** {avg_properties:.1f}

📈 **Average Buyer Age:** {avg_age:.1f} Years

🏦 **Loan Application Rate:** {loan_rate:.1f}%
""")

# ==========================================
# Dataset Preview
# ==========================================

st.subheader("Dataset Preview")

st.dataframe(filtered_df.head())    