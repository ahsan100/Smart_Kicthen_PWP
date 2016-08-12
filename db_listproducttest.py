import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

GROUP1_ID= 1
LISTPRODUCT1 = {'groupid': GROUP1_ID,
				'inventoryid' : 3}

LISTPRODUCT2 = {'groupid': GROUP1_ID,
				'inventoryid' : 10}

GROUP1_LISTPRODUCT = [3, 10]

NEW_INVENTORY={'name' : 'Test',
				'description' : 'Doing Test',
				'threshold': 2,
				'quantity': 5,
		  		'groupid': 1,
		  		'unit': 'KG'}

GROUP_WRONG_ID = -2
INITIAL_SIZE = 3


class listproductDBTest(unittest.TestCase):

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

	def test_listproduct_table_created(self):

		print '('+self.test_listproduct_table_created.__name__+')',self.test_listproduct_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM list_product'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_listproduct_object(self):

		print '('+self.test_listproduct_object.__name__+')',self.test_listproduct_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM list_product'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		listproduct = self.connection.listproduct_object(row)
		self.assertDictContainsSubset(listproduct,LISTPRODUCT1)

	def test_get_listproduct(self):

		print '('+self.test_get_listproduct.__name__+')',self.test_get_listproduct.__doc__
		listproducts = self.connection.get_listproduct(GROUP1_ID)
		i=0
		for listproduct in listproducts:
			self.assertEquals(listproduct['inventoryid'], GROUP1_LISTPRODUCT[i])
			i =i +1
		

	def test_get_listproduct_noexistingid(self):

		print '('+self.test_get_listproduct_noexistingid.__name__+')',self.test_get_listproduct_noexistingid.__doc__
		listproduct = self.connection.get_listproduct(GROUP_WRONG_ID)
		self.assertIsNone(listproduct)

	def test_new_listproduct(self):
		print '('+self.test_new_listproduct.__name__+')',self.test_new_listproduct.__doc__
		inventoryid = self.connection.create_inventory(NEW_INVENTORY['name'],NEW_INVENTORY['description'],NEW_INVENTORY['threshold'],NEW_INVENTORY['quantity'], NEW_INVENTORY['groupid'],NEW_INVENTORY['unit'])
		listproduct = self.connection.create_listproduct(GROUP1_ID,inventoryid)
		self.assertTrue(listproduct)

	def test_new_existing_listproduct(self):
		print '('+self.test_new_existing_listproduct.__name__+')',self.test_new_existing_listproduct.__doc__
		listproduct = self.connection.create_listproduct(GROUP1_ID,LISTPRODUCT1['inventoryid'])
		self.assertIsNone(listproduct)

	def test_delete_listproduct(self):
		print '('+self.test_delete_listproduct.__name__+')',self.test_delete_listproduct.__doc__
		listproduct = self.connection.delete_listproduct(GROUP1_ID, LISTPRODUCT1['inventoryid'])
		self.assertTrue(listproduct)

	def test_delete_listproduct_noexistingID(self):
		print '('+self.test_delete_listproduct_noexistingID.__name__+')',self.test_delete_listproduct_noexistingID.__doc__
		listproduct = self.connection.delete_listproduct(GROUP_WRONG_ID, LISTPRODUCT1['inventoryid'])
		self.assertFalse(listproduct)


	def test_delete_listproducts(self):
		print '('+self.test_delete_listproducts.__name__+')',self.test_delete_listproducts.__doc__
		listproduct = self.connection.delete_listproducts(GROUP1_ID)
		self.assertTrue(listproduct)

	def test_delete_listproducts_noexistingID(self):
		print '('+self.test_delete_listproducts_noexistingID.__name__+')',self.test_delete_listproducts_noexistingID.__doc__
		listproduct = self.connection.delete_listproducts(GROUP_WRONG_ID)
		self.assertFalse(listproduct)

if __name__ == '__main__':
	print 'Start running List_Products tests'
	unittest.main()	
