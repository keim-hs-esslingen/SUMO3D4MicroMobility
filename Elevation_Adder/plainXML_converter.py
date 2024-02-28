import subprocess
import shutil
import gzip
import os

class PlainXMLConverter:

    def __init__(self, _filepath, _zipFilename, _filename, _plainPath, _plainNodesFile, _plainEdgesFile):
        self.filepath = _filepath
        self.zipFilename = _zipFilename
        self.filename = _filename
        self.plainPath = _plainPath
        self.plainNodesFile = _plainNodesFile
        self.plainEdgesFile = _plainEdgesFile

    def createPlainXML(self):
        print("Create PLAIN XML files ... ", end="")
        self.unzipNetFile()
        os.environ['SUMO_HOME'] = '/usr/share/sumo'
        sh = "netconvert -s " + self.filepath + self.filename + " --plain-output-prefix " + self.filepath + "plainfiles/PLAIN"
        print(sh)
        os.system(sh)
        print("done")

    def unzipNetFile(self):
        print("Unzip net XML file ... ", end="")
        source = self.filepath + self.zipFilename
        print(source)
        destination = self.filepath + self.filename
        print(destination)
        with gzip.open(source, 'rb') as f_in:
            with open(destination, 'wb') as f_out:
                shutil.copyfileobj(f_in, f_out)

        print("done")

    def createNetFileFromPlainFiles(self):
        print("Create net XML file with new elevation data ... ")
        os.environ['SUMO_HOME'] = '/usr/share/sumo'
        sh = "netconvert --node-files=" + self.filepath + self.plainNodesFile + " --edge-files=" + self.filepath + self.plainPath + "PLAIN.edg.xml --connection-files=" + self.filepath + self.plainPath + "PLAIN.con.xml --type-files=" + self.filepath + self.plainPath + "PLAIN.typ.xml --tllogic-files=" + self.filepath + self.plainPath + "PLAIN.tll.xml --output-file=" + self.filepath + "osm.net.xml"
        print(sh)
        os.system(sh)
        print("Done")
        pass

