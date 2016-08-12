'''
Created on 20 May 2016
Runs all Database tests
'''
import os

class Run():
	print 'Start running tests'
	os.system('python db_usertest.py')
	os.system('python db_groupmembertest.py')
	os.system('python db_groupstest.py')
	os.system('python db_inventorytest.py')
	os.system('python db_listproducttest.py')
	os.system('python db_membercoordinatetest.py')
	os.system('python db_membertest.py')
	os.system('python db_monitormembertest.py')
	os.system('python db_recipeinventorytest.py')
	os.system('python db_recipetest.py')
	os.system('python db_shopscoordinatetest.py')
	print 'End running tests'
