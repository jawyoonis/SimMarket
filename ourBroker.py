from Tariff import Tariff
import random


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
        # usage_data = {}
        # other_data = {}
        #
        # customer_file = open('CustomerNums.csv', 'r')
        # all_data = [i[:-1].split(',')[1:] for i in customer_file.readlines()[1:]]
        # for i in range(1, len(all_data) + 1):
        #     usage_data[i] = [float(j) for j in all_data[i-1]]
        # customer_file.close()
        #
        # other_file = open('OtherData.csv')
        # all_data = [i[:-1].split(',')[1:] for i in other_file.readlines()[1:]]
        # other_data['Cleared Price'] = [float(j) for j in all_data[0]]
        # other_data['Cleared Quantity'] = [float(j) for j in all_data[1]]
        # other_data['Difference'] = [float(j) for j in all_data[2]]
        # other_data['Total Demand'] = [float(j) for j in all_data[3]]
        # self.usage = usage_data
        # self.other = other_data
        # print(other_data)

    # Returns a list of asks of the form ( price, quantity ).
    def post_asks(self,time):
        # prices = self.other_data["Cleared Quantity"]
        # for i in range(len(prices)):
        #     if i % 24 ==0:
        #         print(prices[i])
        # return [(i, 100) for i in range(1, 101)]
        average_price = sum(self.other_data['Cleared Price'])/len(self.other_data['Cleared Price'])
        average_quantity = sum(self.other_data['Total Demand'])/len(self.other_data['Total Demand'])
        print("averageprice", average_price)
        print("averagequantity", average_quantity)

        # need to calculate the current price and quantity
        # see how much much it is less or higher than the average price and quantity
        # then we gotta randomize it based on that, I have no idea




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
