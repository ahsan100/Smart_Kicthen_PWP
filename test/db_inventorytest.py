import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

INVENTORY1_ID= 1
INVENTORY1 = {'inventoryid': INVENTORY1_ID,
				'name' : 'Banana',
				'description' : 'Long Yellow bananas',
				'threshold': 1,
				'quantity': 2,
		  		'groupid': 1,
		  		'unit': 'KG'}

INVENTORY2_ID= 2
INVENTORY2 = {'inventoryid': INVENTORY2_ID,
				'name' : 'Tomato',
				'description' : 'Red Colourd balls',
				'threshold': 0.5,
				'quantity': 3,
		  		'groupid': 1,
		  		'unit': 'KG'}

NEW_INVENTORY={'name' : 'Test',
				'description' : 'Doing Test',
				'threshold': 2,
				'quantity': 5,
		  		'groupid': 1,
		  		'unit': 'KG'}

MODIFIED_INVENTORY1={'inventoryid': INVENTORY1_ID,
				'name' : 'changed',
				'description' : 'changed',
				'threshold': 3,
				'quantity': 2,
		  		'unit': 'LIT'}

GROUP2_ID = 2
GROUP_WRONG_ID = -1
GROUP2_INVENTORYS = ['Bread', 'Mango Juice', 'Yogurt', 'Jam']

INVENTORY_WRONG_ID = -2
INVENTORY_WRONG_NAME = 'WRONG'
INITIAL_SIZE = 14

class inventoryDBTest(unittest.TestCase):

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

	def test_inventory_table_created(self):

		print '('+self.test_inventory_table_created.__name__+')',self.test_inventory_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM inventory'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_inventory_object(self):

		print '('+self.test_inventory_object.__name__+')',self.test_inventory_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM inventory'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		inventory = self.connection.inventory_object(row)
		self.assertDictContainsSubset(inventory, INVENTORY1)

	def test_get_inventory(self):

		print '('+self.test_get_inventory.__name__+')',self.test_get_inventory.__doc__
		inventory = self.connection.get_inventory(INVENTORY1_ID)
		self.assertDictContainsSubset(inventory, INVENTORY1)
		inventory = self.connection.get_inventory(INVENTORY2_ID)
		self.assertDictContainsSubset(inventory, INVENTORY2)

	def test_get_inventory_noexistingid(self):

		print '('+self.test_get_inventory_noexistingid.__name__+')',self.test_get_inventory_noexistingid.__doc__
		inventory = self.connection.get_inventory(INVENTORY_WRONG_ID)
		self.assertIsNone(inventory)

	def test_get_inventory_name(self):

		print '('+self.test_get_inventory_name.__name__+')',self.test_get_inventory_name.__doc__
		inventory = self.connection.get_inventory_name(INVENTORY1['name'], INVENTORY1['groupid'])
		self.assertDictContainsSubset(inventory, INVENTORY1)
		inventory = self.connection.get_inventory_name(INVENTORY2['name'], INVENTORY2['groupid'])
		self.assertDictContainsSubset(inventory, INVENTORY2)

	def test_get_inventory_noexistingname(self):

		print '('+self.test_get_inventory_noexistingname.__name__+')',self.test_get_inventory_noexistingname.__doc__
		inventory = self.connection.get_inventory_name(INVENTORY_WRONG_NAME, INVENTORY1['groupid'])
		self.assertIsNone(inventory)


	def test_get_inventory_groupid(self):

		print '('+self.test_get_inventory_groupid.__name__+')',self.test_get_inventory_groupid.__doc__
		i=0;
		inventorys = self.connection.get_inventorys(GROUP2_ID)
		for inventory in inventorys:
			self.assertEquals(inventory['name'], GROUP2_INVENTORYS[i])
			i= i +1

	def test_get_inventory_noexistinggroupid(self):

		print '('+self.test_get_inventory_noexistinggroupid.__name__+')',self.test_get_inventory_noexistinggroupid.__doc__
		inventory = self.connection.get_inventorys(GROUP_WRONG_ID)
		self.assertIsNone(inventory)

	def test_new_inventory(self):
		print '('+self.test_new_inventory.__name__+')',self.test_new_inventory.__doc__
		inventoryid = self.connection.create_inventory(NEW_INVENTORY['name'],NEW_INVENTORY['description'],NEW_INVENTORY['threshold'],NEW_INVENTORY['quantity'], NEW_INVENTORY['groupid'],NEW_INVENTORY['unit'])
		self.assertIsNotNone(inventoryid)

	def test_new_exsisting_inventory(self):
		print '('+self.test_new_inventory.__name__+')',self.test_new_inventory.__doc__
		inventoryid = self.connection.create_inventory(INVENTORY1['name'],NEW_INVENTORY['description'],NEW_INVENTORY['threshold'],NEW_INVENTORY['quantity'], INVENTORY1['groupid'],NEW_INVENTORY['unit'])
		self.assertIsNone(inventoryid)

	def test_delete_inventory(self):
		print '('+self.test_delete_inventory.__name__+')',self.test_delete_inventory.__doc__
		inventory = self.connection.delete_inventory(INVENTORY1_ID)
		self.assertTrue(inventory)
		inventory = self.connection.get_inventory(INVENTORY1_ID)
		self.assertIsNone(inventory)

	def test_delete_inventory_noexistingID(self):
		print '('+self.test_delete_inventory_noexistingID.__name__+')',self.test_delete_inventory_noexistingID.__doc__
		inventory = self.connection.delete_inventory(INVENTORY_WRONG_ID)
		self.assertFalse(inventory)

	def test_update_inventory(self):
		print '('+self.test_update_inventory.__name__+')',self.test_update_inventory.__doc__
		inventory = self.connection.update_inventory(INVENTORY1_ID,MODIFIED_INVENTORY1['name'],MODIFIED_INVENTORY1['description'],MODIFIED_INVENTORY1['threshold'],MODIFIED_INVENTORY1['quantity'],MODIFIED_INVENTORY1['unit'])
		self.assertEquals(inventory, INVENTORY1_ID)
		inventory = self.connection.get_inventory(INVENTORY1_ID)
		self.assertEquals(MODIFIED_INVENTORY1['name'], inventory['name'])
		self.assertEquals(MODIFIED_INVENTORY1['description'], inventory['description'])
		self.assertEquals(MODIFIED_INVENTORY1['threshold'], inventory['threshold'])
		self.assertEquals(MODIFIED_INVENTORY1['quantity'], inventory['quantity'])
		self.assertEquals(MODIFIED_INVENTORY1['unit'], inventory['unit'])

	def test_update_inventory_noexistingid(self):
		print '('+self.test_update_inventory_noexistingid.__name__+')',self.test_update_inventory_noexistingid.__doc__
		inventory = self.connection.update_inventory(INVENTORY_WRONG_ID, MODIFIED_INVENTORY1['name'],MODIFIED_INVENTORY1['description'],MODIFIED_INVENTORY1['threshold'],MODIFIED_INVENTORY1['quantity'],MODIFIED_INVENTORY1['unit'])
		self.assertIsNone(inventory)


if __name__ == '__main__':
	print 'Start running Inventory tests'
	unittest.main()		