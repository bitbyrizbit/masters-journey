from typing import List

class Solution:
    def intervalIntersection(self, firstList: List[List[int]], secondList: List[List[int]]) -> List[List[int]]:
        """
        Returns the intersection of two disjoint, sorted interval lists.
        """
        i = 0
        j = 0
        intersections = []
        
        # Two-pointer sweep across both lists
        while i < len(firstList) and j < len(secondList):
            # The intersection bounds are the max of the starts and the min of the ends
            start = max(firstList[i][0], secondList[j][0])
            end = min(firstList[i][1], secondList[j][1])
            
            # If the calculated bounds form a valid interval, record it
            if start <= end:
                intersections.append([start, end])
                
            # Advance the pointer of the interval that finishes earliest.
            # This is because the one that finishes earliest has completely exhausted its potential
            # to intersect with any future intervals in the other list.
            if firstList[i][1] < secondList[j][1]:
                i += 1
            else:
                j += 1
                
        return intersections
