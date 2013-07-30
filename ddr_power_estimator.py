from DDRMemory import *
from DDRPowerEstimator import *
import sys

ddrMem = DDRMemory(sys.argv[1])
ddrPower = DDRPowerEstimator(ddrMem)

fp = open(sys.argv[2])

buff = fp.readlines()

print ddrPower.getHeader()
for line in buff:
	elems = line.split()
	inputValues = ddrPower.parseLine(elems)
	print ddrPower.estimate(inputValues)

fp.close()

