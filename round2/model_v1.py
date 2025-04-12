"""
Round 1 Strategies: 

(1). Rainforest Resin: 
above a threshold: sell
below a threshold: buy

"""


from typing import Dict, List
from datamodel import *

class Trader:

    def run(self, state: TradingState) -> Dict[str, List[Order]]:
        # Initialize the method output dict as an empty dict
        result = {}

        print(state.position)

        # Iterate over all the keys (the available products) contained in the order dephts
        for product in state.order_depths.keys():
            
            # Retrieve the Order Depth containing all the market BUY and SELL orders
            order_depth: OrderDepth = state.order_depths[product]
            position: Position = 0
            if product in state.position.keys():
                position = state.position[product]
            limit = 50
            
            # Initialize the list of Orders to be sent as an empty list
            orders: list[Order] = []

            # if product == "RAINFOREST_RESIN":

            #     buy_price = 10000 - 2 # we buy when below this
            #     sell_price = 10000 + 2 # we sell when above this

            #     if len(order_depth.sell_orders) > 0: # if there are any SELL orders in the market
            #         prices = list(order_depth.sell_orders.keys())
            #         prices.sort() # sort from small to large

            #         for price in prices:
            #             if price <= buy_price: # buy it
            #                 amount = -order_depth.sell_orders[price]
            #                 buy_amount = min(amount, limit - position)
            #                 position += buy_amount
            #                 print(f"someone sell at {price}. we buy {buy_amount}. ")
            #                 if buy_amount:
            #                     orders.append(Order(product, price, buy_amount))
            #             else:
            #                 break # all the rest prices are not good

            #     if len(order_depth.buy_orders) > 0: # if there are any BUY orders in the market
            #         prices = list(order_depth.buy_orders.keys())
            #         prices.sort()
            #         prices.reverse() # sort fromm large to small

            #         for price in prices:
            #             if price >= sell_price: # sell it
            #                 amount = order_depth.buy_orders[price]
            #                 sell_amount = min(amount, position + limit)
            #                 position -= sell_amount
            #                 if sell_amount:
            #                     orders.append(Order(product, price, -sell_amount))

            # Add all the above the orders to the result dict
            result[product] = orders
        

        # Trading strategy on basket 1:
        """
        PICNIC_BASKET2: y
        4 CROISSANTS: y1
        2 JAMS: y2

        we assume y' = b1y1 + b2y2 + c
        and solve for b1, b2, c using a linear regression model we have

        We study the distribution of y' - y
        and according to the current value of y' - y, make our trading decision
        """

        b1 = 8.42543335
        b2 = 3.10280571
        b3 = -0.51088565
        c = 9247.413503579926
        miss_information = False
        left_threshold = -132.61453956267687
        right_threshold = 128.1524804991444

        midprice = {"PICNIC_BASKET1": 0, "CROISSANTS": 0, "JAMS": 0, "DJEMBES": 0}
        position = {"PICNIC_BASKET1": 0, "CROISSANTS": 0, "JAMS": 0, "DJEMBES": 0}
        for product in position.keys():
            if product in state.position.keys():
                position[product] = state.position[product]
            else:
                position[product] = 0
        for product in midprice.keys():
            if product in state.order_depths.keys():
                order_depth: OrderDepth = state.order_depths[product]
                cnt = 0
                sum = 0
                if len(order_depth.sell_orders) > 0:
                    # find the cheapest in sell
                    cnt += 1
                    sum += min(order_depth.sell_orders.keys())
                if len(order_depth.buy_orders) > 0:
                    # find the most expensive in buy
                    cnt += 1
                    sum += max(order_depth.buy_orders.keys())
                if cnt==2:
                    midprice[product] = sum / cnt
                else:
                    miss_information = True
            else:
                miss_information = True
        

        if not miss_information:
            print(f"midprice: {midprice["PICNIC_BASKET1"], midprice["CROISSANTS"], midprice['JAMS'], midprice['DJEMBES']}")
            diff = midprice["PICNIC_BASKET1"] - b1*midprice["CROISSANTS"] - b2*midprice["JAMS"] - b3*midprice["DJEMBES"] - c
            print(f"the diff is {diff}")
            # if diff < left_threshold: 
            #     print("We need to long basket, short ingredient")
            #     # long basket, short ingredients
            #     result["PICNIC_BASKET2"] = [Order("PICNIC_BASKET2", midprice["PICNIC_BASKET2"], 100 - position["PICNIC_BASKET2"])]
            #     result["CROISSANTS"] = [Order("CROISSANTS", midprice["CROISSANTS"], int(-b1*(100 - position["PICNIC_BASKET2"])))]
            #     result["JAMS"] = [Order("JAMS", midprice["JAMS"], int(-b2*(100 - position["JAMS"])))]
            # if diff > right_threshold:
            #     print("We need to short basket, long ingredient")
            #     # short basket, long ingredients
            #     result["PICNIC_BASKET2"] = [Order("PICNIC_BASKET2", midprice["PICNIC_BASKET2"], -(position["PICNIC_BASKET2"] + 100))]
            #     result["CROISSANTS"] = [Order("CROISSANTS", midprice["CROISSANTS"], int(b1*(position["PICNIC_BASKET2"] + 100)))]
            #     result["JAMS"] = [Order("JAMS", midprice["JAMS"], int(b2*(position["PICNIC_BASKET2"] + 100)))]
        
        # print(result)

        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        conversions = 1 
        # Return the dict of orders
        # These possibly contain buy or sell orders
        # Depending on the logic above
        
        return result, conversions, traderData
