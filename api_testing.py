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
SHOP_PROFILE = "/profiles/shop"

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
		print "Testing Start: ", cls.__name__ ,"\n" 
		Engine.remove_db()
		Engine.create_table()

	@classmethod
	def tearDownClass(cls):
		print "Testing Ended : ", cls.__name__, "\n"
		Engine.remove_db()

	def setUp(self):
		Engine.data_table()
		self.app_context = resources.app.app_context()
		self.app_context.push()
		self.client = resources.app.test_client()
		#self.connection = Engine.connect()

	def tearDown(self):
		Engine.clear_table()
		self.app_context.pop()

class MembersTestCase (ResourcesAPITestCase):

	#Existing member
	member1_request = {"member": {"dob": "030191", "phone": "+358413660505", 
					"email": "ahsan.manzoor@student.oulu.fi", "name": "Ahsan Manzoor", 
					"gender": "Male"}}
	member1_mod = {"phone": "12345"}
	def setUp(self):
		super(MembersTestCase, self).setUp()
		member_ID = 1
		wrong_ID = -2
		self.url= resources.api.url_for(resources.Member,memberid=member_ID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Member,memberid=wrong_ID,_external=False)
	
	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/member/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Member)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_member_mimetype(self):
		print '('+self.test_get_member_mimetype.__name__+')', self.test_get_member_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+MEMBER_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		data = json.loads(resp.data)
		
		attributes = ('member', 'href', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		member = data['member']
		self.assertDictContainsSubset(member,self.member1_request['member'])

	def test_delete_member(self):

		print '('+self.test_delete_member.__name__+')', self.test_delete_member.__doc__
		resp = self.client.delete(self.url)
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 404)

	def test_delete_nonexisting_member(self):

		print '('+self.test_delete_nonexisting_member.__name__+')', self.test_delete_nonexisting_member.__doc__
		resp = self.client.delete(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_modify_member(self):
		print '('+self.test_modify_member.__name__+')', self.test_modify_member.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.member1_mod),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 200)
		data = json.loads(resp2.data)
		self.assertEquals(data['member']['phone'],self.member1_mod['phone'])

	def test_modify_nonexisting_member(self):

		print '('+self.test_modify_nonexisting_member.__name__+')', self.test_modify_nonexisting_member.__doc__
		resp = self.client.put(self.url_wrong,data=json.dumps(self.member1_mod),headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 404)

class Search_MembersTestCase (ResourcesAPITestCase):

	def setUp(self):
		super(Search_MembersTestCase, self).setUp()
		member_EMAIL = 'ahsan.manzoor@student.oulu.fi'
		wrong_EMAIL = 'wrong@student.oulu.fi'
		self.url= resources.api.url_for(resources.Search_Member,email=member_EMAIL,_external=False)
		self.url_wrong = resources.api.url_for(resources.Search_Member,email=wrong_EMAIL,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/search_members/ahsan.manzoor@student.oulu.fi"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Search_Member)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_searchmember_mimetype(self):
		print '('+self.test_get_searchmember_mimetype.__name__+')', self.test_get_searchmember_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+SEARCH_PROFILE)

class User_LoginTestCase (ResourcesAPITestCase):

	user1= {
		"email":"ahsan.manzoor@student.oulu.fi",
		"password":"ahsan123"
	}

	wrong_user = {
		"email":"test@student.oulu.fi",
		"password":"test"
	}

	wrong_password = {
		"email":"ahsan.manzoor@student.oulu.fi",
		"password":"wrong"
	}
	
	def setUp(self):
		super(User_LoginTestCase, self).setUp()
		self.url= resources.api.url_for(resources.User_Login)

	def test_login_user(self):
		print '('+self.test_login_user.__name__+')', self.test_login_user.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.user1),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 200)

	def test_login_wrong_type(self):
		print '('+self.test_login_wrong_type.__name__+')', self.test_login_wrong_type.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.user1),headers={"Content-Type": "application/json"})
		self.assertEquals(resp.status_code, 415)

	def test_login_unexisting_user(self):
		print '('+self.test_login_unexisting_user.__name__+')', self.test_login_unexisting_user.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.wrong_user),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 404)

	def test_login_wrong_password(self):
		print '('+self.test_login_wrong_password.__name__+')', self.test_login_wrong_password.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.wrong_password),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 401)


