from twython import Twython
import time
import csv

APP_KEY= CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)


next_cursor=-1
f = open('wsbt_followers.txt','w')
while(next_cursor):

	search = twitter.get_followers_list(screen_name='WSBT',count=200,cursor=next_cursor)
	for result in search['users']:
		time_zone =result['time_zone'] if result['time_zone'] != None else "N/A"
		print result["screen_name"].encode('utf-8')+ ' '+time_zone.encode('utf-8')
        csv.writer(f).writerow([result["screen_name"].encode('utf-8')])

	next_cursor = search["next_cursor"]
	time.sleep(60)
print(twitter.get_followers_list()['ids'])
f.close()


