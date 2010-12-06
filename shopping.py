#Name:          shopping.py

#Scenario:      Customers visit some kind of store and get a service number and
#               are fed into one a checkout lane.  Some times the customers
#               are dissatisfied and they need to be helped a second time.


#Author:        Paul Stenius
#                Anthony Mayes
#                Jase Payne

#Created    Oct 27th 2010

#!/usr/bin/env python

from SimPy.Simulation import *

from random import expovariate, seed

import getopt
import sys
verbose = False
priority = False
cap = 5
#model components
    
waitMonitor = Monitor()
serverTimeMonitor = Monitor()
totalTimeMonitor = Monitor()
class Source(Process):
    def generate(self, numberOfCustomers, resource, interval=5.):
        for i in range(numberOfCustomers):
            c = Customer(name="Customer%02d" % (i,))
            activate(c, c.visit(res=resource,P=0))
            t = expovariate(1.0/interval)#takes the mean
            yield hold,self,t
def probWillHappen(probability):
    rand = random.random()
    if rand < probability:
        return True
    return False
class Customer(Process):
    def visit(self, timeBeingServed=1, res=None, P=0, satisfied=False):
        timeBeingServed = random.uniform(2./(P+1.),2.8/(P+1.))
        arrive = now()
        if verbose:
            print "%8.3f %s(%1i): Queue has %d customers in line on arrival"%(now(),self.name,P,Nwaiting)

        if priority:
		    yield request,self,res,P
        else:
            yield request,self,res
        wait = now() - arrive #waiting time
        totalWait = wait
        if verbose:
            print "%8.3f %s: Waited %6.3f in line"%(now(),self.name,wait)
        yield hold,self,timeBeingServed
        serviceTimeTotal = timeBeingServed
        if verbose:
            print "%8.3f %s(%1i): cashier took %8.3f minutes to check out items."%(now(),self.name,P,timeBeingServed)
        timeThrough = P
        while not satisfied:
            if probWillHappen(.2/(P+1)):
                #make the customer rejoin the queue
                if verbose:
                    print "%8.3f %s: Customer Displeased "%(now(),self.name)
                P = P+1
                timeThrough += 1
                arrive = now()
                yield release,self,res
                if priority:
				    yield request,self,res,P
                else:
                    yield request,self,res
                timeBeingServed = random.uniform(2./(timeThrough+1.),2.8/(timeThrough+1.))
                serviceTimeTotal += timeBeingServed
                wait = now() - arrive #waiting time
                totalWait += wait
                if verbose:
                    print "%8.3f %s: Waited %6.3f in line"%(now(),self.name,wait)
                yield hold,self,timeBeingServed
                if verbose:
                    print "%8.3f %s(%1i): waited on the cashier for %8.3f minutes, again"%(now(),self.name,P,timeBeingServed)
            else:
                satisfied=True
        yield release,self,res
        serverTimeMonitor.observe(serviceTimeTotal)
        waitMonitor.observe(totalWait)
        totalTimeMonitor.observe(serviceTimeTotal + totalWait)
#        if not random.randint(0,4):#1/5 chance of rejoing queue
            #rejoin the queue
#            yield request,self,res,P+1
        if verbose:
            print "%8.3f %s: Completed"%(now(),self.name)

#simulation data
maxTime = 480. #minutes
def main():
    global priority
    seeds = [
	99999,
	99998,
	99997,
	99996,
	99995,
	99994,
	99993,
	99992,
	99991,
    99990,]
    for seedVal in seeds:
        for toggle in (True,False):
            if toggle:
                priority = True
                print 'with a priority queue'
                shop = Resource(capacity=cap, name='Shop', unitName="Lane",
                   qType=PriorityQ,monitored=True,monitorType=Monitor)
            else:
                priority = False
                print 'without a priority queue'
                shop = Resource(capacity=cap, name='Shop', unitName="Lane",
                   monitored=True,monitorType=Monitor)  
            print 'using seed value ' + str(seedVal) + ':'
            seed(seedVal)
            initialize()
            waitMonitor.reset()
            serverTimeMonitor.reset()
            totalTimeMonitor.reset()
            s = Source('Source')
            #make a boatload of customers
            activate(s,s.generate(numberOfCustomers=500, resource=shop), at=0.0)
            simulate(until=maxTime)

            result = waitMonitor.count(),waitMonitor.mean()
            results = waitMonitor.yseries()
            results.sort()
            print "\tAverage wait in queue for %3d transactions was %5.3f minutes."% result
            print '\tmin:',results[0],'max:',results[-1]

            results = shop.waitMon.yseries()
            results.sort()
            result = shop.waitMon.mean()                           
            print "\tAverage queue length was %5.3f customers."% result
            print '\tmin:',results[0],'max:',results[-1]

            result = serverTimeMonitor.count(),serverTimeMonitor.mean()                             
            results = serverTimeMonitor.yseries()
            results.sort()
            print "\tAverage time server took in lane for %3d transactions was %5.3f \
    minutes."% result
            print '\tmin:',results[0],'max:',results[-1]

            result = totalTimeMonitor.count(),totalTimeMonitor.mean() 
            results = totalTimeMonitor.yseries()
            results.sort()
            print "\tAverage Total time for %3d customers was %5.3f minutes."% result
            print '\tmin:',results[0],'max:',results[-1]
			
            result = shop.actMon.yseries()
            print "\tMax number of servers busy:",max(result)
            stopSimulation()
def usage():
	print "This program will run a simulation using pre-programmed seed values multiple times."
	print "\n\tOptions:\n\t\t\t-h\tBring up the help menu\n\t\t\t-v\tEnable verbose mode."
	print "\t\t\t-p\tEnable Priority option for requeuing dissatisfied customers.\n"
if __name__ == "__main__":
    try:
        opts = getopt.getopt(sys.argv, "v:p:h", ["verbose", "priority", "help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt in opts[1]:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--priority"):
            priority = True
        elif opt in ("-v", "--verbose"):
            verbose = True
    main()