class New_UserTestCase (ResourcesAPITestCase):

	NEW_USER_EMAIL = 'new.user@student.oulu.fi'
	USER1={'name': 'kaleema',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295',
			'email': NEW_USER_EMAIL,
			'password': 'test'}

	WRONG_EMAIL = 'ahsan.manzoor@student.oulu.fi'
	WRONG_USER = {'name': 'Ahsan Manzoor',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295',
			'email': WRONG_EMAIL,
			'password': 'test'}


	def setUp(self):
		super(New_UserTestCase, self).setUp()
		self.url= resources.api.url_for(resources.New_User)

	def test_new_user(self):
		print '('+self.test_new_user.__name__+')', self.test_new_user.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.USER1),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)

	def test_newuser_wrong_type(self):
		print '('+self.test_newuser_wrong_type.__name__+')', self.test_newuser_wrong_type.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.USER1),headers={"Content-Type": "application/json"})
		self.assertEquals(resp.status_code, 415)

	def test_newuser_wrong_user(self):
		print '('+self.test_newuser_wrong_user.__name__+')', self.test_newuser_wrong_user.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.WRONG_USER),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 400)

class Group_Member_TestCase (ResourcesAPITestCase):

	GROUP1_REQ = {"group": [{"href": "/api/member/1", "data": [{"name": "membername", "value": "Ahsan Manzoor"}], "read-only": True}, {"href": "/api/member/2", "data": [{"name": "membername", "value": "Awais Aslam"}], "read-only": True}]}

	NEW_USER_EMAIL = 'new.user@student.oulu.fi'
	USER1={'name': 'kaleema',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295',
			'email': NEW_USER_EMAIL,
			'password': 'test'}

	WRONG_POST = {"memberid": 2}

	GROUP_POST = {"memberid": 6}

	def setUp(self):
		super(Group_Member_TestCase, self).setUp()
		GROUPID = 1
		WRONG_GROUPID = -2
		self.url= resources.api.url_for(resources.Group_Member,groupid=GROUPID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Group_Member,groupid=WRONG_GROUPID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/group_member/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Group_Member)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_groupmember_mimetype(self):
		print '('+self.test_get_groupmember_mimetype.__name__+')', self.test_get_groupmember_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),COLLECTIONJSON+";"+GROUP_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["group"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.GROUP1_REQ)

	def test_new_groupmember(self):
		print '('+self.test_new_groupmember.__name__+')', self.test_new_groupmember.__doc__
		newuser_url= resources.api.url_for(resources.New_User)
		resp = self.client.post(newuser_url,data=json.dumps(self.USER1),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)
		resp = self.client.post(self.url,data=json.dumps(self.GROUP_POST),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)

	def test_groupmember_wrong_type(self):
		print '('+self.test_groupmember_wrong_type.__name__+')', self.test_groupmember_wrong_type.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.GROUP_POST),headers={"Content-Type": "application/json"})
		self.assertEquals(resp.status_code, 415)

	def test_groupmember_wrong_memberid(self):
		print '('+self.test_groupmember_wrong_memberid.__name__+')', self.test_groupmember_wrong_memberid.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.WRONG_POST),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 400)

