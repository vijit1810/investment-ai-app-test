
import streamlit as st
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier
import json

@st.cache_data
def generate_and_train_model():
    data = []
    risk_levels = ['Low', 'Medium', 'High']
    goals = ['Wealth Creation', 'Retirement', 'Education', 'Travel']
    horizons = ['1-3 yrs', '3-5 yrs', '5+ yrs']

    for _ in range(500):
        age = random.randint(22, 60)
        income = random.randint(20000, 150000)
        savings = random.randint(5000, 500000)
        risk = random.choice(risk_levels)
        goal = random.choice(goals)
        horizon = random.choice(horizons)

        if risk == 'High' and income > 60000 and horizon == '5+ yrs':
            category = 'Aggressive'
        elif risk == 'Medium' and horizon in ['3-5 yrs', '5+ yrs']:
            category = 'Balanced'
        else:
            category = 'Conservative'

        data.append([age, income, savings, risk, goal, horizon, category])

    df = pd.DataFrame(data, columns=['Age', 'Income', 'Savings', 'Risk', 'Goal', 'Horizon', 'Category'])
    df['Risk'] = df['Risk'].map({'Low': 0, 'Medium': 1, 'High': 2})
    df['Goal'] = df['Goal'].map({'Education': 0, 'Travel': 1, 'Retirement': 2, 'Wealth Creation': 3})
    df['Horizon'] = df['Horizon'].map({'1-3 yrs': 0, '3-5 yrs': 1, '5+ yrs': 2})
    df['Category'] = df['Category'].map({'Conservative': 0, 'Balanced': 1, 'Aggressive': 2})

    X = df.drop('Category', axis=1)
    y = df['Category']
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    return model

# Load fund data
fund_data = json.loads("""{
    "Conservative": [
        {
            "name": "HDFC Short Term Debt Fund",
            "returns": "1Y: 7.25%, 3Y: 5.80%",
            "rating": "4\u2605",
            "risk": "Low",
            "etmoney": "https://www.etmoney.com/mutual-funds/hdfc-short-term-debt-fund-direct-plan-growth/15718",
            "groww": "https://groww.in/mutual-funds/hdfc-short-term-opportunities-fund-direct-growth"
        },
        {
            "name": "ICICI Prudential Corporate Bond Fund",
            "returns": "1Y: 7.12%, 3Y: 6.23%",
            "rating": "4\u2605",
            "risk": "Moderate",
            "etmoney": "https://www.etmoney.com/mutual-funds/icici-prudential-corporate-bond-fund-direct-plan-growth/15135",
            "groww": "https://groww.in/mutual-funds/icici-prudential-corporate-bond-fund-direct-growth"
        },
        {
            "name": "SBI Magnum Low Duration Fund",
            "returns": "1Y: 6.84%, 3Y: 5.61%",
            "rating": "3\u2605",
            "risk": "Low",
            "etmoney": "https://www.etmoney.com/mutual-funds/sbi-magnum-low-duration-fund-direct-plan-growth/15883",
            "groww": "https://groww.in/mutual-funds/sbi-ultra-short-term-debt-fund-direct-growth"
        }
    ],
    "Balanced": [
        {
            "name": "Mirae Asset Hybrid Equity Fund",
            "returns": "1Y: 16.75%, 3Y: 12.89%",
            "rating": "5\u2605",
            "risk": "Moderately High",
            "etmoney": "https://www.etmoney.com/mutual-funds/mirae-asset-hybrid-equity-fund-direct-plan-growth/val0s",
            "groww": "https://groww.in/mutual-funds/mirae-asset-hybrid-equity-fund-direct-growth"
        },
        {
            "name": "HDFC Balanced Advantage Fund",
            "returns": "1Y: 13.42%, 3Y: 11.27%",
            "rating": "4\u2605",
            "risk": "Moderate",
            "etmoney": "https://www.etmoney.com/mutual-funds/hdfc-balanced-advantage-fund-direct-plan-growth/val74",
            "groww": "https://groww.in/mutual-funds/hdfc-balanced-advantage-fund-direct-growth"
        },
        {
            "name": "ICICI Prudential Multi-Asset Fund",
            "returns": "1Y: 18.05%, 3Y: 14.43%",
            "rating": "4\u2605",
            "risk": "Moderately High",
            "etmoney": "https://www.etmoney.com/mutual-funds/icici-prudential-multi-asset-fund-direct-plan-growth/val7t",
            "groww": "https://groww.in/mutual-funds/icici-prudential-multi-asset-fund-direct-growth"
        }
    ],
    "Aggressive": [
        {
            "name": "Parag Parikh Flexi Cap Fund",
            "returns": "1Y: 22.5%, 3Y: 19.2%",
            "rating": "5\u2605",
            "risk": "Moderately High",
            "etmoney": "https://www.etmoney.com/mutual-funds/parag-parikh-flexi-cap-fund-direct-plan-growth/valk2",
            "groww": "https://groww.in/mutual-funds/parag-parikh-flexi-cap-fund-direct-growth"
        },
        {
            "name": "Quant Small Cap Fund",
            "returns": "1Y: 35.6%, 3Y: 37.8%",
            "rating": "5\u2605",
            "risk": "High",
            "etmoney": "https://www.etmoney.com/mutual-funds/quant-small-cap-fund-direct-plan-growth/valzd",
            "groww": "https://groww.in/mutual-funds/quant-small-cap-fund-direct-growth"
        },
        {
            "name": "Axis Midcap Fund",
            "returns": "1Y: 26.3%, 3Y: 20.8%",
            "rating": "4\u2605",
            "risk": "High",
            "etmoney": "https://www.etmoney.com/mutual-funds/axis-midcap-fund-direct-plan-growth/val77",
            "groww": "https://groww.in/mutual-funds/axis-midcap-fund-direct-growth"
        }
    ]
}""")

