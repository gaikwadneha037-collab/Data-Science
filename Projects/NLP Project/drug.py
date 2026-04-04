#streamlit 
import streamlit as st
import joblib

# Load model
sentiment_model = joblib.load("sentiment_model.pkl")
disease_model = joblib.load("disease_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

st.title("Drug Review Analyzer")

user_input = st.text_area("Enter Patient Review:")

if st.button("Predict"):
    input_vec = vectorizer.transform([user_input])
    
    sentiment = sentiment_model.predict(input_vec)[0]
    disease = disease_model.predict(input_vec)[0]
    
    st.subheader("Prediction:")
    st.write("Sentiment:", sentiment)
    st.write("Predicted Condition:", disease)