import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
from google.genai import Client
from google.genai.types import HttpOptions
import httpx
import pandas as pd
import sqlite3

conn = sqlite3.connect("budget_history.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS allocations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        income REAL,
        percent_allocated REAL,
        leftover_cash REAL
)
""")
conn.commit()

# Code to get Integrated AI working
os.environ["CURL_CA_BUNDLE"] = ""
client = Client(http_options=HttpOptions(timeout=15.0),)

st.title("Personal Finance Dashboard")

# Creating different tabs for the dashboard
tab_planner, tab_history, tab_insights = st.tabs(["Budget Planner", "Budget History", "Insights"])

# Tab to figure out budgets based on your percents
with tab_planner:
    st.header("Choose Which Accounts to Include")

# Creates select buttons
    col_chk, col_sav, col_hys, col_rot = st.columns(4)
    with col_chk:
        show_checking = st.checkbox("Include Checking", value = False)
    with col_sav:
        show_saving = st.checkbox("Include Saving", value = False)
    with col_hys:
        show_hys = st.checkbox("Include High-Yield Saving", value = False)
    with col_rot:
        show_roth_ira = st.checkbox("Include Roth-IRA", value = False)

    col_bro, col_tra, col_cha = st.columns(3)
    with col_bro:
        show_brokerage = st.checkbox("Include Brokerage", value = False)
    with col_tra:
        show_travel_fund = st.checkbox("Include Travel Fund", value = False)
    with col_cha:
        show_charity = st.checkbox("Include Charity", value = False)

    st.write("---")
    st.header("Allocate Your Income")
    # Create slider and income buttons
    income_col, saving_col, checking_col = st.columns(3)
    with income_col:
        income = st.number_input(
            label = "Total Period Income ($)",
            min_value = 0.0,
            value = 500.00,
            step = 10.00,
            format="%.2f"
        )
    with saving_col:
        saving_pct = st.slider("Saving Percentage:", 0, 100, 0)
    with checking_col:
        checking_pct = st.slider("Checking Account Percentage:", 0, 100, 0)

    hys_col, roth_ira_col, brokerage_col = st.columns(3)
    with hys_col:
        hys_pct = st.slider("High-Yield Saving Percentage", 0, 100, 0)
    with roth_ira_col:
        roth_ira_pct = st.slider("Roth-IRA Percentage", 0, 100, 0)
    with brokerage_col:
        brokerage_pct = st.slider("Brokerage Percentage", 0, 100, 0)
    
    travel_fund_col, charity_col = st.columns(2)
    with travel_fund_col:
        travel_fund_pct = st.slider("Travel Fund Percentage", 0, 100, 0)
    with charity_col:
        charity_pct = st.slider("Charity Percentage", 0, 100, 0)

    if saving_pct + checking_pct + hys_pct + roth_ira_pct + brokerage_pct + travel_fund_pct + charity_pct > 100:
        st.error("The sum of your percentages cannot exceed 100%. Please adjust the sliders.")
        st.stop()  # Stop execution if the condition is met
    elif saving_pct + checking_pct + hys_pct + roth_ira_pct + brokerage_pct + travel_fund_pct + charity_pct < 100:
        st.info("The of your percentages is less than 100%. The leftover cash will be calculated accordingly.")
    else:
        st.success("The sum of your percentages is exactly 100%. No leftover cash will be available.")

    # Budget math
    base_saving_amount = income * (saving_pct / 100)
    base_checking_amount = income * (checking_pct / 100)
    base_hys_amount = income * (hys_pct / 100)
    base_roth_ira_amount = income * (roth_ira_pct / 100)
    base_brokerage_amount = income * (brokerage_pct / 100)
    base_travel_fund_amount = income * (travel_fund_pct / 100)
    base_charity_amount = income * (charity_pct / 100)


    saving_amount = base_saving_amount if show_saving else 0.00
    checking_amount = base_checking_amount if show_checking else 0.00
    hys_amount = base_hys_amount if show_hys else 0.00
    roth_ira_amount = base_roth_ira_amount if show_roth_ira else 0.00
    brokerage_amount = base_brokerage_amount if show_brokerage else 0.00
    travel_fund_amount = base_travel_fund_amount if show_travel_fund else 0.00
    charity_amount = base_charity_amount if show_charity else 0.00
    leftover_amount = income - (checking_amount + saving_amount + hys_amount + roth_ira_amount + brokerage_amount + travel_fund_amount + charity_amount)


    st.markdown("---") # Visual divider line
    st.header("Financial Breakdown")

    # Data Table
    chart_data = pd.DataFrame(
        {
            "Account": ["Saving", "Checking", "High-Yield Saving", "Roth-IRA", "Brokerage", "Travel Fund", "Charity", "Leftover Cash"],
            "Amount": [saving_amount, checking_amount, hys_amount, roth_ira_amount, brokerage_amount, travel_fund_amount, charity_amount, leftover_amount],
            "Color": ["#2ecc71", "#3498db", "#9b59b6", "#e67e22", "#34495e", "#1abc9c", "#f1c40f",  "#e74c3c"]
        }
    )

    allowed_accounts = ["Leftover Cash"]
    if show_checking:
        allowed_accounts.append("Checking")
    if show_saving:
        allowed_accounts.append("Saving")
    if show_hys:
        allowed_accounts.append("High-Yield Saving")
    if show_roth_ira:
        allowed_accounts.append("Roth-IRA")
    if show_brokerage:
        allowed_accounts.append("Brokerage")
    if show_travel_fund:
        allowed_accounts.append("Travel Fund")
    if show_charity:
        allowed_accounts.append("Charity")

    filtered_data = chart_data[chart_data["Account"].isin(allowed_accounts)].copy()

    filtered_data["Account"] = pd.Categorical(
        filtered_data["Account"],
        categories = ["Checking", "Saving", "High-Yield Saving", "Roth-IRA", "Brokerage", "Travel Fund", "Charity", "Leftover Cash"],
        ordered = True
    )
    filtered_data = filtered_data.sort_values("Account")

    chart_data["Account"] = pd.Categorical(
        chart_data["Account"],
        categories=["Checking", "Saving", "High-Yield Saving", "Roth-IRA", "Brokerage", "Travel Fund", "Charity", "Leftover Cash"],
        ordered = True
    )

    chart_data = chart_data.sort_values("Account")
    chart_data = chart_data.set_index("Account")

    if not filtered_data.empty:
        st.bar_chart(
            filtered_data,
            x = "Account",
            y = "Amount",
            color = "Color"
        )

        
    else:
        st.info("Select at least one account category above to view the graph.")

    if st.button("Save Transaction History"):
        # Save to SQL db
        cursor.execute("""
        INSERT INTO allocations (income, percent_allocated, leftover_cash) 
        VALUES (?, ?, ?)
        """, (income, saving_pct + checking_pct + hys_pct + roth_ira_pct + brokerage_pct + travel_fund_pct + charity_pct, leftover_amount))

        conn.commit()
        st.success("Transaction history saved successfully!")



# Tab to see recent history of budgets
with tab_history:
    st.header("Budget History")
    # Creating Database History Table
    df = pd.read_sql_query("SELECT * FROM allocations", conn)
    st.dataframe(df)

    # Clear Button
    if st.button("Clear Transaction History"):
        cursor.execute("DELETE FROM allocations")
        conn.commit()
        st.success("Transaction history cleared successfully!")



# AI Integration Section
with tab_insights:
    st.header("Financial Insights")
    st.write("Ask me about investing rules, strategies, and tips for personal finance management!")

    if "message" not in st.session_state:
        st.session_state.message = [
            {"role": "assistant", "content": "Hello! I'm your personal finance assistant. How can I help you today?"}
        ]

    for message in st.session_state.message:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if user_query := st.chat_input("Ask a financial question..."):
        with st.chat_message("user"):
            st.markdown(user_query)
        st.session_state.message.append({"role": "user", "content": user_query})


    
        with st.spinner("Thinking..."):
            ai_response = "Sorry, I couldn't generate a response."
            try:
                system_instruction = "Your are a helpful, encouraging personal finance assistant. Keep your answers clear, concise, and easy for a beginner to understand. Avoid using technical jargan."

                response = client.models.generate_content(
                    model='gemini-3.5-flash',
                    contents=user_query,
                    config={
                        "system_instruction": system_instruction,
                    }
                )
                ai_response = response.text
            except Exception as e:
                ai_response = f"Oops, I had trouble connecting to my brain. Error: {e}"
    
        with st.chat_message("assistant"):
            st.write(ai_response)
        st.session_state.message.append({"role": "assistant", "content": ai_response})

# Close Database IMPORTANT
conn.close()