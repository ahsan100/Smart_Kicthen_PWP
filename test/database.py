'''
Created on 15.03.2016
Provides the database API
'''
from datetime import datetime
import sqlite3, os,time
DEFAULT_DB = 'db/main.db'
DEFAULT_SCHEMA = 'db/schema.sql'
DEFAULT_DATA = 'db/data.sql'

class Engine(object):
	def __init__(self, db_path=None):
		super(Engine, self).__init__()
		if db_path is not None:
			self.db_path = db_path
		else:
			self.db_path=DEFAULT_DB

	def connect(self):
		return Connection(self.db_path)

	def remove_db(self):
		if os.path.exists(self.db_path):
			os.remove(self.db_path)

	def clear_table(self):
		keys_on = 'PRAGMA foreign_keys = ON'
		con = sqlite3.connect(self.db_path)
		cur = con.cursor()
		cur.execute(keys_on)
		with con:
			cur = con.cursor()
			cur.execute("DELETE FROM members")
			cur.execute("DELETE FROM inventory")
			cur.execute("DELETE FROM recipe")
			cur.execute("DELETE FROM user_login")
			cur.execute("DELETE FROM groups")
			cur.execute("DELETE FROM group_member")
			cur.execute("DELETE FROM recipe_inventory")
			cur.execute("DELETE FROM list_product")
			cur.execute("DELETE FROM shops_coordinate")
			cur.execute("DELETE FROM members_coordinate")
			cur.execute("DELETE FROM monitor_member")

	def create_table(self, schema = None):
		con = sqlite3.connect(self.db_path)
		if schema is None:
			schema = DEFAULT_SCHEMA
		try:
			with open(schema) as s:
				sql = s.read()
				cur = con.cursor()
				cur.executescript(sql)
		finally:
			con.close()

	def data_table(self, data = None):
		keys_on = 'PRAGMA foreign_keys = ON'
		con = sqlite3.connect(self.db_path)
		cur = con.cursor()
		cur.execute(keys_on)
		if data is None:
			data = DEFAULT_DATA
		try:
			with open (data) as f:
				sql = f.read()
				cur = con.cursor()
				cur.executescript(sql)
		finally:
			con.close()

