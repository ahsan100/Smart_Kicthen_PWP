'''
CREATED on 24 May 2016
Provides WEB API TESTING
'''
import unittest, copy
import json

import flask

import resources as resources
import database as database

DB_PATH = 'db/forum_test.db'
Engine = database.Engine(DB_PATH)

COLLECTIONJSON = "application/vnd.collection+json"
HAL = "application/hal+json"
MEMBER_PROFILE ="/profiles/member-profile"
INVENTORY_PROFILE = "/profiles/inventory"
RECIPE_PROFILE = "/profiles/recipe"
LIST_PROFILE = "/profiles/listproduct"
GROUP_PROFILE ="/profiles/group"
LOCATION_PROFILE ="/profiles/location"
SEARCH_PROFILE ="/profiles/search"
MONITOR_PROFILE ="/profiles/monitor"

resources.app.config['TESTING'] = True

resources.app.config['SERVER_NAME'] = 'localhost:5000'

resources.app.config.update({'Engine': Engine})

initial_members = 5
initial_groups = 3
initial_inventory = 14
initial_recipe = 5

class ResourcesAPITestCase(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		print "Testing Start: ", cls.__name__
		Engine.remove_db()
		Engine.create_table()

	@classmethod
	def tearDownClass(cls):
		print "Testing Ended : ", cls.__name__
		Engine.remove_db()

	def setUp(self):
		Engine.data_table()
		self.connection = Engine.connect()

	def tearDown(self):
		self.connection.close()
		Engine.clear_table()

class MembersTestCase (ResourcesAPITestCase):

	#Existing member
	member1_ID = 1
	member1_request = {"member": {"dob": "030191", "phone": "+358413660505", 
					"email": "ahsan.manzoor@student.oulu.fi", "name": "Ahsan Manzoor", 
					"gender": "Male"}}

	#Non exsiting member
	member2_request = {"member": {"dob": "030191", "phone": "+358413660505", 
					"email": "ahsan.manzoor@student.oulu.fi", "name": "Ahsan Manzoor", 
					"gender": "Male"}}

	url = "/forum/api/member/"

	def test_url(self):
		print '('+self.test_url.__name__+')', self.test_url.__doc__,
		with resources.app.test_request_context(self.url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Member)

if __name__ == '__main__':
    print 'Start running WEB API tests'
    unittest.main()