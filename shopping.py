#Name:          shopping.py

#Scenario:      Customers visit some kind of store and get a service number and
#               are fed into one a a checkout lane.  Some times the customers
#               are dissatisfied and they need to be helped a second time.


#Author:        Paul Stenius

#Created    Oct 27th 2010

#!/usr/bin/env python
from random import *

from SimPy.Simulation import *

from random import expovariate, seed

#model components
    
waitMonitor = Monitor()
queueLengthMonitor = Monitor()
serverTimeMonitor = Monitor()
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
        timeBeingServed = uniform(2./(P+1),2.8/(P+1))
        arrive = now()
        Nwaiting = len(res.waitQ)
        queueLengthMonitor.observe(Nwaiting)
        print "%8.3f %s(%1i): Queue has %d customers in line on arrival"%(now(),self.name,P,Nwaiting)

        yield request,self,res,P
        wait = now() - arrive #waiting time
        waitMonitor.observe(wait)
        print "%8.3f %s: Waited %6.3f in line"%(now(),self.name,wait)
        yield hold,self,timeBeingServed
        serverTimeMonitor.observe(timeBeingServed)
        print "%8.3f %s(%1i): waited on the cashier for %8.3f minutes"%(now(),self.name,P,timeBeingServed)
        yield release,self,res
        while not satisfied:
            if probWillHappen(.2/(P+1)):
                #make the customer rejoin the queue
                print "%8.3f %s: Customer Displeased "%(now(),self.name)
                P = P+1
                arrive = now()
                yield request,self,res,P
                timeBeingServed = uniform(2./(P+1),2.8/(P+1))

                wait = now() - arrive #waiting time
                print "%8.3f %s: Waited %6.3f in line"%(now(),self.name,wait)
                yield hold,self,timeBeingServed
                print "%8.3f %s(%1i): waited on the cashier for %8.3f minutes, again"%(now(),self.name,P,timeBeingServed)
                yield release,self,res

            else:
                satisfied=True

        if not random.randint(0,4):
            #rejoin the queue
            yield request,self,res,P+1
        print "%8.3f %s: Completed"%(now(),self.name)

#simulation data
maxTime = 480. #minutes
def main():
    shop = Resource(capacity=5, name='Shop', unitName="Lane", qType=PriorityQ)
    seed(99999)
    initialize()
    s = Source('Source')
    #make a boatload of customers
    activate(s,s.generate(numberOfCustomers=500, resource=shop), at=0.0)
    simulate(until=maxTime)

    result = waitMonitor.count(),waitMonitor.mean()                             
    print "Average wait in queue was for %3d completions was %5.3f minutes."% result
    result = queueLengthMonitor.count(),queueLengthMonitor.mean()                             
    print "Average queue length for %3d completions was %5.3f cusomters."% result
    result = serverTimeMonitor.count(),serverTimeMonitor.mean()                             
    print "Average time server took in lane for %3d completions was %5.3f \
    minutes."% result
if __name__ == "__main__":
    main()
