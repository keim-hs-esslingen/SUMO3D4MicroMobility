# SUMO3D4MicroMobility
A tool-set of Python-scripts to add topological map information to existing Traffic Simulation Models for SUMO (Simulation of Urban Mobility) Web-Link: https://eclipse.dev/sumo/  
The Focus of this tool-set is to add topological map information to Traffic-Simulation Models in order to consider micro-mobility vehicles (such as bikes, e-bikes, e-mopeds and e-scooters) in hilly and steep terrain. 

## Usage:

### Step 1: add topological map information to existing 2D SUMO-Models
```bash
cd Elevation_Adder
python3 main.py
```
For further information and customized usage see ./Elevation_Adder/README.md
If this step worked out fine, a new net.xml file, containing topological map information, was created.
Now this 3D SUMO-Model existing Model can be utilized for any hilly and steep SUMO-Scenario.

### Step 2 (optional): add bike-sharing-Stations from GBFS-Data for station-based micro-mobility scenarios
For further information and customized usage see ./GBFS_Import/README.md

### Step 3 (optional): draw route, elevation and electricity-consumption for e-micro-mobility scenarios
For further information and customized usage see ./Route_Elevation_Mapper/README.md










