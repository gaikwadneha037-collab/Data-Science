import streamlit as st
import pandas as pd
import numpy as np
import pickle

from tensorflow.keras.models import load_model

st.set_page_config(
    page_title="Tesla Stock Forecast",
    layout="centered"
)

st.title("📈 Tesla Stock Price Forecast")

st.write(
    """
    Predict Tesla Closing Prices using
    SimpleRNN and LSTM Models.
    """
)

# ----------------------------------

rnn_model = load_model(
    "best_rnn_model.keras"
)

lstm_model = load_model(
    "best_lstm_model.keras"
)

with open("scaler.pkl","rb") as f:
    scaler = pickle.load(f)

# Load Tesla historical data

df = pd.read_csv("TSLA.csv")

data = df[['Adj Close']]

scaled_data = scaler.transform(data)

# ----------------------------------

model_choice = st.selectbox(
    "Select Model",
    ["SimpleRNN","LSTM"]
)

forecast_days = st.selectbox(
    "Forecast Horizon",
    [1,5,10]
)

# ----------------------------------

if st.button("Predict Future Price"):

    model = (
        rnn_model
        if model_choice=="SimpleRNN"
        else lstm_model
    )

    last_60 = scaled_data[-60:]

    sequence = last_60.copy()

    forecasts = []

    for i in range(forecast_days):

        X = sequence.reshape(
            1,
            60,
            1
        )

        pred = model.predict(
            X,
            verbose=0
        )

        forecasts.append(
            pred[0][0]
        )

        sequence = np.append(
            sequence[1:],
            pred
        )

    forecasts = scaler.inverse_transform(
        np.array(forecasts).reshape(-1,1)
    )

    st.success(
        f"Forecast for Next {forecast_days} Day(s)"
    )

    for i,value in enumerate(
        forecasts.flatten(),
        start=1
    ):

        st.metric(
            f"Day {i}",
            f"${value:.2f}"
        )