class Connection(object):

	def __init__(self, db_path):
		super(Connection, self).__init__()
		self.con = sqlite3.connect(db_path)

	def close(self):
		if self.con:
			self.con.commit()
			self.con.close()

	def foreign_key(self):
		keys_on = 'PRAGMA foreign_keys = ON'
		try:
			cur = self.con.cursor()
			cur.execute(keys_on)
			return True
		except sqlite3.Error, excp:
			print "Error %s:" % excp.args[0]
			return False

	
	'''
	MEMBERS
	'''
	def member_object(self, row):
		return {'memberid': row['member_id'],
				'name':row['name'],
				'phone': row['phone'],
				'gender': row['gender'],
				'dob': row['dob']}

	def create_member(self, name, phone,gender,dob):
		query='INSERT INTO members(name,phone,gender,dob) VALUES(?,?,?,?)'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name,phone,gender,dob)
		cur.execute(query, pvalue)
		self.con.commit()
		memberid = cur.lastrowid
		if cur.rowcount < 1:
			return False
		return memberid


	def get_member(self, memberid):
		query = 'SELECT * FROM members WHERE member_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue =(memberid,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.member_object(row)

	def update_member(self, memberid, phone):
		query = 'UPDATE members SET phone =? WHERE member_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (phone, memberid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return None
		return memberid


	def delete_member(self, memberid):
		query = 'DELETE FROM members WHERE member_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (memberid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True


	'''
	USER_LOGIN
	'''
	def user_object(self, row):
		return {'userid': row['user_id'],
				'memberid':row['member_id'],
				'email': row['email'],
				'password': row['password'],
				'timestamp': row['timestamp']}

	def get_user(self, email):
		query = 'SELECT * FROM user_login WHERE email = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue =(email,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.user_object(row)

	def get_useremail(self, memberid):
		query1 = 'SELECT * FROM user_login WHERE member_id =?'
		member_id = None
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (memberid,)
		cur.execute(query1, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.user_object(row)

	def create_user(self, member_id ,email, password):
		query='INSERT INTO user_login(member_id, email,password,timestamp) VALUES(?,?,?,?)'
		query1 ='SELECT * FROM user_login WHERE email=?'
		self.foreign_key()
		timestamp = time.mktime(datetime.now().timetuple())
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (email,)
		cur.execute(query1, pvalue)
		row = cur.fetchone()
		if row is None:
			pvalue = (member_id,email,password,timestamp)
			cur.execute(query, pvalue)
			self.con.commit()
			if cur.rowcount < 1:
				return False
			return True
		else:
			return None

	def update_user(self, memberid,password):
		query = 'UPDATE user_login SET password =?, timestamp=? WHERE member_id =?'
		self.foreign_key()
		timestamp = time.mktime(datetime.now().timetuple())
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (password,timestamp, memberid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return None
		return memberid

	'''
	GROUPS
	'''
	def group_object(self, row):
		return {'groupid': row['group_id'],
				'name':row['name']}

	def get_group(self, groupid):
		query = 'SELECT * FROM groups WHERE group_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue =(groupid,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.group_object(row)

	def create_group(self, name):
		query='INSERT INTO groups(name) VALUES(?)'
		query1 ='SELECT * FROM groups WHERE name = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name,)
		cur.execute(query1, pvalue)
		row = cur.fetchone()
		if row is None:
			pvalue = (name,)
			cur.execute(query, pvalue)
			self.con.commit()
			groupid = cur.lastrowid
			if cur.rowcount < 1:
				return False
			return groupid
		else:
			return None

	def delete_group(self, groupid):
		query = 'DELETE FROM groups WHERE group_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def update_group(self, groupid, name):
		query = 'UPDATE groups SET name= ? WHERE group_id=?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name , groupid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return None
		return groupid

	def get_group_name(self, groupname):
		query = 'SELECT * FROM groups WHERE name = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue =(groupname,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.group_object(row)


	'''
	GROUP_MEMBER
	'''
	def groupmember_object(self, row):
		return {'groupid': row['group_id'],
				'memberid':row['member_id']}

	def get_group_memberid(self, memberid):
		query = 'SELECT * FROM group_member WHERE member_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue =(memberid,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.groupmember_object(row)

	def get_group_groupid(self, groupid):
		query = 'SELECT * FROM group_member WHERE group_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue =(groupid,)
		cur.execute(query, pvalue)
		rows= cur.fetchall()
		if len(rows) is 0:
			return None
		members = []
		for row in rows:
			member = self.groupmember_object(row)
			members.append(member)
		return members

	def create_groupmember(self, groupid, memberid):
		query='INSERT INTO group_member(group_id, member_id) VALUES(?,?)'
		query1 ='SELECT * FROM group_member WHERE member_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (memberid,)
		cur.execute(query1, pvalue)
		row = cur.fetchone()
		if row is None:
			pvalue = (groupid, memberid)
			cur.execute(query, pvalue)
			self.con.commit()
			if cur.rowcount < 1:
				return False
			return True
		else:
			return None

	def delete_groupmember(self, memberid):
		query = 'DELETE FROM group_member WHERE member_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (memberid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True


	'''
	INVENTORY
	'''

	def inventory_object(self, row):
		return {'inventoryid': row['inventory_id'],
				'name': row['name'],
				'description':row['description'],
				'threshold': row['threshold'],
				'quantity':row['quantity'],
				'groupid': row['group_id'],
				'unit':row['unit']}

	def create_inventory(self, name, description, threshold, quantity, groupid, unit):
		query='INSERT INTO inventory(name,description,threshold,quantity,group_id,unit) VALUES(?,?,?,?,?,?)'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		inventory = self.get_inventory_name(name, groupid)
		if inventory is None: 
			pvalue = (name, description, threshold, quantity, groupid, unit)
			cur.execute(query, pvalue)
			self.con.commit()
			inventoryid = cur.lastrowid
			if cur.rowcount < 1:
				return False
			return inventoryid
		else:
			return None

	def get_inventory_name(self, name, groupid):
		query= 'SELECT * FROM inventory WHERE  name =? AND group_id= ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name,groupid)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.inventory_object(row)

	def get_inventory(self, inventoryid):
		query= 'SELECT * FROM inventory WHERE inventory_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (inventoryid,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.inventory_object(row)

	def get_inventorys(self, groupid):
		query= 'SELECT * FROM inventory WHERE group_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid,)
		cur.execute(query, pvalue)
		rows = cur.fetchall()
		if len(rows) is 0:
			return None
		inventorys = []
		for row in rows:
			inventory = self.inventory_object(row)
			inventorys.append(inventory)
		return inventorys

	def delete_inventory(self, inventoryid):
		query = 'DELETE FROM inventory WHERE inventory_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (inventoryid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def update_inventory(self, inventoryid, name, description, threshold, quantity, unit):
		query = 'UPDATE inventory SET name =?, description=?, threshold =?, quantity=?, unit = ? WHERE inventory_id=?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name, description, threshold, quantity, unit, inventoryid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return None
		return inventoryid

	'''
	RECIPE
	'''

	def recipe_object(self, row):
		return {'recipeid': row['recipe_id'],
				'name': row['name'],
				'details':row['details'],
				'groupid': row['group_id'],
				'preparationtime':row['preparation_time']}

	def create_recipe(self, name, details,groupid, preparationtime):
		query='INSERT INTO recipe(name, details,group_id, preparation_time) VALUES(?,?,?,?)'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		recipe = self.get_recipe_name( groupid, name)
		if recipe is None: 
			pvalue = (name, details,groupid, preparationtime)
			cur.execute(query, pvalue)
			self.con.commit()
			recipeid = cur.lastrowid
			if cur.rowcount < 1:
				return False
			return recipeid
		else:
			return None

	def get_recipe(self, recipeid):
		query = 'SELECT * FROM recipe WHERE recipe_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (recipeid,)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.recipe_object(row)

	def get_recipes(self, groupid):
		query = 'SELECT * FROM recipe WHERE group_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid,)
		cur.execute(query, pvalue)
		rows = cur.fetchall()
		if len(rows) is 0:
			return None
		recipes = []
		for row in rows:
			recipe = self.recipe_object(row)
			recipes.append(recipe)
		return recipes

	def get_recipe_name(self, groupid, name):
		query = 'SELECT * FROM recipe WHERE group_id = ? AND name= ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid, name)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.recipe_object(row)

	def delete_recipe(self, recipeid):
		query = 'DELETE FROM recipe WHERE recipe_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (recipeid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True


	def update_recipe(self, recipeid, name, details, preparationtime):
		query = 'UPDATE recipe SET name =?, details=?,preparation_time=? WHERE recipe_id=?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name, details, preparationtime, recipeid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return None
		return recipeid

	'''
	RECIPE_INVENTORY
	'''

	def recipeinventory_object(self, row):
		return {'recipeid': row['recipe_id'],
				'inventoryid': row['inventory_id'],
				'quantity':row['quantity']}

	def get_recipeinventory(self, recipeid):
		query = 'SELECT * FROM recipe_inventory WHERE recipe_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (recipeid,)
		cur.execute(query, pvalue)
		rows = cur.fetchall()
		if len(rows) is 0:
			return None
		recipeinventorys = []
		for row in rows:
			recipeinventory = self.recipeinventory_object(row)
			recipeinventorys.append(recipeinventory)
		return recipeinventorys


	def create_recipeinventory(self, recipeid, inventoryid, quantity):
		query='INSERT INTO recipe_inventory(recipe_id, inventory_id, quantity) VALUES(?,?,?)'
		query1 ='SELECT * FROM recipe_inventory WHERE recipe_id = ? AND inventory_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (recipeid,inventoryid)
		cur.execute(query1, pvalue)
		row = cur.fetchone()
		if row is None:
			pvalue = (recipeid, inventoryid, quantity)
			cur.execute(query, pvalue)
			self.con.commit()
			if cur.rowcount < 1:
				return False
			return True
		else:
			return None

	def delete_recipeinventory(self, recipeid, inventoryid):
		query = 'DELETE FROM recipe_inventory WHERE recipe_id = ? AND inventory_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (recipeid, inventoryid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def update_recipeinventory(self, recipeid, inventoryid, quantity):
		query = 'UPDATE recipe_inventory SET quantity = ? WHERE recipe_id=? AND inventory_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (quantity,recipeid, inventoryid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	'''
	LIST_PRODUCT
	'''

	def listproduct_object(self, row):
		return {'groupid': row['group_id'],
				'inventoryid': row['inventory_id']}

	def get_listproduct(self, groupid):
		query = 'SELECT * FROM list_product WHERE group_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid,)
		cur.execute(query, pvalue)
		rows = cur.fetchall()
		if len(rows) is 0:
			return None
		listproducts = []
		for row in rows:
			listproduct = self.listproduct_object(row)
			listproducts.append(listproduct)
		return listproducts

	def create_listproduct(self, groupid, inventoryid):
		query='INSERT INTO list_product(group_id, inventory_id) VALUES(?,?)'
		query1 ='SELECT * FROM list_product WHERE group_id = ? AND inventory_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid,inventoryid)
		cur.execute(query1, pvalue)
		row = cur.fetchone()
		if row is None:
			pvalue = (groupid, inventoryid)
			cur.execute(query, pvalue)
			self.con.commit()
			if cur.rowcount < 1:
				return False
			return True
		else:
			return None

	def delete_listproduct(self, groupid, inventoryid):
		query = 'DELETE FROM list_product WHERE group_id = ? AND inventory_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid, inventoryid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def delete_listproducts(self, groupid):
		query = 'DELETE FROM list_product WHERE group_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True


	'''
	Members_Coordinate
	'''

	def memberscoordinate_object(self, row):
		return {'groupid': row['group_id'],
				'memberid': row['member_id'],
				'latitude': row['latitude'],
				'longitude': row['longitude']}

	def get_memberscoordinate(self, groupid, memberid):
		query = 'SELECT * FROM members_coordinate WHERE group_id = ? AND member_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid, memberid)
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.memberscoordinate_object(row)

	def create_memberscoordinate(self, groupid, memberid, latitude, longitude):
		query='INSERT INTO members_coordinate(group_id, member_id, latitude, longitude) VALUES(?,?,?,?)'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		membercoordinate = self.get_memberscoordinate(groupid, memberid)
		if membercoordinate is None:
			pvalue = (groupid, memberid, latitude, longitude)
			cur.execute(query, pvalue)
			self.con.commit()
			if cur.rowcount < 1:
				return False
			return True
		else:
			return None

	def delete_memberscoordinate(self, groupid, memberid):
		query = 'DELETE FROM members_coordinate WHERE group_id = ? AND member_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (groupid, memberid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def update_memberscoordinate(self, groupid, memberid, latitude, longitude):
		query = 'UPDATE members_coordinate SET latitude = ?, longitude = ? WHERE group_id=? AND member_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (latitude, longitude,groupid, memberid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	'''
	Monitor_member
	'''

	def monitormember_object(self, row):
		return {'memberid': row['member_id'],
				'flag': row['flag']}

	def get_monitormember(self, memberid):
		query = 'SELECT * FROM monitor_member WHERE member_id = ?'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (memberid, )
		cur.execute(query, pvalue)
		row = cur.fetchone()
		if row is None:
			return None
		return self.monitormember_object(row)

	def create_monitormember(self, memberid, flag):
		query='INSERT INTO monitor_member(member_id, flag) VALUES(?,?)'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		monitormember = self.get_monitormember(memberid)
		if monitormember is None:
			pvalue = (memberid, flag)
			cur.execute(query, pvalue)
			self.con.commit()
			if cur.rowcount < 1:
				return False
			return True
		else:
			return None

	def delete_monitormember(self, memberid):
		query = 'DELETE FROM monitor_member WHERE member_id = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (memberid,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def update_monitormember(self, memberid, flag):
		query = 'UPDATE monitor_member SET flag = ? WHERE member_id =?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (flag, memberid)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return None
		return memberid


	'''
	Shops_coordinate
	'''

	def shopscoordinate_object(self, row):
		return {'shopid': row['shop_id'],
				'name': row['name'],
				'latitude1': row['latitude1'],
				'longitude1': row['longitude1'],
				'latitude2': row['latitude2'],
				'longitude2': row['longitude2']}

	def get_shopscoordinate(self):
		query = 'SELECT * FROM shops_coordinate'
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		cur.execute(query,)
		rows = cur.fetchall()
		if len(rows) is 0:
			return None
		shopscoordinates = []
		for row in rows:
			shopscoordinate = self.shopscoordinate_object(row)
			shopscoordinates.append(shopscoordinate)
		return shopscoordinates

	def create_shopscoordinate(self, name, latitude1, longitude1, latitude2, longitude2):
		query='INSERT INTO shops_coordinate(name, latitude1, longitude1, latitude2, longitude2) VALUES(?,?,?,?,?)'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name, latitude1, longitude1, latitude2, longitude2)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True

	def delete_shopscoordinate(self, name):
		query = 'DELETE FROM shops_coordinate WHERE name = ?'
		self.foreign_key()
		self.con.row_factory = sqlite3.Row
		cur = self.con.cursor()
		pvalue = (name,)
		cur.execute(query, pvalue)
		self.con.commit()
		if cur.rowcount < 1:
			return False
		return True
