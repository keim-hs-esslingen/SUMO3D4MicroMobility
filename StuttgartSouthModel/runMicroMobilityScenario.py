import os
import sys
if 'SUMO_HOME' in os.environ:
    sys.path.append(os.path.join(os.environ['SUMO_HOME'], 'tools'))
import traci

traci.start(["sumo-gui", "-c", "osm.sumocfg"])

# read maximum battery capacity [Wh]
maxBatteryCapacity= float(traci.vehicle.getParameter(str("test_ebike"),"device.battery.maximumBatteryCapacity"))

# set battery to 100% SOC-Level
traci.vehicle.setParameter(str("test_ebike"),"device.battery.actualBatteryCapacity",maxBatteryCapacity)

while traci.simulation.getMinExpectedNumber() > 0:
    traci.simulationStep()
    actualBatteryCapacity = (float(traci.vehicle.getParameter(str("test_ebike"),"device.battery.actualBatteryCapacity")))
    print("SOC[%]: ",str(round(actualBatteryCapacity/maxBatteryCapacity *100,2)))
    print("3D-Position[m]",traci.vehicle.getPosition3D("test_ebike"))
    print("total consumed Energy[Wh] ", traci.vehicle.getParameter(str("test_ebike"),"device.battery.totalEnergyConsumed"))
traci.close()  
