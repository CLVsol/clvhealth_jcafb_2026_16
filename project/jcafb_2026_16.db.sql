BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "clv_global_tag" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	INTEGER,
	"color"	INTEGER,
	"notes"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_patient_category" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	INTEGER,
	"color"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_patient_marker" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	"color"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_patient_tag" (
	"id"	INTEGER NOT NULL,
	"name"	TEXT,
	"description"	INTEGER,
	"color"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "clv_phase" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"description"	TEXT,
	"code"	INTEGER,
	"notes"	INTEGER,
	"active"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_company" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_country" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"code"	TEXT,
	"ext_index"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_partner" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"type"	TEXT,
	"street_name"	TEXT,
	"street"	TEXT,
	"street_number"	TEXT,
	"street_number2"	TEXT,
	"street2"	TEXT,
	"district"	TEXT,
	"zip"	INTEGER,
	"city_id"	INTEGER,
	"city"	TEXT,
	"state_id"	INTEGER,
	"country_state"	TEXT,
	"country_id"	INTEGER,
	"country"	TEXT,
	"active"	TEXT,
	"ext_id"	INTEGER,
	PRIMARY KEY("id")
);
CREATE TABLE IF NOT EXISTS "res_users" (
	"id"	INTEGER NOT NULL UNIQUE,
	"name"	TEXT,
	"partner_id"	INTEGER,
	"partner"	TEXT,
	"company_id"	INTEGER,
	"company"	TEXT,
	"parent_id"	INTEGER,
	"parent"	TEXT,
	"tz"	TEXT,
	"lang"	TEXT,
	"country_id"	INTEGER,
	"country"	TEXT,
	"login"	TEXT,
	"password"	TEXT,
	"active"	INTEGER,
	"image_1920"	TEXT,
	PRIMARY KEY("id")
);
COMMIT;
