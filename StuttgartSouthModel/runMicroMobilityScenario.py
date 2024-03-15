import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci

traci.start(["sumo-gui", "-c", "osm.sumocfg"])

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
traci.close()  
