#Name:          shopping.py

#Scenario:      Customers visit some kind of store and get a service number and
#               are fed into one a a checkout lane.  Some times the customers
#               are dissatisfied and they need to be helped a second time.


#Author:        Paul Stenius
#                Anthony Mayes

#Created    Oct 27th 2010

#!/usr/bin/env python
from random import *

from SimPy.Simulation import *

from random import expovariate, seed

import getopt
import sys
verbose = False
priority = False
#model components
    
waitMonitor = Monitor()
queueLengthMonitor = Monitor()
serverTimeMonitor = Monitor()
totalTimeMonitor = Monitor()
class Source(Process):
    def generate(self, numberOfCustomers, resource, interval=5.):
        for i in range(numberOfCustomers):
            c = Customer(name="Customer%02d" % (i,))
            activate(c, c.visit(res=resource,P=0))
            t = expovariate(1.0/interval)
            yield hold,self,t
def probWillHappen(probability):
    rand = random.random()
    if rand < probability:
        return True
    return False
class Customer(Process):
    def visit(self, timeBeingServed=1, res=None, P=0, satisfied=False):
        """P plays double duty as both the probability and the priority"""
        timeBeingServed = uniform(2./(P+1.),2.8/(P+1.))
        arrive = now()
        Nwaiting = len(res.waitQ)
        queueLengthMonitor.observe(Nwaiting)
        if verbose:
            print "%8.3f %s(%1i): Queue has %d customers in line on arrival"%(now(),self.name,P,Nwaiting)

        yield request,self,res,P
        wait = now() - arrive #waiting time
        totalWait = wait
        if verbose:
            print "%8.3f %s: Waited %6.3f in line"%(now(),self.name,wait)
        yield hold,self,timeBeingServed
        serviceTimeTotal = timeBeingServed
        if verbose:
            print "%8.3f %s(%1i): cashier took %8.3f minutes to check out items."%(now(),self.name,P,timeBeingServed)
        yield release,self,res
        while not satisfied:
            if probWillHappen(.2/(P+1)):
                #make the customer rejoin the queue
                if verbose:
                    print "%8.3f %s: Customer Displeased "%(now(),self.name)
                if priority:
                    P = P+1
                arrive = now()
                yield request,self,res,P
                timeBeingServed = uniform(2./(P+1.),2.8/(P+1.))
                serviceTimeTotal += timeBeingServed
                wait = now() - arrive #waiting time
                totalWait += wait
                if verbose:
                    print "%8.3f %s: Waited %6.3f in line"%(now(),self.name,wait)
                yield hold,self,timeBeingServed
                if verbose:
                    print "%8.3f %s(%1i): waited on the cashier for %8.3f minutes, again"%(now(),self.name,P,timeBeingServed)
                yield release,self,res
            else:
                satisfied=True

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
            else:
                priority = False
                print 'without a priority queue'
            print 'using seed value ' + str(seedVal) + ':'
            shop = Resource(capacity=5, name='Shop', unitName="Lane", qType=PriorityQ)
            seed(seedVal)
            initialize()
            waitMonitor.reset()
            queueLengthMonitor.reset()
            serverTimeMonitor.reset()
            s = Source('Source')
            #make a boatload of customers
            activate(s,s.generate(numberOfCustomers=500, resource=shop), at=0.0)
            simulate(until=maxTime)
            result = waitMonitor.count(),waitMonitor.mean()                             
            print "\tAverage wait in queue was for %3d completions was %5.3f minutes."% result
            result = queueLengthMonitor.count(),queueLengthMonitor.mean()                             
            print "\tAverage queue length for %3d completions was %5.3f customers."% result
            result = serverTimeMonitor.count(),serverTimeMonitor.mean()                             
            print "\tAverage time server took in lane for %3d completions was %5.3f \
    minutes."% result
            result = totalTimeMonitor.count(),totalTimeMonitor.mean()                             
            print "\tAverage Total wait time for %3d customers was %5.3f customers."% result
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
