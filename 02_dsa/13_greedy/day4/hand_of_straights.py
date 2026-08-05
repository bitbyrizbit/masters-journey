from collections import Counter

class Solution:
    def isNStraightHand(self, hand: list[int], groupSize: int) -> bool:
        if len(hand) % groupSize != 0:
            return False
            
        counts = Counter(hand)
        # Sort keys to evaluate the smallest cards first
        sorted_cards = sorted(counts.keys())
        
        for card in sorted_cards:
            if counts[card] > 0:
                needed = counts[card]
                # We must form 'needed' groups starting with this card
                for i in range(groupSize):
                    curr_card = card + i
                    # If any card needed to complete the straight is missing
                    if counts[curr_card] < needed:
                        return False
                    counts[curr_card] -= needed
                    
        return True

if __name__ == "__main__":
    sol = Solution()
    print(sol.isNStraightHand([1,2,3,6,2,3,4,7,8], 3)) # Output: True
    print(sol.isNStraightHand([1,2,3,4,5], 4))         # Output: False
