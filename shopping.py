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
    
class Source(Process):
    def generate(self, numberOfCustomers, resource, interval=5.):
        for i in range(numberOfCustomers):
            c = Customer(name="Customer%02d" % (i,))
            activate(c, c.visit(res=resource,P=0))
            t = expovariate(1.0/interval)
            yield hold,self,t

class Customer(Process):
    def visit(self, timeBeingServed=1, res=None, P=0):
        timeBeingServed = uniform(2/(P+1),2.8/(P+1))
        arrive = now()
        Nwaiting = len(res.waitQ)
        print "%8.3f %s: Queue is %d on arrival"%(now(),self.name,Nwaiting)

        yield request,self,res,P
        wait = now() - arrive #waiting time
        print "%8.3f %s: Waited %6.3f"%(now(),self.name,wait)
        yield hold,self,timeBeingServed
        yield release,self,res
        if not random.randint(0,4):
            print "%8.3f %s: Customer Displeased"%(now(),self.name)
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
    activate(s,s.generate(numberOfCustomers=500, resource=shop), at=0.0)
    guido = Customer(name='Guido')
    activate(guido,guido.visit(timeBeingServed=12.0, res=shop,P=100), at=23.0)
    simulate(until=maxTime)


if __name__ == "__main__":
    main()
