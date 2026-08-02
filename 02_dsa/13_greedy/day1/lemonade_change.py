class Solution:
    def lemonadeChange(self, bills: list[int]) -> bool:
        five = 0
        ten = 0
        
        for bill in bills:
            if bill == 5:
                five += 1
            elif bill == 10:
                if five == 0:
                    return False
                five -= 1
                ten += 1
            else: # bill == 20
                # Greedily give one $10 and one $5 first, as $5 is more versatile for future change
                if ten > 0 and five > 0:
                    ten -= 1
                    five -= 1
                elif five >= 3:
                    five -= 3
                else:
                    return False
        return True

if __name__ == "__main__":
    sol = Solution()
    print(sol.lemonadeChange([5,5,5,10,20]))  # Output: True
    print(sol.lemonadeChange([5,5,10,10,20])) # Output: False
