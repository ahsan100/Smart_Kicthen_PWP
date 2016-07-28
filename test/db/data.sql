INSERT INTO "members" VALUES(1,'Ahsan Manzoor','+358413660505', 'Male', '030191');
INSERT INTO "members" VALUES(2,'Awais Aslam','+358414735298', 'Male', '140291');
INSERT INTO "members" VALUES(3,'Kaleemullah Khan','+358449220732', 'Male', '090991');
INSERT INTO "members" VALUES(4,'Abdul Hannan','+358413674839', 'Male', '170392');
INSERT INTO "members" VALUES(5,'Qandeel Baloch','+923008474974', 'Female', '150289');
INSERT INTO "user_login" VALUES(1, 1, 'ahsan.manzoor@student.oulu.fi', 'ahsan123' , '2016-03-15 01:48:05');
INSERT INTO "user_login" VALUES(2, 2, 'awais.aslam@student.oulu.fi', 'awais123' , '2016-03-16 12:48:43');
INSERT INTO "user_login" VALUES(3, 3, 'Kaleemullah.khan@student.oulu.fi', 'kaleem123' , '2016-03-16 07:33:05');
INSERT INTO "user_login" VALUES(4, 4, 'abdul.hannan@student.oulu.fi', 'abdul123' , '2016-03-17 11:55:56');
INSERT INTO "user_login" VALUES(5, 5, 'qandeel.baloch@student.oulu.fi', 'qandeel123' , '2016-03-18 23:36:21');
INSERT INTO "groups" VALUES(1, 'admins');
INSERT INTO "groups" VALUES(2, 'friends');
INSERT INTO "groups" VALUES(3, 'gasti');
INSERT INTO "group_member" VALUES(1, 1);
INSERT INTO "group_member" VALUES(1, 2);
INSERT INTO "group_member" VALUES(2, 3);
INSERT INTO "group_member" VALUES(2, 4);
INSERT INTO "group_member" VALUES(3, 5);
INSERT INTO "inventory" VALUES(1, 'Banana', 'Long Yellow bananas', 1, 2, 1, 'KG');
INSERT INTO "inventory" VALUES(2, 'Tomato', 'Red Colourd balls', 0.5, 3,1, 'KG');
INSERT INTO "inventory" VALUES(3, 'Bread', 'Morning Food Yum Yum', 6, 5,1, 'PIECE');
INSERT INTO "inventory" VALUES(4, 'Bread', 'Morning Food Yum Yum', 6, 18,2, 'PIECE');
INSERT INTO "inventory" VALUES(5, 'Mango Juice', 'Liquid with mango', 0.5,0.4, 2, 'LITRE');
INSERT INTO "inventory" VALUES(6, 'Yogurt', 'Frozen Milk' , 0.5, 1.5,2, 'KG');
INSERT INTO "inventory" VALUES(7, 'Cucumber', 'Very Long', 0.5, 1,3, 'KG');
INSERT INTO "inventory" VALUES(8, 'Banana', 'Long Yellow' , 0.5, 2,3, 'KG');
INSERT INTO "inventory" VALUES(9, 'Egg', 'Ducky Ducky' , 3, 8,3, 'PIECE');
INSERT INTO "inventory" VALUES(10, 'Egg', 'Ducky Ducky', 3, 2,1, 'PIECE');
INSERT INTO "inventory" VALUES(11, 'Potato', 'Sweet', 0.5, 2,1, 'KG');
INSERT INTO "inventory" VALUES(12, 'Milk', 'Power', 0.5, 4,1, 'LITRE');
INSERT INTO "inventory" VALUES(13, 'Jam', 'Breakfast with it', 0.1, 0.6, 2, 'KG');
INSERT INTO "inventory" VALUES(14, 'Milk', 'Power', 0.5, 3.5,3, 'LITRE');
INSERT INTO "recipe" VALUES(1, 'Potato & Eggs', 'Pakistani Cusine', 1, 15);
INSERT INTO "recipe" VALUES(2, 'Banana Milkshake', 'Protien Drink', 1, 5);
INSERT INTO "recipe" VALUES(3, 'Tomato Sauce', 'Sauce with alot of tomatoes', 1, 5);
INSERT INTO "recipe" VALUES(4, 'Bread Jam', 'Good Food', 2, 3);
INSERT INTO "recipe" VALUES(5, 'Omelette', 'Egg Omelette', 3, 10);
INSERT INTO "recipe" VALUES(6, 'Banana Milkshake', 'Protien Drink', 3, 5);
INSERT INTO "recipe_inventory" VALUES(1, 10, 4);
INSERT INTO "recipe_inventory" VALUES(1, 11, .3);
INSERT INTO "recipe_inventory" VALUES(2, 1, .2);
INSERT INTO "recipe_inventory" VALUES(2, 12, .4);
INSERT INTO "recipe_inventory" VALUES(3, 2, .25);
INSERT INTO "recipe_inventory" VALUES(4, 4, 2);
INSERT INTO "recipe_inventory" VALUES(4, 13, .05);
INSERT INTO "recipe_inventory" VALUES(5, 9, .4);
INSERT INTO "recipe_inventory" VALUES(6, 8, .2);
INSERT INTO "recipe_inventory" VALUES(6, 14, .4);
INSERT INTO "list_product" VALUES(1, 3);
INSERT INTO "list_product" VALUES(1, 10);
INSERT INTO "list_product" VALUES(2, 5);
INSERT INTO "members_coordinate" VALUES(1,1, '65.058428', '25.465373');
INSERT INTO "shops_coordinate" VALUES(1, 'Sale', '65.059914', '25.478718', '65.060602', '25.480799');
INSERT INTO "shops_coordinate" VALUES(2, 'Tokmanni', '65.058348', '25.476137', '65.059081', '25.478980');
INSERT INTO "shops_coordinate" VALUES(3, 'University E Gate', '65.057866', '25.468665', '65.058472', '25.470339');
INSERT INTO "monitor_member" VALUES(1, 0);
INSERT INTO "monitor_member" VALUES(2, 0);
INSERT INTO "monitor_member" VALUES(3, 0);















