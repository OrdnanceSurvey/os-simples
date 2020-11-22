import shapely
from shapely.geometry import shape, MultiPoint
import numpy as np

import json
import geojson
import sys
import os
from datetime import datetime

# check the number of arguments
numargs = len(sys.argv)

# set the current directory in case we need to use it
current_directory=os.path.dirname(os.path.abspath(__file__))

# total arguments should be three, including the python script name it should be four
# if just a filename is given (ie a file dropped onto the script) use defaults (could read from a config)
if(numargs==4):
  # add some checks around this lot
  infile = str(sys.argv[1])
  tolerance = int(sys.argv[2])
  output_file = str(sys.argv[3])
elif(numargs==2):
  # use defaults
  infile = str(sys.argv[1])
  tolerance = 25
  output_file = current_directory+'\output.geojson'
else:
  print("\nWrong number of arguments, must be three!!")
  print("\nUsage: Simplifier <infile> <tolerance> <outfile>")
  print("   eg: Simplifier scotland.geojson 100 scotland_100.geojson")
  print("   or: Simplifier  wales.geojson 50 wales_50.geojson")
  print("\nIf the tolerance is set to zero, the process will attempt a convex hull from the input")
  print("\nAssumes files are in the same directory as this script. Use full paths to access remote files")

  # pause for user input and then exit with a return value
  os.system('pause')
  os._exit(2)

# validate existence of input file

# read the input file
print("\n\nReading "+infile)

# we're assuming json input, otherwise we're a bit buggered
# would probably make sense to include a check on the format/quality of the selected file
with open(infile) as f:
  data = json.load(f)
f.close()
 
# there is only one feature in our test input file (single coastline)
# but this will allow for multiple features should we so wish
for feature in data['features']:
  data_properties = feature['properties']
  coastline = feature['geometry']
  
  # get the geometry from the geojson
  s = shape(coastline)
  
  # if the tolerance is zero, attempt a convex hull instead of a simplify
  if(tolerance>0):
    # simplify the geometry by setting a minimum distance between nodes
    # and remove any that are too close
    generalised_polygon = s.simplify(tolerance, preserve_topology = False)
  else:
    # sadly, this will fail on a MultiPolygon geometry, so it will need some more work
    try:
      points = MultiPoint(s.boundary.coords)
      # points = np.array(s) - this won't work with the convex_hull because convex_hull isn't a method on a numpy array
      generalised_polygon = points.convex_hull()
    except:
      print("\nThat didn't work at all well!!")
      print("\nA multi-part geometry doesn't provide a coordinate sequence")
      os._exit(3)

# this needs to be in the loop if we're really going to write individual features

# write out to new file
print('\nWriting to output file '+output_file+'...')

with open(output_file, 'w') as outfile:
  # fudged output for now to make sure we get a valid file
  # this bit would be the header, which should be written outside of the loop
  outfile.write("{")
  outfile.write('"type": "FeatureCollection",')
  
  # name would be added as a parameter, it won't always be Scotland
  outfile.write('"name": "scottish_mainland",')
  outfile.write('"crs": { "type": "name", "properties": { "name": "urn:ogc:def:crs:EPSG::27700" } },')
  outfile.write('"features": [')
  
  # this is kind of where the individual output features would start writing
  outfile.write('{ "type": "Feature", "properties":')
  geojson.dump(data_properties, outfile)
  outfile.write(', "geometry": ')
  geojson.dump(generalised_polygon, outfile)
  
  # this will need a comma after the brace if there's going to be another feature
  outfile.write('}')
  
  # this closes off the collection
  outfile.write(']')
  # and this closes off the json document
  outfile.write('}')

# and this just says goodnight and thanks for all the fish
print("\nDone...\n")

# pause here to keep the window open (in case user has dropped a file onto the executable)
os.system('pause')

# and exit with a return value of 0 (success!)
os._exit(0)

# various functions to be populated as necessary
# would be better in a separate script really, but they're fine here as placeholders

def validate_file(filename):
  # do some validation to make sure the file is what we expect
  return(true)
  
def grid_points(in_array):
  # run an array of x,y points against a square grid
  return(some_value)
  
def set_header():
  # set a header section for the output file
  return(the_header)
  
def set_precision(x,y,precision):
  # set the precision for the point coordinates
  x=round(x,precision)
  y=round(y,precision)
  return(x,y)
