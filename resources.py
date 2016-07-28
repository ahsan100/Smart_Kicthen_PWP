'''
Created on 21 March 2016
Provides Web Api
'''

from flask import Flask, request, Response, g, jsonify, _request_ctx_stack, redirect
from flask.ext.restful import Resource, Api, abort
from flask.ext.cors import CORS

from werkzeug.exceptions import NotFound,  UnsupportedMediaType
from utils import RegexConverter
import database
import json
import math

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

app = Flask(__name__)
app.debug = True

app.config.update({'Engine': database.Engine()})
api = Api(app)
CORS(app)

def distance(xi,xii,yi,yii):
	sq1 = (xi-xii)*(xi-xii)
	sq2 = (yi-yii)*(yi-yii)
	return math.sqrt(sq1 + sq2)

def create_error_response(status_code, title, message=None):
	resource_type = None
	resource_url = None
	ctx = _request_ctx_stack.top
	if ctx is not None:
		resource_url = request.path
		resource_type = ctx.url_adapter.match(resource_url)[0]
	response = jsonify(title=title,
					message=message,
					resource_url=resource_url,
					resource_type=resource_type)
	response.status_code = status_code
	return response


@app.errorhandler(404)
def resource_not_found(error):
	return create_error_response(404, "Resource not found",
						"This resource url does not exit")

@app.errorhandler(400)
def resource_not_found(error):
	return create_error_response(400, "Malformed input format",
						"The format of the input is incorrect")

@app.errorhandler(500)
def unknown_error(error):
	return create_error_response(500, "Error",
    					"The system has failed. Please, contact the administrator")

@app.before_request
def connect_db():
	g.con = app.config['Engine'].connect()
@app.teardown_request
def close_connection(exc):
	if hasattr(g, 'con'):
		g.con.close()

class Member(Resource):

	'''
	To work with the members
	GET is to get details of the specific member
	PUT is to update the details of the member
	DELETE is to delet member
	IMPLEMENTED
	'''

	def get(self, memberid):

		member_db = g.con.get_member(memberid)
		if not member_db:
			return create_error_response(404,"Member not found", "There is no a member with id %s" % memberid)
		user_db = g.con.get_useremail(memberid)

		envelope = {}
		_url = api.url_for(Member, memberid = memberid)
		envelope['href'] = _url
		envelope['read-only'] = True

		member = {'name': member_db['name'],
					'phone': member_db['phone'],'gender': member_db['gender'],
					'dob': member_db['dob'], 'email': user_db['email']}
		envelope['member'] = member

		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+MEMBER_PROFILE)

	def put(self, memberid):
		if not g.con.get_member(memberid):
			return create_error_response(404, "Member not found","There is no a member with id %s" % memberid)
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType", "Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			phone = data['phone']
		except:
			return create_error_response(400, "Wrong request format", "Problem in phone number")
		if not g.con.update_member(memberid, phone):
			return create_error_response(500, "Internal error", "Member information cannot be updated")
		return Response(status=204)

	def delete(self, memberid):
		if g.con.delete_member(memberid):
			return Response(status=204)
		else:
			return create_error_response(404,"Member not found", "There is no a member with id %s" % memberid)


class Search_Member(Resource):
	'''
	To search the member using the email.
	GET IS IMPLEMENTED ONLY
	'''

	def get(self, email):
		user_db = g.con.get_user(email)
		if not user_db:
			return create_error_response(404, "User not found", "There is no group with e-mail %s" %email)
		envelope = {}
		items =[]
		_memberid = user_db["memberid"]
		_url = api.url_for(Member, memberid = _memberid)
		user = {}
		user['href'] = _url
		user['read-only'] = True
		user["data"] =[]
		value = {'name': 'memberid', 'value': _memberid}
		user['data'].append(value)
		items.append(user)

		envelope['user'] = items

		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+SEARCH_PROFILE)