class Group_TestCase (ResourcesAPITestCase):

	GROUP1_REQ = {"group": [{"href": "/api/group/1", "data": [{"name": "groupname", "value": "admins"}], "read-only": True}]}

	MODIFY_GROUPNAME = {'name': "newnaming"}

	WRONG_GROUPNAME = {'name': None}

	def setUp(self):
		super(Group_TestCase, self).setUp()
		GROUPID = 1
		WRONG_GROUPID = -2
		self.url= resources.api.url_for(resources.Group,groupid=GROUPID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Group,groupid=WRONG_GROUPID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/group/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Group)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_group_mimetype(self):
		print '('+self.test_get_group_mimetype.__name__+')', self.test_get_group_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+GROUP_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["group"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.GROUP1_REQ)

	def test_delete_group(self):

		print '('+self.test_delete_group.__name__+')', self.test_delete_group.__doc__
		resp = self.client.delete(self.url)
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 404)

	def test_delete_nonexisting_group(self):

		print '('+self.test_delete_nonexisting_group.__name__+')', self.test_delete_nonexisting_group.__doc__
		resp = self.client.delete(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_modify_group(self):
		print '('+self.test_modify_group.__name__+')', self.test_modify_group.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_GROUPNAME),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 200)
		data = json.loads(resp2.data)
		self.assertEquals(data["group"][0]["data"][0]["value"],self.MODIFY_GROUPNAME['name'])

	def test_modify_nonexisting_group(self):

		print '('+self.test_modify_nonexisting_group.__name__+')', self.test_modify_nonexisting_group.__doc__
		resp = self.client.put(self.url_wrong,data=json.dumps(self.MODIFY_GROUPNAME),headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 404)

	def test_modify_wrong_group(self):
		print '('+self.test_modify_wrong_group.__name__+')', self.test_modify_wrong_group.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.WRONG_GROUPNAME),headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 400)

class Manage_Group_TestCase (ResourcesAPITestCase):

	GROUP1_REQ = {"group": [{"href": "/api/group/1", "data": [{"name": "groupname", "value": "admins"}], "read-only": True}]}

	NEW_GROUP = 'newname'

	WRONG_GROUP = 'admins'

	def setUp(self):
		super(Manage_Group_TestCase, self).setUp()
		GROUPNAME = 'admins'
		WRONG_GROUPNAME = 'name'
		self.url= resources.api.url_for(resources.Manage_Group,groupname=GROUPNAME,_external=False)
		self.url_wrong = resources.api.url_for(resources.Manage_Group,groupname=WRONG_GROUPNAME,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/manage_group/admins"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Manage_Group)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_managegroup_mimetype(self):
		print '('+self.test_get_managegroup_mimetype.__name__+')', self.test_get_managegroup_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+GROUP_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["group"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.GROUP1_REQ)

	def test_new_group(self):
		print '('+self.test_new_group.__name__+')', self.test_new_group.__doc__
		url = resources.api.url_for(resources.Manage_Group,groupname=self.NEW_GROUP,_external=False)
		resp = self.client.post(url,headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)


	def test_group_exsisting_name(self):
		print '('+self.test_group_exsisting_name.__name__+')', self.test_group_exsisting_name.__doc__
		url = resources.api.url_for(resources.Manage_Group,groupname=self.WRONG_GROUP,_external=False)
		resp = self.client.post(url,headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 400)

class Inventorys_TestCase (ResourcesAPITestCase):

	INVENTORYS1_REQ = {"inventory": [{"href": "/api/inventory/1", "data": [{"name": "Inventoryname", "value": "Banana"}], 
						"read-only": True}, {"href": "/api/inventory/2", "data": [{"name": "Inventoryname", "value": "Tomato"}], 
						"read-only": True}, {"href": "/api/inventory/3", "data": [{"name": "Inventoryname", "value": "Bread"}], 
						"read-only": True}, {"href": "/api/inventory/10", "data": [{"name": "Inventoryname", "value": "Egg"}], 
						"read-only": True}, {"href": "/api/inventory/11", "data": [{"name": "Inventoryname", "value": "Potato"}],
						"read-only": True}, {"href": "/api/inventory/12", "data": [{"name": "Inventoryname", "value": "Milk"}], 
						"read-only": True}]}

	NEW_INVENTORY = {"name" : "new",
					"description": "new",
					"threshold" : 1,
					"quantity" : 3,
					"unit": "KG"}

	def setUp(self):
		super(Inventorys_TestCase, self).setUp()
		GROUPID = 1
		WRONG_GROUPID =-2
		self.url= resources.api.url_for(resources.Inventorys,groupid=GROUPID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Inventorys,groupid=WRONG_GROUPID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/inventorys/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Inventorys)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_inventorys_mimetype(self):
		print '('+self.test_get_inventorys_mimetype.__name__+')', self.test_get_inventorys_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),COLLECTIONJSON+";"+INVENTORY_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["inventory"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.INVENTORYS1_REQ)

	def test_new_inventory(self):
		print '('+self.test_new_inventory.__name__+')', self.test_new_inventory.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.NEW_INVENTORY),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)

	def test_new_inventory_wrongtype(self):
		print '('+self.test_new_inventory.__name__+')', self.test_new_inventory.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.NEW_INVENTORY),headers={"Content-Type": "application/json"})
		self.assertEquals(resp.status_code, 415)



