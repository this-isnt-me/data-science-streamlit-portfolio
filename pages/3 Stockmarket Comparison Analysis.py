import pandas as pd
import streamlit as st
import plotly.express as px
import yfinance as yf
import datetime


def convert_date_format(date_str):
    # Convert string to datetime object
    date_obj = datetime.datetime.strptime(str(date_str), "%Y-%m-%d")
    # Format the date as DD/MM/YYYY
    formatted_date = date_obj.strftime("%d/%m/%Y")

    return formatted_date

stock_dict = {
    "Adobe": ("ADBE", '#d2e21b', "solid"),
    "Alphabet": ("GOOG", '#22a884', "dot"),
    "Amazon": ("AMZN", '#7ad151', "dash"),
    "Apple": ("AAPL", '#fde725', "longdash"),
    "Applied Materials": ("AMAT", '#a5db36', "dashdot"),
    "Broadcom": ("AVGO", '#54c568', "longdashdot"),
    "Cisco": ("CSCO", '#35b779', "solid"),
    "IBM": ("IBM", '#1f988b', "dot"),
    "Meta Platforms": ("META", '#23888e', "dash"),
    "Microsoft": ("MSFT",'#2a788e', "longdash"),
    "Netflix": ("NFLX", '#31688e', "dashdot"),
    "NVIDIA": ("NVDA", '#39568c', "longdashdot"),
    "Oracle": ("ORCL", '#414487', "solid"),
    "QUALCOMM": ("QCOM", '#472f7d', "dot"),
    "Tesla": ("TSLA", '#481a6c', "dash"),
    "Texas Instruments": ("TXN", '#440154', "longdash")
}


st.set_page_config(
    layout="wide",
    initial_sidebar_state="expanded")


@st.cache_data
def load_csv_data(data_path):
    loaded_df = pd.read_csv(data_path)
    return loaded_df


src_data_path = 'https://raw.githubusercontent.com/this-isnt-me/credit-card-fraud-network/main/dataset/online_retail.csv'

header_cont = st.container()
main_cont = st.container()

hdr1a, hdr1b = header_cont.columns([1, 6])
hdr2a, hdr2b, hdr2c = header_cont.columns([1, 4, 1])
logo_path = 'img/art_deco.png'
hdr1a.image(logo_path)
st.sidebar.image(logo_path)
hdr2b.markdown(
    "<h1 style='text-align: center; color: white;'>Stockmarket Comparison Analysis Project</h1>",
    unsafe_allow_html=True)
header_cont.markdown('---')
hdr3a, hdr3b, hdr3c = header_cont.columns([1, 10, 1])
hdr3b.markdown('''Stock Market Comparison Analysis entails a systematic evaluation of numerous stocks or financial 
assets traded within the stock market. This process entails scrutinizing the performance of different stocks or
assets to understand their comparative performance and their standing concerning the broader market. Such analysis 
serves as a valuable resource for investors, financial analysts, and decision-makers, enabling them to make 
well-founded investment choices.''')
header_cont.markdown('---')

mn1a, mn1b, mn1c, mn1d, mn15d, mn1e = main_cont.columns([1, 3, 3, 3, 1, 1])

stock_lists = mn1b.multiselect(
    'Choose the stocks you wish to analyse (select at least 2)',
    list(stock_dict.keys()),
    placeholder='Choose stocks')

moving_average = mn15d.selectbox(
    'Moving Average (Days)',
    (5, 10, 20, 50))

today_date = datetime.datetime.today()
previous_date = today_date - datetime.timedelta(weeks=4)

start_date = mn1c.date_input(label="Start Date for Analysis", format="DD/MM/YYYY",
                             value=datetime.date(previous_date.year, previous_date.month, previous_date.day))
end_date = mn1d.date_input(label="End Date for Analysis", format="DD/MM/YYYY",
                           value=datetime.date(today_date.year, today_date.month, today_date.day))

