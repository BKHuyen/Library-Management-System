BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "django_migrations" (
	"id"	integer NOT NULL,
	"app"	varchar(255) NOT NULL,
	"name"	varchar(255) NOT NULL,
	"applied"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group_permissions" (
	"id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_groups" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"group_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("group_id") REFERENCES "auth_group"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_user_user_permissions" (
	"id"	integer NOT NULL,
	"user_id"	integer NOT NULL,
	"permission_id"	integer NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("permission_id") REFERENCES "auth_permission"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_admin_log" (
	"id"	integer NOT NULL,
	"action_time"	datetime NOT NULL,
	"object_id"	text,
	"object_repr"	varchar(200) NOT NULL,
	"change_message"	text NOT NULL,
	"content_type_id"	integer,
	"user_id"	integer NOT NULL,
	"action_flag"	smallint unsigned NOT NULL CHECK("action_flag" >= 0),
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	FOREIGN KEY("user_id") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_content_type" (
	"id"	integer NOT NULL,
	"app_label"	varchar(100) NOT NULL,
	"model"	varchar(100) NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_permission" (
	"id"	integer NOT NULL,
	"content_type_id"	integer NOT NULL,
	"codename"	varchar(100) NOT NULL,
	"name"	varchar(255) NOT NULL,
	FOREIGN KEY("content_type_id") REFERENCES "django_content_type"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "auth_group" (
	"id"	integer NOT NULL,
	"name"	varchar(150) NOT NULL UNIQUE,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "django_session" (
	"session_key"	varchar(40) NOT NULL,
	"session_data"	text NOT NULL,
	"expire_date"	datetime NOT NULL,
	PRIMARY KEY("session_key")
);
CREATE TABLE IF NOT EXISTS "lmsApp_subcategory" (
	"id"	integer NOT NULL,
	"name"	varchar(250) NOT NULL,
	"description"	text,
	"status"	varchar(2) NOT NULL,
	"delete_flag"	integer NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_created"	datetime NOT NULL,
	"category_id"	bigint NOT NULL,
	FOREIGN KEY("category_id") REFERENCES "lmsApp_category"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "lmsApp_students" (
	"id"	integer NOT NULL,
	"code"	varchar(250) NOT NULL,
	"first_name"	varchar(250) NOT NULL,
	"middle_name"	varchar(250),
	"last_name"	varchar(250) NOT NULL,
	"gender"	varchar(20) NOT NULL,
	"contact"	varchar(250) NOT NULL,
	"email"	varchar(250) NOT NULL,
	"address"	varchar(250) NOT NULL,
	"status"	varchar(2) NOT NULL,
	"delete_flag"	integer NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_created"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "lmsApp_author" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name_author"	varchar(150) NOT NULL,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "lmsApp_category" (
	"id"	integer NOT NULL,
	"name"	varchar(250) NOT NULL,
	"description"	text,
	"status"	varchar(2) NOT NULL,
	"delete_flag"	integer NOT NULL,
	"date_added"	datetime NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "lmsApp_publisher" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name_publisher"	varchar(250) NOT NULL UNIQUE,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "lmsApp_borrow" (
	"id"	integer NOT NULL,
	"borrowing_date"	date NOT NULL,
	"date_added"	datetime NOT NULL,
	"id_user"	INTEGER NOT NULL,
	FOREIGN KEY("id_user") REFERENCES "auth_user"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "borrowing_detail" (
	"return_date"	datetime,
	"status"	bool,
	"id_book"	INTEGER,
	"id_borrow"	INTEGER,
	PRIMARY KEY("id_book","id_borrow")
);
CREATE TABLE IF NOT EXISTS "writed" (
	"id_author"	INTEGER,
	"id_book"	INTEGER
);
CREATE TABLE IF NOT EXISTS "auth_user" (
	"id"	integer NOT NULL,
	"first_name"	varchar(150) NOT NULL,
	"middle_name"	varchar(150),
	"last_name"	varchar(150) NOT NULL,
	"username"	varchar(100),
	"password"	varchar(128) NOT NULL,
	"gender"	varchar(10),
	"birth_date"	datetime,
	"email"	varchar(254) NOT NULL,
	"contact"	varchar(150),
	"address"	TEXT,
	"date_joined"	datetime NOT NULL,
	"is_active"	bool NOT NULL,
	"is_superuser"	bool NOT NULL,
	"last_login"	datetime,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "lmsApp_books" (
	"id"	integer NOT NULL,
	"isbn"	varchar(250) NOT NULL,
	"title"	varchar(250) NOT NULL,
	"description"	text,
	"author"	text,
	"publisher"	varchar(250) NOT NULL,
	"date_published"	datetime NOT NULL,
	"status"	varchar(2) NOT NULL,
	"delete_flag"	integer NOT NULL,
	"date_added"	datetime NOT NULL,
	"date_created"	datetime NOT NULL,
	"category_id"	bigint NOT NULL,
	"quantity"	integer NOT NULL,
	FOREIGN KEY("category_id") REFERENCES "lmsApp_category"("id") DEFERRABLE INITIALLY DEFERRED,
	PRIMARY KEY("id" AUTOINCREMENT)
);
INSERT INTO "django_migrations" VALUES (1,'contenttypes','0001_initial','2022-05-13 00:56:09.268750');
INSERT INTO "django_migrations" VALUES (2,'auth','0001_initial','2022-05-13 00:56:09.397893');
INSERT INTO "django_migrations" VALUES (3,'admin','0001_initial','2022-05-13 00:56:09.514623');
INSERT INTO "django_migrations" VALUES (4,'admin','0002_logentry_remove_auto_add','2022-05-13 00:56:09.570638');
INSERT INTO "django_migrations" VALUES (5,'admin','0003_logentry_add_action_flag_choices','2022-05-13 00:56:09.638038');
INSERT INTO "django_migrations" VALUES (6,'contenttypes','0002_remove_content_type_name','2022-05-13 00:56:09.720363');
INSERT INTO "django_migrations" VALUES (7,'auth','0002_alter_permission_name_max_length','2022-05-13 00:56:09.780382');
INSERT INTO "django_migrations" VALUES (8,'auth','0003_alter_user_email_max_length','2022-05-13 00:56:09.840382');
INSERT INTO "django_migrations" VALUES (9,'auth','0004_alter_user_username_opts','2022-05-13 00:56:09.888385');
INSERT INTO "django_migrations" VALUES (10,'auth','0005_alter_user_last_login_null','2022-05-13 00:56:09.940390');
INSERT INTO "django_migrations" VALUES (11,'auth','0006_require_contenttypes_0002','2022-05-13 00:56:10.014399');
INSERT INTO "django_migrations" VALUES (12,'auth','0007_alter_validators_add_error_messages','2022-05-13 00:56:10.120221');
INSERT INTO "django_migrations" VALUES (13,'auth','0008_alter_user_username_max_length','2022-05-13 00:56:10.174226');
INSERT INTO "django_migrations" VALUES (14,'auth','0009_alter_user_last_name_max_length','2022-05-13 00:56:10.241229');
INSERT INTO "django_migrations" VALUES (15,'auth','0010_alter_group_name_max_length','2022-05-13 00:56:10.302236');
INSERT INTO "django_migrations" VALUES (16,'auth','0011_update_proxy_permissions','2022-05-13 00:56:10.383241');
INSERT INTO "django_migrations" VALUES (17,'auth','0012_alter_user_first_name_max_length','2022-05-13 00:56:10.441874');
INSERT INTO "django_migrations" VALUES (18,'sessions','0001_initial','2022-05-13 00:56:10.564301');
INSERT INTO "django_migrations" VALUES (19,'lmsApp','0001_initial','2022-05-13 00:56:52.888608');
INSERT INTO "django_migrations" VALUES (20,'lmsApp','0002_books','2022-05-13 05:22:45.500145');
INSERT INTO "django_migrations" VALUES (21,'lmsApp','0003_students','2022-05-13 05:43:18.961943');
INSERT INTO "django_migrations" VALUES (22,'lmsApp','0004_students_course_students_department','2022-05-13 05:55:06.367003');
INSERT INTO "django_migrations" VALUES (23,'lmsApp','0005_borrow','2022-05-13 06:09:12.992037');
INSERT INTO "django_migrations" VALUES (24,'lmsApp','0006_rename_sub_category_books_category_and_more','2023-12-26 08:43:17.727396');
INSERT INTO "django_content_type" VALUES (1,'admin','logentry');
INSERT INTO "django_content_type" VALUES (2,'auth','permission');
INSERT INTO "django_content_type" VALUES (3,'auth','group');
INSERT INTO "django_content_type" VALUES (4,'auth','user');
INSERT INTO "django_content_type" VALUES (5,'contenttypes','contenttype');
INSERT INTO "django_content_type" VALUES (6,'sessions','session');
INSERT INTO "django_content_type" VALUES (7,'lmsApp','subcategory');
INSERT INTO "django_content_type" VALUES (8,'lmsApp','category');
INSERT INTO "django_content_type" VALUES (9,'lmsApp','books');
INSERT INTO "django_content_type" VALUES (10,'lmsApp','students');
INSERT INTO "django_content_type" VALUES (11,'lmsApp','borrow');
INSERT INTO "auth_permission" VALUES (1,1,'add_logentry','Can add log entry');
INSERT INTO "auth_permission" VALUES (2,1,'change_logentry','Can change log entry');
INSERT INTO "auth_permission" VALUES (3,1,'delete_logentry','Can delete log entry');
INSERT INTO "auth_permission" VALUES (4,1,'view_logentry','Can view log entry');
INSERT INTO "auth_permission" VALUES (5,2,'add_permission','Can add permission');
INSERT INTO "auth_permission" VALUES (6,2,'change_permission','Can change permission');
INSERT INTO "auth_permission" VALUES (7,2,'delete_permission','Can delete permission');
INSERT INTO "auth_permission" VALUES (8,2,'view_permission','Can view permission');
INSERT INTO "auth_permission" VALUES (9,3,'add_group','Can add group');
INSERT INTO "auth_permission" VALUES (10,3,'change_group','Can change group');
INSERT INTO "auth_permission" VALUES (11,3,'delete_group','Can delete group');
INSERT INTO "auth_permission" VALUES (12,3,'view_group','Can view group');
INSERT INTO "auth_permission" VALUES (13,4,'add_user','Can add user');
INSERT INTO "auth_permission" VALUES (14,4,'change_user','Can change user');
INSERT INTO "auth_permission" VALUES (15,4,'delete_user','Can delete user');
INSERT INTO "auth_permission" VALUES (16,4,'view_user','Can view user');
INSERT INTO "auth_permission" VALUES (17,5,'add_contenttype','Can add content type');
INSERT INTO "auth_permission" VALUES (18,5,'change_contenttype','Can change content type');
INSERT INTO "auth_permission" VALUES (19,5,'delete_contenttype','Can delete content type');
INSERT INTO "auth_permission" VALUES (20,5,'view_contenttype','Can view content type');
INSERT INTO "auth_permission" VALUES (21,6,'add_session','Can add session');
INSERT INTO "auth_permission" VALUES (22,6,'change_session','Can change session');
INSERT INTO "auth_permission" VALUES (23,6,'delete_session','Can delete session');
INSERT INTO "auth_permission" VALUES (24,6,'view_session','Can view session');
INSERT INTO "auth_permission" VALUES (25,7,'add_subcategory','Can add sub category');
INSERT INTO "auth_permission" VALUES (26,7,'change_subcategory','Can change sub category');
INSERT INTO "auth_permission" VALUES (27,7,'delete_subcategory','Can delete sub category');
INSERT INTO "auth_permission" VALUES (28,7,'view_subcategory','Can view sub category');
INSERT INTO "auth_permission" VALUES (29,8,'add_category','Can add category');
INSERT INTO "auth_permission" VALUES (30,8,'change_category','Can change category');
INSERT INTO "auth_permission" VALUES (31,8,'delete_category','Can delete category');
INSERT INTO "auth_permission" VALUES (32,8,'view_category','Can view category');
INSERT INTO "auth_permission" VALUES (33,9,'add_books','Can add books');
INSERT INTO "auth_permission" VALUES (34,9,'change_books','Can change books');
INSERT INTO "auth_permission" VALUES (35,9,'delete_books','Can delete books');
INSERT INTO "auth_permission" VALUES (36,9,'view_books','Can view books');
INSERT INTO "auth_permission" VALUES (37,10,'add_students','Can add students');
INSERT INTO "auth_permission" VALUES (38,10,'change_students','Can change students');
INSERT INTO "auth_permission" VALUES (39,10,'delete_students','Can delete students');
INSERT INTO "auth_permission" VALUES (40,10,'view_students','Can view students');
INSERT INTO "auth_permission" VALUES (41,11,'add_borrow','Can add borrow');
INSERT INTO "auth_permission" VALUES (42,11,'change_borrow','Can change borrow');
INSERT INTO "auth_permission" VALUES (43,11,'delete_borrow','Can delete borrow');
INSERT INTO "auth_permission" VALUES (44,11,'view_borrow','Can view borrow');
INSERT INTO "django_session" VALUES ('lt3k4jzqxfju3gu8a13z2b7l72hqdj5b','.eJxVjEEOwiAQRe_C2hCgWBiX7nsGMsyAVA0kpV0Z765NutDtf-_9lwi4rSVsPS1hZnERWpx-t4j0SHUHfMd6a5JaXZc5yl2RB-1yapye18P9OyjYy7c2OfmIhs-DRuuZQGdlwSnrMRE5Bg15ZB6AcnLgEfXoUbHLpL3NaMT7A_t3OKQ:1npPYG:wB_SOp7u7utsnF_oHNjMWUuEUYe1BEL9fMuWZE_Or7k','2022-05-27 07:17:28.182072');
INSERT INTO "django_session" VALUES ('1cg4iftlsau080dq445pvbohvxd3xesb','.eJxVjMsOwiAQRf-FtSHyHly67zcQhgGpGkhKuzL-uzbpQrf3nHNfLMRtrWEbeQkzsQuT7PS7YUyP3HZA99hunafe1mVGviv8oINPnfLzerh_BzWO-q2FIa8LKm8J_FlqLNkCWNSStCgJQBmphEOlDQltFTkHQipER94DOvb-AMP_NtQ:1npQJE:79FGnS-0YyvhiLEwAyShmlhHPAtSHzYQhdQXjjUl2hQ','2022-05-27 08:06:00.165097');
INSERT INTO "django_session" VALUES ('1g7mhx4m3jfekuj5e63vgzfuu2lo9eq8','.eJxVjMsOwiAQRf-FtSE86hRcuu83kIEZpGogKe3K-O_apAvd3nPOfYmA21rC1nkJM4mL0OL0u0VMD647oDvWW5Op1XWZo9wVedAup0b8vB7u30HBXr41QiJMaMAbYsfkrAWjdYyYFSoFrMiSM569juOZFOpsCDIYHEZMA4v3BwT9OKY:1rDbUS:1Qz38FZS_kBQLXogGIVJkoEOHaQU4kgyBcY69XWTXzY','2023-12-28 02:30:20.173716');
INSERT INTO "django_session" VALUES ('hainju7o7ungibdpu9n2a5jbycnfb6il','.eJxVjMEOwiAQRP-FsyGwshQ8evcbyLKAVA1NSnsy_rtt0oPOcd6beYtA61LD2vMcxiQuQovTbxeJn7ntID2o3SfJU1vmMcpdkQft8jal_Loe7t9BpV63tULQPODgkjUekK0DdEjmTKyQgVgrVaInE0vRHgB4C1nKno0nD-LzBcHPN8M:1rE4bG:oULmLYkONnFzmeqcpakAgsjnUJLav4PFg0PjZ0TBNo8','2023-12-29 09:35:18.951179');
INSERT INTO "lmsApp_category" VALUES (1,'Educational','Educational Books','1',0,'2022-05-13 04:52:48.087133');
INSERT INTO "lmsApp_category" VALUES (2,'Fiction','Fiction Books','1',0,'2022-05-13 04:53:37.717878');
INSERT INTO "lmsApp_category" VALUES (3,'Fantasy','Fantasy Books','1',0,'2022-05-13 04:54:13.753450');
INSERT INTO "lmsApp_category" VALUES (5,'Sample 101','This is a sample book category only.','1',0,'2022-05-13 07:54:57.109668');
INSERT INTO "lmsApp_category" VALUES (6,'Sample 102','Sample Book Category 101','1',0,'2022-05-13 07:55:16.389927');
INSERT INTO "lmsApp_category" VALUES (7,'test','test - updated','2',1,'2022-05-13 07:55:29.659537');
INSERT INTO "lmsApp_category" VALUES (8,'Toán','sách giáo dục','1',0,'2023-12-14 02:13:32.140205');
CREATE UNIQUE INDEX IF NOT EXISTS "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" ON "auth_group_permissions" (
	"group_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_group_id_b120cbf9" ON "auth_group_permissions" (
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_group_permissions_permission_id_84c5c92e" ON "auth_group_permissions" (
	"permission_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_groups_user_id_group_id_94350c0c_uniq" ON "auth_user_groups" (
	"user_id",
	"group_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_user_id_6a12ed8b" ON "auth_user_groups" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_groups_group_id_97559544" ON "auth_user_groups" (
	"group_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_permission_id_14a6b632_uniq" ON "auth_user_user_permissions" (
	"user_id",
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_user_id_a95ead1b" ON "auth_user_user_permissions" (
	"user_id"
);
CREATE INDEX IF NOT EXISTS "auth_user_user_permissions_permission_id_1fbb5f2c" ON "auth_user_user_permissions" (
	"permission_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_content_type_id_c4bce8eb" ON "django_admin_log" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_admin_log_user_id_c564eba6" ON "django_admin_log" (
	"user_id"
);
CREATE UNIQUE INDEX IF NOT EXISTS "django_content_type_app_label_model_76bd3d3b_uniq" ON "django_content_type" (
	"app_label",
	"model"
);
CREATE UNIQUE INDEX IF NOT EXISTS "auth_permission_content_type_id_codename_01ab375a_uniq" ON "auth_permission" (
	"content_type_id",
	"codename"
);
CREATE INDEX IF NOT EXISTS "auth_permission_content_type_id_2f476e4b" ON "auth_permission" (
	"content_type_id"
);
CREATE INDEX IF NOT EXISTS "django_session_expire_date_a5c62663" ON "django_session" (
	"expire_date"
);
CREATE INDEX IF NOT EXISTS "lmsApp_subcategory_category_id_cc0f0ee1" ON "lmsApp_subcategory" (
	"category_id"
);
CREATE INDEX IF NOT EXISTS "lmsApp_borrow_student_id_970a8e49" ON "lmsApp_borrow" (
	"id_user"
);
CREATE INDEX IF NOT EXISTS "lmsApp_books_category_id_26e0f052" ON "lmsApp_books" (
	"category_id"
);
COMMIT;
