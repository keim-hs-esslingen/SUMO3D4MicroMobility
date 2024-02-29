# Route Elevation Mapper

Maps the specified route and draws the electricity consumption or speed over time.

## Usage
In all of the commands replace <SUMO_BINARY> and <SUMO_SCENARIO> with the appropriate paths

- To draw the route and elevation with electricity consumption over time, call (assumes that there is information about the stations in *GBFS_Import/station_information.json*):
```
python main.py -b <SUMO_BINARY> -s <SUMO_SCENARIO> --draw-elevation-time electricityConsumption --origin="4821895#1" --destination="-96266013#0"
```
  - This produces two figures in the folder such as the following:

|<img src=./1_electricityConsumption_elevationOverTime.png alt="Elevation change over time" width=400> | <img src=./2_electricityConsumption_elevationOverTime.png alt="Route" width=400> |
|:-:|:-:|
|Elevation change over time|Route|

- Generate data by simulating the trip, for example:
```
python main.py -b <SUMO_BINARY> -s <SUMO_SCENARIO> --generate="without_elevation.pkl" --origin="4821895#1" --destination="-96266013#0"
```
- (Optional) If you want to compare the results between different setups, you should change the configuration (`.sumocfg`). For instance, you could change the network file to the one with the elevation and run the same command as in the previous step with a different name.
```
python main.py -b <SUMO_BINARY> -s <SUMO_SCENARIO> --generate="with_elevation.pkl" --origin="4821895#1" --destination="-96266013#0"
```
- To draw consumption over time with the generated data call either
```
python main.py --draw-consumption "['./with_elevation.pkl', './without_elevation.pkl']"
```
or
```
python main.py --draw-consumption "['./without_elevation.pkl']"
```
  - This produces the following figure:

|<img src=./consumptionOverTime.png alt="Electricity consumption over time" width=400> |
|:-:|
|Electricity consumption over time|

### Options
```
usage: ConsumptionOverTime [-h] [-b SUMO_BINARY] [-s SUMO_SCENARIO] [-o ORIGIN] [-d DESTINATION] [-g GENERATE] [-c DRAW_CONSUMPTION] [-e DRAW_ELEVATION_TIME]

Maps the route and draws the electricity consumption or speed over time. Either `--generate` or `--draw` option have to be used.

options:
  -h, --help            show this help message and exit
  -b SUMO_BINARY, --sumo-binary SUMO_BINARY
                        Path to sumo or sumo-gui
  -s SUMO_SCENARIO, --sumo-scenario SUMO_SCENARIO
                        Path to sumo scenario ('.sumocfg' file)
  -o ORIGIN, --origin ORIGIN
                        EdgeID from netedit that represents the route origin
  -d DESTINATION, --destination DESTINATION
                        EdgeID from netedit that represents the route destination
  -g GENERATE, --generate GENERATE
                        Generates the data in the given path
  -c DRAW_CONSUMPTION, --draw-consumption DRAW_CONSUMPTION
                        Draws the data at the given paths
  -e DRAW_ELEVATION_TIME, --draw-elevation-time DRAW_ELEVATION_TIME
                        Draws the route and elevation over time with the given property name. Property name should be "electricityConsumption" or "speed"
```
