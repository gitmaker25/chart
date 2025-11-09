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
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime, timedelta
import yfinance as yf
import requests
import ta  # Technical analysis library

# Page configuration
st.set_page_config(
    page_title="Varsity Chart Analyzer",
    page_icon="📚",
    layout="wide"
)

# Title with Varsity theme
st.title("🎓 Varsity Style Chart Analyzer")
st.markdown("**Zerodha Varsity Concepts + Technical Analysis**")

# Sidebar navigation
st.sidebar.title("Varsity Modules")
page = st.sidebar.selectbox(
    "Choose Analysis:",
    ["Stock Analysis", "Volume Analysis", "Support/Resistance", "Candlestick Patterns", "Learning Center"]
)

# Technical analysis functions
def calculate_support_resistance(df, window=20):
    """Calculate support and resistance levels"""
    df['Resistance'] = df['High'].rolling(window=window).max()
    df['Support'] = df['Low'].rolling(window=window).min()
    return df

def calculate_volume_profile(df):
    """Calculate volume-based support/resistance"""
    price_bins = np.linspace(df['Low'].min(), df['High'].max(), 20)
    volume_profile = []
    for i in range(len(price_bins)-1):
        volume_in_range = df[(df['Close'] >= price_bins[i]) & (df['Close'] < price_bins[i+1])]['Volume'].sum()
        volume_profile.append({'price': (price_bins[i] + price_bins[i+1])/2, 'volume': volume_in_range})
    return pd.DataFrame(volume_profile)

def identify_candlestick_patterns(df):
    """Identify bullish/bearish candlestick patterns"""
    patterns = []
    
    # Simple pattern detection (expand with more patterns)
    for i in range(2, len(df)):
        current = df.iloc[i]
        prev = df.iloc[i-1]
        prev2 = df.iloc[i-2]
        
        # Bullish Engulfing
        if (prev['Close'] < prev['Open'] and 
            current['Close'] > current['Open'] and 
            current['Open'] < prev['Close'] and 
            current['Close'] > prev['Open']):
            patterns.append((df.index[i], 'Bullish Engulfing', '🟢'))
        
        # Bearish Engulfing
        elif (prev['Close'] > prev['Open'] and 
              current['Close'] < current['Open'] and 
              current['Open'] > prev['Close'] and 
              current['Close'] < prev['Open']):
            patterns.append((df.index[i], 'Bearish Engulfing', '🔴'))
        
        # Hammer (Bullish)
        elif (current['Close'] > current['Open'] and 
              (current['Low'] - current['Open']) > 2 * (current['Close'] - current['Open']) and
              (current['Close'] - current['Open']) > 0):
            patterns.append((df.index[i], 'Hammer (Bullish)', '🟢'))
        
        # Shooting Star (Bearish)
        elif (current['Close'] < current['Open'] and 
              (current['High'] - current['Open']) > 2 * (current['Open'] - current['Close']) and
              (current['Open'] - current['Close']) > 0):
            patterns.append((df.index[i], 'Shooting Star (Bearish)', '🔴'))
    
    return patterns

def get_technical_indicators(df):
    """Calculate multiple technical indicators"""
    # RSI
    df['RSI'] = ta.momentum.RSIIndicator(df['Close']).rsi()
    
    # Moving Averages
    df['SMA_20'] = ta.trend.SMAIndicator(df['Close'], window=20).sma_indicator()
    df['SMA_50'] = ta.trend.SMAIndicator(df['Close'], window=50).sma_indicator()
    df['EMA_12'] = ta.trend.EMAIndicator(df['Close'], window=12).ema_indicator()
    df['EMA_26'] = ta.trend.EMAIndicator(df['Close'], window=26).ema_indicator()
    
    # MACD
    macd = ta.trend.MACD(df['Close'])
    df['MACD'] = macd.macd()
    df['MACD_Signal'] = macd.macd_signal()
    df['MACD_Histogram'] = macd.macd_diff()
    
    # Bollinger Bands
    bollinger = ta.volatility.BollingerBands(df['Close'])
    df['BB_Upper'] = bollinger.bollinger_hband()
    df['BB_Lower'] = bollinger.bollinger_lband()
    df['BB_Middle'] = bollinger.bollinger_mavg()
    
    # Volume indicators
    df['Volume_SMA'] = ta.trend.SMAIndicator(df['Volume'], window=20).sma_indicator()
    
    return df

