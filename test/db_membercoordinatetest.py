import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

GROUP1_ID= 1
MEMBERCOORDINATE = {'groupid': GROUP1_ID,
					'memberid': 1,
					'latitude' : '65.058428',
					'longitude': '25.465373'}


NEW_MEMBERCOORDINATE = {'groupid': GROUP1_ID,
					'memberid': 2,
					'latitude' : '55.058324',
					'longitude': '35.464323'}

MODIFIED_MEMBERCOORDINATE = {'latitude': '12.324211',
							 'longitude': '32.123456'}

GROUP_WRONG_ID = -2
INITIAL_SIZE = 1


class membercoordinateDBTest(unittest.TestCase):

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

	def test_membercoordinate_table_created(self):

		print '('+self.test_membercoordinate_table_created.__name__+')',self.test_membercoordinate_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM members_coordinate'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_membercoordinate_object(self):

		print '('+self.test_membercoordinate_object.__name__+')',self.test_membercoordinate_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM members_coordinate'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		membercoordinate = self.connection.memberscoordinate_object(row)
		self.assertDictContainsSubset(membercoordinate, MEMBERCOORDINATE)

	def test_get_membercoordinate(self):

		print '('+self.test_get_membercoordinate.__name__+')',self.test_get_membercoordinate.__doc__
		membercoordinate = self.connection.get_memberscoordinate(GROUP1_ID, MEMBERCOORDINATE['memberid'])
		self.assertDictContainsSubset(membercoordinate, MEMBERCOORDINATE)

	def test_get_membercoordinate_noexistingid(self):

		print '('+self.test_get_membercoordinate_noexistingid.__name__+')',self.test_get_membercoordinate_noexistingid.__doc__
		membercoordinate = self.connection.get_memberscoordinate(GROUP_WRONG_ID, MEMBERCOORDINATE['memberid'])
		self.assertIsNone(membercoordinate)

	def test_new_membercoordinate(self):
		print '('+self.test_new_membercoordinate.__name__+')',self.test_new_membercoordinate.__doc__
		membercoordinate = self.connection.create_memberscoordinate(NEW_MEMBERCOORDINATE['groupid'],NEW_MEMBERCOORDINATE['memberid'],NEW_MEMBERCOORDINATE['latitude'],NEW_MEMBERCOORDINATE['longitude'])
		self.assertTrue(membercoordinate)

	def test_new_existing_membercoordinate(self):
		print '('+self.test_new_existing_membercoordinate.__name__+')',self.test_new_existing_membercoordinate.__doc__
		membercoordinate = self.connection.create_memberscoordinate(GROUP1_ID,MEMBERCOORDINATE['memberid'], NEW_MEMBERCOORDINATE['latitude'],NEW_MEMBERCOORDINATE['longitude'])
		self.assertIsNone(membercoordinate)

	def test_delete_membercoordinate(self):
		print '('+self.test_delete_membercoordinate.__name__+')',self.test_delete_membercoordinate.__doc__
		membercoordinate = self.connection.delete_memberscoordinate(GROUP1_ID, MEMBERCOORDINATE['memberid'])
		self.assertTrue(membercoordinate)
		membercoordinate = self.connection.get_memberscoordinate(GROUP1_ID, MEMBERCOORDINATE['memberid'])
		self.assertIsNone(membercoordinate)

	def test_delete_membercoordinate_noexistingID(self):
		print '('+self.test_delete_membercoordinate_noexistingID.__name__+')',self.test_delete_membercoordinate_noexistingID.__doc__
		membercoordinate = self.connection.delete_memberscoordinate(GROUP_WRONG_ID, MEMBERCOORDINATE['memberid'])
		self.assertFalse(membercoordinate)

	def test_update_recipeinventory(self):
		print '('+self.test_update_recipeinventory.__name__+')',self.test_update_recipeinventory.__doc__
		membercoordinate = self.connection.update_memberscoordinate(GROUP1_ID, MEMBERCOORDINATE['memberid'], MODIFIED_MEMBERCOORDINATE['latitude'], MODIFIED_MEMBERCOORDINATE['longitude'])
		self.assertTrue(membercoordinate)

	def test_update_membercoordinate_noexistingid(self):
		print '('+self.test_update_membercoordinate_noexistingid.__name__+')',self.test_update_membercoordinate_noexistingid.__doc__
		membercoordinate = self.connection.update_memberscoordinate(GROUP_WRONG_ID, MEMBERCOORDINATE['memberid'], MODIFIED_MEMBERCOORDINATE['latitude'], MODIFIED_MEMBERCOORDINATE['longitude'])
		self.assertFalse(membercoordinate)

if __name__ == '__main__':
	print 'Start running Member_Coordinate tests'
	unittest.main()	

