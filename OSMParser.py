import xml.etree.ElementTree as ET
import math
from PIL import Image, ImageDraw

#GLOBAL VARIABLES BAD OOP GOOD
#radius of the earth in meters
SCALE = 1000


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
	min = (float(bounds.get('minlat')), float(bounds.get('minlon')))
	max = (float(bounds.get('maxlat')), float(bounds.get('maxlon')))
	
	#types of ways we care about
	typeList = ["highway", "building", "barrier"]
	typeDict = {'highway' : 0, 'building' : 1, 'barrier' : 2, 0 : 'highway', 1 : 'building', 2 : 'barrier'}
	
	
	#build data structure
	highwayList = []
	buildingList = []
	barrierList = []
	
	osmData.append(highwayList)
	osmData.append(buildingList)
	osmData.append(barrierList)
	
	ratio = 0
	#map nodes to pixel coordinates
	idDict = {}
	for item in nodeList:
		cord = (item.get('lat'), item.get('lon'))
		id = item.get('id')
		#picked an arbitrary scaling value
		pix = cord_to_pix(min, max, cord, SCALE)
		ratio = pix[2]
		idDict[id] = (pix[0], pix[1])

	
	#populate datastructure with ways
	for item in wayList:
		tagList = []
		if(item.find('tag') != None):
			tagList = item.findall('tag')
			for tag in tagList:
				if tag.items()[0][1] in typeList:
					osmData[typeDict[tag.items()[0][1]]].append(item)
					break
	
	
	#generate maps
	counter = 0
	bounded = True;
	for item in osmData:
		#highways are not polygons
		if (counter == 0):
			bounded = True
		else:
			bounded = False
		image_gen(idDict, item, bounds, typeDict[counter], bounded, ratio)
		counter = counter + 1
		
			

	return osmData
	
def image_gen(idDict, objList, bounds, name, bounded, ratio):
	image = Image.new('RGBA', (int(SCALE*1.1), int(SCALE * ratio* 1.1)), 'white')
	
	count = 0
	for item in objList:
		nodes = item.findall('nd')
		points = []
		for nd in nodes:
			#picked an arbitrary road width
			#print(idDict[nd.get('ref')])
			points.append(idDict[nd.get('ref')])
		
		draw = ImageDraw.Draw(image)
		if(bounded):
			draw.line(points, fill = 'black', width = 1)
		else:
			draw.polygon(points, fill = 'black')
		
		count = count + 1
		
	string = name + '.png'
	
	
	
	image = image.rotate(180)
	image.transpose(Image.FLIP_LEFT_RIGHT).save(string)

#maps coordinates in a bounded space to pixel locations in an image.
def cord_to_pix(min, max, cord, scale):
	
	minlat = float(min[0])
	minlon = float(min[1])
	maxlat = float(max[0])
	maxlon = float(max[1])
	
	#convert to cartesian
	#radius of earth in meters
	r = 6371000
	centerlat = ((maxlat-minlat)/2) + minlat
	
	minx = r*minlon*math.cos(math.radians(centerlat))
	miny = r*minlat
	maxx = r*maxlon*math.cos(math.radians(centerlat))
	maxy = r*maxlat
	
	
	locx = r*float(cord[1])*math.cos(math.radians(centerlat))
	locy = r*float(cord[0])
	
	offsetx = maxx - minx
	offsety = maxy - miny
	
	offsetCordx = locx - minx
	offsetCordy = locy - miny
	
	scalex = offsetCordx / offsetx
	scaley = offsetCordy / offsety
	
	pixY = round(scale * scaley)
	pixX = round(scale * scalex * (abs(offsetx)/abs(offsety)))
	
	ratio = (abs(offsetx)/abs(offsety))
	
	pix = (pixX, pixY, ratio)
	
	return pix
	

	
#handle what to do when the script is called
def main():
	parseOut = parse_XML("map.osm.xml")
	
	#output all the ways
	#for item in parseOut[2]:
	#	print(item.attrib)
	#	print("\n")
	
#call main
if __name__ == "__main__":
	main()
	