class Inventory_TestCase (ResourcesAPITestCase):

	INVENTORY1_REQ = {"inventory": {"threshold": 1.0, "quantity": 2.0, "name": "Banana", "unit": "KG", "description": "Long Yellow bananas"}, 
	"links": {"curies": [{"href": "/profiles/inventory/{rels}", "name": "recipe", "templated": True}],
	"self": {"profile": "/profiles/inventory", "href": "/api/inventory/1"}, "inventory:edit": {"profile": "/profiles/inventory", 
	"href": "/api/inventory/1"}, "inventory:delete": {"profile": "/profiles/inventory", "href": "/api/inventory/1"}}}

	MODIFY_INVENTORY = {"name" : "new",
					"description": "new",
					"threshold" : 1,
					"quantity" : 3,
					"unit": "KG"}

	def setUp(self):
		super(Inventory_TestCase, self).setUp()
		INVENTORYID = 1
		WRONG_INVENTORYID =-2
		self.url= resources.api.url_for(resources.Inventory,inventoryid=INVENTORYID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Inventory,inventoryid=WRONG_INVENTORYID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/inventory/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Inventory)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_inventory_mimetype(self):
		print '('+self.test_get_inventory_mimetype.__name__+')', self.test_get_inventory_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+INVENTORY_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		self.assertDictContainsSubset(jsondata,self.INVENTORY1_REQ)

	def test_delete_inventory(self):

		print '('+self.test_delete_inventory.__name__+')', self.test_delete_inventory.__doc__
		resp = self.client.delete(self.url)
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 404)

	def test_delete_nonexisting_inventory(self):

		print '('+self.test_delete_nonexisting_inventory.__name__+')', self.test_delete_nonexisting_inventory.__doc__
		resp = self.client.delete(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_modify_inventory(self):
		print '('+self.test_modify_inventory.__name__+')', self.test_modify_inventory.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_INVENTORY),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 200)

	def test_modify_nonexisting_inventory(self):

		print '('+self.test_modify_nonexisting_inventory.__name__+')', self.test_modify_nonexisting_inventory.__doc__
		resp = self.client.put(self.url_wrong,data=json.dumps(self.MODIFY_INVENTORY),headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 404)

	def test_modify_wrong_type(self):
		print '('+self.test_modify_wrong_type.__name__+')', self.test_modify_wrong_type.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_INVENTORY),headers={"Content-Type":"application/json"})
		self.assertEquals(resp.status_code, 415)

