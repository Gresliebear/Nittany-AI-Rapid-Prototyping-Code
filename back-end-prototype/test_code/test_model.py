import numpy as np
import pandas as pd


def calculate_dca_return(stock_data, monthly_investment, months_to_invest):
    """
    Dollar Cost Averaging (DCA) Monte Carlo Sitmulation Implementation
    Invest $1000 per month in ETF. Once every month, randomly choose one day to purchase the maximum number of shares allowed with available buying power
    Calculate the return of dollar-cost averaging on a stock.

    Parameters:
    stock_data (DataFrame): Historical stock data.
    monthly_investment (float): Amount invested each month.
    months_to_invest (int): Number of months over which investments are made.

    Returns:
    float: ROI (Return on Investment)
    """
    # Ensure 'Date' column is in datetime format
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    # Generate a range of dates for analysis
    start_date = stock_data['Date'].min()
    end_date = stock_data['Date'].max() - pd.DateOffset(months=months_to_invest)
    date_range = pd.date_range(start=start_date, end=end_date, freq='M')

    # Randomly select a start month for investing
    invest_start_date = np.random.choice(date_range)

    # Initialize investment tracking variables
    total_investment = 0
    total_value = 0
    shares_owned = 0

    # Loop over each month to calculate investment progress
    for month_count in range(months_to_invest):
        current_date = invest_start_date + pd.DateOffset(months=month_count)
        current_stock_data = stock_data[stock_data['Date'].dt.to_period('M') == current_date.to_period('M')]

        if not current_stock_data.empty:
            # Randomly select a trading day in the month
            random_trading_day = current_stock_data.sample()

            # Get closing price and calculate number of shares bought
            closing_price = float(random_trading_day['close'].iloc[0])
            shares_bought = monthly_investment / closing_price

            # Update investment totals
            total_investment += monthly_investment
            shares_owned += shares_bought
            total_value = shares_owned * closing_price

    # Calculate ROI
    roi = (total_value - total_investment) / total_investment

    return roi


def apply_model(stock_data, num_iter, dollars, num_months):
    # dca_simulation SPY 12-month simulation
    num_iter = num_iter
    stock_data = stock_data
    # ticker_string = 'test SPY'
    dollars = float(dollars)
    num_months = int(num_months)
    ticker_sim_dat = []

    for k in range(num_iter):
        # caluations for simulation
        x = calculate_dca_return(stock_data, dollars, num_months)
        ticker_sim_dat.append(100*x)
        # print("iterating", k)
    
    return ticker_sim_dat

from api_call_test import time_series_fun_monthly

API_KEY = 'D03VFL5XJ25QWELA'
TICKER = 'AAPL'
df = time_series_fun_monthly(API_KEY, TICKER)

# monte carlo iterations 
num_iter = 1000
# $1000 dollars
amountForDCA = 1000
#time line 12 months
months = 12

simulation_data  = apply_model(df, num_iter, amountForDCA, months)

print(simulation_data)

## lets plot the data
import matplotlib.pyplot as plt
ticker_hist = plt.hist(simulation_data,bins='auto')
plt.title(TICKER + '' + str(months) + '-month ROI Simulation (' + str(num_iter) + ' Iterations)')
plt.xlabel(str(months) + '-month return (%)')
plt.ylabel('Iterations')
plt.xlim([-40,30])
plt.show()
