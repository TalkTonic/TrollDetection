import requests
import json
import random
from matplotlib import pyplot as p
import troll_detector as td





def mean(array):
    asum = 0
    for items in array:
        asum += items
    return asum/len(array)

#def travis(string):
 #   return random.randint(40,60)


def removeDuplicates(thelist):
    i = 0
    itemtable= {}
    while i < len(thelist):
        if thelist[i][0] == 'y':
            itemtable[thelist[i]] = 0
        i+=1
    return itemtable.keys()


def access1(zeta,rawsource):

    firstlist = []
    firstbase = []
    secondlist = []
    secondbase = []
    i = 0

    travis = td.targeted_sentiment

    while i < len(rawsource[zeta]):
        if rawsource[zeta][i]['sender'] == rawsource[zeta][0]['sender']:
            firstlist.append(
                mean(travis(rawsource[zeta][i]['message'])
                ))
            firstbase.append(i)
        else:
            secondlist.append(
                (travis(rawsource[zeta][i]['message'])))
            secondbase.append(i)
                                    
        i+=1
    return [firstlist,secondlist]

def access2(zeta):

    firstlist = []
    firstbase = []
    secondlist = []
    secondbase = []
    i = 0

    travis = td.targeted_sentiment

      

    while i < len(rawsource[zeta]):
        if rawsource[zeta][i]['sender'] == rawsource[zeta][0]['sender']:
            firstlist.append(
                mean(travis(rawsource[zeta][i]['message'])
                ))
            firstbase.append(i)
        else:
            secondlist.append(
                (travis(rawsource[zeta][i]['message'])))
            secondbase.append(i)
                                    
        i+=1
    return [firstlist,firstbase, secondlist,secondbase]

if __name__== '__main__':

    print "hi"

    matt2 = 'http://10.59.74.200:8080/api'
    matt = 'http://96bcf3c1.ngrok.io/api'

    x= requests.get(matt2)
    rawsource  = x.json() #get loaded
    
    zeta = '0'

    u = access2(zeta)

    firstlist = u[0]
    firstbase = u[1]
    secondlist = u[2]
    secondbase = u[3]

    ax = p.subplot()
    print "something subtle"
    print len(firstbase)
    print len(secondbase)
    p.axis([0, len(rawsource[zeta]),-1,1])
    p.tight_layout()
    #fig = p.figure() #changes outer patch
    #fig.patch.set_facecolor('black')
    p.plot(firstbase, firstlist,'r', secondbase, secondlist,'b')
    ax.set_axis_bgcolor((0,0,0))
    p.show()

