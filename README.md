# os-simples
Methods for simplifying geospatial data

Scripts in here use python 2.7.18 and shapely 1.6.4

Simplifier.py takes a geojson file as input and uses the shapely simplify method to smooth a polygon boundary.

Syntax for the script is 'Simplifier.py <input_file> <tolerance> <output_file)'. The input file should be in the same directory as Simplifier.py, otherwise use a full path to the file. Tolerance is an integer value representing the metre tolerance that will be used for smoothing (ie the minimum distance permitted between vertices). Output file will be written to the same directory as the python script.

If Simplifier.py is called with a single argument (or if a geojson file is dropped onto the application in an explorer window) the process will use a default tolerance of 25 and write to a file called output.geojson.
