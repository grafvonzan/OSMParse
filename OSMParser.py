import xml.etree.ElementTree as ET

#Straight Outta an Internet Tutorial
#WARNING! This function uses a module that is not secure against maliciously constructed data!
def parse_XML(xmlfile):
	
	#use prebuilt parser to make a tree out of the XML file
	tree = ET.parse(xmlfile)
	
	root = tree.getroot()
	
	#create data structure to hold all of the elements in a convinient way
	#XML is inherently tree like, but OSM creates very short, extremely wide trees.
	osmData = []
	
	
	nodeList = []
	for item in root.findall('node'):
		nodeList.append(item)
	osmData.append(nodeList)
	
	wayList = []
	for item in root.findall('way'):
		wayList.append(item)
	osmData.append(wayList)
	
	return osmData
	
#handle what to do when the script is called
def main():
	parseOut = parse_XML("map.osm.xml")
	
	#output all the ways
	for item in parseOut[1]:
		print(item.attrib)
		print("\n")
	
#call main
if __name__ == "__main__":
	main()
	