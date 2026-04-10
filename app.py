import streamlit as st
import requests
from bs4 import BeautifulSoup

st.set_page_config(page_title="Eiendom Dashboard", layout="wide")

st.title("📊 Eiendom Investeringsanalyse")

# --- Input ---
url = st.text_input("Lim inn FINN-lenke")

st.subheader("Manuelle input (overstyr ved behov)")
price = st.number_input("Pris (kr)", value=3000000)
rent = st.number_input("Årsleige (kr)", value=500000)
ltv = st.slider("Belåning (%)", 0, 100, 70) / 100
interest = st.slider("Rente (%)", 0.0, 10.0, 5.0) / 100
vacancy = st.slider("Vakans (%)", 0, 50, 10) / 100
exit_yield = st.slider("Exit yield (%)", 1.0, 15.0, 8.0) / 100

# --- Default cost rule ---
operating_costs = rent * 0.30

# --- Calculations ---
net_income = rent * (1 - vacancy) - operating_costs
net_yield = net_income / price
loan = price * ltv
interest_cost = loan * interest
cash_flow = net_income - interest_cost

dscr = net_income / interest_cost if interest_cost > 0 else 0

# --- Score ---
def score_yield(y):
    if y > 0.10: return 100
    elif y > 0.08: return 80
    elif y > 0.06: return 60
    elif y > 0.04: return 40
    else: return 20

def score_total():
    s1 = score_yield(net_yield)
    s2 = 100 if cash_flow > 0 else 20
    s3 = 100 if dscr > 1.3 else 40
    total = s1*0.4 + s2*0.3 + s3*0.3
    return round(total,1)

score = score_total()

# --- Display ---
col1, col2, col3 = st.columns(3)

col1.metric("Nettoyield", f"{net_yield*100:.2f}%")
col2.metric("Cash flow", f"{cash_flow:,.0f} kr")
col3.metric("DSCR", f"{dscr:.2f}")

st.subheader("Investeringsscore")
st.write(f"## {score} / 100")

if score > 80:
    st.success("KJØP")
elif score > 65:
    st.warning("VURDER NÆRARE")
else:
    st.error("IKKJE KJØP")
