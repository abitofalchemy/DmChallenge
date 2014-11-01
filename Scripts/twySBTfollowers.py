import json
from pprint import pprint

json_file = raw_input("Enter JSON file: ")
with open(json_file) as data_file:
    #for line in data_file:
    data = json.load(data_file)


#print data['users']
#for k,v in data.iteritems():
#    print k,v
fnum = 1
followers = []
for i in range(fnum):
    followers.append(data['users'][i])


#pprint followers
#for x in followers:
#    print("""Name:  %s
#Username:  %s
#""" % (x["name"], x["screen_name"]))

#for k,v in followers.iteritems():
#    print k,v

for x in data['users']:
    print("""Name:  %s
Username:  %s
""" % (x["name"], x["screen_name"]))
