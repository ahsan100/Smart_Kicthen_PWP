import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

RECIPE1_ID= 1
RECIPEINVENTORY1 = {'recipeid': RECIPE1_ID,
				'inventoryid' : 10,
				'quantity' : 4}

RECIPEINVENTORY2 = {'recipeid': RECIPE1_ID,
				'inventoryid' : 11,
		  		'quantity': 0.3}

NEW_RECIPE={'name' : 'Test',
				'details' : 'Doing Test',
		  		'groupid': 1,
		  		'preparationtime': 'KG'}

NEW_INVENTORY={'name' : 'Test',
				'description' : 'Doing Test',
				'threshold': 2,
				'quantity': 5,
		  		'groupid': 1,
		  		'unit': 'KG'}

NEW_RECIPEINVENTORY = {'quantity' : 5}

MODIFIED_RECIPEINVENTORY1 = {'quantity': 2}

RECIPE_WRONG_ID = -2
RECIPE1_INVENTORY = [10, 11]

INITIAL_SIZE = 10

class recipeinventoryDBTest(unittest.TestCase):

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

	def test_recipeinventory_table_created(self):

		print '('+self.test_recipeinventory_table_created.__name__+')',self.test_recipeinventory_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM recipe_inventory'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_recipeinventory_object(self):

		print '('+self.test_recipeinventory_object.__name__+')',self.test_recipeinventory_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM recipe_inventory'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		recipeinventory = self.connection.recipeinventory_object(row)
		self.assertDictContainsSubset(recipeinventory, RECIPEINVENTORY1)

	def test_get_recipeinventory(self):

		print '('+self.test_get_recipeinventory.__name__+')',self.test_get_recipeinventory.__doc__
		recipeinventorys = self.connection.get_recipeinventory(RECIPE1_ID)
		i=0
		for recipeinventory in recipeinventorys:
			self.assertEquals(recipeinventory['inventoryid'], RECIPE1_INVENTORY[i])
			i =i +1

	def test_get_recipeinventory_noexistingid(self):

		print '('+self.test_get_recipeinventory_noexistingid.__name__+')',self.test_get_recipeinventory_noexistingid.__doc__
		recipeinventory = self.connection.get_recipeinventory(RECIPE_WRONG_ID)
		self.assertIsNone(recipeinventory)

	def test_new_recipeinventory(self):

		print '('+self.test_new_recipeinventory.__name__+')',self.test_new_recipeinventory.__doc__
		recipeid = self.connection.create_recipe(NEW_RECIPE['name'],NEW_RECIPE['details'], NEW_RECIPE['groupid'],NEW_RECIPE['preparationtime'])
		inventoryid = self.connection.create_inventory(NEW_INVENTORY['name'],NEW_INVENTORY['description'],NEW_INVENTORY['threshold'],NEW_INVENTORY['quantity'], NEW_INVENTORY['groupid'],NEW_INVENTORY['unit'])
		recipeinventory = self.connection.create_recipeinventory(recipeid,inventoryid, NEW_RECIPEINVENTORY['quantity'])
		self.assertTrue(recipeinventory)

	def test_new_existing_recipeinventory(self):
		print '('+self.test_new_existing_recipeinventory.__name__+')',self.test_new_existing_recipeinventory.__doc__
		inventoryid = self.connection.create_inventory(NEW_INVENTORY['name'],NEW_INVENTORY['description'],NEW_INVENTORY['threshold'],NEW_INVENTORY['quantity'], NEW_INVENTORY['groupid'],NEW_INVENTORY['unit'])
		recipeinventory = self.connection.create_recipeinventory(RECIPE1_ID,RECIPEINVENTORY1['inventoryid'], NEW_RECIPEINVENTORY['quantity'])
		self.assertIsNone(recipeinventory)


	def test_delete_recipeinventory(self):
		print '('+self.test_delete_recipeinventory.__name__+')',self.test_delete_recipeinventory.__doc__
		recipeinventory = self.connection.delete_recipeinventory(RECIPE1_ID, RECIPEINVENTORY1['inventoryid'])
		self.assertTrue(recipeinventory)

	def test_delete_recipeinventory_noexistingID(self):
		print '('+self.test_delete_recipeinventory_noexistingID.__name__+')',self.test_delete_recipeinventory_noexistingID.__doc__
		recipeinventory = self.connection.delete_recipeinventory(RECIPE_WRONG_ID, RECIPEINVENTORY1['inventoryid'])
		self.assertFalse(recipeinventory)

	def test_update_recipeinventory(self):
		print '('+self.test_update_recipeinventory.__name__+')',self.test_update_recipeinventory.__doc__
		recipeinventory = self.connection.update_recipeinventory(RECIPE1_ID, RECIPEINVENTORY1['inventoryid'], MODIFIED_RECIPEINVENTORY1['quantity'])
		self.assertTrue(recipeinventory)

	def test_update_recipeinventory_noexistingid(self):
		print '('+self.test_update_recipeinventory_noexistingid.__name__+')',self.test_update_recipeinventory_noexistingid.__doc__
		recipeinventory = self.connection.update_recipeinventory(RECIPE_WRONG_ID,RECIPEINVENTORY1['inventoryid'], MODIFIED_RECIPEINVENTORY1['quantity'])
		self.assertFalse(recipeinventory)

if __name__ == '__main__':
	print 'Start running Recipe Inventory tests'
	unittest.main()	


