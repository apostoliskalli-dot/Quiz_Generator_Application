import streamlit as st
import yfinance as yf
import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt

st.title('Interactive Financial Stock Market Comparative Analysis Tool')

# Function to fetch stock data
def get_stock_data(ticker, start_date='2024-01-01', end_date='2024-02-01'):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data

# Sidebar for user inputs
st.sidebar.header('User Input Options')
selected_stock = st.sidebar.text_input('Enter Stock Ticker 1', 'AAPL').upper()

# Fetch stock data
stock_data = get_stock_data(selected_stock)
stock_data.columns = stock_data.columns.get_level_values(0)
# Display stock data

st.subheader(f"Displaying data for: {selected_stock}")
st.write(stock_data)

chart_type = st.sidebar.selectbox(f'Select Chart Type for {selected_stock}', ['Line', 'Bar'])


if chart_type == 'Line':
    fig = px.line(stock_data, x=stock_data.index, y='Close', title='Trend Analysis', labels={'Close': 'Price (USD)'})
    fig.update_traces(line_color='#00CC96')
    st.plotly_chart(fig)

elif chart_type == 'Bar':
    fig = px.bar(stock_data, x=stock_data.index, y='Close', title='Price Bar Chart', labels={'Close': 'Price (USD)'})
    fig.update_traces(marker_color='#636EFA')
    st.plotly_chart(fig)


fig = px.scatter(stock_data, x=stock_data.index, y='Close', size='Volume',
                         color='Close', title=f'Scatterplot of {selected_stock} Prices vs Volume')
st.plotly_chart(fig)


fig = px.bar(stock_data, x=stock_data.index, y='Close', color='Close',
             title=f'Bar Chart for {selected_stock}')
st.plotly_chart(fig)

# Εμφάνιση του πίνακα describe
st.write("Εδώ βλέπεις τα βασικά στατιστικά στοιχεία για την επιλεγμένη μετοχή:")
st.table(stock_data.describe())

# Δημιουργία του Area Chart με Plotly
fig = px.area(stock_data,
              x=stock_data.index,
              y='Close',
              title=f"Εξέλιξη Τιμής για τη μετοχή: {selected_stock}",
              labels={'Close': 'Τιμή Κλεισίματος ($)', 'Date': 'Ημερομηνία'})

# Εμφάνιση του γραφήματος
st.plotly_chart(fig)