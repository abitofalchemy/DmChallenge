import math
from twython import Twython
import csv


APP_KEY= CONSUMER_KEY = 'knDYepbodjYllFB52VkVXnvJh'
APP_SECRET = CONSUMER_SECRET = 'e14U476NypS6rcLOuIZptd1GqcYMieuvFOlZeoaxVLnmTRBzXV'
OAUTH_TOKEN = '354043186-Mk8Unrssg6CfhLknqZrQr0Y3BkJWJzlChINKwP5n'
OAUTH_TOKEN_SECRET = '8Tgmu7lBl781DRccVMcjzyCBVwhJB2AQpvTAggVIafzDK'

twitter = Twython(APP_KEY, APP_SECRET,
                  OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

#print twitter.get_home_timeline()
user = raw_input("Enter Twitter handle to get followers of: ")
suser = twitter.show_user(screen_name=user)
fnum = 200
pnum = int(math.ceil(float(suser["followers_count"]) / fnum))
print 'count:', suser["followers_count"], ', pnum:',pnum
pnum = 14

pages = []
for i in range(pnum):
    pages.append("p"+str(i+1))

oldpages = []
for i in range(pnum):
    oldpages.append("p"+str(i))

print 'pages:',   len(pages)
print 'oldpages:',len(oldpages)
p0 = { "next_cursor": -1 } # So the following exec() call doesn't fail.

for i in range(pnum):
    print 'page:', i
    exec(pages[i]+" = twitter.get_followers_list(screen_name=user, count=fnum, skip_status=1, cursor="+oldpages[i]+"['next_cursor'])")


followers = []
#f = open('wsbt_followers.txt','w')

for p in range(pnum):
    print p
    if p>14: break
    try:
        exec("for i in range(fnum): followers.append("+pages[p]+"['users'][i])")
    except(IndexError):
        pass
#csv.writer(f).writerows(followers)
#f.close()
#csv.writer(f).writerow([x["screen_name"]])

print(len(followers))

## Outupt followers to a file
f = open('sbt_followers.txt','w')
for x in followers:
#    print("""Name:  %s
#Username:  %s
#""" % (x["name"], x["screen_name"]))
    csv.writer(f).writerow([x["screen_name"]])

f.close()
