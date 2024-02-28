
from elevation_adder import ElevationAdder
from plainXML_converter import PlainXMLConverter

def main():
    filepath = "../StuttgartSouthModel/"
    zipFilename = "osm.net.xml.gz"
    netFilename = "osm.net.xml"
    plainPath = "../StuttgartSouthModel/plainfiles/"
    plainNodesFile = "plainfiles/PLAIN.nod.xml"
    plainEdgesFile = "plainfiles/PLAIN.edg.xml"
    plainXML_converter = PlainXMLConverter(filepath, zipFilename, netFilename, plainPath, plainNodesFile, plainEdgesFile)
    plainXML_converter.createPlainXML()
    elevation_adder = ElevationAdder(filepath, netFilename, plainNodesFile, plainEdgesFile)
    elevation_adder.addElevations()
    plainXML_converter.createNetFileFromPlainFiles();

if __name__ == "__main__":
    main()
