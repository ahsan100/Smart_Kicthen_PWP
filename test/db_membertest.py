import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

MEMBER1_ID = 1
MEMBER1 ={'memberid': MEMBER1_ID,
			'name': 'Ahsan Manzoor',
			'gender': 'Male',
			'phone': '+358413660505',
			'dob':'030191' }
MODIFIED_MEMBER1 = {'phone': '+3589876543'}
MEMBER2_ID = 2
MEMBER2 = {'memberid': MEMBER2_ID,
			'name': 'Awais Aslam',
			'gender': 'Male',
			'phone': '+358414735298',
			'dob':'140291' }

NEW_MEMBER={'name': 'kaleema',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295'}

MEMBER_WRONG_ID = -2
INITIAL_SIZE = 5

class MemberDBTest(unittest.TestCase):

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

	def test_member_table_created(self):

		print '('+self.test_member_table_created.__name__+')',self.test_member_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM members'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_member_object(self):

		print '('+self.test_member_object.__name__+')',self.test_member_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM members'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		member = self.connection.member_object(row)
		self.assertDictContainsSubset(member, MEMBER1)

	def test_get_member(self):

		print '('+self.test_get_member.__name__+')',self.test_get_member.__doc__
		member = self.connection.get_member(MEMBER1_ID)
		self.assertDictContainsSubset(member, MEMBER1)
		member = self.connection.get_member(MEMBER2_ID)
		self.assertDictContainsSubset(member, MEMBER2)

	def test_get_member_noexistingid(self):

		print '('+self.test_get_member_noexistingid.__name__+')',self.test_get_member_noexistingid.__doc__
		member = self.connection.get_member(MEMBER_WRONG_ID)
		self.assertIsNone(member)

	def test_delete_member(self):

		print '('+self.test_delete_member.__name__+')',self.test_delete_member.__doc__
		member = self.connection.delete_member(MEMBER1_ID)
		self.assertTrue(member)
		member = self.connection.get_member(MEMBER1_ID)
		self.assertIsNone(member)
		member = self.connection.get_group_memberid(MEMBER1_ID)
		self.assertIsNone(member)

	def test_delete_member_noexistingID(self):
		print '('+self.test_delete_member_noexistingID.__name__+')',self.test_delete_member_noexistingID.__doc__
		member = self.connection.delete_member(MEMBER_WRONG_ID)
		self.assertFalse(member)

	def test_update_member(self):
		print '('+self.test_update_member.__name__+')',self.test_update_member.__doc__
		member = self.connection.update_member(MEMBER1_ID, MODIFIED_MEMBER1['phone'])
		self.assertEquals(member, MEMBER1_ID)
		member = self.connection.get_member(MEMBER1_ID)
		self.assertEquals(MODIFIED_MEMBER1['phone'], member['phone'])

	def test_update_member_noexistingID(self):
		print '('+self.test_update_member_noexistingID.__name__+')',self.test_update_member_noexistingID.__doc__
		member = self.connection.update_member(MEMBER_WRONG_ID, MODIFIED_MEMBER1['phone'])
		self.assertIsNone(member)

	def test_new_member(self):
		print '('+self.test_new_member.__name__+')',self.test_new_member.__doc__
		memberid = self.connection.create_member(NEW_MEMBER['name'],NEW_MEMBER['phone'],NEW_MEMBER['gender'],NEW_MEMBER['dob'])
		self.assertIsNotNone(memberid)



if __name__ == '__main__':
	print 'Start running Member tests'
	unittest.main()
			
