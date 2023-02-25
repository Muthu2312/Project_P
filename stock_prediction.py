#Import required Libraries
import streamlit as st
from streamlit_option_menu import option_menu
import time
import requests
from plotly.subplots import make_subplots
import streamlit as st
from datetime import date
import plotly.express as px
import yfinance as yf
from plotly import graph_objs as go
import numpy as np
import numpy
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.layers import LSTM
from sklearn.preprocessing import MinMaxScaler

import datetime as dt

selected=option_menu(
        menu_title='Main Menu',
        options= ['Data Viewer','Graphical Analyser','Predictions'],
        icons=['info-circle-fill','graph-up','activity'],
        default_index=0,
        orientation='horizontal',
        styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "30px"}, 
        "nav-link": {"font-size": "14px", "text-align": "left", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"}
        }
    )
START=  dt.date(2021, 1, 1)
END =  dt.datetime.today()

# def load_data(ticker):
#     data = yf.download(ticker, START, END)
#     data.reset_index(inplace=True)
#     return data
@st.cache_data
@st.cache_resource
def search_symbol(stock_name):
    # create sample dataframe
    df = pd.read_csv('stock.csv')
    df.dropna(inplace=True)
    return df


# load the stock symbols and names

START=  dt.date(2021, 1, 1)
END =  dt.datetime.today()
df = pd.read_csv('stock.csv')
df.dropna(inplace=True)
@st.cache_data
@st.cache_resource
def search_symbol(stock_symbol):
    df = pd.read_csv('stock.csv')
    df.dropna(inplace=True)
    # find the stock name for the given symbol
    #stock_name = df[df['Symbol'] == stock_symbol]['Name'].iloc[0]
    # download data for the stock symbol
    data = yf.download(stock_symbol,START,END)
    data.reset_index(inplace=True)
    # st.header(f"{stock_name} ({stock_symbol}) Stock Price")
    return data
try:
        search_term1 = st.text_input("Enter a stock symbol:")
        search_term = search_term1.upper()
        stock_name = df[df['Symbol'] == search_term]['Name'].iloc[0]
        data1=search_symbol(search_term)
except:
        pass

if selected=='Data Viewer':
        if search_term:
                if search_term in df['Symbol'].values:
                        data1=search_symbol(search_term)
                        st.header(f"{stock_name} ({search_term}) Stock Price")
                        st.experimental_data_editor(data1)
                else:
                        st.write(f"No stock found for symbol '{search_term}'")

if selected=='Graphical Analyser':
    options = ['Option 1', 'Option 2', 'Option 3','Option 4','Option 5','Option 6']
    selected_options = st.selectbox('Select options:', options)
    if selected_options=='Option 1':
                fig = make_subplots(rows=1, cols=1)
                fig.add_trace(go.Candlestick(x=data1['Date'],
                        open=data1['Open'], high=data1['High'],
                        low=data1['Low'], close=data1['Close']),
                        row=1, col=1)
                fig.update_layout(
            title='Animated Candlestick Chart',
            yaxis_title='Price',
            xaxis_rangeslider_visible=True)
                st.plotly_chart(fig, use_container_width=True,renderer='webgl')
                agree = st.checkbox('Explanation')
                if agree:
                    st.write('A candlestick chart is a financial chart that typically shows price movements of currency, securities, or derivatives. It looks like a candlestick with a vertical rectangle and a wick at the top and bottom.\nThe top and bottom of the candlestick show open and closed prices.\n The top of the wick shows the high price, and the bottom of the wick shows the low price.')
                    st.write('**Candlestick charts show a range of information:**')
                    st.write('-Open Price.')
                    st.write('-Close Price.')
                    st.write('-Highest Price.')
                    st.write('-Lowest Buy Price.')
                    st.write('-Patterns and Trends in Share Prices.')
                    st.write('-Emotions of Trades.')

                        

    if selected_options=='Option 2':
        trace_close = go.Scatter(
            x=data1['Date'],
            y=data1['Close'],
            name='Closing Price')
        layout = go.Layout(
            title=f'Trend of Closing Prices',
            xaxis={'title': 'Date'},
            yaxis={'title': 'Price'})
        fig2 = go.Figure(data=[trace_close], layout=layout) 
        fig2.update_xaxes(rangeslider_visible=True,rangeselector=dict(buttons=list([
        dict(count=1, label="1m", step="month", stepmode="backward"),
        dict(count=6, label="6m", step="month", stepmode="backward"),
        dict(count=1, label="YTD", step="year", stepmode="todate"),
        dict(count=1, label="1y", step="year", stepmode="backward"),
        dict(step="all")])))
        st.plotly_chart(fig2,renderer='webgl')
        agree1 = st.checkbox('Explanation')
        if agree1:
            st.write('-A closing price trendline is a graphical representation of a closing price trend over time.')
            st.write('-The closing price is the final price at which a security or asset is traded at the end of the trading day.')
            st.write('-A trendline is a straight line drawn on a chart to indicate the direction of a trend or the general direction of closing price movement.')
            st.write('-If the trendline slopes upwards, it indicates an uptrend, which means that the closing prices have been increasing over time.')
            st.write('-Conversely, if the trendline slopes downwards, it indicates a downtrend, which means that the closing prices have been decreasing over time.')
            st.write('-Traders and investors use closing price trendlines to identify the overall trend of an asset and make informed decisions about whether to buy, sell or hold that asset.')
            st.write('-Its Important to note that trendlines are based on historical data and may not always accurately predict future price movements.')
    
    if selected_options=='Option 3':
        fig3 = px.box(data1, x=data1['Date'].dt.year, y='Close', points='all', title='Closing Prices by Year')
        st.plotly_chart(fig3,renderer='webgl')
        

