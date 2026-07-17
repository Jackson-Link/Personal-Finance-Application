import streamlit as st
from dotenv import load_dotenv
import os
load_dotenv()  # Load environment variables from .env file
from google.genai import Client
from google.genai.types import HttpOptions
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

client = Client(http_options=HttpOptions(timeout=15.0))

st.title("Personal Finance Dashboard")

# Creating different tabs for the dashboard
tab_planner, tab_history, tab_insights = st.tabs(["Budget Planner", "Budget History", "Insights"])

with tab_planner:
    st.header("Allocate your income")
    # Create side-by-side columns
    col1, col2, col3 = st.columns(3)

    with col1:
        income = st.slider("Monthly Income:", 0, 10000, 2000)

    with col2:
        saving_pct = st.slider("Saving Percentage:", 0, 100, 20)

    with col3:
        checking_pct = st.slider("Checking Account Percentage:", 0, 100, 20)

    if saving_pct + checking_pct > 100:
        st.error("The sum of saving and checking percentages cannot exceed 100%. Please adjust the sliders.")
        st.stop()  # Stop execution if the condition is met
    elif saving_pct + checking_pct < 100:
        st.info("The sum of saving and checking percentages is less than 100%. The leftover cash will be calculated accordingly.")
    else:
        st.success("The sum of saving and checking percentages is exactly 100%. No leftover cash will be available.")

    # Budget math
    saving_amount = income * (saving_pct / 100)
    checking_amount = income * (checking_pct / 100)
    leftover_amount = income - saving_amount - checking_amount

    st.markdown("---") # Visual divider line
    st.header("Financial Breakdown")

    # Data Table
    chart_data = pd.DataFrame(
        {
            "Account": ["Saving", "Checking", "Leftover Cash"],
            "Amount": [saving_amount, checking_amount, leftover_amount]
        }
    )
    chart_data = chart_data.set_index("Account")
    st.bar_chart(chart_data)

    if st.button("Save Transaction History"):
        # Save to SQL db
        cursor.execute("""
        INSERT INTO allocations (income, percent_allocated, leftover_cash) 
        VALUES (?, ?, ?)
        """, (income, saving_pct + checking_pct, leftover_amount))

        conn.commit()
        st.success("Transaction history saved successfully!")
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