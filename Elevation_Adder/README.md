# The Elevation Adder Scripts

## Usage
To use these elevation-adder scripts for custom models, follow these steps:
* copy your custom model to /SUMO3D4MicroMobility/myModel/
* run netconvert for the net-file
```bash
cd /SUMO3D4MicroMobility/myModel/
netconvert -s osm.net.xml --plain-output-prefix Plain
```
* move plain-files (created by netconvert) to a subfolder
```bash
mkdir plainfiles
mv Plain* ./plainfiles
```
* Adjust the file-paths in main.py
* Afterwards run main.py
```bash
python3 main.py
```

## Please Note: 
The used Open Topo Data REST-service may be limited for a certain number of nodes at once.