def recommend_funds(category):
    return fund_data.get(category, [])

model = generate_and_train_model()

st.title("AI-Based Mutual Fund Recommendation")

st.subheader("Enter your investment profile:")
age = st.slider("Age", 18, 65, 30)
income = st.number_input("Monthly Income (INR)", 10000, 200000, step=1000)
savings = st.number_input("Current Savings (INR)", 0, 1000000, step=10000)
risk = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])
goal = st.selectbox("Goal", ["Wealth Creation", "Retirement", "Education", "Travel"])
horizon = st.selectbox("Investment Horizon", ["1-3 yrs", "3-5 yrs", "5+ yrs"])

if st.button("Get Recommendation"):
    input_data = {
        "Age": age,
        "Income": income,
        "Savings": savings,
        "Risk": {"Low": 0, "Medium": 1, "High": 2}[risk],
        "Goal": {"Education": 0, "Travel": 1, "Retirement": 2, "Wealth Creation": 3}[goal],
        "Horizon": {"1-3 yrs": 0, "3-5 yrs": 1, "5+ yrs": 2}[horizon]
    }

    df_input = pd.DataFrame([input_data])
    prediction = model.predict(df_input)[0]
    labels = ['Conservative', 'Balanced', 'Aggressive']
    category = labels[prediction]

    st.success(f"You're a {category} investor!")

    funds = recommend_funds(category)
    st.markdown("### Top Fund Recommendations:")

    for fund in funds:
        st.markdown(f"**{fund['name']}**")
        st.markdown(f"- Returns: {fund['returns']}")
        st.markdown(f"- Rating: {fund['rating']} | Risk: {fund['risk']}")
        st.markdown(f'<a href="{fund["etmoney"]}" target="_blank"><button style="background-color:#2E8B57;color:white;border:none;padding:8px 16px;margin-top:5px;border-radius:5px;">Explore on ETMoney</button></a>', unsafe_allow_html=True)
        st.markdown(f'[Invest via Groww]({fund["groww"]})')
        st.markdown("---")
