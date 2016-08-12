import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

MEMBER1_ID= 1
MEMBER1 = {'memberid': MEMBER1_ID,
			'flag': 0}

MEMBER2_ID= 2
MEMBER2 = {'memberid': MEMBER2_ID,
			'flag': 0}

NEW_USER={'name': 'kaleema',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295'}

MODIFIED_MONITORMEMBER1 = {'flag': 1}

NEW_MONITORMEMBER = {'flag': 0}

MEMBER_WRONG_ID = -2
INITIAL_SIZE = 3


class monitormemberDBTest(unittest.TestCase):

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

	def test_monitormember_table_created(self):

		print '('+self.test_monitormember_table_created.__name__+')',self.test_monitormember_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM monitor_member'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_monitormember_object(self):

		print '('+self.test_monitormember_object.__name__+')',self.test_monitormember_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM monitor_member'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		monitormember = self.connection.monitormember_object(row)
		self.assertDictContainsSubset(monitormember, MEMBER1)

	def test_get_monitormember(self):

		print '('+self.test_get_monitormember.__name__+')',self.test_get_monitormember.__doc__
		monitormember = self.connection.get_monitormember(MEMBER1_ID)
		self.assertDictContainsSubset(monitormember, MEMBER1)
		monitormember = self.connection.get_monitormember(MEMBER2_ID)
		self.assertDictContainsSubset(monitormember, MEMBER2)

	def test_get_monitormember_noexistingid(self):

		print '('+self.test_get_monitormember_noexistingid.__name__+')',self.test_get_monitormember_noexistingid.__doc__
		monitormember = self.connection.get_monitormember(MEMBER_WRONG_ID)
		self.assertIsNone(monitormember)

	def test_update_monitormember(self):
		print '('+self.test_update_monitormember.__name__+')',self.test_update_monitormember.__doc__
		monitormember = self.connection.update_monitormember(MEMBER1_ID, MODIFIED_MONITORMEMBER1['flag'])
		self.assertEquals(monitormember, MEMBER1_ID)
		monitormember = self.connection.get_monitormember(MEMBER1_ID)
		self.assertEquals(MODIFIED_MONITORMEMBER1['flag'], monitormember['flag'])

	def test_update_monitormember_noexistingid(self):
		print '('+self.test_update_monitormember_noexistingid.__name__+')',self.test_update_monitormember_noexistingid.__doc__
		monitormember = self.connection.update_monitormember(MEMBER_WRONG_ID, MODIFIED_MONITORMEMBER1['flag'])
		self.assertIsNone(monitormember)

	def test_new_monitormember(self):
		print '('+self.test_new_monitormember.__name__+')',self.test_new_monitormember.__doc__
		memberid = self.connection.create_member(NEW_USER['name'],NEW_USER['phone'],NEW_USER['gender'],NEW_USER['dob'])
		monitormember = self.connection.create_monitormember(memberid, NEW_MONITORMEMBER['flag'])
		self.assertIsNotNone(monitormember)

	def test_new_existing_monitormember(self):
		print '('+self.test_new_existing_monitormember.__name__+')',self.test_new_existing_monitormember.__doc__
		monitormember = self.connection.create_monitormember(MEMBER1_ID, NEW_MONITORMEMBER['flag'])
		self.assertIsNone(monitormember)

	def test_delete_monitormember(self):
		print '('+self.test_delete_monitormember.__name__+')',self.test_delete_monitormember.__doc__
		monitormember = self.connection.delete_monitormember(MEMBER1_ID)
		self.assertTrue(monitormember)
		monitormember = self.connection.get_monitormember(MEMBER1_ID)
		self.assertIsNone(monitormember)

	def test_delete_monitormember_noexistingID(self):
		print '('+self.test_delete_monitormember_noexistingID.__name__+')',self.test_delete_monitormember_noexistingID.__doc__
		monitormember = self.connection.delete_monitormember(MEMBER_WRONG_ID)
		self.assertFalse(monitormember)


if __name__ == '__main__':
	print 'Start running Monitor_Member tests'
	unittest.main()	
