PRAGMA foreign_keys=ON;

CREATE TABLE IF NOT EXISTS `members` (
	`member_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`phone`	TEXT,
	'gender' TEXT,
	'dob' TEXT
);

CREATE TABLE IF NOT EXISTS `user_login` (
	`user_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`member_id`	INTEGER NOT NULL UNIQUE,
	`email`	TEXT NOT NULL UNIQUE,
	`password`	NOT NULL TEXT,
	`timestamp`	TEXT,
	FOREIGN KEY(`member_id`) REFERENCES `members` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `groups` (
	`group_id`	INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT UNIQUE
);

CREATE TABLE IF NOT EXISTS `group_member` (
	`group_id`	INTEGER,
	`member_id`	INTEGER,
	FOREIGN KEY(`group_id`) REFERENCES `groups` ON DELETE CASCADE,
	FOREIGN KEY(`member_id`) REFERENCES `members` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `inventory` (
	`inventory_id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`description`	TEXT,
	`threshold`	REAL,
	`quantity`REAL,
	`group_id`	INTEGER,
	`unit`	TEXT,
	FOREIGN KEY(`group_id`) REFERENCES `groups` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `recipe` (
	`recipe_id`	INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name`	TEXT,
	`details`	TEXT,
	`group_id`	INTEGER,
	`preparation_time`	INTEGER,
	FOREIGN KEY(`group_id`) REFERENCES `groups` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `recipe_inventory` (
	`recipe_id`	INTEGER,
	`inventory_id`	INTEGER,
	`quantity`	REAL,
	FOREIGN KEY(`recipe_id`) REFERENCES `recipe` ON DELETE CASCADE,
	FOREIGN KEY(`inventory_id`) REFERENCES `inventory` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `list_product` (
	`group_id` INTEGER,
	`inventory_id`	INTEGER,
	FOREIGN KEY(`group_id`) REFERENCES `groups` ON DELETE CASCADE,
	FOREIGN KEY(`inventory_id`) REFERENCES `inventory` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `members_coordinate` (
	`group_id` INTEGER,
	`member_id`	INTEGER,
	`latitude` TEXT,
	`longitude` TEXT,
	FOREIGN KEY(`group_id`) REFERENCES `groups` ON DELETE CASCADE,
	FOREIGN KEY(`member_id`) REFERENCES `members` ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS `shops_coordinate` (
	`shop_id` INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT UNIQUE,
	`name` TEXT,
	`latitude1` TEXT,
	`longitude1` TEXT,
	`latitude2` TEXT,
	`longitude2` TEXT
);

CREATE TABLE IF NOT EXISTS `monitor_member` (
	`member_id` INTEGER,
	`flag` INTEGER,
	FOREIGN KEY(`member_id`) REFERENCES `members` ON DELETE CASCADE
);