class User_Login(Resource):
	'''
	TO LOG IN THE APPLICATION
	POST GETS THE E-mail and password & logs in
	IMPLEMENTED
	'''

	def post(self):
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			email = data['email']
			password = data['password']
		except:
			return create_error_response(400, "Wrong request format","Check E-mail and Password")

		user_db = g.con.get_user(email)
		if not user_db:
			return create_error_response(404,"User not found", "There is no user with E-mail:  %s" % email)

		if password == user_db["password"]:
			groupid = g.con.get_group_memberid(user_db["memberid"])
			if not groupid:
				return Response(status=200)
			_url = api.url_for(Group, groupid=groupid["groupid"])
			return Response(status=200, headers={'Location': _url})
		else:
			return create_error_response(401,"User Not Authorized", "Please Check your password")

class New_User(Resource):
	'''
	TO CREATE A NEW USER IN THE START OF THE APPLICATION
	POST is implemented
	'''

	def post(self):
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		email = data['email']
		password = data['password']
		name = data['name']
		phone = data['phone']
		gender = data['gender']
		dob = data['dob']
		try:
			newid = g.con.create_member(name,phone,gender,dob)
			resp = g.con.create_user(newid,email,password) 
			if not resp:
				return create_error_response(400, "User Already Registered",
											"This Email is already registered")
		except:
			return create_error_response(500, "Problem with the database",
											"Cannot access the database")
	
		return Response(status=201)

class Group_Member(Resource):
	'''
	GET is for getting the ID of MEMBERS in that Group ID & displaying it to the client
	POST is to put the NEW MEMBER in that GROUP ID 
	Implemented
	'''

	def get(self, groupid):
		group_db = g.con.get_group_groupid(groupid)
		if not group_db:
			return create_error_response(404,"Group Error", "There is no group with id %s" % groupid)
		envelope = {}
	
		items =[]
		for group in group_db:
			_memberid = group["memberid"]
			_url = api.url_for(Member, memberid = _memberid)
			member_db = g.con.get_member(_memberid)
			group = {}
			group['href'] = _url
			group['read-only'] = True
			group["data"] =[]
			value = {'name': 'membername', 'value': member_db["name"]}
			group['data'].append(value)
			items.append(group)

		envelope['group'] = items

		return Response(json.dumps(envelope), 200, mimetype=COLLECTIONJSON+";"+GROUP_PROFILE)

	def post(self, groupid):
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		resp = g.con.create_groupmember(groupid,data['memberid'])
		if not resp:
			return create_error_response(400, "Member Already in group",
										"PLease check the member again")
		return Response(status=201)

class Group(Resource):
	'''
	GET is for get the name of the group & displaying it to the client
	PUT is to update the name of the group
	DELETE is delete the group
	DONE
	'''

	def get(self, groupid):
		group_db = g.con.get_group(groupid)
		if not group_db:
			return create_error_response(404,"Group not found", "There is no group with id %s" % groupid)
		envelope = {}
		items =[]
		groupname = group_db["name"]
		_url = api.url_for(Group, groupid = groupid)
		group = {}
		group['href'] = _url
		group['read-only'] = True
		group["data"] =[]
		value = {'name': 'groupname', 'value': groupname}
		group['data'].append(value)
		items.append(group)

		envelope['group'] = items

		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+GROUP_PROFILE)

	def put(self, groupid):
		if not g.con.get_group(groupid):
			return create_error_response(404,"Group not found", "There is no group with id %s" % groupid)
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType", "Use a JSON compatible format")
		data = request.get_json(force=True)
		if data["name"] is None:
			return create_error_response(400, "Wrong request format",
										"PLease check the Group Name")
		else:
			name = data["name"]
		newid= g.con.update_group(groupid, name)
		url = api.url_for(Group, groupid = newid)
		return Response(status=204, headers={'Location': url})

	def delete(self, groupid):
		if g.con.delete_group(groupid):
			return Response(status=204)
		else:
			return create_error_response(404,"Group not found", "There is no group with id %s" % groupid)

class Manage_Group(Resource):

	'''
	DONE
	IMPLEMENTED & WORKING, POST ADD NEW GROUP & RETURNS THE URL OF THE NEW GROUP
	GET SEARCHES FOR THE GROUP USING THE NAME
	'''

	def get(self,groupname):
		group_db = g.con.get_group_name(groupname)
		if not group_db:
			return create_error_response(404,"Group not found", "There is no group with name %s" % groupname)

		envelope = {}
		items =[]
		_url = api.url_for(Group, groupid = group_db["groupid"])
		group = {}
		group['href'] = _url
		group['read-only'] = True
		group["data"] =[]
		value = {'name': 'groupname', 'value': groupname}
		group['data'].append(value)
		items.append(group)

		envelope['group'] = items

		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+GROUP_PROFILE)

	def post(self, groupname):
		_groupid = g.con.create_group(groupname)
		if not _groupid:
			return create_error_response(400, "Name Already in Use",
											"Group Name Already in use, please change")
		_url = api.url_for(Group, groupid = _groupid)
		
		return Response(status=201, headers={'Location': _url})

