from pymongo import MongoClient
from flask import Flask,request,jsonify
from bson.json_util import dumps


"""
Initialisation code.
"""
app = Flask(__name__)
client = MongoClient()
db = client.uber
db.food.create_index([("loc", "2dsphere")])


"""
This is a custom Exception class which can be easily extended further for elaborate and detailed response messages.
"""
class InvalidUsage(Exception):
    status_code = 400

    def __init__(self, message, status_code=None, payload=None):
        Exception.__init__(self)
        self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload

    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        return rv


@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response


"""
This function is used to ensure that the values passed in the query are valid. It checks for 3 types of errors: TypeError, ValueError and KeyError.
If the value passed is valid, it returns the value. In cases where passing the value is optional, it returns the default_value passed.
"""
def get_valid_argument(argument_name, default_value=None):
	try:
		return_value = float(request.args[argument_name])
	except TypeError:
		raise InvalidUsage('%s is an invalid argument' %(argument_name), status_code=400)
	except ValueError:
		raise InvalidUsage('%s is an invalid argument' %(argument_name), status_code=400)
	except KeyError:
		if default_value == None:		   #argument_name=="latitude" or argument_name=="longitude":
			raise InvalidUsage('%s is not an optional argument' %(argument_name), status_code=400)	
		else:
			return_value = default_value

	return return_value


"""
This function ensures that the argument value is an integer in addition to the get_valid_argument method and raises an Exception otherwise.
"""
def get_valid_integer_argument(argument_name, default_value):
	return_value=get_valid_argument(argument_name,default_value)
	if int(return_value) != return_value:
		raise InvalidUsage('%s should be an integer' %(argument_name), status_code=400)
	else:
		return int(return_value)


"""
Api end point for searching. Query parameters are as follows:
1.Required parameters: Longitude and Latitude of the location
2.Optional parameters: radius_limit: search radius in meters, sort: sort mode, limit: number of food truck results to return. 
"""
@app.route('/search')
def search_by_location():
	longitude = get_valid_argument('longitude')
	latitude = get_valid_argument('latitude')

	#Optional Arguments
	radius_limit = get_valid_argument('radius_limit', 5000) # Default value = 5km
	if radius_limit<0:
		raise InvalidUsage('radius_limit is a negative argument', status_code=400)
	sort=get_valid_integer_argument(('sort'), 0)	# Default value = 0, sorted based on distance by default		
	limit=get_valid_integer_argument(('limit'), 100)	# Limit on the number of entries to be returned, default=100
	if limit<0:
		raise InvalidUsage('limit is a negative argument', status_code=400)

	cursor = db['food'].find(
	   {
	     'loc':
	       { '$near' :
	          {
	            '$geometry': { 'type': "Point", 'coordinates': [longitude, latitude] },
	            '$maxDistance': radius_limit
	            
	          }
	       }
	   }
	)
	all_trucks = list(cursor)

	#By default, the mongodb query sorts based on distance. Handling the sort parameter, use this in the future to sort based on other parameters.
	if sort == 1:
		for each_truck in all_trucks:
			distance = (each_truck['loc']['coordinates'][0]-longitude)**2-(each_truck['loc']['coordinates'][1]-latitude)**2
			each_truck['distance']=distance
		all_trucks = sorted(all_trucks, key=lambda k: k['distance'])
	
	#Handling the limit parameter		
	all_trucks=all_trucks[:min(limit, len(all_trucks))]

	all_trucks_location_food_type={}
	for each_truck in all_trucks:
		key=each_truck["LocationDescription"]+each_truck['FoodItems']
		if not all_trucks_location_food_type.has_key(key): #To avoid duplicate entries
			each_truck_location_food_type=dict()
			each_truck_location_food_type['LocationDescription']=each_truck["LocationDescription"]
			each_truck_location_food_type['food_type']=each_truck['FoodItems']
			all_trucks_location_food_type[key]=each_truck_location_food_type
		
	return dumps(all_trucks_location_food_type.values())

if __name__ == '__main__':
    app.run()