class Recipes_TestCase (ResourcesAPITestCase):

	RECIPES1_REQ = {"recipes": [{"href": "/api/recipe/1", "data": [{"name": "recipename", "value": "Potato & Eggs"}], 
						"read-only": True}, {"href": "/api/recipe/2", "data": [{"name": "recipename", "value": "Banana Milkshake"}], 
						"read-only": True}, {"href": "/api/recipe/3", "data": [{"name": "recipename", "value": "Tomato Sauce"}], 
						"read-only": True}]}

	NEW_RECIPE = {"recipe": ["new","new", 14]}

	def setUp(self):
		super(Recipes_TestCase, self).setUp()
		GROUPID = 1
		WRONG_GROUPID =-2
		self.url= resources.api.url_for(resources.Recipes,groupid=GROUPID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Recipes,groupid=WRONG_GROUPID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/recipes/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Recipes)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_recipes_mimetype(self):
		print '('+self.test_get_recipes_mimetype.__name__+')', self.test_get_recipes_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),COLLECTIONJSON+";"+RECIPE_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["recipes"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.RECIPES1_REQ)

	def test_new_recipe(self):
		print '('+self.test_new_recipe.__name__+')', self.test_new_recipe.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.NEW_RECIPE),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)

	def test_new_recipe_wrongtype(self):
		print '('+self.test_new_recipe_wrongtype.__name__+')', self.test_new_recipe_wrongtype.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.NEW_RECIPE),headers={"Content-Type": "application/json"})
		self.assertEquals(resp.status_code, 415)



class Recipe_TestCase (ResourcesAPITestCase):

	RECIPE1_REQ = {"recipe": {"preparation_time": 15, "name": "Potato & Eggs", "details": "Pakistani Cusine"}, 
	"links": {"recipe:delete": {"profile": "/profiles/recipe", "href": "/api/recipe/1"}, "curies": [{"href": "/profiles/recipe/{rels}", 
	"name": "recipe", "templated": True}], "self": {"profile": "/profiles/recipe", "href": "/api/recipe/1"}, 
	"recipe:edit": {"profile": "/profiles/recipe", "href": "/api/recipe/1"}}}

	MODIFY_RECIPE = {"name" : "new",
					"details": "new",
					"preparation_time" : 14}

	def setUp(self):
		super(Recipe_TestCase, self).setUp()
		RECIPEID = 1
		WRONG_RECIPEID =-2
		self.url= resources.api.url_for(resources.Recipe,recipeid=RECIPEID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Recipe,recipeid=WRONG_RECIPEID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/recipe/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Recipe)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_recipe_mimetype(self):
		print '('+self.test_get_recipe_mimetype.__name__+')', self.test_get_recipe_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+RECIPE_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		self.assertDictContainsSubset(jsondata,self.RECIPE1_REQ)

	def test_delete_recipe(self):

		print '('+self.test_delete_recipe.__name__+')', self.test_delete_recipe.__doc__
		resp = self.client.delete(self.url)
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 404)

	def test_delete_nonexisting_recipe(self):

		print '('+self.test_delete_nonexisting_recipe.__name__+')', self.test_delete_nonexisting_recipe.__doc__
		resp = self.client.delete(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_modify_recipe(self):
		print '('+self.test_modify_recipe.__name__+')', self.test_modify_recipe.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_RECIPE),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 200)

	def test_modify_nonexisting_recipe(self):

		print '('+self.test_modify_nonexisting_recipe.__name__+')', self.test_modify_nonexisting_recipe.__doc__
		resp = self.client.put(self.url_wrong,data=json.dumps(self.MODIFY_RECIPE),headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 404)

	def test_modify_wrong_type(self):
		print '('+self.test_modify_wrong_type.__name__+')', self.test_modify_wrong_type.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_RECIPE),headers={"Content-Type":"application/json"})
		self.assertEquals(resp.status_code, 415)


