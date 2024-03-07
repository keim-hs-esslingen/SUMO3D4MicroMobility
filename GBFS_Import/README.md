# The GBFS-Import Script 

This script converts positions of bike-sharing stations from GBFS json Data (e.g. from https://apis.deutschebahn.com)
For further information see: https://github.com/MobilityData/gbfs


## Usage-example 
```bash
python3 convertGBFSbikeStations2SUMO.py --stations ./station_information.json --net ../StuttgartSouthModel/osm.net.xml 

```

## Options:
  -h, --help            show this help message and exit
  --stations GBFSSTATIONSJSON
                        JSON File containing the Bikesharing Stations from GBFS
  --net NET_FILE        SUMO network file.
  --output OUTPUT_FILE  Output File for GBFS Bikesharing Stations
  --offset ID_OFFSET    Offset for the POI-Id
  --color POI_COLOR     POI-Color for the Bikesharing Stations
