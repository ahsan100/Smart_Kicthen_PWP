import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

GROUP1_ID= 1
GROUP1 = {'groupid': GROUP1_ID,
		  'name': 'admins'}

MODIFIED_GROUP1 = {'name': 'MODIFIEDNAME'}

GROUP2_ID= 2
GROUP2 = {'groupid': GROUP2_ID,
		  'name': 'friends'}

NEW_GROUP = {'name' : ' NEWGROUP'}

GROUP_WRONG_ID = -2
INITIAL_SIZE = 3

class groupsDBTest(unittest.TestCase):

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

	def test_groups_table_created(self):

		print '('+self.test_groups_table_created.__name__+')',self.test_groups_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM groups'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_group_object(self):

		print '('+self.test_group_object.__name__+')',self.test_group_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM groups'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		group = self.connection.group_object(row)
		self.assertDictContainsSubset(group, GROUP1)

	def test_get_group(self):

		print '('+self.test_get_group.__name__+')',self.test_get_group.__doc__
		group = self.connection.get_group(GROUP1_ID)
		self.assertDictContainsSubset(group, GROUP1)
		group = self.connection.get_group(GROUP2_ID)
		self.assertDictContainsSubset(group, GROUP2)

	def test_get_group_noexistingid(self):

		print '('+self.test_get_group_noexistingid.__name__+')',self.test_get_group_noexistingid.__doc__
		group = self.connection.get_group(GROUP_WRONG_ID)
		self.assertIsNone(group)

	def test_update_group(self):
		print '('+self.test_update_group.__name__+')',self.test_update_group.__doc__
		group = self.connection.update_group(GROUP1['groupid'], MODIFIED_GROUP1['name'])
		self.assertEquals(group, GROUP1['groupid'])
		group = self.connection.get_group(GROUP1_ID)
		self.assertEquals(MODIFIED_GROUP1['name'], group['name'])

	def test_update_group_noexistingid(self):
		print '('+self.test_update_group_noexistingid.__name__+')',self.test_update_group_noexistingid.__doc__
		group = self.connection.update_group(GROUP_WRONG_ID, MODIFIED_GROUP1['name'])
		self.assertIsNone(group)

	def test_new_group(self):
		print '('+self.test_new_group.__name__+')',self.test_new_group.__doc__
		groupid = self.connection.create_group(NEW_GROUP['name'])
		self.assertIsNotNone(groupid)

	def test_new_existing_group(self):
		print '('+self.test_new_existing_group.__name__+')',self.test_new_existing_group.__doc__
		groupid = self.connection.create_group(GROUP1['name'])
		self.assertIsNone(groupid)

	def test_delete_group(self):
		print '('+self.test_delete_group.__name__+')',self.test_delete_group.__doc__
		group = self.connection.delete_group(GROUP1_ID)
		self.assertTrue(group)
		group = self.connection.get_group(GROUP1_ID)
		self.assertIsNone(group)

	def test_delete_group_noexistingID(self):
		print '('+self.test_delete_group_noexistingID.__name__+')',self.test_delete_group_noexistingID.__doc__
		group = self.connection.delete_member(GROUP_WRONG_ID)
		self.assertFalse(group)

if __name__ == '__main__':
	print 'Start running Groups tests'
	unittest.main()