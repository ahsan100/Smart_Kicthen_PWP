'''
Created on 20 May 2016
Runs all Database tests
'''
import os

class Run():
	print 'Start running tests'
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_usertest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_groupmembertest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_groupstest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_inventorytest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_listproducttest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_membercoordinatetest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_membertest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_monitormembertest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_recipeinventorytest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_recipetest.py')
	os.system('python /Users/ahsanmanzoor/desktop/Oulu\ Study/pwp/projects/test/db_shopscoordinatetest.py')
	print 'End running tests'
