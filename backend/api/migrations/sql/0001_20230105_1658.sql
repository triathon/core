-- ----------------------------
-- Sequence structure for api_document_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_document_id_seq";
CREATE SEQUENCE "public"."api_document_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for api_documentresult_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_documentresult_id_seq";
CREATE SEQUENCE "public"."api_documentresult_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for api_onlinecontract_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_onlinecontract_id_seq";
CREATE SEQUENCE "public"."api_onlinecontract_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for api_uploadcontract_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_uploadcontract_id_seq";
CREATE SEQUENCE "public"."api_uploadcontract_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for api_user_groups_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_user_groups_id_seq";
CREATE SEQUENCE "public"."api_user_groups_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for api_user_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_user_id_seq";
CREATE SEQUENCE "public"."api_user_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for api_user_user_permissions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_user_user_permissions_id_seq";
CREATE SEQUENCE "public"."api_user_user_permissions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for auth_group_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_group_id_seq";
CREATE SEQUENCE "public"."auth_group_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for auth_group_permissions_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_group_permissions_id_seq";
CREATE SEQUENCE "public"."auth_group_permissions_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for auth_permission_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."auth_permission_id_seq";
CREATE SEQUENCE "public"."auth_permission_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for django_content_type_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."django_content_type_id_seq";
CREATE SEQUENCE "public"."django_content_type_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for django_migrations_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."django_migrations_id_seq";
CREATE SEQUENCE "public"."django_migrations_id_seq" 
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for api_document
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_document";
CREATE TABLE "public"."api_document" (
  "id" int8 NOT NULL DEFAULT nextval('api_document_id_seq'::regclass),
  "file_name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "file_type" varchar(5) COLLATE "pg_catalog"."default" NOT NULL,
  "date" int8 NOT NULL,
  "sha1" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "file" bytea NOT NULL,
  "network" text COLLATE "pg_catalog"."default",
  "contract_address" text COLLATE "pg_catalog"."default",
  "user_id" int8 NOT NULL,
  "contract" text COLLATE "pg_catalog"."default" NOT NULL,
  "functions" text COLLATE "pg_catalog"."default",
  "result" jsonb,
  "score" varchar(10) COLLATE "pg_catalog"."default",
  "score_ratio" jsonb
)
;

