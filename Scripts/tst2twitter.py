from twitter import Twitter
  # ...
CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twitter(auth=OAuth(OAUTH_TOKEN, OAUTH_TOKEN_SECRET, CONSUMER_SECRET, CONSUMER_KEY))

		    # Get the public timeline
twitter.statuses.public_timeline()
