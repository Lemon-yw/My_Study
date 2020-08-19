def maxProfit(prices):
    n = len(prices)
    dp = [[0] * 2 for _ in range(n)]
    for i in range(n):
        # 定义base case
        if i == 0:
            """
            dp[i][0] = max(dp[-1][0], dp[-1][1] + prices[i])
                    = max(0, float('-inf') + prices[i]) = 0
            """
            # dp[i][0] = 0
            """
            dp[i][1] = max(dp[-1][1], dp[-1][0] - prices[i])
                    = max(float('-inf'), 0 - prices[i]) = -prices[i]
            """
            dp[i][1] = -prices[i]
            continue
        dp[i][0] = max(dp[i - 1][0], dp[i - 1][1] + prices[i])
        dp[i][1] = max(dp[i - 1][1], -prices[i])
    return dp[n - 1][0]