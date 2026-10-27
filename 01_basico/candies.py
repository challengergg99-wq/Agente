class Solution(object):
    def kidsWithCandies(self, candies, extraCandies):
        max_candies = max(candies)
        result = []
        for candy in candies:
            if candy + extraCandies >= max_candies:
                result.append(True)
            else:
                result.append(False)
        return result

print(Solution().kidsWithCandies([2, 3, 5, 1, 3], 3))  # Output: [True, True, True, False, True]