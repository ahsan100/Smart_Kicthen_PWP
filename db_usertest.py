import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

USER1_EMAIL = 'ahsan.manzoor@student.oulu.fi'
USER1= {'userid': 1, 
		'memberid': 1, 
		'email':USER1_EMAIL,
		'password': 'ahsan123' ,
		'timestamp': '2016-03-15 01:48:05'}

MODIFIED_USER1 = {'password': 'passwordupdated'}

USER2_EMAIL = 'awais.aslam@student.oulu.fi'
USER2 = {'userid': 2,
		 'memberid': 2,
		 'email': USER2_EMAIL, 
		 'password': 'awais123' ,
		 'timestamp': '2016-03-16 12:48:43'}

NEW_USER_EMAIL = 'test@student.oulu.fi'
NEW_USER={'name': 'kaleema',
			'gender': 'Female',
			'phone': '+92300123457',
			'dob':'290295',
			'email': NEW_USER_EMAIL,
			'password': 'test'}

USER_WRONG_EMAIL = 'wrong@student.oulu.fi'
USER_WRONG_ID = -2
INITIAL_SIZE = 5


class userDBTest(unittest.TestCase):

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

	def test_userlogin_table_created(self):

		print '('+self.test_userlogin_table_created.__name__+')',self.test_userlogin_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM user_login'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_user_object(self):

		print '('+self.test_user_object.__name__+')',self.test_user_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM user_login'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		user = self.connection.user_object(row)
		self.assertDictContainsSubset(user, USER1)

	def test_get_user(self):

		print '('+self.test_get_user.__name__+')',self.test_get_user.__doc__
		user = self.connection.get_user(USER1_EMAIL)
		self.assertDictContainsSubset(user, USER1)
		user = self.connection.get_user(USER2_EMAIL)
		self.assertDictContainsSubset(user, USER2)

	def test_get_user_noexistingemail(self):

		print '('+self.test_get_user_noexistingemail.__name__+')',self.test_get_user_noexistingemail.__doc__
		user = self.connection.get_user(USER_WRONG_EMAIL)
		self.assertIsNone(user)

	def test_update_user(self):
		print '('+self.test_update_user.__name__+')',self.test_update_user.__doc__
		user = self.connection.update_user(USER1['memberid'], MODIFIED_USER1['password'])
		self.assertEquals(user, USER1['memberid'])
		user = self.connection.get_user(USER1_EMAIL)
		self.assertEquals(MODIFIED_USER1['password'], user['password'])

	def test_update_user_noexistingemail(self):
		print '('+self.test_update_user_noexistingemail.__name__+')',self.test_update_user_noexistingemail.__doc__
		user = self.connection.update_user(USER_WRONG_EMAIL, MODIFIED_USER1['password'])
		self.assertIsNone(user)

	def test_new_user(self):
		print '('+self.test_new_user.__name__+')',self.test_new_user.__doc__
		memberid = self.connection.create_member(NEW_USER['name'],NEW_USER['phone'],NEW_USER['gender'],NEW_USER['dob'])
		userid = self.connection.create_user(memberid,NEW_USER_EMAIL, NEW_USER['password'])
		self.assertIsNotNone(userid)

	def test_new_existing_user(self):
		print '('+self.test_new_existing_user.__name__+')',self.test_new_existing_user.__doc__
		memberid = self.connection.create_member(NEW_USER['name'],NEW_USER['phone'],NEW_USER['gender'],NEW_USER['dob'])
		userid = self.connection.create_user(memberid,USER1_EMAIL, NEW_USER['password'])
		self.assertIsNone(userid)

	def test_get_useremail(self):
		print '('+self.test_get_useremail.__name__+')',self.test_get_useremail.__doc__
		user = self.connection.get_useremail(USER1['memberid'])
		self.assertDictContainsSubset(user, USER1)
		user = self.connection.get_useremail(USER2['memberid'])
		self.assertDictContainsSubset(user, USER2)

	def test_get_useremail_nonexistingid(self):
		print '('+self.test_get_useremail_nonexistingid.__name__+')',self.test_get_useremail_nonexistingid.__doc__
		user = self.connection.get_useremail(USER_WRONG_ID)
		self.assertIsNone(user)

if __name__ == '__main__':
	print 'Start running User tests'
	unittest.main()
