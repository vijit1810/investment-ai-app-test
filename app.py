
import streamlit as st
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Step 1: Generate synthetic data
@st.cache_data
def generate_and_train_model():
    data = []
    risk_levels = ['Low', 'Medium', 'High']
    goals = ['Wealth Creation', 'Retirement', 'Education', 'Travel']
    horizons = ['1-3 yrs', '3-5 yrs', '5+ yrs']

    for _ in range(500):
        age = random.randint(22, 60)
        income = random.randint(20000, 250000)
        savings = random.randint(5000, 5000000)
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

    # Encode
    df['Risk'] = df['Risk'].map({'Low': 0, 'Medium': 1, 'High': 2})
    df['Goal'] = df['Goal'].map({'Education': 0, 'Travel': 1, 'Retirement': 2, 'Wealth Creation': 3})
    df['Horizon'] = df['Horizon'].map({'1-3 yrs': 0, '3-5 yrs': 1, '5+ yrs': 2})
    df['Category'] = df['Category'].map({'Conservative': 0, 'Balanced': 1, 'Aggressive': 2})

    X = df.drop('Category', axis=1)
    y = df['Category']

    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)

    return model

# Step 2: Load trained model
model = generate_and_train_model()

# Step 3: Streamlit input
st.title("AI-Based Mutual Fund Recommendation")

st.subheader("Enter your investment profile:")

age = st.slider("Age", 18, 65, 30)
income = st.number_input("Monthly Income (INR)", 10000, 300000, step=3000)
savings = st.number_input("Current Savings (INR)", 0, 5000000, step=20000)
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

    def recommend_portfolio(category):
        portfolios = {
            'Conservative': {
                'Equity': [('Axis Bluechip Fund',50)],
                'Debt': [('HDFC Short Term Debt Fund'),30],
                'Gold': [('SBI Gold Fund'),20]
            },
            'Balanced': {
                'Equity': [('HDFC Mid Cap Opportunities Fund',60)],
                'Debt': [('ICICI Prudential Short Term Fund',20)],
                'Gold': [('Nippon India Gold Savings',20)]
            },
            'Aggressive': {
                'Equity': [('TATA Small Cap Fund',70)],
                'Debt': [('UTI Credit Risk Fund',15)],
                'Gold': [('HDFC Gold Fund',15)]
            }
        }
        return portfolios[category]

    portfolio = recommend_portfolio(category)

    st.success(f"You're a {category} investor!")
    st.markdown("### Recommended Portfolio:")
    for asset, funds in portfolio.items():
        st.markdown(f"**{asset}**: {', '.join(funds)}")
