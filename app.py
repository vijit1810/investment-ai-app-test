
import streamlit as st
import pandas as pd
import random
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from fpdf import FPDF
import smtplib
from email.message import EmailMessage
import os

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

def generate_pdf(data_dict, category, portfolio, filename):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Your Personalized Investment Plan", ln=True, align='C')
    pdf.ln(10)
    for key, value in data_dict.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt=f"Recommended Category: {category}", ln=True)
    pdf.ln(5)
    pdf.cell(200, 10, txt="Suggested Mutual Funds:", ln=True)
    for asset, funds in portfolio.items():
        pdf.cell(200, 10, txt=f"{asset}: {', '.join(funds)}", ln=True)
    pdf.output(filename)

def send_email(recipient, filepath):
    sender = os.environ.get("investai.bot@gmail.com")
    app_password = os.environ.get("Reebok@1810")
    msg = EmailMessage()
    msg['Subject'] = 'Your Personalized Mutual Fund Investment Plan'
    msg['From'] = sender
    msg['To'] = recipient
    msg.set_content('Hi there! Please find your personalized mutual fund recommendation PDF attached.')
    with open(filepath, 'rb') as f:
        file_data = f.read()
        msg.add_attachment(file_data, maintype='application', subtype='pdf', filename=os.path.basename(filepath))
    with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
        smtp.login(sender, app_password)
        smtp.send_message(msg)

model = generate_and_train_model()
st.title("AI-Based Mutual Fund Recommendation + Email Report")
st.subheader("Enter your investment profile:")
age = st.slider("Age", 18, 65, 30)
income = st.number_input("Monthly Income (INR)", 10000, 200000, step=1000)
savings = st.number_input("Current Savings (INR)", 0, 1000000, step=10000)
risk = st.selectbox("Risk Appetite", ["Low", "Medium", "High"])
goal = st.selectbox("Goal", ["Wealth Creation", "Retirement", "Education", "Travel"])
horizon = st.selectbox("Investment Horizon", ["1-3 yrs", "3-5 yrs", "5+ yrs"])
email = st.text_input("Enter your email to receive PDF report:")

if st.button("Get My Recommendation + Email PDF"):
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
            'Conservative': {'Equity': ['Kotak Equity Arbitrage'], 'Debt': ['HDFC Short Term Debt Fund'], 'Gold': ['SBI Gold Fund']},
            'Balanced': {'Equity': ['Axis Bluechip Fund', 'Mirae Asset Hybrid Equity'], 'Debt': ['ICICI Prudential Short Term Fund'], 'Gold': ['Nippon India Gold Savings']},
            'Aggressive': {'Equity': ['Parag Parikh Flexi Cap', 'Mirae Asset Large Cap'], 'Debt': ['UTI Credit Risk Fund'], 'Gold': ['HDFC Gold Fund']}
        }
        return portfolios[category]

    portfolio = recommend_portfolio(category)
    st.success(f"You're a {category} investor!")
    pdf_filename = "investment_plan.pdf"
    generate_pdf(input_data, category, portfolio, pdf_filename)
    st.success("PDF generated successfully.")
    if email:
        try:
            send_email(email, pdf_filename)
            st.success(f"PDF sent to {email}")
        except Exception as e:
            st.error(f"Failed to send email: {e}")
    else:
        st.warning("Please enter a valid email.")
