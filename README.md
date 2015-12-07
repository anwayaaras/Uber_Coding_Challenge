#Uber Coding challenge
I chose to implement the food trucks service that tells the user what types of food trucks might be found near a specific location on a map. As a fresh graduate out of UCSD, all my industry experience comes from solely from my internships. Additionally, this is my finals week and I have two finals tomorrow. Hence, I couldn’t devote a lot of time to this coding challenge.  Please do take these two things into consideration while evaluating my code.

So here’s all you need to know about this service!

I have used Python for my backend. It is a REST API which uses Flask to route requests. For my database I have used MongoDB. Since we have geo-spatial data and we have many complicated queries in the future, I chose MongoDB since it can provide efficient processing of such data. During my research, I also discovered that Uber uses MongoDB as well. So win-win!

MongoDB can be initialized with json data. However, to exploit MongoDB’s geo spatial methods, the data needs to be formatted to include a location parameter in a particular format:
Example:
```
“loc": {
    "type": "Point", 
    "coordinates": [-122.377797368962, 37.7438311721327]
    }
```
For our needs, we just need ‘point’. But this can be easily extended to other geometries if needed in the future. For getting data in this format, I downloaded the data on the website as a csv file and converted it into JSON which includes the above field.

### Instructions to run this code
To run the service you need the following installed on your system:

1. PyMongo
2. MongoDB
3. flask

This is the order of scripts to be executed(assuming all the the files were downloaded correctly from this directory) :
1. Create an instance of mongoDB (command- mongod)
2. Run import.sh to insert the food.json file on to the database.
3. Run the server code: python main_server.py
4. Hit it with your search query as per the format specified in API docs.
5. View the results!
6. Run the test.py script to test the code.


Here is what each script does:
* _food.csv_ - The given data was extracted from the website as a csv file. 

* _csv_to_json.py_ - Converts the csv files into a json file. The json file available on the SF data website contained a lot of unnecessary meta data. Hence, I implemented this code to clean and preprocess the data.

* _food.json_ - Contains the data in form of a json file.

* _import.sh_ - Uploading the food.json file onto the database. I’ve used MongoDB. Database is named “Uber” and collection is named “food”

* _main_server.py_ - This is the main code to be deployed on the server. It contains the search method with all the functionalities as described in API docs.

Things to note about main_server.py :

1. Code has been designed with extensibility in mind. Parameters like sort,radius_limit, limit have been initialised to default values. However, they can be easily extended in the future to fine tune the search truck results.

2. Error checking has been implemented for numerous scenarios that may not necessarily be encountered with the given database.

3. The data had multiple entries for the same location with different licence status. Since, the problem statement expected food trucks near a given location, duplicate entries have been omitted.

* _test.py_ - Various test cases for the search api.


With my limited experience and the given amount of time, this was all I could do. Hope it suffices!


