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

            if product == "RAINFOREST_RESIN":

                buy_price = 10000 - 2 # we buy when below this
                sell_price = 10000 + 2 # we sell when above this

                if len(order_depth.sell_orders) > 0: # if there are any SELL orders in the market
                    prices = list(order_depth.sell_orders.keys())
                    prices.sort() # sort from small to large

                    for price in prices:
                        if price <= buy_price: # buy it
                            amount = -order_depth.sell_orders[price]
                            buy_amount = min(amount, limit - position)
                            position += buy_amount
                            print(f"someone sell at {price}. we buy {buy_amount}. ")
                            if buy_amount:
                                orders.append(Order(product, price, buy_amount))
                        else:
                            break # all the rest prices are not good

                if len(order_depth.buy_orders) > 0: # if there are any BUY orders in the market
                    prices = list(order_depth.buy_orders.keys())
                    prices.sort()
                    prices.reverse() # sort fromm large to small

                    for price in prices:
                        if price >= sell_price: # sell it
                            amount = order_depth.buy_orders[price]
                            sell_amount = min(amount, position + limit)
                            position -= sell_amount
                            if sell_amount:
                                orders.append(Order(product, price, -sell_amount))
            
            # if product == "SQUID_INK":
            #     buy_price = 1971 - 90 # we buy when below this
            #     sell_price = 1971 + 136 # we sell when above this

            #     if len(order_depth.sell_orders) > 0: # if there are any SELL orders in the market
            #         prices = list(order_depth.sell_orders.keys())
            #         prices.sort() # sort from small to large

            #         for price in prices:
            #             if price <= buy_price: # buy it
            #                 amount = -order_depth.sell_orders[price]
            #                 buy_amount = min(amount, limit - position)
            #                 position += buy_amount
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

        traderData = "SAMPLE" # String value holding Trader state data required. It will be delivered as TradingState.traderData on next execution.
        
        conversions = 1 

        # Return the dict of orders
        # These possibly contain buy or sell orders
        # Depending on the logic above
        
        return result, conversions, traderData
