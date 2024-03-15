# SUMO3D4MicroMobility
A tool-set of Python-scripts to add topological map information to existing Traffic Simulation Models for SUMO (Simulation of Urban Mobility) Web-Link: https://eclipse.dev/sumo/  
The Focus of this tool-set is to add topological map information to Traffic-Simulation Models in order to consider micro-mobility vehicles (such as bikes, e-bikes, e-mopeds and e-scooters) in hilly and steep terrain. 

## Reqirements to use the SUMO3D4MicroMobility tool-set:

- Python 3.11.5 or higher
- Eclipse SUMO Version 1.19.0 or higher (Download from https://www.eclipse.org/sumo )
- The environment varibale SUMO_HOME must be set proberly (e.g. export SUMO_HOME="/usr/share/sumo")

### Clone the SUMO3D4MicroMobility Repo:

```bash
git clone https://github.com/keim-hs-esslingen/SUMO3D4MicroMobility
cd SUMO3D4MicroMobility
```

### Some Python Packages need to be installed:

```bash
sudo pip3 install -r requirements.txt
```
Hint: the requirements.txt file may not be complete, so maybe you have to install further packages if error messages arise

## Usage of the SUMO3D4MicroMobility tool-set :

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