-- ----------------------------
-- Table structure for api_documentresult
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_documentresult";
CREATE TABLE "public"."api_documentresult" (
  "id" int8 NOT NULL DEFAULT nextval('api_documentresult_id_seq'::regclass),
  "title" varchar(100) COLLATE "pg_catalog"."default",
  "level" varchar(30) COLLATE "pg_catalog"."default",
  "description" text COLLATE "pg_catalog"."default",
  "details" jsonb,
  "document_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for api_onlinecontract
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_onlinecontract";
CREATE TABLE "public"."api_onlinecontract" (
  "id" int8 NOT NULL DEFAULT nextval('api_onlinecontract_id_seq'::regclass),
  "address" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "result" jsonb,
  "functions" text COLLATE "pg_catalog"."default",
  "contract" text COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for api_uploadcontract
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_uploadcontract";
CREATE TABLE "public"."api_uploadcontract" (
  "id" int8 NOT NULL DEFAULT nextval('api_uploadcontract_id_seq'::regclass),
  "result" jsonb,
  "functions" text COLLATE "pg_catalog"."default",
  "contract" text COLLATE "pg_catalog"."default" NOT NULL,
  "user_id" int8 NOT NULL
)
;

-- ----------------------------
-- Table structure for api_user
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_user";
CREATE TABLE "public"."api_user" (
  "id" int8 NOT NULL DEFAULT nextval('api_user_id_seq'::regclass),
  "password" varchar(128) COLLATE "pg_catalog"."default" NOT NULL,
  "last_login" timestamptz(6),
  "is_superuser" bool NOT NULL,
  "username" varchar(150) COLLATE "pg_catalog"."default" NOT NULL,
  "first_name" varchar(150) COLLATE "pg_catalog"."default" NOT NULL,
  "last_name" varchar(150) COLLATE "pg_catalog"."default" NOT NULL,
  "email" varchar(254) COLLATE "pg_catalog"."default" NOT NULL,
  "is_staff" bool NOT NULL,
  "is_active" bool NOT NULL,
  "date_joined" timestamptz(6) NOT NULL,
  "wallet_address" varchar(42) COLLATE "pg_catalog"."default" NOT NULL,
  "nonce" varchar(6) COLLATE "pg_catalog"."default" NOT NULL,
  "rsa_privateKey" varchar(1000) COLLATE "pg_catalog"."default"
)
;

-- ----------------------------
-- Table structure for api_user_groups
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_user_groups";
CREATE TABLE "public"."api_user_groups" (
  "id" int8 NOT NULL DEFAULT nextval('api_user_groups_id_seq'::regclass),
  "user_id" int8 NOT NULL,
  "group_id" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for api_user_user_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_user_user_permissions";
CREATE TABLE "public"."api_user_user_permissions" (
  "id" int8 NOT NULL DEFAULT nextval('api_user_user_permissions_id_seq'::regclass),
  "user_id" int8 NOT NULL,
  "permission_id" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for auth_group
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_group";
CREATE TABLE "public"."auth_group" (
  "id" int4 NOT NULL DEFAULT nextval('auth_group_id_seq'::regclass),
  "name" varchar(150) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for auth_group_permissions
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_group_permissions";
CREATE TABLE "public"."auth_group_permissions" (
  "id" int8 NOT NULL DEFAULT nextval('auth_group_permissions_id_seq'::regclass),
  "group_id" int4 NOT NULL,
  "permission_id" int4 NOT NULL
)
;

-- ----------------------------
-- Table structure for auth_permission
-- ----------------------------
DROP TABLE IF EXISTS "public"."auth_permission";
CREATE TABLE "public"."auth_permission" (
  "id" int4 NOT NULL DEFAULT nextval('auth_permission_id_seq'::regclass),
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "content_type_id" int4 NOT NULL,
  "codename" varchar(100) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for django_content_type
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_content_type";
CREATE TABLE "public"."django_content_type" (
  "id" int4 NOT NULL DEFAULT nextval('django_content_type_id_seq'::regclass),
  "app_label" varchar(100) COLLATE "pg_catalog"."default" NOT NULL,
  "model" varchar(100) COLLATE "pg_catalog"."default" NOT NULL
)
;

-- ----------------------------
-- Table structure for django_migrations
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_migrations";
CREATE TABLE "public"."django_migrations" (
  "id" int8 NOT NULL DEFAULT nextval('django_migrations_id_seq'::regclass),
  "app" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "name" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "applied" timestamptz(6) NOT NULL
)
;

-- ----------------------------
-- Table structure for django_session
-- ----------------------------
DROP TABLE IF EXISTS "public"."django_session";
CREATE TABLE "public"."django_session" (
  "session_key" varchar(40) COLLATE "pg_catalog"."default" NOT NULL,
  "session_data" text COLLATE "pg_catalog"."default" NOT NULL,
  "expire_date" timestamptz(6) NOT NULL
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_document_id_seq"
OWNED BY "public"."api_document"."id";
SELECT setval('"public"."api_document_id_seq"', 145, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_documentresult_id_seq"
OWNED BY "public"."api_documentresult"."id";
SELECT setval('"public"."api_documentresult_id_seq"', 2254, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_onlinecontract_id_seq"
OWNED BY "public"."api_onlinecontract"."id";
SELECT setval('"public"."api_onlinecontract_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_uploadcontract_id_seq"
OWNED BY "public"."api_uploadcontract"."id";
SELECT setval('"public"."api_uploadcontract_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_user_groups_id_seq"
OWNED BY "public"."api_user_groups"."id";
SELECT setval('"public"."api_user_groups_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_user_id_seq"
OWNED BY "public"."api_user"."id";
SELECT setval('"public"."api_user_id_seq"', 16, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_user_user_permissions_id_seq"
OWNED BY "public"."api_user_user_permissions"."id";
SELECT setval('"public"."api_user_user_permissions_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_group_id_seq"
OWNED BY "public"."auth_group"."id";
SELECT setval('"public"."auth_group_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_group_permissions_id_seq"
OWNED BY "public"."auth_group_permissions"."id";
SELECT setval('"public"."auth_group_permissions_id_seq"', 2, false);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."auth_permission_id_seq"
OWNED BY "public"."auth_permission"."id";
SELECT setval('"public"."auth_permission_id_seq"', 45, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."django_content_type_id_seq"
OWNED BY "public"."django_content_type"."id";
SELECT setval('"public"."django_content_type_id_seq"', 12, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."django_migrations_id_seq"
OWNED BY "public"."django_migrations"."id";
SELECT setval('"public"."django_migrations_id_seq"', 29, true);

-- ----------------------------
-- Indexes structure for table api_document
-- ----------------------------
CREATE INDEX "api_document_user_id_fffdf76b" ON "public"."api_document" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table api_document
-- ----------------------------
ALTER TABLE "public"."api_document" ADD CONSTRAINT "api_document_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table api_documentresult
-- ----------------------------
CREATE INDEX "api_documentresult_document_id_7277778b" ON "public"."api_documentresult" USING btree (
  "document_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table api_documentresult
-- ----------------------------
ALTER TABLE "public"."api_documentresult" ADD CONSTRAINT "api_documentresult_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table api_onlinecontract
-- ----------------------------
ALTER TABLE "public"."api_onlinecontract" ADD CONSTRAINT "api_onlinecontract_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table api_uploadcontract
-- ----------------------------
CREATE INDEX "api_uploadcontract_user_id_b4f4cd81" ON "public"."api_uploadcontract" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table api_uploadcontract
-- ----------------------------
ALTER TABLE "public"."api_uploadcontract" ADD CONSTRAINT "api_uploadcontract_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table api_user
-- ----------------------------
CREATE INDEX "api_user_username_cf4e88d2_like" ON "public"."api_user" USING btree (
  "username" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);
CREATE INDEX "api_user_wallet_address_0a002d28_like" ON "public"."api_user" USING btree (
  "wallet_address" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table api_user
-- ----------------------------
ALTER TABLE "public"."api_user" ADD CONSTRAINT "api_user_username_key" UNIQUE ("username");
ALTER TABLE "public"."api_user" ADD CONSTRAINT "api_user_wallet_address_key" UNIQUE ("wallet_address");

-- ----------------------------
-- Primary Key structure for table api_user
-- ----------------------------
ALTER TABLE "public"."api_user" ADD CONSTRAINT "api_user_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table api_user_groups
-- ----------------------------
CREATE INDEX "api_user_groups_group_id_3af85785" ON "public"."api_user_groups" USING btree (
  "group_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "api_user_groups_user_id_a5ff39fa" ON "public"."api_user_groups" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table api_user_groups
-- ----------------------------
ALTER TABLE "public"."api_user_groups" ADD CONSTRAINT "api_user_groups_user_id_group_id_9c7ddfb5_uniq" UNIQUE ("user_id", "group_id");

-- ----------------------------
-- Primary Key structure for table api_user_groups
-- ----------------------------
ALTER TABLE "public"."api_user_groups" ADD CONSTRAINT "api_user_groups_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table api_user_user_permissions
-- ----------------------------
CREATE INDEX "api_user_user_permissions_permission_id_305b7fea" ON "public"."api_user_user_permissions" USING btree (
  "permission_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "api_user_user_permissions_user_id_f3945d65" ON "public"."api_user_user_permissions" USING btree (
  "user_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table api_user_user_permissions
-- ----------------------------
ALTER TABLE "public"."api_user_user_permissions" ADD CONSTRAINT "api_user_user_permissions_user_id_permission_id_a06dd704_uniq" UNIQUE ("user_id", "permission_id");

-- ----------------------------
-- Primary Key structure for table api_user_user_permissions
-- ----------------------------
ALTER TABLE "public"."api_user_user_permissions" ADD CONSTRAINT "api_user_user_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table auth_group
-- ----------------------------
CREATE INDEX "auth_group_name_a6ea08ec_like" ON "public"."auth_group" USING btree (
  "name" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table auth_group
-- ----------------------------
ALTER TABLE "public"."auth_group" ADD CONSTRAINT "auth_group_name_key" UNIQUE ("name");

-- ----------------------------
-- Primary Key structure for table auth_group
-- ----------------------------
ALTER TABLE "public"."auth_group" ADD CONSTRAINT "auth_group_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table auth_group_permissions
-- ----------------------------
CREATE INDEX "auth_group_permissions_group_id_b120cbf9" ON "public"."auth_group_permissions" USING btree (
  "group_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);
CREATE INDEX "auth_group_permissions_permission_id_84c5c92e" ON "public"."auth_group_permissions" USING btree (
  "permission_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table auth_group_permissions
-- ----------------------------
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_group_id_permission_id_0cd325b0_uniq" UNIQUE ("group_id", "permission_id");

-- ----------------------------
-- Primary Key structure for table auth_group_permissions
-- ----------------------------
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table auth_permission
-- ----------------------------
CREATE INDEX "auth_permission_content_type_id_2f476e4b" ON "public"."auth_permission" USING btree (
  "content_type_id" "pg_catalog"."int4_ops" ASC NULLS LAST
);

-- ----------------------------
-- Uniques structure for table auth_permission
-- ----------------------------
ALTER TABLE "public"."auth_permission" ADD CONSTRAINT "auth_permission_content_type_id_codename_01ab375a_uniq" UNIQUE ("content_type_id", "codename");

-- ----------------------------
-- Primary Key structure for table auth_permission
-- ----------------------------
ALTER TABLE "public"."auth_permission" ADD CONSTRAINT "auth_permission_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Uniques structure for table django_content_type
-- ----------------------------
ALTER TABLE "public"."django_content_type" ADD CONSTRAINT "django_content_type_app_label_model_76bd3d3b_uniq" UNIQUE ("app_label", "model");

-- ----------------------------
-- Primary Key structure for table django_content_type
-- ----------------------------
ALTER TABLE "public"."django_content_type" ADD CONSTRAINT "django_content_type_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table django_migrations
-- ----------------------------
ALTER TABLE "public"."django_migrations" ADD CONSTRAINT "django_migrations_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Indexes structure for table django_session
-- ----------------------------
CREATE INDEX "django_session_expire_date_a5c62663" ON "public"."django_session" USING btree (
  "expire_date" "pg_catalog"."timestamptz_ops" ASC NULLS LAST
);
CREATE INDEX "django_session_session_key_c0390e0f_like" ON "public"."django_session" USING btree (
  "session_key" COLLATE "pg_catalog"."default" "pg_catalog"."varchar_pattern_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table django_session
-- ----------------------------
ALTER TABLE "public"."django_session" ADD CONSTRAINT "django_session_pkey" PRIMARY KEY ("session_key");

-- ----------------------------
-- Foreign Keys structure for table api_document
-- ----------------------------
ALTER TABLE "public"."api_document" ADD CONSTRAINT "api_document_user_id_fffdf76b_fk_api_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."api_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- ----------------------------
-- Foreign Keys structure for table api_documentresult
-- ----------------------------
ALTER TABLE "public"."api_documentresult" ADD CONSTRAINT "api_documentresult_document_id_7277778b_fk_api_document_id" FOREIGN KEY ("document_id") REFERENCES "public"."api_document" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- ----------------------------
-- Foreign Keys structure for table api_uploadcontract
-- ----------------------------
ALTER TABLE "public"."api_uploadcontract" ADD CONSTRAINT "api_uploadcontract_user_id_b4f4cd81_fk_api_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."api_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- ----------------------------
-- Foreign Keys structure for table api_user_groups
-- ----------------------------
ALTER TABLE "public"."api_user_groups" ADD CONSTRAINT "api_user_groups_group_id_3af85785_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "public"."api_user_groups" ADD CONSTRAINT "api_user_groups_user_id_a5ff39fa_fk_api_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."api_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- ----------------------------
-- Foreign Keys structure for table api_user_user_permissions
-- ----------------------------
ALTER TABLE "public"."api_user_user_permissions" ADD CONSTRAINT "api_user_user_permis_permission_id_305b7fea_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "public"."api_user_user_permissions" ADD CONSTRAINT "api_user_user_permissions_user_id_f3945d65_fk_api_user_id" FOREIGN KEY ("user_id") REFERENCES "public"."api_user" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- ----------------------------
-- Foreign Keys structure for table auth_group_permissions
-- ----------------------------
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissio_permission_id_84c5c92e_fk_auth_perm" FOREIGN KEY ("permission_id") REFERENCES "public"."auth_permission" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;
ALTER TABLE "public"."auth_group_permissions" ADD CONSTRAINT "auth_group_permissions_group_id_b120cbf9_fk_auth_group_id" FOREIGN KEY ("group_id") REFERENCES "public"."auth_group" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;

-- ----------------------------
-- Foreign Keys structure for table auth_permission
-- ----------------------------
ALTER TABLE "public"."auth_permission" ADD CONSTRAINT "auth_permission_content_type_id_2f476e4b_fk_django_co" FOREIGN KEY ("content_type_id") REFERENCES "public"."django_content_type" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;
