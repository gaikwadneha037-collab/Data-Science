import streamlit as st
import pandas as pd
import numpy as np
import joblib

# MUST BE FIRST STREAMLIT COMMAND
st.set_page_config(
    page_title="Credit Risk Scoring App",
    layout="wide"
)

# =============================
# Load artifacts ONCE
# =============================
@st.cache_resource
def load_artifacts():
    model = joblib.load("model.pkl")
    scaler = joblib.load("scaler.pkl")
    features = joblib.load("features.pkl")
    threshold = joblib.load("threshold.pkl")
    return model, scaler, features, threshold

model, scaler, features, threshold = load_artifacts()

st.title("💳 Credit Risk Scoring App")
st.write("Predict probability of loan default using ML")

# =============================
# User Input Section
# =============================
st.subheader("Enter Applicant Details")

user_input = {}

for feature in features:
    if feature.startswith((
        "home_ownership_", "verification_status_", "purpose_",
        "addr_state_", "initial_list_status_", "disbursement_method_"
    )):
        user_input[feature] = st.selectbox(feature, [0, 1])
    else:
        user_input[feature] = st.number_input(feature, value=0.0)

# =============================
# Prediction
# =============================
if st.button("Predict Risk"):
    df = pd.DataFrame([user_input])
    df = df[features]  # ensure column order

    df_scaled = scaler.transform(df)
    prob = model.predict_proba(df_scaled)[0][1]

    decision = "REJECT" if prob >= threshold else "APPROVE"

    st.subheader("Prediction Result")
    st.metric("Default Probability", f"{prob:.2%}")

    if decision == "REJECT":
        st.error("❌ Loan Rejected (High Risk)")
    else:
        st.success("✅ Loan Approved (Low Risk)")
st.markdown("---")
st.caption(
    "⚠️ This model is for educational purposes only and should not be used for real credit decisions."
)