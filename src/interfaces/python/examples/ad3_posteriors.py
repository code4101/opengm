import opengm
import numpy

length = 6
numLabels = 2  # slow if more than 2 or 3
ilp = False    # slow if true
model  = '2OrderSubmodublarGrid'
model  = '3OrderRandomChain'

# beta of 0.005 will lead to almost no fractional labels
# beta of 0.5 will lead to fractional solutions for 
# '3OrderRandomChain' model, but potts model
# is still integral
beta = 0.005


if opengm.configuration.withAd3:
    rnd = numpy.random.rand
    gm = None
    # second order example
    if model == '2OrderSubmodublarGrid':
        unaries = rnd(length , length, numLabels)
        potts = opengm.PottsFunction([numLabels,numLabels],0.0, beta)
        gm = opengm.grid2d2Order(unaries=unaries, regularizer=potts)

    # third order example
    elif model == '3OrderRandomChain':
        numberOfStates = numpy.ones(length, dtype=opengm.label_type)*numLabels
        gm = opengm.gm(numberOfStates, operator='adder')
        #add some random unaries
        for vi in range(gm.numberOfVariables):
            unaryFuction = rnd(numLabels)
            gm.addFactor(gm.addFunction(unaryFuction), vi)
        #add one 3.order function
        for vi0 in range(length):
            for vi1 in range(vi0+1, length):
                for vi2 in range(vi1+1, length):
                    highOrderFunction = rnd(numLabels, numLabels,
                                            numLabels)*beta
                    gm.addFactor(gm.addFunction(highOrderFunction),[vi0,vi1,vi2])
    else :
        raise RuntimeError("wrong model type")
    # Inference
    if ilp:
        Inf = opengm.inference.Ad3
        param = opengm.InfParam(solverType='ad3_ilp', adaptEta=True,
                                steps=1000,  residualThreshold=1e-6,
                                verbose=1)
        inf = Inf(gm, parameter=param)
    else:
        Inf = opengm.inference.Ad3
        param = opengm.InfParam(solverType='ad3_lp', adaptEta=True,
                                steps=1000,  residualThreshold=1e-6,
                                verbose=1)
        inf = Inf(gm, parameter=param)

    inf.infer()
    arg = inf.arg()
    posteriors = inf.posteriors()

    if model == '2OrderSubmodublarGrid':
        print posteriors
        print arg.reshape([length, length])
    else:
        print posteriors
        print arg

else:
    raise RuntimeError("this example needs WITH_AD3 enabled")