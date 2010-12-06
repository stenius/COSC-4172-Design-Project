#Paul Stenius - 2010 - Senior Seminor
#use simuation to approximate the value of integral from 0 to 1 of e^(-x) dx
#the answer is e-1/e which is about .632121...

import math

def trapezoidRule(function, lowerLimit, uppperLimit, steps):
    """use a linear interpolant to approximate function"""
    
    stepsize = (uppperLimit-lowerLimit)/float(steps-1)

    #divide the interval
    #there is a range function in the python std lib but it only works with integer steps
    pointsToEvalAt = []
    for x in range(0,steps): pointsToEvalAt.append(lowerLimit + stepsize * x)
        
    #apply function to every item of pointsToEvalAt and return a list of the results
    answers = map(function,pointsToEvalAt)
        
    #take only half of the first and last numbers and add the rest up and multiply by the stepsize
    k = (answers.pop(0) + answers.pop(-1)) * .5
    k += sum(answers)
    return stepsize * k
    
if __name__ == '__main__':
    for x in [2,3,4,5,10,15,25,50,100,200,500,1000,100000]:
        print 'at',x,'steps the integral is\t',trapezoidRule(lambda x: math.exp(-x), 0, 1, x)
        
        
"""Sample Output
at 2 steps the integral is	0.683939720586
at 3 steps the integral is	0.645235190149
at 4 steps the integral is	0.637962716731
at 5 steps the integral is	0.635409429028
at 10 steps the integral is	0.632770754848
at 15 steps the integral is	0.632389294719
at 25 steps the integral is	0.63221200881
at 50 steps the integral is	0.632142498165
at 100 steps the integral is	0.632125933446
at 200 steps the integral is	0.632121889014
at 500 steps the integral is	0.632120770381
at 1000 steps the integral is	0.632120611611
at 100000 steps the integral is	0.632120558834"""
