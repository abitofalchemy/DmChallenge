import re
import urllib2
import twitter

APP_KEY= CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'



start_follower = "NYTimesKrugman"
depth = 4

searched = set()

api = twitter.Api(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

def crawl(follower, in_depth):
    if in_depth > 0:
        searched.add(follower)
        users = api.GetFriends(follower)
        names = set([str(u.screen_name) for u in users])
        names -= searched
        for name in list(names)[0:5]:
            crawl(name, in_depth-1) 

crawl(start_follower, depth)
for x in searched:
    print x
print "Program is completed."

