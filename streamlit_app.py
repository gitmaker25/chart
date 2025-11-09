import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf

# Page configuration
st.set_page_config(
    page_title="Indian Market Chart Analyzer",
    page_icon="📈",
    layout="wide"
)

# Title and description
st.title("🇮🇳 Indian Market Chart Analyzer")
st.markdown("Comprehensive technical analysis for Indian stocks")

# Sidebar for navigation
st.sidebar.title("Navigation")
page = st.sidebar.selectbox(
    "Choose a page:",
    ["Market Overview", "Stock Analysis", "Technical Scanner", "Learning Center"]
)

# Sample data function (replace with real API later)
def get_sample_data():
    dates = pd.date_range(start='2024-01-01', end=datetime.now(), freq='D')
    data = pd.DataFrame({
        'Date': dates,
        'Open': np.random.normal(100, 10, len(dates)),
        'High': np.random.normal(105, 10, len(dates)),
        'Low': np.random.normal(95, 10, len(dates)),
        'Close': np.random.normal(102, 10, len(dates)),
        'Volume': np.random.randint(100000, 1000000, len(dates))
    })
    return data

if page == "Market Overview":
    st.header("Market Overview")
    
    # Market indices
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("NIFTY 50", "22,000", "+1.5%")
    with col2:
        st.metric("SENSEX", "73,500", "+1.2%")
    with col3:
        st.metric("BANK NIFTY", "48,000", "+2.1%")
    
    # Sample chart
    data = get_sample_data()
    fig = go.Figure(data=[go.Candlestick(
        x=data['Date'],
        open=data['Open'],
        high=data['High'],
        low=data['Low'],
        close=data['Close']
    )])
    st.plotly_chart(fig, use_container_width=True)

elif page == "Stock Analysis":
    st.header("Stock Analysis")
    
    # Stock selector
    stock_symbol = st.text_input("Enter Stock Symbol (e.g., RELIANCE.NS, TCS.NS):", "RELIANCE.NS")
    
    if stock_symbol:
        try:
            # Get real data from Yahoo Finance
            stock = yf.Ticker(stock_symbol)
            hist = stock.history(period="6mo")
            
            if not hist.empty:
                # Display basic info
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Current Price", f"₹{hist['Close'][-1]:.2f}")
                with col2:
                    change = hist['Close'][-1] - hist['Close'][-2]
                    st.metric("Change", f"₹{change:.2f}")
                with col3:
                    st.metric("Volume", f"{hist['Volume'][-1]:,}")
                
                # Candlestick chart
                fig = go.Figure(data=[go.Candlestick(
                    x=hist.index,
                    open=hist['Open'],
                    high=hist['High'],
                    low=hist['Low'],
                    close=hist['Close'],
                    name=stock_symbol
                )])
                fig.update_layout(title=f"{stock_symbol} Price Chart")
                st.plotly_chart(fig, use_container_width=True)
                
                # Technical indicators
                st.subheader("Technical Indicators")
                
                # Calculate simple moving averages
                hist['SMA_20'] = hist['Close'].rolling(window=20).mean()
                hist['SMA_50'] = hist['Close'].rolling(window=50).mean()
                
                fig_indicators = go.Figure()
                fig_indicators.add_trace(go.Scatter(x=hist.index, y=hist['Close'], name='Close'))
                fig_indicators.add_trace(go.Scatter(x=hist.index, y=hist['SMA_20'], name='SMA 20'))
                fig_indicators.add_trace(go.Scatter(x=hist.index, y=hist['SMA_50'], name='SMA 50'))
                fig_indicators.update_layout(title="Moving Averages")
                st.plotly_chart(fig_indicators, use_container_width=True)
                
            else:
                st.error("No data found for this symbol")
                
        except Exception as e:
            st.error(f"Error fetching data: {e}")

elif page == "Technical Scanner":
    st.header("Technical Scanner")
    st.info("This feature will scan stocks based on technical criteria")
    
    # Scanner criteria
    st.subheader("Scan Criteria")
    col1, col2 = st.columns(2)
    with col1:
        rsi_min = st.slider("Minimum RSI", 0, 100, 30)
        rsi_max = st.slider("Maximum RSI", 0, 100, 70)
    with col2:
        volume_multiplier = st.slider("Volume Multiplier", 1.0, 5.0, 2.0)
    
    if st.button("Run Scan"):
        st.success("Scan completed! (This is a demo - connect real data source)")

elif page == "Learning Center":
    st.header("Learning Center")
    st.markdown("""
    ## Varsity-style Educational Content
    
    ### Technical Analysis Basics
    - Candlestick patterns
    - Support and resistance
    - Trend analysis
    - Volume analysis
    
    ### Risk Management
    - Position sizing
    - Stop-loss strategies
    - Portfolio management
    
    *More content coming soon...*
    """)

# Footer
st.markdown("---")
st.markdown("Built with Streamlit | Data sources: NSE, BSE, Yahoo Finance")
