"""Data loader module for coffee sales data."""

import streamlit as st
import pandas as pd


@st.cache_data
def load_data():
    """Load coffee sales data from CSV file and prepare columns."""
    # Read the new dataset
    df = pd.read_csv("data/index_1.csv")
    
    # Rename columns to match the existing app schema
    df.rename(columns={
        "date": "Date",
        "money": "Amount",
        "coffee_name": "Product"
    }, inplace=True)
    
    # Convert the Date column to datetime (after renaming)
    df["Date"] = pd.to_datetime(df["Date"])
    
    # Create a Category column that duplicates Product
    df["Category"] = df["Product"]
    
    # No need to clean Amount as it is already numeric
    return df
