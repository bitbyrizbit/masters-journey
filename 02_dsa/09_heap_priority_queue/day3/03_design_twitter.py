import collections
import heapq

class Twitter:
    def __init__(self):
        self.count = 0
        self.tweetMap = collections.defaultdict(list)
        self.followMap = collections.defaultdict(set)
    def postTweet(self,userId,tweetId):
        self.tweetMap[userId].append([self.count, tweetId])
        self.count -= 1
    def getNewsFeed(self,userId):
        res = []
        min_heap = []
        self.followMap[userId].add(userId)
        for followeeId in self.followMap[userId]:
            if followeeId in self.tweetMap:
                index = len(self.tweetMap[followeeId]) - 1
                count, tweetId = self.tweetMap[followeeId][index]
                min_heap.append([count, tweetId, followeeId, index - 1])
        heapq.heapify(min_heap)
        while min_heap and len(res) < 10:
            count, tweetId, followeeId, idx = heapq.heappop(min_heap)
            res.append(tweetId)
            if idx >= 0:
                count, tweetId = self.tweetMap[followeeId][idx]
                heapq.heappush(min_heap,[count, tweetId, followeeId, idx - 1])
        return res
    def follow(self, followerId, followeeId):
        self.followMap[followerId].add(followeeId)
    def unfollow(self, followerId, followeeId):
        if followeeId in self.followMap[followerId]:
            self.followMap[followerId].remove(followeeId)


twitter = Twitter()
twitter.postTweet(1,5)
print(twitter.getNewsFeed(1))
twitter.follow(1,2)
twitter.postTweet(2,6)
print(twitter.getNewsFeed(1))
twitter.unfollow(1,2)
print(twitter.getNewsFeed(1))