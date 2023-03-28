-- ----------------------------
-- Sequence structure for nft_detection_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."nft_detection_id_seq";
CREATE SEQUENCE "public"."nft_detection_id_seq"
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;


-- ----------------------------
-- Table structure for nft_detection
-- ----------------------------
DROP TABLE IF EXISTS "public"."nft_detection";
CREATE TABLE "public"."nft_detection" (
  "id" int4 NOT NULL DEFAULT nextval('nft_detection_id_seq'::regclass),
  "logo" varchar(255) COLLATE "pg_catalog"."default",
  "name" varchar(255) COLLATE "pg_catalog"."default",
  "nft_erc" varchar(255) COLLATE "pg_catalog"."default",
  "owner_addr" varchar(255) COLLATE "pg_catalog"."default",
  "trading_holding" jsonb,
  "authenticity" jsonb,
  "trading_security" jsonb,
  "risks" jsonb,
  "error" text COLLATE "pg_catalog"."default",
  "user_detection_id" int4 NOT NULL,
  CONSTRAINT "nft_detection_pkey" PRIMARY KEY ("id"),
  CONSTRAINT "nft_detection_user_detection_id_fkey" FOREIGN KEY ("user_detection_id") REFERENCES "public"."user_detection" ("id") ON DELETE CASCADE ON UPDATE NO ACTION
)
;
COMMENT ON TABLE "public"."nft_detection" IS 'nft检测结果';


-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."nft_detection_id_seq"
OWNED BY "public"."nft_detection"."id";
SELECT setval('"public"."nft_detection_id_seq"', 1, true);

