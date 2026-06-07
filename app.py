import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import requests
from sklearn.linear_model import LinearRegression
from utils.data_loader import load_data

# Coffee Sales Dashboard
# This Streamlit app displays and analyzes coffee sales data

# Set page configuration
st.set_page_config(
    page_title="Coffee Sales Dashboard",
    layout="wide"
)

# Load the data
data = load_data()

# Sidebar filters
st.sidebar.title("Filters")

# Date range filter
min_date = data["Date"].min().date() if "Date" in data.columns else None
max_date = data["Date"].max().date() if "Date" in data.columns else None
start_date, end_date = st.sidebar.date_input(
    "Date Range",
    value=(min_date, max_date) if min_date and max_date else None)

# Category multiselect filter
categories = data["Category"].unique() if "Category" in data.columns else []
selected_categories = st.sidebar.multiselect(
    "Category",
    options=categories,
    default=categories
)

# Apply filters
filtered_data = data.copy()
if "Date" in data.columns and start_date and end_date:
    filtered_data = filtered_data[
        (filtered_data["Date"] >= pd.to_datetime(start_date)) &
        (filtered_data["Date"] <= pd.to_datetime(end_date))
    ]
if "Category" in data.columns:
    filtered_data = filtered_data[filtered_data["Category"].isin(selected_categories)]

# Display main title
st.title("Coffee Sales Dashboard")

# Display filtered data preview
st.write("First 10 rows of filtered data:")
st.dataframe(filtered_data.head(10))

# Display total number of rows after filtering
st.write(f"Total number of rows: {len(filtered_data)}")

# Revenue Over Time - Line chart showing monthly revenue trend
st.subheader("Revenue Over Time")
monthly_revenue = filtered_data.groupby(filtered_data["Date"].dt.to_period("M"))["Amount"].sum().reset_index()
monthly_revenue["Date"] = monthly_revenue["Date"].dt.to_timestamp()
fig1 = px.line(
    monthly_revenue, 
    x="Date", 
    y="Amount", 
    title="Monthly Revenue",
    labels={"Date": "Month", "Amount": "Total Revenue"},
    markers=True
)
st.plotly_chart(fig1, use_container_width=True)

# Add revenue forecast section
st.subheader("Next Month Revenue Forecast")
if len(monthly_revenue) < 2:
    st.info("Not enough data for revenue forecast.")
else:
    # Create numeric month index
    X = np.arange(len(monthly_revenue)).reshape(-1, 1)
    y = monthly_revenue['Amount'].values
    
    # Fit linear regression model
    model = LinearRegression()
    model.fit(X, y)
    
    # Predict next month
    next_month_index = len(monthly_revenue)
    predicted_revenue = model.predict([[next_month_index]])
    
    # Display metric
    st.metric(label="Predicted revenue", value=f"${predicted_revenue[0]:,.2f}")
    
    # Display R-squared
    r2 = model.score(X, y)
    st.caption(f"R-squared: {r2:.2f} (Closer to 1 means better fit)")
    
    # Add explanation
    st.caption("This is a simple linear trend estimate, not a precise prediction.")
    
    # Add warning for small datasets
    if 2 <= len(monthly_revenue) <= 3:
        st.warning("Forecast based on very little data.")

# Top 10 Products by Revenue - Horizontal bar chart
st.subheader("Top 10 Products by Revenue")
top_products = filtered_data.groupby("Product")["Amount"].sum().nlargest(10).reset_index()
fig2 = px.bar(
    top_products, 
    x="Amount", 
    y="Product", 
    orientation="h", 
    title="Top 10 Products by Revenue",
    labels={"Amount": "Total Revenue", "Product": "Product"}
)
fig2.update_yaxes(categoryorder="total ascending")
st.plotly_chart(fig2, use_container_width=True)

# Revenue Share by Category - Pie chart
st.subheader("Revenue Share by Category")
revenue_by_category = filtered_data.groupby("Category")["Amount"].sum().reset_index()
fig3 = px.pie(
    revenue_by_category, 
    names="Category", 
    values="Amount", 
    title="Revenue Share by Category"
)
fig3.update_traces(textposition='inside', textinfo='percent+label')
st.plotly_chart(fig3, use_container_width=True)
# Add AI Data Summary section

st.subheader("AI Data Summary")
if st.button("Generate AI Summary"):
    with st.spinner("Generating AI summary..."):
        try:
            # Compute key statistics
            total_revenue = filtered_data["Amount"].sum()
            num_transactions = len(filtered_data)
            
            # Top product by revenue
            top_product_series = filtered_data.groupby("Product")["Amount"].sum()
            top_product = top_product_series.idxmax()
            top_product_revenue = top_product_series[top_product]
            
            # Month with highest revenue
            max_month = monthly_revenue.loc[monthly_revenue["Amount"].idxmax(), "Date"].strftime("%B %Y")
            max_month_revenue = monthly_revenue.loc[monthly_revenue["Amount"].idxmax(), "Amount"]
            
            # Unique categories
            num_categories = len(filtered_data["Category"].unique())
            
            # Build prompt
            prompt = f"""
Generate a 2-3 sentence business summary based on the following data:

Total Revenue: ${total_revenue:,.2f}
Number of Transactions: {num_transactions}
Top Product by Revenue: {top_product} (${top_product_revenue:,.2f})
Month with Highest Revenue: {max_month} (${max_month_revenue:,.2f})
Number of Unique Categories: {num_categories}

Please provide a concise summary in plain English.
"""
            
            # API call to OpenRouter
            headers = {
                "Authorization": f"Bearer {st.secrets['OPENROUTER_API_KEY']}",
                "Content-Type": "application/json"
            }
            data = {
                "model": "openrouter/free",
                "messages": [{"role": "user", "content": prompt}]
            }
            
            response = requests.post(
                "https://openrouter.ai/api/v1/chat/completions",
                headers=headers,
                json=data
            )
            response.raise_for_status()
            summary = response.json()["choices"][0]["message"]["content"]
            st.write("### AI Business Summary")
            st.write(summary)
            
        except requests.exceptions.RequestException as e:
            st.error(f"API request failed: {str(e)}")
        except KeyError:
            st.error("OpenRouter API key not found in secrets")
        except Exception as e:
            st.error(f"An error occurred: {str(e)}")
            