mn2a, mn2b, mn2c = main_cont.columns([1, 10, 1])
main_cont.markdown('---')
mn3a, mn3b, mn3c = main_cont.columns([1, 10, 1])
if mn2b.button("Run Analysis", use_container_width=True) and len(stock_lists) > 1 and start_date and end_date:
    stock_string = ', '.join(stock_lists[:-1]) + ' & ' + stock_lists[-1]
    stock_lists_code = [stock_dict[entry] for entry in stock_lists]
    con_start_date = convert_date_format(start_date)
    con_end_date = convert_date_format(end_date)
    chart1_title = f'''Daily Returns for {stock_string} between {con_start_date} and {con_end_date}'''
    chart15_title = f'''{moving_average} Day Moving Average for {stock_string} between {con_start_date} and {con_end_date}'''
    chart2_title = f'''Cumulative Returns for {stock_string} between {con_start_date} and {con_end_date}'''
    chart3_title = f'''Closing Prices for {stock_string} between {con_start_date} and {con_end_date}'''
    chart4_title = f'''Volatility Comparison for {stock_string} between {con_start_date} and {con_end_date}'''
    chart5_title = f'''Correlation Matrix of Closing Prices for {stock_string} between {con_start_date} and {con_end_date}'''
    fig1 = px.line(height=800)
    fig15 = px.line(height=800)
    fig2 = px.line(height=800)
    fig3 = px.line(height=800)
    volatility_list = []
    colour_map = {}
    beta_list = []
    market_data = yf.download('^GSPC', start=start_date, end=end_date)
    market_data['Daily_Return'] = market_data['Adj Close'].pct_change()
    var_market = market_data['Daily_Return'].var()
    ticker_df = pd.DataFrame(columns=['Date', 'Ticker', 'Close'])
    for index, entry in enumerate(stock_lists_code):
        (ticker_code, colour, line_style) = entry
        stock_name = stock_lists[index]
        colour_map[stock_name] = colour
        ticker_data = yf.download(ticker_code, start=start_date, end=end_date)
        # Calculate Daily Return
        sub_df = pd.DataFrame({'Date': list(ticker_data.index),
                               'Close': list(ticker_data['Adj Close'])})
        sub_df['Ticker'] = stock_lists[index]
        pd.set_option('expand_frame_repr', False)
        ticker_df = pd.concat([ticker_df, sub_df], ignore_index=True, axis=0)
        ticker_data['Daily_Return'] = ticker_data['Adj Close'].pct_change()
        fig1.add_scatter(x=ticker_data.index, y=ticker_data['Daily_Return'], mode='lines', name=stock_lists[index],
                         line=dict(color=colour, dash=line_style))
        # Calculate Moving Average
        ticker_data['moving_average'] = ticker_data['Adj Close'].rolling(moving_average).mean()
        fig15.add_scatter(x=ticker_data.index, y=ticker_data['moving_average'], mode='lines', name=stock_lists[index],
                          line=dict(color=colour, dash=line_style))
        # Calculate Daily Return
        cumulative_return = (1 + ticker_data['Daily_Return']).cumprod() - 1
        fig2.add_scatter(x=ticker_data.index, y=cumulative_return, mode='lines', name=stock_lists[index],
                         line=dict(color=colour, dash=line_style))
        # Closing Price
        fig3.add_scatter(x=ticker_data.index, y=ticker_data['Adj Close'], mode='lines', name=stock_lists[index],
                         line=dict(color=colour, dash=line_style))

        # Calculate Volatility
        volatility_list.append(ticker_data['Daily_Return'].std())
        # Calculate Beta
        cov_ticker = ticker_data['Daily_Return'].cov(market_data['Daily_Return'])
        beta_ticker = cov_ticker / var_market
        beta_list.append((stock_name, beta_ticker))
    fig1.update_layout(xaxis_title='Date', yaxis_title='Daily Return',
                       legend=dict(x=0.02, y=0.95))
    fig15.update_layout(xaxis_title='Date', yaxis_title=f'Closing Price {moving_average} Day Moving Average')
    fig2.update_layout(xaxis_title='Date', yaxis_title='Cumulative Daily Return',
                       legend=dict(x=0.02, y=0.95))
    fig3.update_layout(xaxis_title='Date', yaxis_title='Closing Price',
                       legend=dict(x=0.02, y=0.95))
    text_list = []
    zipped_list = sorted(zip(stock_lists, volatility_list),
                         key=lambda x: x[1],
                         reverse=True)
    stock_lists, volatility_list = zip(*zipped_list)
    for index, entry in enumerate(volatility_list):
        text_list.append(f'{entry:.4f}')
    fig4 = px.bar(x=stock_lists, y=volatility_list,
                  text=text_list,
                  labels={'x': 'Stock', 'y': 'Volatility (Standard Deviation)'},
                  color=stock_lists,
                  color_discrete_map=colour_map, height=800)
    fig4.update_traces(textposition='auto')
    fig4.update_layout(bargap=0.5)

    mn3b.markdown(f'#### {chart1_title}')
    mn3b.plotly_chart(fig1, use_container_width=True)
    mn3b.markdown(f'''The above charts displays the daily returns for {stock_string} between {con_start_date}' 
    and {con_end_date}. This information will provide the foundation for a range of financial 
    assessments and comparisons, including the calculation of returns, volatility, and additional metrics aimed at 
    evaluating both the performance and risk profiles linked to the selected stocks.''')
    mn3b.markdown('###')
    mn3b.markdown('---')
    mn3b.markdown('###')

    mn3b.markdown(f'#### {chart2_title}')
    mn3b.plotly_chart(fig2, use_container_width=True)
    mn3b.markdown(f'''In this analysis, we initially calculated the cumulative returns 
    for {stock_string} between {con_start_date}' and {con_end_date}. 
    Cumulative returns indicate the overall percentage change in the stock's value across the defined timeframe, 
    considering the compounding impact of daily returns. Subsequently, we evaluated the investment performance of the 
    stocks during the designated period, highlighting which stock exhibited superior or inferior cumulative returns 
    over the Timeframe selected.''')
    mn3b.markdown('###')
    mn3b.markdown('---')
    mn3b.markdown('###')

    mn3b.markdown(f'#### {chart3_title}')
    mn3b.plotly_chart(fig3, use_container_width=True)
    mn3b.markdown('###')

    mn3b.markdown(f'#### {chart15_title}')
    mn3b.plotly_chart(fig15, use_container_width=True)
    mn3b.markdown(f'''The above charts display the closing price for {stock_string} between {con_start_date}
    and {con_end_date}. The closing stock price holds paramount importance in stock market analysis as it encapsulates 
    the culmination of daily market activity and investor sentiment. As the last traded price of a stock for the 
    trading day, it serves as a key reference point for evaluating overall market performance, determining daily gains 
    or losses, and assessing the effectiveness of investment strategies. Moreover, the closing price is utilised in 
    technical analysis to identify trends, support and resistance levels, and chart patterns, aiding traders and 
    investors in making informed decisions regarding entry and exit points.''')
    mn3b.markdown('###')
    mn3b.markdown('---')
    mn3b.markdown('###')

    mn3b.markdown(f'#### {chart4_title}')
    mn3b.plotly_chart(fig4, use_container_width=True)
    mn3b.markdown(f'''Initially, we determined the historical volatility for the {stock_string}. Volatility signifies 
    the extent of price fluctuation over time. Specifically, we utilized the standard deviation of daily returns to 
    quantify volatility. Subsequently, we visually represented the computed volatility to evaluate and compare the 
    level of volatility or risk associated with the stocks selected during the designated timeframe. 
    Our analysis reveals that the company with the higher score in the bar chart underwent more significant price 
    fluctuations or greater variability over the time period selected.''')
    mn3b.markdown('###')
    mn3b.markdown('---')
    mn3b.markdown('###')
    mn3b.markdown(f'#### Volatility Calculation (beta) for {stock_string} between {con_start_date} and {con_end_date}')
    beta_list = sorted(beta_list, key=lambda x: x[1], reverse=True)
    for entry in beta_list:
        mn3b.markdown(f'* Beta for {entry[0]} : {entry[1]:.10f}')
    mn3b.markdown(f'''Above we analyze the relative sensitivity of {stock_string} to overall market 
    fluctuations, offering insights into their comparative volatility and risk concerning the broader U.S. stock market 
    as represented by the S&P 500 index. The S&P 500 serves as a widely acknowledged benchmark index in the United 
    States. Comprising 500 of the largest publicly traded companies, selected based on factors like market 
    capitalization, liquidity, and industry representation, the S&P 500 offers a holistic perspective on the 
    performance and vitality of the U.S. stock market.''')

    mn3b.markdown('''A beta exceeding 1 implies that a stock tends to exhibit greater volatility than the market, 
    suggesting a heightened volatility and sensitivity to market fluctuations. Investors should factor in this insight 
    when formulating investment strategies, recognizing that higher-beta stocks may offer increased return potential 
    alongside elevated risk levels.
    ''')
    ticker_df = ticker_df.pivot(index='Date',
                                columns='Ticker',
                                values='Close')
    correlation_matrix = ticker_df.corr()

    fig5 = px.imshow(
        correlation_matrix,
        x=correlation_matrix.columns,
        y=correlation_matrix.columns,
        color_continuous_scale='viridis',
        height=800
    )
    annotations = []
    for i, row in enumerate(correlation_matrix.values):
        for j, value in enumerate(row):
            annotations.append(dict(x=correlation_matrix.columns[j], y=correlation_matrix.index[i],
                                    text=f'{value:.2f}', showarrow=False, font=dict(color='white')))

    # Update layout
    fig5.update_layout(
        xaxis_title='Ticker',
        yaxis_title='Ticker',
        coloraxis_colorbar=dict(title='Correlation'),
        annotations=annotations
    )
    mn3b.markdown('###')
    mn3b.markdown('---')
    mn3b.markdown('###')
    mn3b.markdown(f'#### {chart5_title}')
    mn3b.plotly_chart(fig5, use_container_width=True)
    mn3b.markdown(f'''Correlation analysis of closing stock prices plays a pivotal role in stock market analysis by 
    providing insights into the relationships between different stocks or assets within a portfolio. By quantifying 
    the degree to which the prices of various securities move in tandem, correlation analysis aids investors in 
    diversifying their portfolios effectively and managing risk. A high positive correlation suggests that the prices 
    of two assets tend to move in the same direction, indicating similar market behavior and potentially reducing 
    diversification benefits. Conversely, a negative correlation indicates that the prices move in opposite directions, 
    potentially offering hedging opportunities. By understanding the correlations between different stocks, investors 
    can make informed decisions about portfolio allocation, minimize exposure to risk, and optimize returns in dynamic 
    market conditions.''')

