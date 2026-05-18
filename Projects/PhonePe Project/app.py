import streamlit as st
import pandas as pd
import joblib

import matplotlib.pyplot as plt
import seaborn as sns


# -----------------------------------
# PAGE CONFIG
# -----------------------------------

st.set_page_config(

    page_title="PhonePe Analytics Dashboard",

    layout="wide"
)


# -----------------------------------
# TITLE
# -----------------------------------

st.title("PhonePe Transaction Insights Dashboard")


# -----------------------------------
# LOAD DATASET
# -----------------------------------

df = pd.read_csv(
    "aggregated_transaction_combined.csv"
)


# -----------------------------------
# SIDEBAR FILTERS
# -----------------------------------

st.sidebar.header("Filters")


# State Filter

selected_state = st.sidebar.selectbox(

    "Select State",

    sorted(df['state'].dropna().unique())
)


# Year Filter

selected_year = st.sidebar.selectbox(

    "Select Year",

    sorted(df['year'].unique())
)


# FILTER DATA

if selected_state == "No State":

    filtered_df = df[
        (df['state'].isna()) &
        (df['year'] == selected_year)
    ]

else:

    filtered_df = df[

        (df['state'] == selected_state) &

        (df['year'] == selected_year)

    ]


# -----------------------------------
# KPI METRICS
# -----------------------------------

total_amount = filtered_df['amount'].sum()

total_count = filtered_df['count'].sum()

avg_amount = filtered_df['amount'].mean()


# -----------------------------------
# DISPLAY METRICS
# -----------------------------------

st.header("Key Metrics")

col1, col2, col3 = st.columns(3)

with col1:

    st.metric(

        "Total Transaction Amount",

        f"₹ {total_amount:,.0f}"
    )

with col2:

    st.metric(

        "Total Transaction Count",

        f"{total_count:,.0f}"
    )

with col3:

    st.metric(

        "Average Transaction Amount",

        f"₹ {avg_amount:,.0f}"
    )


st.markdown("---")


# ===================================
# VISUALIZATION SECTION
# ===================================

st.header("Visual Analysis")


# -----------------------------------
# BAR CHART
# -----------------------------------

st.subheader("Transaction Amount by Type")

transaction_chart = (

    filtered_df.groupby(
        'transaction_type'
    )['amount']

    .sum()

    .reset_index()

    .sort_values(by='amount', ascending=False)

)

fig1, ax1 = plt.subplots(figsize=(10,5))

sns.barplot(

    data=transaction_chart,

    x='transaction_type',

    y='amount',

    ax=ax1

)

plt.xticks(rotation=45)

plt.title(
    f"Transaction Amount by Type - {selected_state.title()} ({selected_year})"
)

plt.xlabel("Transaction Type")

plt.ylabel("Amount")

st.pyplot(fig1)

st.markdown("---")


# -----------------------------------
# PIE CHART
# -----------------------------------

st.subheader("Transaction Share by Type")

fig2, ax2 = plt.subplots(figsize=(7,7))

ax2.pie(

    transaction_chart['amount'],

    labels=transaction_chart['transaction_type'],

    autopct='%1.1f%%'

)

plt.title(
    f"Transaction Share - {selected_state.title()} ({selected_year})"
)

st.pyplot(fig2)

st.markdown("---")


# -----------------------------------
# YEARLY TREND
# -----------------------------------

st.subheader("Yearly Transaction Trend")


# Filter ONLY by state
yearly_trend = (

    df[df['state'] == selected_state]

    .groupby('year')['amount']

    .sum()

    .reset_index()

)

fig3, ax3 = plt.subplots(figsize=(10,5))

sns.lineplot(

    data=yearly_trend,

    x='year',

    y='amount',

    marker='o',

    ax=ax3

)

plt.title(
    f"Yearly Transaction Trend - {selected_state.title()}"
)

plt.xlabel("Year")

plt.ylabel("Transaction Amount")

st.pyplot(fig3)

st.markdown("---")


# -----------------------------------
# QUARTERLY TREND
# -----------------------------------

st.subheader("Quarterly Transaction Trend")

quarterly_trend = (

    filtered_df.groupby('quarter')['amount']

    .sum()

    .reset_index()

)

fig4, ax4 = plt.subplots(figsize=(10,5))

sns.lineplot(

    data=quarterly_trend,

    x='quarter',

    y='amount',

    marker='o',

    ax=ax4

)

plt.title(
    f"Quarterly Transaction Trend - {selected_state.title()} ({selected_year})"
)

plt.xlabel("Quarter")

plt.ylabel("Transaction Amount")

st.pyplot(fig4)

st.markdown("---")


fig5, ax5 = plt.subplots(figsize=(10,6))


# ===================================
# LOAD MODEL
# ===================================

model = joblib.load(
    "phonepe_transaction_model.pkl"
)


# ===================================
# PREDICTION SECTION
# ===================================

st.header("Transaction Amount Prediction")


# -----------------------------------
# USER INPUTS
# -----------------------------------

state_input = st.selectbox(

    "Prediction State",

    sorted(df['state'].dropna().unique())
)

year_input = st.selectbox(

    "Prediction Year",

    [2020, 2021, 2022, 2023, 2024, 2025, 2026, 2027]
)

quarter_input = st.selectbox(

    "Prediction Quarter",

    [1, 2, 3, 4]
)

transaction_input = st.selectbox(

    "Prediction Transaction Type",

    df['transaction_type'].unique()
)

count_input = st.number_input(

    "Transaction Count",

    min_value=1
)


# -----------------------------------
# PREDICTION
# -----------------------------------

if st.button("Predict Transaction Amount"):

    input_df = pd.DataFrame({

        'state': [state_input],

        'year': [year_input],

        'quarter': [quarter_input],

        'transaction_type': [transaction_input],

        'count': [count_input]

    })

    prediction = model.predict(input_df)

    st.success(

        f"Predicted Transaction Amount: ₹ {prediction[0]:,.2f}"

    )