import unittest, sqlite3
import database

DB_PATH = 'db/main.db'
Engine = database.Engine(DB_PATH)

RECIPE1_ID= 1
RECIPE1 = {'recipeid': RECIPE1_ID,
				'name' : 'Potato & Eggs',
				'details' : 'Pakistani Cusine',
		  		'groupid': 1,
		  		'preparationtime': 15}

RECIPE2_ID= 2
RECIPE2 = {'recipeid': RECIPE2_ID,
				'name' : 'Banana Milkshake',
				'details' : 'Protien Drink',
		  		'groupid': 1,
		  		'preparationtime': 5}

NEW_RECIPE={'name' : 'Test',
				'details' : 'Doing Test',
		  		'groupid': 1,
		  		'preparationtime': 'KG'}

MODIFIED_RECIPE1={'recipeid': RECIPE1_ID,
				'name' : 'changed',
				'details' : 'changed',
		  		'preparationtime': 11}

GROUP1_ID = 1
GROUP_WRONG_ID = -1
GROUP1_RECIPES = ['Potato & Eggs', 'Banana Milkshake', 'Tomato Sauce']

RECIPE_WRONG_ID = -2
RECIPE_WRONG_NAME = 'WRONG'
INITIAL_SIZE = 6

class recipeDBTest(unittest.TestCase):

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

	def test_recipe_table_created(self):

		print '('+self.test_recipe_table_created.__name__+')',self.test_recipe_table_created.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM recipe'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchall()
			self.assertEquals(len(row), INITIAL_SIZE)

	def test_recipe_object(self):

		print '('+self.test_recipe_object.__name__+')',self.test_recipe_object.__doc__
		keys_on = 'PRAGMA foreign_keys = ON'
		query = 'SELECT * FROM recipe'
		con = self.connection.con
		with con:
			con.row_factory = sqlite3.Row
			cur = con.cursor()
			cur.execute(keys_on)
			cur.execute(query)
			row = cur.fetchone()
		recipe = self.connection.recipe_object(row)
		self.assertDictContainsSubset(recipe, RECIPE1)

	def test_get_recipe(self):

		print '('+self.test_get_recipe.__name__+')',self.test_get_recipe.__doc__
		recipe = self.connection.get_recipe(RECIPE1_ID)
		self.assertDictContainsSubset(recipe, RECIPE1)
		recipe = self.connection.get_recipe(RECIPE2_ID)
		self.assertDictContainsSubset(recipe, RECIPE2)

	def test_get_recipe_noexistingid(self):

		print '('+self.test_get_recipe_noexistingid.__name__+')',self.test_get_recipe_noexistingid.__doc__
		recipe = self.connection.get_recipe(RECIPE_WRONG_ID)
		self.assertIsNone(recipe)

	def test_get_recipe_name(self):

		print '('+self.test_get_recipe_name.__name__+')',self.test_get_recipe_name.__doc__
		recipe = self.connection.get_recipe_name(RECIPE1['groupid'], RECIPE1['name'])
		self.assertDictContainsSubset(recipe, RECIPE1)
		recipe = self.connection.get_recipe_name(RECIPE2['groupid'], RECIPE2['name'])
		self.assertDictContainsSubset(recipe, RECIPE2)

	def test_get_recipe_noexistingname(self):

		print '('+self.test_get_recipe_noexistingname.__name__+')',self.test_get_recipe_noexistingname.__doc__
		recipe = self.connection.get_recipe_name(RECIPE_WRONG_NAME, RECIPE1['groupid'])
		self.assertIsNone(recipe)


	def test_get_recipe_groupid(self):

		print '('+self.test_get_recipe_groupid.__name__+')',self.test_get_recipe_groupid.__doc__
		i=0;
		recipes = self.connection.get_recipes(GROUP1_ID)
		for recipe in recipes:
			self.assertEquals(recipe['name'], GROUP1_RECIPES[i])
			i= i +1

	def test_get_recipe_noexistinggroupid(self):

		print '('+self.test_get_recipe_noexistinggroupid.__name__+')',self.test_get_recipe_noexistinggroupid.__doc__
		recipe = self.connection.get_recipes(GROUP_WRONG_ID)
		self.assertIsNone(recipe)

	def test_new_recipe(self):
		print '('+self.test_new_recipe.__name__+')',self.test_new_recipe.__doc__
		recipeid = self.connection.create_recipe(NEW_RECIPE['name'],NEW_RECIPE['details'], NEW_RECIPE['groupid'],NEW_RECIPE['preparationtime'])
		self.assertIsNotNone(recipeid)

	def test_new_exsisting_recipe(self):
		print '('+self.test_new_recipe.__name__+')',self.test_new_recipe.__doc__
		recipeid = self.connection.create_recipe(RECIPE1['name'],NEW_RECIPE['details'], RECIPE1['groupid'],NEW_RECIPE['preparationtime'])
		self.assertIsNone(recipeid)

	def test_delete_recipe(self):
		print '('+self.test_delete_recipe.__name__+')',self.test_delete_recipe.__doc__
		recipe = self.connection.delete_recipe(RECIPE1_ID)
		self.assertTrue(recipe)
		recipe = self.connection.get_recipe(RECIPE1_ID)
		self.assertIsNone(recipe)
		recipe = self.connection.get_recipeinventory(RECIPE1_ID)
		self.assertIsNone(recipe)

	def test_delete_recipe_noexistingID(self):
		print '('+self.test_delete_recipe_noexistingID.__name__+')',self.test_delete_recipe_noexistingID.__doc__
		recipe = self.connection.delete_recipe(RECIPE_WRONG_ID)
		self.assertFalse(recipe)

	def test_update_recipe(self):
		print '('+self.test_update_recipe.__name__+')',self.test_update_recipe.__doc__
		recipe = self.connection.update_recipe(RECIPE1_ID,MODIFIED_RECIPE1['name'],MODIFIED_RECIPE1['details'],MODIFIED_RECIPE1['preparationtime'])
		self.assertEquals(recipe, RECIPE1_ID)
		recipe = self.connection.get_recipe(RECIPE1_ID)
		self.assertEquals(MODIFIED_RECIPE1['name'], recipe['name'])
		self.assertEquals(MODIFIED_RECIPE1['details'], recipe['details'])
		self.assertEquals(MODIFIED_RECIPE1['preparationtime'], recipe['preparationtime'])

	def test_update_recipe_noexistingid(self):
		print '('+self.test_update_recipe_noexistingid.__name__+')',self.test_update_recipe_noexistingid.__doc__
		recipe = self.connection.update_recipe(RECIPE_WRONG_ID, MODIFIED_RECIPE1['name'],MODIFIED_RECIPE1['details'],MODIFIED_RECIPE1['preparationtime'])
		self.assertIsNone(recipe)


if __name__ == '__main__':
	print 'Start running recipe tests'
	unittest.main()		