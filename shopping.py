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
    
class CustomerGenerator(Process):
    def generate(self, numberOfCustomers, meanTBA, resource):
        for i in range(numberOfCustomers):
            c = Customer(name="Customer%02d" % (i,))
            activate(c, c.visit(b=resource)

##Model
class Customer(Resource):
    pass
shop = Resource(capacity=5, name='Shop', unitName='Lane')
def main():
    pass


if __name__ == "__main__":
    main()
