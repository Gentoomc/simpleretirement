import streamlit as st
import pandas as pd

def calculate_retirement_savings(current_age, current_savings, retirement_age, annual_retirement_income, balance_growth_rate, inflation_rate, life_expectancy):
    data = []
    balance = current_savings

    for year in range(life_expectancy - current_age + 1):
        age = current_age + year
        amount_withdrawn_today = 0
        amount_withdrawn_actual = 0

        if age >= retirement_age:
            amount_withdrawn_today = annual_retirement_income
            amount_withdrawn_actual = annual_retirement_income * (1 + inflation_rate) ** (age - retirement_age)

        balance_start = balance
        balance_end = max(balance * (1 + balance_growth_rate) - amount_withdrawn_actual, 0)
        balance = balance_end

        data.append([year, age, balance_start, amount_withdrawn_today, amount_withdrawn_actual, balance_growth_rate, inflation_rate, balance_end])

    df = pd.DataFrame(data, columns=['Year', 'Age', 'Balance at Start of Year', 'Amount Withdrawn (Today\'s Dollars)',
                                      'Amount Withdrawn (Actual)', 'Balance Growth Rate', 'Inflation Rate', 'Balance at End of Year'])
    df['Balance at Start of Year'] = df['Balance at Start of Year'].apply(lambda x: '${:,.2f}'.format(x))
    df['Amount Withdrawn (Today\'s Dollars)'] = df['Amount Withdrawn (Today\'s Dollars)'].apply(lambda x: '${:,.2f}'.format(x))
    df['Amount Withdrawn (Actual)'] = df['Amount Withdrawn (Actual)'].apply(lambda x: '${:,.2f}'.format(x))
    df['Balance Growth Rate'] = df['Balance Growth Rate'].apply(lambda x: '{:.2%}'.format(x))
    df['Inflation Rate'] = df['Inflation Rate'].apply(lambda x: '{:.2%}'.format(x))
    df['Balance at End of Year'] = df['Balance at End of Year'].apply(lambda x: '${:,.2f}'.format(x))

    return df

st.title('Retirement Savings Calculator')

current_age = st.number_input('Current Age', min_value=1, max_value=100, value=30)
current_savings = st.number_input('Current Savings', min_value=0, value=50000)
retirement_age = st.number_input('Desired Retirement Age', min_value=current_age, max_value=100, value=65)
annual_retirement_income = st.number_input('Desired Annual Retirement Income (in today\'s dollars)', min_value=0, value=40000)
balance_growth_rate = st.slider('Balance Growth Rate per Year', min_value=0.0, max_value=0.2, value=0.07, step=0.01)
inflation_rate = st.slider('Inflation Rate per Year', min_value=0.0, max_value=0.1, value=0.025, step=0.005)
life_expectancy = st.slider('Expected Life Expectancy', min_value=current_age, max_value=120, value=90)

if st.button('Calculate'):
    df = calculate_retirement_savings(current_age, current_savings, retirement_age, annual_retirement_income, balance_growth_rate, inflation_rate, life_expectancy)
    st.write(df.to_html(index=False), unsafe_allow_html=True)