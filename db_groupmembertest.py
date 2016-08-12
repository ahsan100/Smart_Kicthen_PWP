import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

GROUP1_ID= 1
GROUPMEMBER1 = {'groupid': GROUP1_ID,
		  		'memberid': 1}

GROUP2_ID= 3
GROUPMEMBER2 = {'groupid': GROUP2_ID,
		  'memberid': 5}

NEW_USER={'name': 'kaleema',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295'}

NEW_GROUP = {'name' : ' NEWGROUP'}

GROUP_WRONG_ID = -2
MEMBER_WRONG_ID = -2
INITIAL_SIZE = 5

class groupmemberDBTest(unittest.TestCase):

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

	def test_groupmember_table_created(self):

		print '('+self.test_groupmember_table_created.__name__+')',self.test_groupmember_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM group_member'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_groupmember_object(self):

		print '('+self.test_groupmember_object.__name__+')',self.test_groupmember_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM group_member'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		group = self.connection.groupmember_object(row)
		self.assertDictContainsSubset(group, GROUPMEMBER1)

	def test_get_group_memberid(self):

		print '('+self.test_get_group_memberid.__name__+')',self.test_get_group_memberid.__doc__
		group = self.connection.get_group_memberid(GROUPMEMBER1['memberid'])
		self.assertDictContainsSubset(group, GROUPMEMBER1)
		group = self.connection.get_group_memberid(GROUPMEMBER2['memberid'])
		self.assertDictContainsSubset(group, GROUPMEMBER2)

	def test_get_group_noexisting_memberid(self):

		print '('+self.test_get_group_noexisting_memberid.__name__+')',self.test_get_group_noexisting_memberid.__doc__
		group = self.connection.get_group_memberid(MEMBER_WRONG_ID)
		self.assertIsNone(group)

	def test_get_group_groupid(self):

		print '('+self.test_get_group_groupid.__name__+')',self.test_get_group_groupid.__doc__
		group = self.connection.get_group_groupid(GROUP1_ID)
		self.assertDictContainsSubset(group[0], GROUPMEMBER1)
		group = self.connection.get_group_groupid(GROUP2_ID)
		self.assertDictContainsSubset(group[0], GROUPMEMBER2)

	def test_get_group_noexisting_groupid(self):

		print '('+self.test_get_group_noexisting_groupid.__name__+')',self.test_get_group_noexisting_groupid.__doc__
		group = self.connection.get_group_groupid(GROUP_WRONG_ID)
		self.assertIsNone(group)

	def test_new_groupmember(self):
		print '('+self.test_new_groupmember.__name__+')',self.test_new_groupmember.__doc__
		memberid = self.connection.create_member(NEW_USER['name'],NEW_USER['phone'],NEW_USER['gender'],NEW_USER['dob'])
		groupid = self.connection.create_group(NEW_GROUP['name'])
		groupmember = self.connection.create_groupmember(groupid,memberid)
		self.assertTrue(groupmember)

	def test_new_existing_groupmember(self):
		print '('+self.test_new_existing_groupmember.__name__+')',self.test_new_existing_groupmember.__doc__
		groupid = self.connection.create_group(NEW_GROUP['name'])
		groupmember = self.connection.create_groupmember(groupid,GROUPMEMBER1['memberid'])
		self.assertIsNone(groupmember)

	def test_delete_groupmember(self):
		print '('+self.test_delete_groupmember.__name__+')',self.test_delete_groupmember.__doc__
		group = self.connection.delete_group(GROUPMEMBER1['memberid'])
		self.assertTrue(group)
		group = self.connection.get_group(GROUPMEMBER1['memberid'])
		self.assertIsNone(group)

	def test_delete_groupmember_noexistingID(self):
		print '('+self.test_delete_groupmember_noexistingID.__name__+')',self.test_delete_groupmember_noexistingID.__doc__
		group = self.connection.delete_groupmember(MEMBER_WRONG_ID)
		self.assertFalse(group)


if __name__ == '__main__':
	print 'Start running Group_Member tests'
	unittest.main()
