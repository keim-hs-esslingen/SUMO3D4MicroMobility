import argparse
import os
import sys
import lxml.etree as ET
import json

if "SUMO_HOME" in os.environ:
    sys.path.append(os.path.join(os.environ["SUMO_HOME"], "tools"))
    import sumolib
else:
    sys.exit("please declare the environment variable 'SUMO_HOME'")


def get_options(cmd_args=None):
    """Argument Parser"""
    parser = argparse.ArgumentParser(
        prog="convertGBFSbikeStations2SUMO",
        usage="%(prog)s [options]",
        description="Extract Parking Areas from OSM.",
    )
    parser.add_argument(
        "--stations", type=str, dest="gbfsStationsJSON", required=True, help="JSON File containing the Bikesharing Stations from GBFS"
    )
    parser.add_argument(
        "--net", type=str, dest="net_file", required=True, help="SUMO network file."
    )
    parser.add_argument(
        "--output", type=str, dest="output_file", required=False, help="Output File for GBFS Bikesharing Stations", default="GBFS_bikesharingStations.xml"
    )
    parser.add_argument(
        "--offset", type=str, dest="id_offset", required=False, help="Offset for the POI-Id", default="8000000"
    )
    parser.add_argument(
        "--color", type=str, dest="poi_color", required=False, help="POI-Color for the Bikesharing Stations", default="200,0,0"
    )
    return parser.parse_args(cmd_args)



def main(cmd_args):
    """ Converte Bikesharing- Stations from GBFS to SUMO POIs"""
    options = get_options(cmd_args)
    net = sumolib.net.readNet(options.net_file)
    
    try:
        with open(options.gbfsStationsJSON) as jsonFile:
            bikeSharingStationsFromGBFS = json.load(jsonFile).get("data").get("stations")

            xml_output = ET.Element("additional")
            poiIndex = 1

            for station in bikeSharingStationsFromGBFS:
                lon = station.get("lon")
                lat = station.get("lat")
                stationXY = net.convertLonLat2XY(lon,lat)
                poi_Id = str(int(options.id_offset) + poiIndex)
                poiIndex = poiIndex + 1 
                ET.SubElement(
                xml_output,
                "poi",
                id=poi_Id,
                type = "amenity.bicycle_rental",
                color = options.poi_color,
                layer = "5.00",    
                x= str(stationXY[0]),
                y= str(stationXY[1]),
                lon = str(lon),    
                lat = str(lat),
                stationID = station.get("station_id"),
                capacity = str(station.get("capacity"))    
                )

            jsonFile.close()

            tree = ET.ElementTree(xml_output)

            # formatting and writing the xml file
            tree.write(
                options.output_file,
                encoding="UTF-8",
                xml_declaration=True,
                pretty_print=True,
            )
            print("The Bikesharing- Stations from GBFS were successfully converted to SUMO POIs")
    except IOError:
        print("The Input-JSON File couldn't be read properly")

    

if __name__ == "__main__":
    main(sys.argv[1:])





    
