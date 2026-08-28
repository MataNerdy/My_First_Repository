def maxProfit(prices):
    min_p = float('inf')
    max_profit = 0
    for p in prices:
        if p < min_p:
            min_p = p
            print(f"{min_p=}")
        elif p - min_p > max_profit:
            max_profit = p - min_p
            print(f"{max_profit=}")
    return max_profit
prices = [7,1,5,3,6,4]
print(maxProfit(prices))
