import streamlit as st
import requests

# Streamlit app title
st.title("Banking Simulator")

# Input fields for loan details
st.sidebar.header("Loan Details")
principal = st.sidebar.text_input("Principal Amount", value="10,000.00")

# Convert the input to a float after removing commas
try:
    principal = float(principal.replace(",", ""))
except ValueError:
    st.sidebar.error("Please enter a valid number for the principal amount.")

annual_interest_rate = st.sidebar.number_input("Annual Interest Rate (%)", min_value=0.0, value=5.0, step=0.1)
years = st.sidebar.number_input("Loan Term (Years)", min_value=1, value=5, step=1)
funding_cost_rate = st.sidebar.number_input("Funding Cost Rate (%)", min_value=0.0, value=2.0, step=0.1)

# Button to calculate loan details
if st.sidebar.button("Calculate"):
    # API endpoint
    api_url = "http://127.0.0.1:8000/calculate-loan-returns"

    # Request payload
    payload = {
        "principal": principal,
        "annual_interest_rate": annual_interest_rate,
        "years": years,
        "funding_cost_rate": funding_cost_rate
    }

    # Make a POST request to the API
    try:
        response = requests.post(api_url, json=payload)
        response_data = response.json()

        if response.status_code == 200:
            # Display results
            st.subheader("Loan Calculation Results")
            st.write(f"**Principal:** ${response_data['principal']:,.2f}")
            st.write(f"**Total Repayments:** ${response_data['total_repayments']:,.2f}")
            st.write(f"**Interest Income:** ${response_data['interest_income']:,.2f}")
            st.write(f"**Interest Expense:** ${response_data['interest_expense']:,.2f}")
            st.write(f"**Net Interest Margin (NIM):** {response_data['net_interest_margin'] * 100:,.2f}%")
            st.write(f"**Net Interest Income:** ${response_data['net_interest_income']:,.2f}")
        else:
            st.error(f"Error: {response_data.get('detail', 'Unknown error')}")
    except requests.exceptions.RequestException as e:
        st.error(f"Error connecting to the API: {e}")