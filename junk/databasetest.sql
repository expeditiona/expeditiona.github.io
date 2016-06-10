BEGIN TRANSACTION;
CREATE TABLE "Restaurant_Info" (
	`restaurant_id`	INTEGER PRIMARY KEY AUTOINCREMENT,
	`restaurant_name`	TEXT
);
INSERT INTO `Restaurant_Info` VALUES (1,'Wendy''s');
INSERT INTO `Restaurant_Info` VALUES (2,'Roy Rogers');
INSERT INTO `Restaurant_Info` VALUES (3,'Burger King');
INSERT INTO `Restaurant_Info` VALUES (4,'Applebee''s');
INSERT INTO `Restaurant_Info` VALUES (5,'TGI Friday''s');
INSERT INTO `Restaurant_Info` VALUES (6,'Olive Garden');
COMMIT;
