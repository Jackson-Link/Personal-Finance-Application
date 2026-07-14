import streamlit as st

st.title("Personal Finance Dashboard")

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

col3, col4, col5 = st.columns(3)

with col3:
    st.metric(label = "Total Savings", value = f"${saving_amount:,.2f}")

with col4:
    st.metric(label = "Checking Account", value = f"${checking_amount:,.2f}")

with col5:
    st.metric(label = "Leftover Cash", value = f"${leftover_amount:,.2f}")