class Inventorys(Resource):
	'''
	DONE
	FOR GIVING THE LIST OF THE INVENTORY & ADD LINK
	ALSO ADD NEW INVENTORY IN THE GROUP
	'''
	def get(self, groupid):
		inventorys_db = g.con.get_inventorys(groupid)
		if not inventorys_db:
			return create_error_response(404,"Group not found", "There is no Inventory with this Group")

		envelope = {}
		items =[]
		for inventory in inventorys_db:
			_inventoryid = inventory["inventoryid"]
			_inventoryname = inventory["name"]
			_url = api.url_for(Inventory, inventoryid = _inventoryid)
			inventory = {}
			inventory['href'] = _url
			inventory['read-only'] = True
			inventory["data"] =[]
			value = {'name': 'Inventoryname', 'value': _inventoryname}
			inventory['data'].append(value)
			items.append(inventory)

		envelope['inventory'] = items

		return  Response(json.dumps(envelope), 200, mimetype=COLLECTIONJSON+";"+INVENTORY_PROFILE)

	def post(self, groupid):

		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			name = data['name']
			description = data['description']
			threshold = data['threshold']
			quantity = data['quantity']
			unit =data['unit']
		except:
			return create_error_response(400, "Wrong request format", "Check your inventory details")

		inventoryid= g.con.create_inventory(name, description, threshold,quantity,groupid, unit)
		if not inventoryid:
			return create_error_response(500, "Problem with the database",
											"Cannot access the database")
		
		url= api.url_for(Inventory, inventoryid=inventoryid)
		return Response(status=201, headers={'Location':url})

class Inventory(Resource):
	'''
	FOR GIVING THE DETAILS OF A SPECIFIC RECIPE & UPDATING, DELETEING IT
	GET & DELETE ARE DONE IMPLEMENTED 
	PUT PROPERLY LIKE POST BEFORE
	'''

	def get(self, inventoryid):
		inventory_db = g.con.get_inventory(inventoryid)
		if not inventory_db:
			return create_error_response(404,"Inventory Error", "There is no such Inventory with this Group")

		envelope = {}
		links ={}
		envelope["links"] = links
		_curies =[
			{ "name":"recipe",
			"href": INVENTORY_PROFILE + "/{rels}",
			"templated": True
		}]

		links['curies'] = _curies
		links['self'] = {'href': api.url_for(Inventory, inventoryid=inventoryid),
						'profile': INVENTORY_PROFILE}
		links['inventory:edit'] = {'href': api.url_for(Inventory, inventoryid=inventoryid),
						'profile': INVENTORY_PROFILE}
		links['inventory:delete'] = {'href': api.url_for(Inventory, inventoryid=inventoryid),
						'profile': INVENTORY_PROFILE}
		
		envelope['inventory']  = {'name': inventory_db['name'], 
								'description': inventory_db['description'], 
								'threshold': inventory_db['threshold'], 
								'quantity': inventory_db['quantity'], 'unit': inventory_db['unit'] }
		
		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+INVENTORY_PROFILE)

	def put(self, inventoryid):

		if not g.con.get_inventory(inventoryid):
			return create_error_response(404,"Inventory Error", "There is no Inventory with this Group")
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			name = data['name']
			description = data['description']
			threshold = data['threshold']
			quantity = data['quantity']
			unit =data['unit']
		except:
			return create_error_response(400, "Wrong request format", "Please check Inventory details")

		newid= g.con.update_inventory(inventoryid, name, description, threshold,quantity, unit)
		url = api.url_for(Inventory, inventoryid = newid)
		return Response(status=204, headers={'Location': url})

	def delete(self, inventoryid):
		if g.con.delete_inventory(inventoryid):
			return Response(status=204)
		else:
			return create_error_response(404,"Inventory Error", "There is no such Inventory " )