# df1=data1.reset_index()['Close']
# scaler=MinMaxScaler(feature_range=(0,1))
# df1=scaler.fit_transform(np.array(df1).reshape(-1,1))

# training_size=int(len(df1)*0.65)
# test_size=len(df1)-training_size
# train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
# @st.cache_resource
# def create_dataset(dataset, time_step=1):
# 	dataX, dataY = [], []
# 	for i in range(len(dataset)-time_step-1):
# 		a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
# 		dataX.append(a)
# 		dataY.append(dataset[i + time_step, 0])
# 	return numpy.array(dataX), numpy.array(dataY)

# time_step = 100
# X_train, y_train = create_dataset(train_data, time_step)
# X_test, ytest = create_dataset(test_data, time_step)

# X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
# X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

# model=Sequential()
# model.add(LSTM(50,activation='relu',return_sequences=True,input_shape=(100,1)))
# model.add(LSTM(50,activation='relu',return_sequences=True))
# model.add(Dense(1))
# model.compile(loss='mean_squared_error',optimizer='adam')
# model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=18,batch_size=64,verbose=1)
# train_predict=model.predict(X_train)
# test_predict=model.predict(X_test)
# train_predict=scaler.inverse_transform(train_predict)
# test_predict=scaler.inverse_transform(test_predict)

# x_input=test_data[len(test_data)-100:].reshape(1,-1)
# temp_input=list(x_input)
# temp_input=temp_input[0].tolist()


if selected=='Predictions':
        df1=data1.reset_index()['Close']
        scaler=MinMaxScaler(feature_range=(0,1))
        df1=scaler.fit_transform(np.array(df1).reshape(-1,1))

        training_size=int(len(df1)*0.65)
        test_size=len(df1)-training_size
        train_data,test_data=df1[0:training_size,:],df1[training_size:len(df1),:1]
        @st.cache_resource
        def create_dataset(dataset, time_step=1):
	        dataX, dataY = [], []
	        for i in range(len(dataset)-time_step-1):
		        a = dataset[i:(i+time_step), 0]   ###i=0, 0,1,2,3-----99   100 
		        dataX.append(a)
		        dataY.append(dataset[i + time_step, 0])
	        return numpy.array(dataX), numpy.array(dataY)

        time_step = 100
        X_train, y_train = create_dataset(train_data, time_step)
        X_test, ytest = create_dataset(test_data, time_step)

        X_train =X_train.reshape(X_train.shape[0],X_train.shape[1] , 1)
        X_test = X_test.reshape(X_test.shape[0],X_test.shape[1] , 1)

        model=Sequential()
        model.add(LSTM(50,activation='relu',return_sequences=True,input_shape=(100,1)))
        model.add(LSTM(50,activation='relu',return_sequences=True))
        model.add(Dense(1))
        model.compile(loss='mean_squared_error',optimizer='adam')
        model.fit(X_train,y_train,validation_data=(X_test,ytest),epochs=18,batch_size=64,verbose=1)
        train_predict=model.predict(X_train)
        test_predict=model.predict(X_test)

        x_input=test_data[len(test_data)-100:].reshape(1,-1)
        temp_input=list(x_input)
        temp_input=temp_input[0].tolist()

        lst_output=[]
        n_steps=100
        i=0
        while(i<30):
                if(len(temp_input)>100):
                        x_input=np.array(temp_input[1:])
            #print("{} day input {}".format(i,x_input))
                        x_input=x_input.reshape(1,-1)
                        x_input = x_input.reshape((1, n_steps, 1))
            #print(x_input)
                        yhat = model.predict(x_input, verbose=0)
                        st.write("For Day {}, the predicted output is {}".format(i,scaler.inverse_transform(yhat)))
                        temp_input.extend(yhat[0].tolist())
                        temp_input=temp_input[1:]
            #print(temp_input)
                        lst_output.extend(yhat.tolist())
                        i=i+1
                else:
                        x_input = x_input.reshape((1, n_steps,1))
                        yhat = model.predict(x_input, verbose=0)
            # print(yhat[0])
                        temp_input.extend(yhat[0].tolist())
            #print(len(temp_input))
                        lst_output.extend(yhat.tolist())
                        i=i+1

