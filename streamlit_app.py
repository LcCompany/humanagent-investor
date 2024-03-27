import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import requests
from bs4 import BeautifulSoup
import ast
import json

def get_stock_data(ticker, years):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=years*365)
    stock = yf.Ticker(ticker)
    # Retrieve historical price data
    hist_data = stock.history(start=start_date, end=end_date)
    return hist_data

def get_current_price(ticker):
    try:
        stock = yf.Ticker(ticker)
        data = stock.history(period='1d', interval='1m')
        return data['Close'].iloc[-1]  # Use iloc instead of square bracket indexing
    except IndexError:
        st.error(f"Error: No data found for ticker '{ticker}'. Please ensure the ticker is entered exactly as it appears on Yahoo Finance.")
        return None

def generate_analysis(ticker, hist_data, current_price, api_key):
    system_prompt = f"""<role_definition>
Act as a technical trade analyzer, specializing in the interpretation of price graphs for financial assets.
</role_definition>
<skill_alignment>
- Expertise in analyzing financial data and identifying patterns.
- Proficiency in technical analysis indicators such as moving averages, RSI, MACD, and Bollinger Bands.
- Capability to assess market sentiment and trends from data.
- Skilled in risk assessment and management strategies.
- Ability to articulate analysis and recommendations clearly, with a specified confidence level.
</skill_alignment>
<knowledge_application>
- Deep understanding of financial markets and the factors influencing price movements.
- Familiarity with various data types and their implications.
- Insight into volume trends and their significance in confirming patterns.
- Comprehensive knowledge of historical price behavior and statistical analysis for prediction accuracy.
</knowledge_application>
<parameter_customization>
Your heightened parameters are:
"analysis_depth": "high",
"confidence_reporting": "enabled",
"risk_assessment_sensitivity": "moderate",
"market_sentiment_analysis": "integrated"
</parameter_customization>
<role_based_parameters>
- "pattern_recognition_accuracy": "enhanced",
- "indicator_sensitivity": "customized_for_volatility",
- "historical_data_reliance": "balanced",
- "prediction_time_frame": "short_to_medium_term"
</role_based_parameters>
<core_responsibilities>
- Analyze the provided price graph using technical indicators and patterns.
- Determine whether the graph presents a buy or sell signal, based on the analysis.
- Report the level of confidence in the analysis, considering the current market conditions and historical data accuracy.
- Offer insights into potential risk factors and suggest mitigation strategies if applicable.
</core_responsibilities>
<role_summary>
Your role is to meticulously examine financial data, apply technical analysis principles, and deliver actionable trading signals with a clear indication of confidence level in percentages. This includes evaluating the strength of buy or sell signals and providing a reasoned analysis that supports decision-making in trading activities.
</role_summary>
<task>
Given the historical price data and the current price for {ticker}, apply the above role definition, skill alignment, knowledge application, parameter customization, and core responsibilities to analyze the data. Start the analysis with the most recent date in the dataset and consider the current price. Use the defined technical analysis indicators to determine buy or sell signals and articulate your analysis and recommendation clearly, including a confidence level and potential risk factors.
</task>"""
    messages = [
    {"role": "user", "content": f"Historical price data for {ticker}:\n{hist_data.to_string()}\n\nCurrent price: {current_price}"},
    ]
    headers = {
        "x-api-key": api_key,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": 'claude-3-haiku-20240307',  #claude-3-opus-20240229
        "max_tokens": 4096,
        "temperature": 0.1,
        "system": system_prompt,
        "messages": messages,
    }
    response = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=data)
    response_text = response.json()['content'][0]['text']
    return response_text

def main():
    st.title("Stock Analysis App")

    api_key = st.text_input("Enter your Anthropic API key:", type="password")
    ticker = st.text_input("Enter the stock ticker to analyze, exactly as it appears on [Yahoo Finance](https://finance.yahoo.com/):")
    years = 1

    if st.button("Analyze"):
        if api_key and ticker:
            # Get stock data
            hist_data = get_stock_data(ticker, years)
            current_price = get_current_price(ticker)
            if current_price is not None:
                # Generate analysis
                analysis = generate_analysis(ticker, hist_data, current_price, api_key)
                st.subheader(f"Analysis for {ticker}:")
                st.write(analysis)
            else:
                st.error("Unable to generate analysis due to missing data.")
        else:
            if not api_key:
                st.warning("Please enter your Anthropic API key.")
            if not ticker:
                st.warning("Please enter a stock ticker.")

if __name__ == "__main__":
    main()
    #endgame