class Recipes(Resource):
	'''
	DONE
	FOR GIVING THE LIST OF THE RECIPES & ADD + DELETE LINKS
	ALSO ADD NEW RECIPES IN THE GROUP
	'''
	def get(self, groupid):

		recipes_db = g.con.get_recipes(groupid)
		if not recipes_db:
			return create_error_response(404,"Recipe Error" "There is no Recipe with this Group " )

		envelope = {}
		items =[]
		for recipe in recipes_db:
			_recipeid = recipe["recipeid"]
			_recipename = recipe["name"]
			_url = api.url_for(Recipe, recipeid = _recipeid)
			recipe = {}
			recipe['href'] = _url
			recipe['read-only'] = True
			recipe["data"] =[]
			value = {'name': 'recipename', 'value': _recipename}
			recipe['data'].append(value)
			items.append(recipe)

		envelope['recipes'] = items

		return  Response(json.dumps(envelope), 200, mimetype=COLLECTIONJSON+";"+RECIPE_PROFILE)

	def post(self, groupid):

		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			recipe = data["recipe"]
		except:
			return create_error_response(400, "Wrong request format", "Check recipe")

		recipeid = g.con.create_recipe(recipe[0],recipe[1],groupid,recipe[2])
		if not recipeid:
			return create_error_response(500, "Problem with the database",
											"Cannot access the database")
		try:
			for x in range(1, len(data)):
				inventory = data["inventory%s" %x]
				print inventory[0]
				inventorydb = g.con.get_inventory_name(inventory[0], groupid)
				if g.con.create_recipeinventory(recipeid,inventorydb["inventoryid"],inventory[1]) is False:
					return create_error_response(500, "Problem with the database",
											"Cannot access the database")
		except:
			return create_error_response(400, "Wrong request format", "Check inventory in recipes")
		
		return Response(status=201)


class Recipe(Resource):
	'''
	FOR GIVING THE DETAILS OF A SPECIFIC RECIPE & UPDATING, DELETEING IT
	GET & DELETE ARE DONE IMPLEMENT PUT PROPERLY LIKE POST BEFORE
	'''

	def get(self, recipeid):
		recipe_db = g.con.get_recipe(recipeid)
		if not recipe_db:
			return create_error_response(404,"Unknown Recipe", 
								"There is no Recipe with Id %s" % recipeid)
		envelope = {}
		links ={}
		envelope["links"] = links
		_curies =[
			{ "name":"recipe",
			"href": RECIPE_PROFILE + "/{rels}",
			"templated": True
		}]
		links['curies'] = _curies
		links['self'] = {'href': api.url_for(Recipe, recipeid=recipeid),
						'profile': RECIPE_PROFILE}
		links['recipe:edit'] = {'href': api.url_for(Recipe, recipeid=recipeid),
						'profile': RECIPE_PROFILE}
		links['recipe:delete'] = {'href': api.url_for(Recipe, recipeid=recipeid),
						'profile': RECIPE_PROFILE}

		envelope['recipe']  = {'name': recipe_db['name'], 
								'details': recipe_db['details'], 
								'preparation_time': recipe_db['preparationtime'] }


		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+RECIPE_PROFILE)

	def put(self, recipeid):
		if not g.con.get_recipe(recipeid):
			return create_error_response(404,"Unknown Recipe", 
								"There is no Recipe with Id %s" % recipeid)
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			name = data['name']
			details = data['details']
			preparation_time = data['preparation_time']
		except:
			return create_error_response(400, "Wrong request format", "Check your fields")

		newid= g.con.update_recipe(recipeid, name, details, preparation_time)
		url = api.url_for(Recipe, recipeid = newid)
		return Response(status=204, headers={'Location': url})

	def delete(self, recipeid):
		if g.con.delete_recipe(recipeid):
			return Response(status=204)
		else:
			return create_error_response(404,"Unknown Recipe", 
								"There is no Recipe with Id %s" % recipeid)