# Stock Analysis Page
if page == "Stock Analysis":
    st.header("📊 Comprehensive Stock Analysis")
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        stock_symbol = st.text_input("NSE Symbol (e.g., RELIANCE.NS, TCS.NS):", "RELIANCE.NS")
        period = st.selectbox("Time Period", ["1mo", "3mo", "6mo", "1y", "2y"])
        
        if st.button("Analyze Stock"):
            try:
                # Get stock data
                stock = yf.Ticker(stock_symbol)
                hist = stock.history(period=period)
                
                if not hist.empty:
                    # Calculate technical indicators
                    hist = get_technical_indicators(hist)
                    hist = calculate_support_resistance(hist)
                    
                    st.session_state.stock_data = hist
                    st.session_state.stock_symbol = stock_symbol
                    st.success("✅ Analysis Complete!")
                
            except Exception as e:
                st.error(f"Error: {e}")
    
    with col2:
        if 'stock_data' in st.session_state:
            hist = st.session_state.stock_data
            
            # Current price metrics
            current_price = hist['Close'][-1]
            prev_price = hist['Close'][-2]
            change = current_price - prev_price
            change_pct = (change / prev_price) * 100
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Current Price", f"₹{current_price:.2f}")
            with col2:
                st.metric("Change", f"₹{change:.2f}", f"{change_pct:.2f}%")
            with col3:
                st.metric("RSI", f"{hist['RSI'][-1]:.1f}")
            with col4:
                volume_ratio = hist['Volume'][-1] / hist['Volume_SMA'][-1]
                st.metric("Volume Ratio", f"{volume_ratio:.2f}x")
            
            # Main chart with indicators
            fig = go.Figure()
            
            # Candlestick
            fig.add_trace(go.Candlestick(
                x=hist.index,
                open=hist['Open'],
                high=hist['High'],
                low=hist['Low'],
                close=hist['Close'],
                name="Price"
            ))
            
            # Moving averages
            fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_20'], name='SMA 20', line=dict(color='orange')))
            fig.add_trace(go.Scatter(x=hist.index, y=hist['SMA_50'], name='SMA 50', line=dict(color='red')))
            
            # Bollinger Bands
            fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Upper'], name='BB Upper', 
                                   line=dict(color='gray', dash='dash')))
            fig.add_trace(go.Scatter(x=hist.index, y=hist['BB_Lower'], name='BB Lower', 
                                   line=dict(color='gray', dash='dash')))
            
            fig.update_layout(title=f"{st.session_state.stock_symbol} - Technical Analysis",
                            xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

# Volume Analysis Page
elif page == "Volume Analysis":
    st.header("📈 Volume Analysis (Varsity Concept)")
    
    if 'stock_data' in st.session_state:
        hist = st.session_state.stock_data
        
        st.subheader("Volume-Price Relationship")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Volume chart
            fig_volume = go.Figure()
            fig_volume.add_trace(go.Bar(x=hist.index, y=hist['Volume'], name='Volume', 
                                      marker_color='lightblue'))
            fig_volume.add_trace(go.Scatter(x=hist.index, y=hist['Volume_SMA'], 
                                          name='Volume SMA', line=dict(color='red')))
            fig_volume.update_layout(title="Volume Analysis")
            st.plotly_chart(fig_volume, use_container_width=True)
        
        with col2:
            # Volume profile
            volume_profile = calculate_volume_profile(hist)
            fig_profile = go.Figure(go.Bar(
                x=volume_profile['volume'],
                y=volume_profile['price'],
                orientation='h',
                marker_color='lightgreen'
            ))
            fig_profile.update_layout(title="Volume Profile", 
                                    xaxis_title="Volume", 
                                    yaxis_title="Price Level")
            st.plotly_chart(fig_profile, use_container_width=True)
        
        # Volume analysis insights
        st.subheader("📋 Volume Insights (Varsity Principles)")
        
        current_volume = hist['Volume'][-1]
        avg_volume = hist['Volume_SMA'][-1]
        volume_ratio = current_volume / avg_volume
        
        if volume_ratio > 2:
            st.success("**High Volume Alert**: Significant trading activity detected!")
            st.write("**Varsity Tip**: High volume with price movement confirms trend strength")
        elif volume_ratio < 0.5:
            st.warning("**Low Volume**: Limited trading interest")
            st.write("**Varsity Tip**: Low volume moves are less reliable")
        
        if hist['Close'][-1] > hist['Close'][-2] and volume_ratio > 1.5:
            st.info("**Bullish Signal**: Price up with above-average volume")
        elif hist['Close'][-1] < hist['Close'][-2] and volume_ratio > 1.5:
            st.error("**Bearish Signal**: Price down with above-average volume")

# Support/Resistance Page
elif page == "Support/Resistance":
    st.header("🛡️ Support & Resistance Levels")
    
    if 'stock_data' in st.session_state:
        hist = st.session_state.stock_data
        
        current_price = hist['Close'][-1]
        support = hist['Support'][-1]
        resistance = hist['Resistance'][-1]
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Current Price", f"₹{current_price:.2f}")
        with col2:
            st.metric("Support Level", f"₹{support:.2f}")
        with col3:
            st.metric("Resistance Level", f"₹{resistance:.2f}")
        
        # Support/Resistance chart
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=hist.index, open=hist['Open'], high=hist['High'], low=hist['Low'], close=hist['Close']
        ))
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Support'], name='Support', 
                               line=dict(color='green', dash='dash')))
        fig.add_trace(go.Scatter(x=hist.index, y=hist['Resistance'], name='Resistance', 
                               line=dict(color='red', dash='dash')))
        fig.update_layout(title="Support & Resistance Levels")
        st.plotly_chart(fig, use_container_width=True)
        
        # Trading signals based on S/R
        distance_to_resistance = resistance - current_price
        distance_to_support = current_price - support
        
        st.subheader("📊 Trading Signals")
        
        if distance_to_resistance < current_price * 0.02:  # Within 2% of resistance
            st.warning("**Near Resistance**: Consider taking profits or tightening stops")
        elif distance_to_support < current_price * 0.02:  # Within 2% of support
            st.info("**Near Support**: Potential buying opportunity if support holds")

