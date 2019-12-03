from Tariff import Tariff
import random

import pandas_datareader.data as web
import pandas as pd
import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style




class BrokerOurs:

    def __init__(self, idx):

        # ID number, cash balance, energy balance
        self.idx = idx
        self.cash = 0
        self.power = 0
        self.customer_usage = None
        self.other_data = None

        # Lists to contain:
        # asks: tuples of the form ( quantity, price )
        # tariffs: Tariff objects to submit to the market
        # customers: integers representing which customers are subscribed
        # to your tariffs.
        self.asks = []
        self.tariffs = []
        self.customers = []

    # A function to accept the bootstrap data set.  The data set contains:
    # usage_data, a dict in which keys are integer customer ID numbers,
    # and values are lists of customer's past usage profiles.
    # other_data, a dict in which 'Total Demand' is a list of past aggregate demand
    # figures, 'Cleared Price' is a list of past wholesale prices,
    # 'Cleared Quantity' is a list of past wholesale quantities,
    # and 'Difference' is a list of differences between cleared
    # quantities and actual usage.

    def get_initial_data(self, usage_data, other_data):

        self.customer_usage = usage_data
        self.other_data = other_data



    def simulation_price(self):
        style.use('ggplot')
        prices= self.other_data["Cleared Price"]
        series = pd.Series(np.array(prices))
        returns= series.pct_change()
        # print(returns)

        # print(prices)
        last_price= self.other_data["Cleared Price"][-1]
        # print(last_price)
        num_simulations = 10
        num_days = 14
        simulation_df = pd.DataFrame()
        for x in range(num_simulations):
            count = 0
            daily_vol = returns.std()

            predicted_prices = []
            price = last_price * (1 + np.random.normal(0, daily_vol))
            predicted_prices.append(price)
            for y in range(num_days):
                if count == 13:
                    break
                price = predicted_prices[count] * (1 + np.random.normal(0, daily_vol))
                predicted_prices.append(price)
                count += 1
            simulation_df[x] = predicted_prices
        # fig = plt.figure()
        # fig.suptitle('Monte Carlo Simulation: cleared prices')
        # plt.plot(simulation_df)
        # plt.axhline(y = last_price, color = 'r', linestyle = '-')
        # plt.xlabel('Day')
        # plt.ylabel('Price')
        # plt.show()
            print(predicted_prices)

    # Returns a list of asks of the form ( price, quantity ).
    def post_asks(self, time):
        # prices = self.other_data["Cleared Quantity"]
        # for i in range(len(prices)):
        #     if i % 24 ==0:
        #         print(prices[i])

        average_price = sum(self.other_data['Cleared Price'])/len(self.other_data['Cleared Price'])
        average_quantity = sum(self.other_data['Total Demand'])/len(self.other_data['Total Demand'])
        # print("average price", average_price)
        # print("average quantity", average_quantity)

        # for i in range(len(self.other_data['Cleared Price'])):
        #
        #     current_price = self.other_data['Cleared Price'][-i]
        #
        #     # current_demand = self.other_data['Total Demand'][i]
        #     print(current_price, "current price")
            # print(current_demand, "current demand", i)
            # demand_difference = (current_demand/average_quantity)*100-100
            # print(demand_difference, "demand difference", i)

        self.simulation_price()
        return [(i, 100) for i in range(1, 101)]

        # need to calculate the current price and quantity
        # see how much much it is less or higher than the average price and quantity
        # then we gotta randomize it based on that, I have no idea
        # what to do if the demand is lower or higher than the average demand




    ## Returns a list of Tariff objects.
    def post_tariffs(self, time):
        return [Tariff(self.idx, price=100, duration=3, exitfee=0)]

    ## Receives data for the last time period from the server.
    def receive_message( self, msg ):
        pass

    ## Returns a negative number if the broker doesn't have enough energy to
    ## meet demand.  Returns a positive number otherwise.
    def get_energy_imbalance( self, data ):
        return self.power

    def gain_revenue( self, customers, data ):
        for c in self.customers:
            self.cash += data[c] * customers[c].tariff.price
            self.power -= data[c]

    ## Alter broker's cash balance based on supply/demand match.
    def adjust_cash( self, amt ):
        self.cash += amt
