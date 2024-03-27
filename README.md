# 📈 Stock Analysis with AI

This Python script leverages the power of AI to provide insightful technical analysis for stocks. By utilizing historical price data from Yahoo Finance and the advanced language model, Claude, from Anthropic, the script generates comprehensive trading signals and risk assessments.

## Features

- Retrieves historical price data for a specified stock ticker and time period
- Fetches the current price of the stock
- Applies technical analysis indicators and patterns to identify buy or sell signals
- Generates a detailed analysis report with confidence levels and risk factors
- Utilizes the Claude AI model for advanced natural language processing and analysis

## Prerequisites

To run this script, you need to have the following dependencies installed:

- Python 3.x
- `yfinance` library
- `requests` library
- `beautifulsoup4` library
- `ast` library
- `json` library

You also need to have an API key from Anthropic to access the Claude AI model. Replace `ANTHROPIC_API_KEY` in the script with your actual API key.

## Usage

1. Clone the repository or download the script file.

2. Install the required dependencies by running the following command:
   ```
   pip install yfinance requests beautifulsoup4
   ```

3. Open the script file and replace `ANTHROPIC_API_KEY` with your actual Anthropic API key.

4. Run the script using the following command:
   ```
   python stock_analysis.py
   ```

5. When prompted, enter the stock ticker exactly as it appears on Yahoo Finance.

6. The script will retrieve the historical price data, fetch the current price, and generate an analysis report using the Claude AI model.

7. The analysis report will be displayed in the console, providing insights into potential buy or sell signals, confidence levels, and risk factors.

## Example

Here's an example of running the script:

```
Enter the stock ticker to analyze (exactly as it appears on Yahoo Finance): AAPL

Analysis for AAPL:
Based on the historical price data and current price for AAPL, the technical analysis suggests a potential sell signal with a confidence level of 65%.

The stock has been trading in a narrow range over the past few days, with a slight downward trend. The current price is near the lower end of the range, indicating a potential breakdown.

The moving averages show a bearish crossover, with the 50-day moving average crossing below the 200-day moving average, further confirming the bearish sentiment.

However, it's important to note that the stock has shown resilience in the past, bouncing back from similar levels. The RSI is approaching the oversold territory, which could trigger a short-term reversal.

Risk factors to consider include the overall market sentiment, upcoming earnings reports, and any company-specific news that may impact the stock price.

As with any trading decision, it's crucial to conduct thorough research, consider your risk tolerance, and have a well-defined trading plan.
```

## Data Passed to the AI Model

The script passes the following data to the Claude AI model:

- Historical price data for the specified stock ticker and time period
- Current price of the stock
- System prompt defining the role, skills, knowledge, parameters, and responsibilities of the AI model

The historical price data and current price are retrieved using the `yfinance` library and passed as part of the user message to the AI model. The system prompt provides the necessary context and instructions for the AI model to perform the technical analysis.

## Disclaimer

This script is for educational and informational purposes only. It does not constitute financial advice. Always conduct your own research and consult with a financial professional before making any trading decisions. The developers of this script are not responsible for any financial losses incurred by using the information provided by the AI model.

## License

This project is licensed under the [MIT License](LICENSE).