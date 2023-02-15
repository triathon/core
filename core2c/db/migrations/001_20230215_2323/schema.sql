-- ----------------------------
-- Sequence structure for token_detection_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."token_detection_id_seq";
CREATE SEQUENCE "public"."token_detection_id_seq"
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Sequence structure for user_detection_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."user_detection_id_seq";
CREATE SEQUENCE "public"."user_detection_id_seq"
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for token_detection
-- ----------------------------
DROP TABLE IF EXISTS "public"."token_detection";
CREATE TABLE "public"."token_detection" (
  "id" int4 NOT NULL DEFAULT nextval('token_detection_id_seq'::regclass),
  "logo" varchar(255) COLLATE "pg_catalog"."default",
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "creater_addr" varchar(255) COLLATE "pg_catalog"."default",
  "owner_addr" varchar(255) COLLATE "pg_catalog"."default",
  "total_supply" varchar(255) COLLATE "pg_catalog"."default",
  "holder_count" varchar(255) COLLATE "pg_catalog"."default",
  "top10_holders" jsonb,
  "top10_lp_token" jsonb,
  "contract_security" jsonb,
  "trading_security" jsonb,
  "error" text COLLATE "pg_catalog"."default",
  "user_detection_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."token_detection"."top10_holders" IS 'Top10 holders info';
COMMENT ON COLUMN "public"."token_detection"."top10_lp_token" IS 'Top10 LP token holders info';
COMMENT ON TABLE "public"."token_detection" IS 'token检测';

-- ----------------------------
-- Table structure for user_detection
-- ----------------------------
DROP TABLE IF EXISTS "public"."user_detection";
CREATE TABLE "public"."user_detection" (
  "id" int4 NOT NULL DEFAULT nextval('user_detection_id_seq'::regclass),
  "address" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "user_address" varchar(255) COLLATE "pg_catalog"."default" NOT NULL,
  "chain" varchar(30) COLLATE "pg_catalog"."default" NOT NULL,
  "type" int4 NOT NULL,
  "create_time" timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  "status" varchar(10) COLLATE "pg_catalog"."default" NOT NULL DEFAULT '0'::character varying
)
;
COMMENT ON COLUMN "public"."user_detection"."address" IS '检测地址';
COMMENT ON COLUMN "public"."user_detection"."user_address" IS '用户钱包地址';
COMMENT ON COLUMN "public"."user_detection"."chain" IS '链类型';
COMMENT ON COLUMN "public"."user_detection"."type" IS '1 token检测';
COMMENT ON COLUMN "public"."user_detection"."create_time" IS '创建时间';
COMMENT ON TABLE "public"."user_detection" IS '用户检测';

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."token_detection_id_seq"
OWNED BY "public"."token_detection"."id";
SELECT setval('"public"."token_detection_id_seq"', 7, true);

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."user_detection_id_seq"
OWNED BY "public"."user_detection"."id";
SELECT setval('"public"."user_detection_id_seq"', 7, true);

-- ----------------------------
-- Primary Key structure for table token_detection
-- ----------------------------
ALTER TABLE "public"."token_detection" ADD CONSTRAINT "token_detection_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Primary Key structure for table user_detection
-- ----------------------------
ALTER TABLE "public"."user_detection" ADD CONSTRAINT "user_detection_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table token_detection
-- ----------------------------
ALTER TABLE "public"."token_detection" ADD CONSTRAINT "token_detection_user_detection_id_fkey" FOREIGN KEY ("user_detection_id") REFERENCES "public"."user_detection" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
