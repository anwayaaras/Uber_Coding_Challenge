import main_server as server
import unittest
import json

class ServerTestCase(unittest.TestCase):

    def setUp(self):
        server.app.config['TESTING'] = True
        self.app = server.app.test_client()

    def test_no_longitude(self):
        response = self.app.get('/search?latitude=37.7428202346759')
        self.assertEqual(json.loads(response.data)["message"], 'longitude is not an optional argument')
        self.assertEqual(response.status_code, 400)

    def test_invalid_longitude(self):
        response = self.app.get('/search?longitude=-122.382_invalid_string&latitude=37.7428202346759')
        self.assertEqual(json.loads(response.data)["message"], 'longitude is an invalid argument')
        self.assertEqual(response.status_code, 400)

    def test_no_latitude(self):
        response = self.app.get('/search?longitude=-122.382847355518')
        self.assertEqual(json.loads(response.data)["message"], 'latitude is not an optional argument')
        self.assertEqual(response.status_code, 400)

    def test_invalid_latitude(self):
     	response = self.app.get('/search?longitude=-122.382847355518&latitude=invalid_string')
    	self.assertEqual(json.loads(response.data)["message"], 'latitude is an invalid argument')
        self.assertEqual(response.status_code, 400)

    def test_invalid_radius_limit(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&radius_limit=invalid_string')
        self.assertEqual(json.loads(response.data)["message"], 'radius_limit is an invalid argument')
        self.assertEqual(response.status_code, 400)

    def test_negative_radius_limit(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&radius_limit=-500')
        self.assertEqual(json.loads(response.data)["message"], 'radius_limit is a negative argument')
        self.assertEqual(response.status_code, 400)

    def test_invalid_sort(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&sort=invalid_string')
        self.assertEqual(json.loads(response.data)["message"], 'sort is an invalid argument')
        self.assertEqual(response.status_code, 400)

    def test_sort_not_an_integer(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&sort=10.08')
        self.assertEqual(json.loads(response.data)["message"], 'sort should be an integer')
        self.assertEqual(response.status_code, 400)

    def test_invalid_limit(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&limit=invalid_string')
        self.assertEqual(json.loads(response.data)["message"], 'limit is an invalid argument')
        self.assertEqual(response.status_code, 400)

    def test_negative_limit(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&limit=-100')
        self.assertEqual(json.loads(response.data)["message"], 'limit is a negative argument')
        self.assertEqual(response.status_code, 400)

    def test_limit_not_an_integer(self):
        response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&limit=12.48')
        self.assertEqual(json.loads(response.data)["message"], 'limit should be an integer')
        self.assertEqual(response.status_code, 400)


    def test_valid_1(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759')
        self.assertEqual(response.status_code, 200)

    def test_valid_2(self):
    	response = self.app.get('/search?longitude=-122&latitude=37')
        self.assertEqual(response.status_code, 200)

    def test_valid_3(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&radius_limit=500')
        self.assertEqual(response.status_code, 200)

    def test_valid_4(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&sort=2')
        self.assertEqual(response.status_code, 200)

    def test_valid_5(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&limit=100')
        self.assertEqual(response.status_code, 200)

    def test_valid_6(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&limit=100000')
        self.assertEqual(response.status_code, 200)

    def test_valid_7(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&radius_limit=100&limit=100')
        self.assertEqual(response.status_code, 200)

    def test_valid_8(self):
    	response = self.app.get('/search?longitude=-122.382847355518&latitude=37.7428202346759&radius_limit=100&sort=0&limit=100')
        self.assertEqual(response.status_code, 200)

    def test_valid_9(self):
    	response = self.app.get('/search?longitude=-123.382847355518&latitude=40.7428202346759&radius_limit=100&sort=0&limit=10')
        self.assertEqual(response.status_code, 200)











if __name__ == '__main__':
    unittest.main()