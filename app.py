import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.title("Strait of Hormuz - Ship Traffic Analysis")

uploaded_file = st.file_uploader("Upload CSV file", type="csv")
if uploaded_file:
    df = pd.read_csv(uploaded_file, parse_dates=["DateTime"])
    df.sort_values("DateTime", inplace=True)

    df["Total Ships"] = df["Number of Tanker Ships"] + df["Number of Cargo Ships"]
    df["Month"] = df["DateTime"].dt.to_period("M")
    df["Week"] = df["DateTime"].dt.to_period("W")

    st.subheader("Raw Data Preview")
    st.dataframe(df.tail(10))

    plot_type = st.radio("Select plot type", ["Single Ship Type", "Overlay All Types"])

    if plot_type == "Single Ship Type":
        ship_type = st.radio("Select ship type for analysis", ["Tanker", "Cargo", "Total"])
        if ship_type == "Tanker":
            column = "Number of Tanker Ships"
        elif ship_type == "Cargo":
            column = "Number of Cargo Ships"
        else:
            column = "Total Ships"

        threshold = st.number_input(f"Set threshold for {ship_type} Ships", min_value=1, max_value=200, value=15)

        st.subheader(f"{ship_type} Ship Traffic Over Time")
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df["DateTime"], df[column], label=f"{ship_type} Ships")
        ax.axhline(y=threshold, color='r', linestyle='--', label=f"Threshold: {threshold}")
        ax.set_ylabel("Number of Ships")
        ax.set_xlabel("Date")
        ax.legend()
        st.pyplot(fig)

        df["Below Threshold"] = df[column] < threshold
        consecutive = (df["Below Threshold"] & df["Below Threshold"].shift(-1)).fillna(False)
        dates_below = df[consecutive][["DateTime", column]]

        st.subheader("Consecutive Days Below Threshold")
        st.dataframe(dates_below)

        st.subheader("Summary")
        st.markdown(f"- Total number of days below threshold: **{int(df['Below Threshold'].sum())}**")
        st.markdown(f"- Number of 2-day consecutive below-threshold events: **{int(consecutive.sum())}**")

    else:
        st.subheader("Overlay of Tanker, Cargo, and Total Ships")
        fig, ax = plt.subplots(figsize=(12, 5))
        ax.plot(df["DateTime"], df["Number of Tanker Ships"], label="Tanker Ships")
        ax.plot(df["DateTime"], df["Number of Cargo Ships"], label="Cargo Ships")
        ax.plot(df["DateTime"], df["Total Ships"], label="Total Ships")
        ax.set_ylabel("Number of Ships")
        ax.set_xlabel("Date")
        ax.legend()
        st.pyplot(fig)

    st.subheader("Weekly Summary")
    weekly_summary = df.groupby("Week")[["Number of Tanker Ships", "Number of Cargo Ships", "Total Ships"]].mean().round(2)
    st.dataframe(weekly_summary)
