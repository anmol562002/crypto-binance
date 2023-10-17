from decouple import config
import ccxt
import streamlit as st
import pandas as pd
import plotly.express as px


# Load API key and secret key from .env file
binance_api_key = config('BINANCE_API_KEY')
binance_api_secret = config('BINANCE_API_SECRET')

# Initialize the Binance API client with your API key and secret key
binance = ccxt.binance({
    'enableRateLimit': True,
    'rateLimit': 1200,
    'apiKey': binance_api_key,
    'secret': binance_api_secret,
})

# Define the symbols for BTC, ETH, XRP, MATIC, and other coins
symbols = [
    'BTC/USDT', 'ETH/USDT', 'XRP/USDT', 'MATIC/USDT', 'HOOK/USDT', 'LOKA/USDT', 'EDU/USDT', 'ARKM/USDT', 'ALPINE/USDT'
]

# Initialize an empty DataFrame to store the combined data
combined_data = pd.DataFrame()

# Fetch historical price data for each symbol
for symbol in symbols:
    ohlcv = binance.fetch_ohlcv(symbol, timeframe='1d', limit=365)
    df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['symbol'] = symbol
    combined_data = pd.concat([combined_data, df])

# Set Streamlit app title
st.title('Cryptocurrency Price, Listing Price, and 1-Year Return (Last 1 Year)')

# Display a selection box for choosing the cryptocurrency
selected_symbol = st.selectbox('Select a cryptocurrency', symbols)

# Filter the data based on the selected cryptocurrency
filtered_data = combined_data[combined_data['symbol'] == selected_symbol]

# Display the price chart
st.plotly_chart(px.line(filtered_data, x='timestamp', y='close', title=f'{selected_symbol} Price (Last 1 Year)'))

# Get listing price and current price
listing_price = filtered_data['open'].iloc[0]
current_price = filtered_data['close'].iloc[-1]

# Calculate 1-year return
one_year_return = ((current_price - listing_price) / listing_price) * 100

# Create a table to display listing price, current price, and 1-year return
roi_data = {
    'Metric': ['Listing Price', 'Current Price', '1-Year Return'],
    'Value': [f'${listing_price:.2f}', f'${current_price:.2f}', f'{one_year_return:.2f}%']
}
st.table(pd.DataFrame(roi_data))
