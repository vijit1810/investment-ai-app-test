
import streamlit as st
import pandas as pd
import random
from sklearn.ensemble import RandomForestClassifier

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

    def recommend_portfolio(category):
        portfolios = {
            'Conservative': {'Equity': ['Kotak Equity Arbitrage']},
            'Balanced': {'Equity': ['Axis Bluechip Fund']},
            'Aggressive': {'Equity': ['Parag Parikh Flexi Cap']}
        }
        return portfolios[category]

    fund_info = {
        "Kotak Equity Arbitrage": {"returns": "1Y: 6.2%, 3Y: 5.8%", "rating": "3★", "risk": "Low",
            "etmoney": "https://www.etmoney.com/mutual-funds/kotak-equity-arbitrage-fund-direct-plan-growth/valf4",
            "groww": "https://groww.in/mutual-funds/kotak-equity-arbitrage-fund-direct-growth"},
        "Axis Bluechip Fund": {"returns": "1Y: 18.2%, 3Y: 14.6%", "rating": "4.5★", "risk": "Moderate",
            "etmoney": "https://www.etmoney.com/mutual-funds/axis-bluechip-fund-direct-plan-growth/val74",
            "groww": "https://groww.in/mutual-funds/axis-bluechip-fund-direct-growth"},
        "Parag Parikh Flexi Cap": {"returns": "1Y: 22.5%, 3Y: 19.2%", "rating": "5★", "risk": "Moderately High",
            "etmoney": "https://www.etmoney.com/mutual-funds/parag-parikh-flexi-cap-fund-direct-plan-growth/valk2",
            "groww": "https://groww.in/mutual-funds/parag-parikh-flexi-cap-fund-direct-growth"}
    }

    portfolio = recommend_portfolio(category)
    
    st.markdown("### Recommended Mutual Funds:")
    for asset, funds in portfolio.items():
        st.markdown(f"**{asset}**")
        for fund in funds:
            info = fund_info.get(fund)
            st.markdown(f"- **{fund}**")
            if info:
                st.markdown(f"  - Returns: {info['returns']}")
                st.markdown(f"  - Rating: {info['rating']} | Risk: {info['risk']}")
                etmoney_link = info['etmoney']
                groww_link = info['groww']
                st.markdown(f"[View on ETMoney]({etmoney_link}) | [Invest via Groww]({groww_link})")
                st.markdown(f'<a href="{etmoney_link}" target="_blank"><button style="background-color:#2E8B57;color:white;border:none;padding:8px 16px;margin-top:5px;border-radius:5px;">Explore on ETMoney</button></a>', unsafe_allow_html=True)
            st.markdown("---")

