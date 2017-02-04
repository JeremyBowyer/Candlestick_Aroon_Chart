## This function will accept a ticker (string),
## start date and end date (as strings in the form %Y-%m-%d
## and output a candlestick chart with aroon up/down subplot

def candle_aroon(ticker, start, end):
    import datetime as dt
    import matplotlib.pyplot as plt
    from matplotlib import style
    from matplotlib.finance import candlestick_ohlc
    import matplotlib.dates as mdates
    import pandas as pd
    import pandas_datareader.data as web
    style.use('ggplot')

    # Store start/end dates
    start = dt.datetime.strptime(start, "%Y-%m-%d")
    end = dt.datetime.strptime(end, "%Y-%m-%d")

    # Download Data
    df = web.DataReader(ticker, 'yahoo', start, end)

    # Create Aroon Indicators
    df['AroonHigh'] = pd.rolling_apply(df['High'], 15, lambda x:  x.tolist().index(max(x)) / float(14) * 100)
    df['AroonLow'] = pd.rolling_apply(df['Low'], 15, lambda x:  x.tolist().index(min(x)) / float(14) * 100)

    # Drop NA
    df.dropna(inplace=True)

    # Reset index and convert to MDate, for charting purposes
    df.reset_index(inplace=True)
    df['Date'] = df['Date'].map(mdates.date2num)

    # Create subplot Grid
    ax1 = plt.subplot2grid((6, 1), (0, 0), rowspan=5, colspan=1)
    ax2 = plt.subplot2grid((6, 1), (5, 0), rowspan=1, colspan=1, sharex=ax1)
    ax1.xaxis_date()

    # Create subplots
    candlestick_ohlc(ax1, df[['Date', 'Open', 'High', 'Low', 'Close']].values, width=1, colorup='g', colordown='r')
    ax2.plot(df['Date'], df['AroonHigh'], color='g')
    ax2.plot(df['Date'], df['AroonLow'], color='r')

    # Show plot
    plt.show()