class Recipe_Add(Resource):

	'''
	THIS IS USED WHEN YOU ADD RECIPE FROM MAKING (ASK NUMBER OF PEOPLE)
	'''

	def put(self, recipeid):
		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			people = data['people']
		except:
			return create_error_response(400, "Wrong request format", " Check Number of People")
		recipe_db = g.con.get_recipeinventory(recipeid)
		if not recipe_db:
			return create_error_response(404,"Unknown Recipe", 
								"There is no Recipe with Id %s" % recipeid)
		for recipe in recipe_db:
			print recipe
			_inventoryid = recipe['inventoryid']
			_quantityrequired = recipe['quantity']
			inventory_db= g.con.get_inventory(_inventoryid)
			_quantityavailible = inventory_db['quantity']
			if _quantityavailible < (_quantityrequired * int(people)):
				return create_error_response(400, "Not Enough Quantity")
			_quantityleft = _quantityavailible - (_quantityrequired * int(people))
			if _quantityleft <= inventory_db['threshold']:
				if g.con.create_listproduct(inventory_db['groupid'], _inventoryid) is not True:
					return create_error_response(404,"Cannot Create List Product", 
								"There is no INVENTORY with Id %s" % _inventoryid)
			if g.con.update_inventory(_inventoryid, inventory_db['name'],inventory_db['description'],inventory_db['threshold'], _quantityavailible - (_quantityrequired * int(people)), inventory_db['unit']) is not True:
				return create_error_response(404,"Cannot Update Inventory", 
								"There is no INVENTORY with Id %s" % _inventoryid)

		url= api.url_for(Group, groupid = inventory_db["groupid"])
		return Response(status=204, headers={'Location': url})

class List_Product(Resource):

	'''
	TO MAKE A LIST OF LOW PRODUCTS 
	GET TO GIVE LIST FOR A SPECIFIC GROUP
	POST TO ADD THE PRODUCTS IN THE LIST
	IMPLEMENT DELETE TO CLEAT THE LIST
	'''

	def get(self, groupid):

		listproduct_db = g.con.get_listproduct(groupid)
		if not listproduct_db:
			return create_error_response(404, "There is no list with this Group " )

		envelope = {}
		items =[]
		for listproduct in listproduct_db:
			_inventoryid = listproduct["inventoryid"]
			inventory_db = g.con.get_inventory(_inventoryid)
			_url = api.url_for(Inventory, inventoryid = _inventoryid)
			_inventoryname = inventory_db["name"]
			listproduct = {}
			listproduct['href'] = _url
			listproduct['read-only'] = True
			listproduct["data"] =[]
			value = {'name': 'inventoryname', 'value': _inventoryname}
			listproduct['data'].append(value)
			items.append(listproduct)

		envelope['listproduct'] = items

		return  Response(json.dumps(envelope), 200, mimetype=COLLECTIONJSON+";"+LIST_PROFILE)

	def post(self, groupid):

		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		inventoryid = data["inventoryid"]
		if not g.con.create_listproduct(groupid,inventoryid):
			return create_error_response(400, "Product Already in List", " This product is already in low list")

		url= api.url_for(Group, groupid=groupid)
		return Response(status=201, headers={'Location': url})

	def delete(self, groupid):
		if g.con.delete_listproducts(groupid):
			return Response(status=204)
		else:
			return create_error_response(404,"Group Error", "There is no such Group" )

class Location_Service(Resource):

	'''
	TO STORE THE VALUE OF THE MEMBER LOCATIONS 
	GET IS USED WHEN THE CLIENT NEED THE LOCATION
	PUT IS USED WHEN THE LOCATION IS UPDATED
	IMPLEMENT POST TO ADD NEW MEMBERS LOCATION
	'''

	def get(self, memberid):

		groupmember_db = g.con.get_group_memberid(memberid)
		if not groupmember_db:
			return create_error_response(404,"Member Error" "There is such no Member Registered " )
		_groupid = groupmember_db['groupid']
		membercoordinate_db = g.con.get_memberscoordinate(_groupid, memberid)
		if not membercoordinate_db:
			return create_error_response(404,"Location Error" "There is no Member in the List " )

		envelope = {}
		latitude = membercoordinate_db["latitude"]
		longitude = membercoordinate_db["longitude"]
		_url = api.url_for(Member, memberid = memberid)
		membercoordinate = {}
		membercoordinate['href'] = _url
		membercoordinate['read-only'] = True
		membercoordinate["data"] =[]
		value = {'name': 'latitude', 'value': latitude}
		membercoordinate['data'].append(value)
		value = {'name': 'longitude', 'value': longitude}
		membercoordinate['data'].append(value)

		envelope['membercoordinate'] = membercoordinate

		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+LOCATION_PROFILE)


	def put(self, memberid):

		if COLLECTIONJSON != request.headers.get('Content-Type',''):
			return create_error_response(415, "UnsupportedMediaType","Use a JSON compatible format")
		data = request.get_json(force=True)
		try:
			latitude = data['latitude']
			longitude = data['longitude']
		except:
			return create_error_response(400, "Wrong request format", "Please check location")

		groupmember_db = g.con.get_group_memberid(memberid)
		if not groupmember_db:
			return create_error_response(404,"Member Error" "There is such no Member Registered " )
		_groupid = groupmember_db['groupid']

		if g.con.update_memberscoordinate(_groupid,memberid, latitude, longitude) is not True:
			return create_error_response(404,"Unknown Member", 
								"There is no Member with Id %s" % memberid)

		url= api.url_for(Group, groupid = _groupid)
		return Response(status=204, headers={'Location': url})