class List_Product_TestCase (ResourcesAPITestCase):

	LISTPRODUCT1_REQ = {"listproduct": [{"href": "/api/inventory/3", "data": [{"name": "inventoryname", "value": "Bread"}],
	 					"read-only": True}, {"href": "/api/inventory/10", "data": [{"name": "inventoryname", "value": "Egg"}], 
	 					"read-only": True}]}

	NEW_LIST = {"inventoryid": 2}

	WRONG_LIST = {"inventoryid": 3}


	def setUp(self):
		super(List_Product_TestCase, self).setUp()
		GROUPID = 1
		WRONG_GROUPID =-2
		self.url= resources.api.url_for(resources.List_Product,groupid=GROUPID,_external=False)
		self.url_wrong = resources.api.url_for(resources.List_Product,groupid=WRONG_GROUPID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/list_product/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.List_Product)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_listproduct_mimetype(self):
		print '('+self.test_get_listproduct_mimetype.__name__+')', self.test_get_listproduct_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),COLLECTIONJSON+";"+LIST_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["listproduct"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.LISTPRODUCT1_REQ)

	def test_new_listproduct(self):
		print '('+self.test_new_listproduct.__name__+')', self.test_new_listproduct.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.NEW_LIST),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 201)

	def test_new_listproduct_wrongtype(self):
		print '('+self.test_new_listproduct_wrongtype.__name__+')', self.test_new_listproduct_wrongtype.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.NEW_LIST),headers={"Content-Type": "application/json"})
		self.assertEquals(resp.status_code, 415)

	def test_new_listproduct_existing(self):
		print '('+self.test_new_listproduct_existing.__name__+')', self.test_new_listproduct_existing.__doc__
		resp = self.client.post(self.url,data=json.dumps(self.WRONG_LIST),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 400)

	def test_delete_listproduct(self):

		print '('+self.test_delete_listproduct.__name__+')', self.test_delete_listproduct.__doc__
		resp = self.client.delete(self.url)
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 404)

	def test_delete_nonexisting_listproduct(self):

		print '('+self.test_delete_nonexisting_listproduct.__name__+')', self.test_delete_nonexisting_listproduct.__doc__
		resp = self.client.delete(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

class Location_Service_TestCase (ResourcesAPITestCase):

	MEMBERCOORDINATE1_REQ = {"membercoordinate": {"href": "/api/member/1", "data": [{"name": "latitude", "value": "65.058428"},
	 {"name": "longitude", "value": "25.465373"}], "read-only": True}}

	MODIFY_LOCATION = {"latitude": "76.5432",
						"longitude": "12.7654"}


	def setUp(self):
		super(Location_Service_TestCase, self).setUp()
		MEMBERID = 1
		WRONG_MEMBERID =-2
		self.url= resources.api.url_for(resources.Location_Service,memberid=MEMBERID,_external=False)
		self.url_wrong = resources.api.url_for(resources.Location_Service,memberid=WRONG_MEMBERID,_external=False)

	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/location_service/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Location_Service)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_locationservice_mimetype(self):
		print '('+self.test_get_locationservice_mimetype.__name__+')', self.test_get_locationservice_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+LOCATION_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["membercoordinate"]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.MEMBERCOORDINATE1_REQ)

	def test_modify_locationservice(self):
		print '('+self.test_modify_locationservice.__name__+')', self.test_modify_locationservice.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_LOCATION),headers={"Content-Type": COLLECTIONJSON})
		self.assertEquals(resp.status_code, 204)
		resp2 = self.client.get(self.url)
		self.assertEquals(resp2.status_code, 200)

	def test_modify_nonexisting_locationservice(self):

		print '('+self.test_modify_nonexisting_locationservice.__name__+')', self.test_modify_nonexisting_locationservice.__doc__
		resp = self.client.put(self.url_wrong,data=json.dumps(self.MODIFY_LOCATION),headers={"Content-Type":COLLECTIONJSON})
		self.assertEquals(resp.status_code, 404)

	def test_modify_wrong_type(self):
		print '('+self.test_modify_wrong_type.__name__+')', self.test_modify_wrong_type.__doc__
		resp = self.client.put(self.url,data=json.dumps(self.MODIFY_LOCATION),headers={"Content-Type":"application/json"})
		self.assertEquals(resp.status_code, 415)

