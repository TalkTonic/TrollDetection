import requests
import json
import random
from matplotlib import pyplot as p


matt2 = 'http://10.59.74.200:8080/api'
matt = 'http://96bcf3c1.ngrok.io/api'

x= requests.get(matt2)
rawsource  = x.json() #get loaded

zeta = '0'
def travis(string):
    return random.randint(40,60)


def removeDuplicates(thelist):
    i = 0
    itemtable= {}
    while i < len(thelist):
        if thelist[i][0] == 'y':
            itemtable[thelist[i]] = 0
        i+=1
    return itemtable.keys()


firstlist = []
firstbase = []
secondlist = []
secondbase = []
i = 0

while i < len(rawsource[zeta]):
    if rawsource[zeta][i]['sender'] == rawsource[zeta][0]['sender']:
        firstlist.append(travis(rawsource[zeta][i]['message']))
        firstbase.append(i)
    else:
        secondlist.append(travis(rawsource[zeta][i]['message']))
        secondbase.append(i)
                                
    i+=1


ax = p.subplot()
print len(firstbase)
print len(secondbase)
p.axis([0, len(rawsource[zeta]),0,100])
p.tight_layout()
#fig = p.figure() #changes outer patch
#fig.patch.set_facecolor('black')
p.plot(firstbase, firstlist,'r', secondbase, secondlist,'b')
ax.set_axis_bgcolor((0,0,0))
p.show()

