
import pandas as pd
import numpy as np
from services.api_calls import time_series_fun_monthly
import pickle

def load_and_preprocess_data(API_KEY, ticker):
    
    # Load the data
    data = time_series_fun_monthly(API_KEY, ticker)
    return data  # assuming coords is the preprocessed data


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
    stock_data = stock_data
    num_iter = int(num_iter)
    dollars = float(dollars)
    num_months = int(num_months)
    ticker_sim_dat = []

    for k in range(num_iter):
        # caluations for simulation
        x = calculate_dca_return(stock_data, dollars, num_months)
        ticker_sim_dat.append(100*x)
        # print("iterating", k)
    
    return ticker_sim_dat


def save_data(new_results):
    
    # we take raw data and  save its as 
    
    # SERALIAZAIION 
    pickled_data = pickle.dumps(new_results)
    print("successfully saved")


def call_model(API_KEY, form_data):
    # Step 1: Preprocess the messy data
    data_for_model = load_and_preprocess_data(API_KEY, form_data['ticker'])
    
    # Step 2: we load model and predict & rearrage the data
    new_results = apply_model(data_for_model, 
                        form_data['num_iter'], 
                        form_data['dollars'], 
                        form_data['num_months'])

    # Step 3: Save the organized data to data base
    save_data(new_results)
    return new_results