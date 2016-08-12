import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)


SHOP1_ID= 1
SHOPSCOORDINATE1 = {'shopid': SHOP1_ID,
					'name': 'Sale',
					'latitude1' : '65.059914',
					'longitude1': '25.478718',
					'latitude2' : '65.060602',
					'longitude2': '25.480799'}

SHOP2_ID= 2
SHOPSCOORDINATE2 = {'shopid': SHOP2_ID,
					'name': 'Tokmanni',
					'latitude1' : '65.058348',
					'longitude1': '25.476137',
					'latitude2' : '65.059081',
					'longitude2': '25.478980'}


NEW_SHOPCOORDINATE = {'name': 'test',
					'latitude1' : '15.058344',
					'longitude1': '35.476132',
					'latitude2' : '15.059086',
					'longitude2': '35.478981'}

SHOP_WRONG_NAME = 'WRONG'
INITIAL_SIZE = 3

class shopscoordinateDBTest(unittest.TestCase):

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

	def test_shopscoordinate_table_created(self):

		print '('+self.test_shopscoordinate_table_created.__name__+')',self.test_shopscoordinate_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM shops_coordinate'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_shopscoordinate_object(self):

		print '('+self.test_shopscoordinate_object.__name__+')',self.test_shopscoordinate_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM shops_coordinate'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		shopscoordinate = self.connection.shopscoordinate_object(row)
		self.assertDictContainsSubset(shopscoordinate, SHOPSCOORDINATE1)

	def test_get_shopscoordinate(self):

		print '('+self.test_get_shopscoordinate.__name__+')',self.test_get_shopscoordinate.__doc__
		shopscoordinate = self.connection.get_shopscoordinate()
		self.assertDictContainsSubset(shopscoordinate[0], SHOPSCOORDINATE1)
		self.assertDictContainsSubset(shopscoordinate[1], SHOPSCOORDINATE2)

	def test_new_shopscoordinate(self):
		print '('+self.test_new_shopscoordinate.__name__+')',self.test_new_shopscoordinate.__doc__
		shopscoordinate = self.connection.create_shopscoordinate(NEW_SHOPCOORDINATE['name'],NEW_SHOPCOORDINATE['latitude1'],NEW_SHOPCOORDINATE['longitude1'],NEW_SHOPCOORDINATE['latitude2'], NEW_SHOPCOORDINATE['longitude2'])
		self.assertIsNotNone(shopscoordinate)

	def test_delete_shopscoordinate(self):
		print '('+self.test_delete_shopscoordinate.__name__+')',self.test_delete_shopscoordinate.__doc__
		shopscoordinate = self.connection.delete_shopscoordinate(SHOPSCOORDINATE1['name'])
		self.assertTrue(shopscoordinate)

	def test_delete_shopscoordinate_noexistingID(self):
		print '('+self.test_delete_shopscoordinate_noexistingID.__name__+')',self.test_delete_shopscoordinate_noexistingID.__doc__
		shopscoordinate = self.connection.delete_shopscoordinate(SHOP_WRONG_NAME)
		self.assertFalse(shopscoordinate)



if __name__ == '__main__':
	print 'Start running Shops_Coordinate tests'
	unittest.main()	