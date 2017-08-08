import sys
import serial
import time
from imaging import noOfVehicles

lowU = 4
mediumU = 8
active = 1 #setting default active phase

#period for each phase has been red in seconds
redTimes = [0, 0, 0, 0]

scenario = [[0, 0], [0, 0], [0, 0], [0, 0]]

lastSentPhase = 0

decisionTable = [
   ['L', 'L', 'Y'],
   ['L', 'M', 'Y'],
   ['L', 'H', 'N'],
   ['M', 'L', 'Y'],
   ['M', 'M', 'Y'],
   ['M', 'H', 'N'],
   ['H', 'L', 'Y'],
   ['H', 'M', 'Y'],
   ['H', 'H', 'Y']
  ]
flowUrgencyTable = [
  ['L', 'L', 'L'],
  ['L', 'M', 'L'],
  ['L', 'H', 'L'],
  ['M', 'L', 'M'],
  ['M', 'M', 'M'],
  ['M', 'H', 'L'],
  ['H', 'L', 'H'],
  ['H', 'M', 'H'],
  ['H', 'H', 'M']
]
redTimeTable = [
  ['L', 'L', 'L'],
  ['L', 'M', 'L'],
  ['L', 'H', 'M'],
  ['M', 'L', 'L'],
  ['M', 'M', 'M'],
  ['M', 'H', 'H'],
  ['H', 'L', 'M'],
  ['H', 'M', 'H'],
  ['H', 'H', 'M']
]
observanceTable = [
  ['L', 'L', 'L'],
  ['L', 'M', 'L'],
  ['L', 'H', 'L'],
  ['M', 'L', 'M'],
  ['M', 'M', 'M'],
  ['M', 'H', 'L'],
  ['H', 'L', 'H'],
  ['H', 'M', 'H'],
  ['H', 'H', 'M']
]

#defining different phases - phases[phaseNo][flowNo][directionsOfTheFlow]
phases = [
  [[0, 1], [0, 2], [0, 3]],
  [[1, 0], [1, 2], [1, 3]],
  [[2, 0], [2, 1], [2, 3]],
  [[3, 0], [3, 1], [3, 2]]
]

def rangeToSeconds(urgency):
    if urgency == 'L':
        return 5
    elif urgency == 'M':
        return 10
    elif urgency == 'H':
        return 15
    else:
        return 30

def rangeToValue(urgency):
    if urgency == 'L':
        return 1
    elif urgency == 'M':
        return lowU+1
    elif urgency == 'H':
        return mediumU+1
    else: return 0

def valueToRange(value):
  if value<=lowU:
    return 'L'
  elif value<=mediumU:
    return 'M'
  else:
    return 'H'

#tells if the current phase should be stopped or not
def observingModule():
  oNumCarD=0
  ofNumCarD=0
  #taking the average of ofNumCar and ofNumCar of all flows in active phase
  oNumCarD = scenario[phases[active][0][0]][1]
  for i in range(0, len(phases[0])):
      ofNumCarD += scenario[phases[active][i][1]][0]
  oNumCar = valueToRange(oNumCarD)
  ofNumCar = valueToRange(ofNumCarD/len(phases[0]))
  for i in range(0, len(observanceTable)):
      if observanceTable[i][0] == oNumCar and observanceTable[i][1] == ofNumCar:
          return observanceTable[i][2]
  return 'L'

#calculates the urgency of a flow
def flowUrgency(phase, in_direction, out_direction):
  urgency = 'L'
  numCar = valueToRange(scenario[in_direction][1])
  redTime = valueToRange(redTimes[phase])
  fNumCar = valueToRange(scenario[out_direction][0])
  for i in range(0, len(flowUrgencyTable)):
    if flowUrgencyTable[i][0] == numCar and flowUrgencyTable[i][1] == fNumCar:
      tempUrgency = flowUrgencyTable[i][2]
      break
  for i in range(0, len(redTimeTable)):
      if tempUrgency==redTimeTable[i][0] and redTime==redTimeTable[i][1]:
          urgency = redTimeTable[i][2]
          break
  return rangeToValue(urgency)