# Candlestick Patterns Page
elif page == "Candlestick Patterns":
    st.header("🕯️ Candlestick Pattern Recognition")
    
    if 'stock_data' in st.session_state:
        hist = st.session_state.stock_data
        
        patterns = identify_candlestick_patterns(hist)
        
        st.subheader("Detected Patterns")
        
        if patterns:
            for date, pattern, signal in patterns[-5:]:  # Show last 5 patterns
                col1, col2, col3 = st.columns([2, 2, 1])
                with col1:
                    st.write(f"**{pattern}**")
                with col2:
                    st.write(date.strftime('%Y-%m-%d'))
                with col3:
                    st.write(signal)
        else:
            st.info("No significant candlestick patterns detected in recent data")
        
        # Candlestick pattern education
        st.subheader("🎓 Varsity Candlestick Guide")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            **Bullish Patterns:**
            - 🟢 **Bullish Engulfing**: Small red candle followed by large green candle
            - 🟢 **Hammer**: Small body with long lower wick at bottom
            - 🟢 **Morning Star**: Downtrend reversal pattern
            
            **Trading View**: Look for confirmation with volume
            """)
        
        with col2:
            st.markdown("""
            **Bearish Patterns:**
            - 🔴 **Bearish Engulfing**: Small green candle followed by large red candle  
            - 🔴 **Shooting Star**: Small body with long upper wick at top
            - 🔴 **Evening Star**: Uptrend reversal pattern
            
            **Trading View**: Combine with resistance levels
            """)

# Learning Center Page
elif page == "Learning Center":
    st.header("🎓 Zerodha Varsity Learning Center")
    
    st.markdown("""
    ## Core Varsity Modules Applied
    
    ### 📈 Technical Analysis Foundation
    **Volume Analysis**
    - Volume confirms price movement
    - High volume breakouts are more reliable
    - Volume divergence can signal reversals
    
    **Support & Resistance**
    - Previous highs act as resistance
    - Previous lows act as support  
    - Breakouts with volume are significant
    
    ### 🕯️ Candlestick Patterns
    **Single Candle Patterns**
    - Doji: Indecision
    - Hammer: Potential bottom
    - Shooting Star: Potential top
    
    **Multi-Candle Patterns**
    - Engulfing patterns: Strong reversal signals
    - Morning/Evening stars: Trend reversal
    - Three white soldiers/black crows: Continuation
    
    ### 📊 Risk Management (Varsity Core)
    - Always use stop-loss
    - Position sizing based on risk
    - Risk-reward ratio minimum 1:2
    - Don't chase prices
    """)
    
    # Interactive examples
    st.subheader("Interactive Examples")
    
    example_pattern = st.selectbox("Choose Pattern to Learn:", 
                                  ["Bullish Engulfing", "Bearish Engulfing", "Hammer", "Shooting Star"])
    
    if example_pattern == "Bullish Engulfing":
        st.image("https://via.placeholder.com/400x200?text=Bullish+Engulfing+Pattern", 
                caption="Small red candle followed by larger green candle that completely engulfs it")
        st.write("**Trading View**: Buy signal when occurring after downtrend, confirmed with volume")

# Footer with Varsity reference
st.markdown("---")
st.markdown("*Based on Zerodha Varsity concepts - Educational purposes only*")
st.markdown("**Trade with knowledge, manage your risk!**")
