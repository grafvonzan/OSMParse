import xml.etree.ElementTree as ET
from PIL import Image, ImageDraw

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
	nodeLocList = []
	for item in root.findall('node'):
		nodeList.append(item)
		#finds nodes that have descriptive tags denoting they are map features
		if (item.find('tag') != None):
			nodeLocList.append(item)
	
	wayList = []
	for item in root.findall('way'):
		wayList.append(item)
	
	bounds = tree.find('bounds')
	min = (bounds.get('minlat'), bounds.get('minlon'))
	max = (bounds.get('maxlat'), bounds.get('maxlon'))
	
	
	idDict = {}
	for item in nodeList:
		cord = (item.get('lat'), item.get('lon'))
		id = item.get('id')
		#picked an arbitrary scaling value
		idDict[id] = cord_to_pix(min, max, cord, 10000000)
		
	typeDict = {}
	numberOfTypes = 0
	for item in wayList:
		if

	return osmData
	
def image_gen(idDict, objList, objectType, bounds):
	image = Image.new('RGBA', (bounds[0], bounds[1]), 'white')
	
	for item in objList:
		nodes = item.findall('nd')
		points = []
		for nd in nodes
			#picked an arbitrary road width
			points.append(nd.get('ref'), width = '10')
		
		draw = ImageDraw.Draw(image)
		draw.line(points)
	
	#this should get the name of the type of objects in the object list
	#assumes the object list consists of objects of the same type
	listType = (objList[0].find('tag').items())[0][0]
	
	image.save(objectType + '.png')

#maps coordinates in a bounded space to pixel locations in an image.
def cord_to_pix(min, max, cord, scale):
	
	minlat = min[0]
	minlon = min[1]
	maxlat = max[0]
	maxlon = max[1]
	
	offsetlat = maxlat - minlat
	offsetlon = maxlon - minlon
	
	offsetCordlat = cord[0] - minlat
	offsetCordlon = cord[1] - minlon
	
	scalelat = offsetCordlat / offsetlat
	scalelon = offsetCordlon / offsetlon
	
	pixX = round(scale * scalelat)
	pixY = round((scale * (offsetCordlon / offsetCordlat)) * scalelon)
	
	pix = (pixX, pixY)
	
	return pix
	
#handle what to do when the script is called
def main():
	parseOut = parse_XML("map.osm.xml")
	
	#output all the ways
	for item in parseOut[2]:
		print(item.attrib)
		print("\n")
	
#call main
if __name__ == "__main__":
	main()
	