#calculates the urgency of a phase
def phaseUrgency(phase):
  urgency_sum = 0
  for i in range(0, len(phases[0])):
    urgency_sum += flowUrgency(phase, phases[phase][i][0], phases[phase][i][1])
  return urgency_sum/len(phases[0])

#calculates the urgency of all non-active phases and returns the urgency of the phase with highest urgency
def nextPhase():
    global lastSentPhase
    urgencies = []
    for i in range(0, len(phases)):
        urgencies.append(i)
    urgencies = sorted(urgencies, key=phaseUrgency, reverse=True)
    for i in range(0, len(urgencies)):
        if urgencies[i]!=active and urgencies[i]!=lastSentPhase:
            lastSentPhase = urgencies[i]
            return (urgencies[i], valueToRange(phaseUrgency(urgencies[i])))

#takes decision whether to continue with current phase or change phase
def decisionMaker():
    decision = 'Y'
    next_phase = nextPhase()
    stop = observingModule()
    #print 'nextPhase: ', str(next_phase[0]), ' with urgency: ', next_phase[1]
    #print 'active: ', str(stop)
    for i in range(0, len(decisionTable)):
        if decisionTable[i][0] == next_phase[1] and decisionTable[i][1] == stop:
            decision = decisionTable[i][2]
            break
    #print 'decision: ', decision
    if decision == 'N':
        next_phase = (active, valueToRange(phaseUrgency(active)))
    return next_phase

def fillScenario(caseNo):
    global scenario
    """scenario1 = [
      [3, 2], [4, 4], [1, 4], [2, 1]
      [2, 1], [4, 4], [1, 4], [3, 2]
      [1, 4], [2, 1], [3, 2], [4, 4]
      [4, 4], [3, 2], [2, 1], [1, 4]
    ]
    """
    for i in range(0, 4):
        #print 'cases/CASE', str(caseNo), 'lane', str(i), '.jpg', 'L'
        #print 'cases/CASE', str(caseNo), 'lane', str(i), '.jpg', 'R'
        scenario[i][0] = noOfVehicles('cases/CASE'+str(caseNo)+'/Lane'+str(i+1)+'.png', 'L')
        scenario[i][1] = noOfVehicles('cases/CASE'+str(caseNo)+'/Lane'+str(i+1)+'.png', 'R')

def signalSlave(active, timer):
    try:
        print 'phase ', str(active), ' will be G for ', str(timer), ' seconds'
        port_no = '/dev/ttyACM'
        ser = [0, 0, 0, 0]
        ser[0] = serial.Serial(port_no+'0', 9600)
        ser[1] = serial.Serial(port_no+'1', 9600)
        ser[2] = serial.Serial(port_no+'2', 9600)
        ser[3] = serial.Serial(port_no+'3', 9600)
        time.sleep(2)
        for i in range(0, 4):
          if i==active:
           ser[i].write('G')
          else: ser[i].write('R')
        time.sleep(1)
        for i in range(0, 4):
          ser[i].write(str(timer))
    except serial.serialutil.SerialException:
        print 'A Slave not connected'

def main():
    """
    fillScenario(1)
    print scenario
    fillScenario(2)
    print scenario
    fillScenario(3)
    print scenario
    fillScenario(4)
    print scenario
    """
    for i in range(1, 5):
        #filling the scenario array
        fillScenario(i)
        i += 1
        print 'vehicles:'
        print scenario
        #taking the decision from decisionMaker
        active = decisionMaker()
        print 'active phase is ', str(active[0]), 'with urgency ', active[1]
        timer = rangeToSeconds(active[1])
        #sending appropriate signals to different arduinos
        signalSlave(active[0], timer)
        redTimes[active[0]] = 0
        for i in range(0, len(phases)):
            if i!=active[0]:
                #signalSlave(i, 'R', timer)
                redTimes[i] += timer
        print 'redTimes are:'
        print redTimes
        time.sleep(timer+3)


if __name__ == '__main__':
    main()