class Monitor_Members_TestCase (ResourcesAPITestCase):

	def setUp(self):
		super(Monitor_Members_TestCase, self).setUp()
		GROUPID = 1;
		WRONG_GROUPID =-2;
		self.url= resources.api.url_for(resources.Monitor_Members,groupid=GROUPID,_external=False)
		self.url_wrong= resources.api.url_for(resources.Monitor_Members,groupid=WRONG_GROUPID,_external=False)

	def test_delete_monitormembers(self):

		print '('+self.test_delete_monitormembers.__name__+')', self.test_delete_monitormembers.__doc__
		resp = self.client.delete(self.url)
		self.assertEquals(resp.status_code, 204)

	def test_delete_nonexisting_monitormembers(self):

		print '('+self.test_delete_nonexisting_monitormembers.__name__+')', self.test_delete_nonexisting_monitormembers.__doc__
		resp = self.client.delete(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

class Monitor_Member_TestCase (ResourcesAPITestCase):

	MONITORMEMBR1_REQ = {"monitormember": [{"href": "/api/monitor_member/1", "data": [{"name": "flag", "value": 0}],
	 "read-only": True}]}

	def setUp(self):
		super(Monitor_Member_TestCase, self).setUp()
		MEMBERID = 1;
		WRONG_MEMBERID =-2;
		self.url= resources.api.url_for(resources.Monitor_Member,memberid=MEMBERID,_external=False)
		self.url_wrong= resources.api.url_for(resources.Monitor_Member,memberid=WRONG_MEMBERID,_external=False)


	def test_url(self):
		
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/monitor_member/1"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Monitor_Member)

	def test_wrong_url(self):
		print '('+self.test_wrong_url.__name__+')', self.test_wrong_url.__doc__
		resp = self.client.get(self.url_wrong)
		self.assertEquals(resp.status_code, 404)

	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_monitormember_mimetype(self):
		print '('+self.test_get_monitormember_mimetype.__name__+')', self.test_get_monitormember_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),HAL+";"+MONITOR_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["monitormember"][0]
		attributes = ('href','data', 'read-only')
		self.assertEquals(len(data), 3)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.MONITORMEMBR1_REQ)


class Shop_Coordinate_TestCase (ResourcesAPITestCase):

	SHOPCOORDINATE1_REQ = {"shop": [{"data": [{"name": "Sale", "latitude1": "65.059914", "latitude2": "65.060602", 
	"longitude2": "25.480799", "longitude1": "25.478718", "shopid": 1}]}, {"data": [{"name": "Tokmanni", 
	"latitude1": "65.058348", "latitude2": "65.059081", "longitude2": "25.478980", "longitude1": "25.476137", 
	"shopid": 2}]}, {"data": [{"name": "University E Gate", "latitude1": "65.057866", "latitude2": "65.058472", 
	"longitude2": "25.470339", "longitude1": "25.468665", "shopid": 3}]}]}

	def setUp(self):
		super(Shop_Coordinate_TestCase, self).setUp()
		self.url= resources.api.url_for(resources.Shop_Coordinate,_external=False)

	def test_url(self):
	
		print '('+self.test_url.__name__+')', self.test_url.__doc__
		url = "/api/shop_coordinate/"
		with resources.app.test_request_context(url):
			rule = flask.request.url_rule
			view_point = resources.app.view_functions[rule.endpoint].view_class
			self.assertEquals(view_point, resources.Shop_Coordinate)


	def test_right_url(self):
		print '('+self.test_right_url.__name__+')', self.test_right_url.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)

	def test_get_shopcoordinate_mimetype(self):
		print '('+self.test_get_shopcoordinate_mimetype.__name__+')', self.test_get_shopcoordinate_mimetype.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		self.assertEquals(resp.headers.get('Content-Type',None),COLLECTIONJSON+";"+SHOP_PROFILE)

	def test_get_format(self):
		print '('+self.test_get_format.__name__+')', self.test_get_format.__doc__
		resp = self.client.get(self.url)
		self.assertEquals(resp.status_code, 200)
		jsondata = json.loads(resp.data)
		data = jsondata["shop"][0]
		attributes = ('data')
		self.assertEquals(len(data), 1)
		for data_attribute in data:
			self.assertIn(data_attribute, attributes)
		self.assertDictContainsSubset(jsondata,self.SHOPCOORDINATE1_REQ)


if __name__ == '__main__':
    print 'Start running WEB API tests'
    unittest.main()