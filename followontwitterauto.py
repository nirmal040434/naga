from TwitterFollowBot import TwitterBot

#create a instance of twitter bot
my_bot = TwitterBot()

#sink with the local cache to find the exixting followers
my_bot.sync_follows()

#auto unfollow people who don't follow
my_bot.auto_unfollow_nonfollowers()

#auto follow the twitter handle that tweets on the given topic
my_bot.auto_follow("docker", count =05)
my_bot.auto_follow("devops", count =05)
my_bot.auto_follow("kubernetes", count =05)

#auto retweet when match is found with a specific topic
my_bot.auto_rt("devops", count = 2)

#auto follow the followers 
my_bot.auto_follow_followers()

