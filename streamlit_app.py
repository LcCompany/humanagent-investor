import streamlit as st
import yfinance as yf
from datetime import datetime, timedelta
import requests
import json

def get_stock_data(ticker, period):
    if period == '1m':
        interval = '1m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)
    elif period == '2m':
        interval = '2m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)
    elif period == '5m':
        interval = '5m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)
    elif period == '15m':
        interval = '15m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=1)
    elif period == '30m':
        interval = '30m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
    elif period == '60m':
        interval = '60m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
    elif period == '90m':
        interval = '90m'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
    elif period == '1h':
        interval = '1h'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=7)
    elif period == '1d':
        interval = '1d'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
    elif period == '5d':
        interval = '1d'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
    elif period == '1wk':
        interval = '1wk'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365)
    elif period == '1mo':
        interval = '1mo'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365 * 3)
    elif period == '3mo':
        interval = '1mo'
        end_date = datetime.now().date()
        start_date = end_date - timedelta(days=365 * 3)
    else:
        st.error(f"Error: Invalid period '{period}'. Please select a valid period.")
        return None

    stock = yf.Ticker(ticker)
    hist_data = stock.history(start=start_date, end=end_date, interval=interval)
    return hist_data

def get_current_price(ticker, period):
    try:
        stock = yf.Ticker(ticker)
        if period == '1m':
            data = stock.history(period='1d', interval='1m')
        elif period == '2m':
            data = stock.history(period='1d', interval='2m')
        elif period == '5m':
            data = stock.history(period='1d', interval='5m')
        elif period == '15m':
            data = stock.history(period='1d', interval='15m')
        elif period == '30m':
            data = stock.history(period='7d', interval='30m')
        elif period == '60m':
            data = stock.history(period='7d', interval='60m')
        elif period == '90m':
            data = stock.history(period='7d', interval='90m')
        elif period == '1h':
            data = stock.history(period='7d', interval='1h')
        elif period in ['1d', '5d', '1wk']:
            data = stock.history(period='1y', interval=period)
        elif period in ['1mo', '3mo']:
            data = stock.history(period='3y', interval='1mo')
        else:
            st.error(f"Error: Invalid period '{period}'. Please select a valid period.")
            return None
        return data['Close'].iloc[-1]
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
- Insight into volume trends, time frames and their significance in confirming patterns.
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
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": 'claude-3-5-sonnet-20240620',
        "max_tokens": 4096,
        "temperature": 0.1,
        "system": system_prompt,
        "messages": messages,
    }

    st.write("Sending request to Anthropic API...")
    
    try:
        safe_data = {**data, "system": "REDACTED"}
        st.write("Request data:", json.dumps(safe_data, indent=2))
    except Exception as e:
        st.error(f"Error while trying to write request data: {str(e)}")
        st.write("Request data (raw):", {k: v if k != "system" else "REDACTED" for k, v in data.items()})

    try:
        response = requests.post("https://api.anthropic.com/v1/messages", headers={**headers, "x-api-key": api_key}, json=data)

        st.write(f"API Response Status Code: {response.status_code}")
        st.write("API Response Headers:", {k: v for k, v in response.headers.items() if k.lower() not in ["set-cookie", "authorization"]})

        if response.status_code != 200:
            st.error(f"API request failed with status code: {response.status_code}")
            return "Failed to generate analysis due to API error."

        try:
            response_json = response.json()
            safe_response = {k: v if k != "system" else "REDACTED" for k, v in response_json.items()}
            st.write("Full API Response:", json.dumps(safe_response, indent=2))

            if 'content' in response_json and len(response_json['content']) > 0:
                response_text = response_json['content'][0]['text']
            else:
                st.warning("Unexpected API response structure")
                response_text = "Unable to extract analysis from API response."
            
            return response_text
        except json.JSONDecodeError:
            st.error("Failed to decode API response as JSON")
            return "Failed to generate analysis due to invalid API response."
    except Exception as e:
        st.error(f"An error occurred while making the API request: {type(e).__name__}")
        return "Failed to generate analysis due to an unexpected error."

def main():
    st.title("Stock Analysis App")
    api_key = st.secrets["ANTHROPIC_API_KEY"]

    ticker = st.text_input("Enter the stock ticker to analyze, exactly as it appears on [Yahoo Finance](https://finance.yahoo.com/):")

    period_options = {
        '1m': '1 minute',
        '5m': '5 minutes',
        '15m': '15 minutes',
        '30m': '30 minutes',
        '1h': '1 hour',
        '1d': '1 day',
        '5d': '5 days',
        '1wk': '1 week',
        '1mo': '1 month'
    }

    period = st.selectbox("Select the timeframe for the analysis:", list(period_options.values()), index=5)

    if st.button("Analyze"):
        if ticker:
            selected_period = list(period_options.keys())[list(period_options.values()).index(period)]
            hist_data = get_stock_data(ticker, selected_period)
            if hist_data is not None:
                current_price = get_current_price(ticker, selected_period)
                if current_price is not None:
                    st.write("Generating analysis...")
                    analysis = generate_analysis(ticker, hist_data, current_price, api_key)
                    st.subheader(f"Analysis for {ticker} ({period}):")
                    st.write(analysis)
            else:
                st.error(f"Failed to fetch historical data for {ticker}")
        else:
            st.warning("Please enter a stock ticker.")

if __name__ == "__main__":
    main()