class Monitor_Members(Resource):

	'''
	PUT is TO CHANGE THE FLAG OF ALL THE MEMBERS IN THE GROUP FOR NOTIFICATION
	DELETE is change flag to 0 & delete products in list
	'''

	def delete(self, groupid):

		group_db = g.con.get_group_groupid(groupid)
		if not group_db:
			return create_error_response(404, "Error ","There is no group with id %s" % groupid)
		for group in group_db:
			_memberid = group["memberid"]
			g.con.update_monitormember(_memberid, 0)
		g.con.delete_listproducts(groupid)

		return Response(status=204)

	# def put(self, groupid):
	# 	groupmember_db = g.con.get_group_groupid(groupid)
	# 	if not groupmember_db:
	# 		return create_error_response(404, "There is no list with this Group " )

	# 	envelope = {}
	# 	items =[]
	# 	for groupmember in groupmember_db:
	# 		_memberid = groupmember["memberid"]
	# 		monitormember_db = g.con.get_monitormember(_memberid)
	# 		if not monitormember_db:
	# 			return create_error_response(404, "There is no member with this Group " )
	# 		shopcoordinate_db = g.con.get_shopscoordinate()
	# 		membercoordinate_db = g.con.get_memberscoordinate(groupid, _memberid)
	# 		if not membercoordinate_db:
	# 			return create_error_response(404, "There is no Member in the List " )
	# 		memberlati = float(membercoordinate_db['latitude'])
	# 		memberlongi= float(membercoordinate_db['longitude'])
	# 		print membercoordinate_db
	# 		for shopcoordinate in shopcoordinate_db:
	# 			shoplati1= float(shopcoordinate['latitude1'])
	# 			shoplati2= float(shopcoordinate['latitude2'])
	# 			shoplongi1= float(shopcoordinate['longitude1'])
	# 			shoplongi2 = float(shopcoordinate['longitude2'])
	# 			if (shoplati1 <= memberlati <=shoplati2) and (shoplongi1 <= memberlongi <= shoplongi2):
	# 				g.con.update_monitormember(_memberid, 1)
	# 				break
	# 			else:
	# 				g.con.update_monitormember(_memberid, 0)

	# 		# if monitormember_db["flag"] == 0:
	# 		# 	g.con.update_monitormember(_memberid, 1)
	# 		# else:
	# 		# 	g.con.update_monitormember(_memberid, 0)

	# 	url= api.url_for(Group, groupid = groupid)
	# 	return Response(status=204, headers={'Location': url})
	
	def put(self, groupid):
		groupmember_db = g.con.get_group_groupid(groupid)
		if not groupmember_db:
			return create_error_response(404,"Group Error", "There is no list with this Group " )

		envelope = {}
		items =[]
		miniold = 100
		mininew = 0
		for groupmember in groupmember_db:
			_memberid = groupmember["memberid"]
			monitormember_db = g.con.get_monitormember(_memberid)
			if not monitormember_db:
				return create_error_response(404,"Member Error", "There is no member with this Group " )
			shopcoordinate_db = g.con.get_shopscoordinate()
			membercoordinate_db = g.con.get_memberscoordinate(groupid, _memberid)
			if not membercoordinate_db:
				return create_error_response(404,"Member Error", "There is no Member in the List " )
			memberlati = float(membercoordinate_db['latitude'])
			memberlongi= float(membercoordinate_db['longitude'])
			print membercoordinate_db
			for shopcoordinate in shopcoordinate_db:
				shoplati1= float(shopcoordinate['latitude1'])
				# shoplati2= float(shopcoordinate['latitude2'])
				shoplongi1= float(shopcoordinate['longitude1'])
				# shoplongi2 = float(shopcoordinate['longitude2'])
				mininew = min(distance(memberlati,shoplati1,memberlongi,shoplongi1), miniold)
				print mininew
				if mininew < miniold:
					miniold = mininew
					minmemberid = _memberid
		g.con.update_monitormember(minmemberid, 2)
		url= api.url_for(Group, groupid = groupid)
		return Response(status=204, headers={'Location': url})

