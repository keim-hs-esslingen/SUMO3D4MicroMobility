import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci

traci.start(["sumo-gui", "-c", "osm.sumocfg"])

# read maximum battery capacity
maxBatteryCapacity= float(traci.vehicle.getParameter(str("test_ebike"),"device.battery.maximumBatteryCapacity"))

# set battery to 100% SOC-Level
traci.vehicle.setParameter(str("test_ebike"),"device.battery.actualBatteryCapacity",maxBatteryCapacity)


while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    actualBatteryCapacity = (float(traci.vehicle.getParameter(str("test_ebike"),"device.battery.actualBatteryCapacity")))
    print("SOC: ",str(round(actualBatteryCapacity/maxBatteryCapacity *100,2)))
    print("3D-Position: ",traci.vehicle.getPosition3D("test_ebike"))
traci.close()  