class Monitor_Member(Resource):

	'''
	POST is working like GET because i wass too lazy to think about something else & i just need to get 
	MEMBER FLAG
	'''

	def get(self, memberid):
		monitormember_db = g.con.get_monitormember(memberid)
		if not monitormember_db:
			return create_error_response(404,"Member Error", "There is no member with this Group " )

		envelope = {}
		items =[]
		_url = api.url_for(Monitor_Member, memberid = memberid)
		_flag = monitormember_db["flag"]
		monitormember = {}
		monitormember['href'] = _url
		monitormember['read-only'] = True
		monitormember["data"] =[]
		value = {'name': 'flag', 'value': _flag}
		monitormember['data'].append(value)
		items.append(monitormember)
			
		envelope['monitormember'] = items

		return Response(json.dumps(envelope), 200, mimetype=HAL+";"+MONITOR_PROFILE)

class Shop_Coordinate(Resource):

	def get(self):

		shop_db = g.con.get_shopscoordinate()
		if not shop_db:
			return create_error_response(404,"Shop location error", "There is no shop in the database " )

		envelope = {}
		items = []
		for shop in shop_db:
			value = {'shopid': shop['shopid'],
					'name': shop['name'],'latitude1': shop['latitude1'],'longitude1': shop['longitude1'], 
					'latitude2': shop['latitude2'], 'longitude2': shop['longitude2']}
			shop ={}
			shop['data'] = []
			shop['data'].append(value)
			items.append(shop)


		envelope['shop'] = items


		return  Response(json.dumps(envelope), 200, mimetype=COLLECTIONJSON+";"+SHOP_PROFILE)



app.url_map.converters['regex'] = RegexConverter

api.add_resource(Member, '/api/member/<memberid>',
						endpoint='member')
api.add_resource(Search_Member, '/api/search_members/<email>',
						endpoint='search_members')
api.add_resource(User_Login, '/api/user/',
						endpoint='user')
api.add_resource(New_User, '/api/new_users/',
						endpoint='new_users')
api.add_resource(Group, '/api/group/<groupid>',
						endpoint='group')
api.add_resource(Group_Member, '/api/group_member/<groupid>',
						endpoint='group_member')
api.add_resource(Manage_Group, '/api/manage_group/<groupname>',
						endpoint='manage_group')
api.add_resource(Inventorys, '/api/inventorys/<groupid>',
						endpoint='inventorys')
api.add_resource(Inventory, '/api/inventory/<inventoryid>',
						endpoint='inventory')
api.add_resource(Recipes, '/api/recipes/<groupid>',
						endpoint='recipes')
api.add_resource(Recipe, '/api/recipe/<recipeid>',
						endpoint='recipe')
api.add_resource(Recipe_Add, '/api/recipe_add/<recipeid>',
						endpoint='recipe_add')
api.add_resource(List_Product, '/api/list_product/<groupid>',
						endpoint='list_product')
api.add_resource(Location_Service, '/api/location_service/<memberid>',
						endpoint='location_service')
api.add_resource(Monitor_Members, '/api/monitor_members/<groupid>',
						endpoint='monitor_members')
api.add_resource(Monitor_Member, '/api/monitor_member/<memberid>',
						endpoint='monitor_member')
api.add_resource(Shop_Coordinate, '/api/shop_coordinate/',
						endpoint='shop_coordinate')






if __name__ == '__main__':
	app.run(debug=True)