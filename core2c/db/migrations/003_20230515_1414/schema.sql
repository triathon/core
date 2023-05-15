-- ----------------------------
-- Sequence structure for detect_total_count_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."detect_total_count_id_seq";
CREATE SEQUENCE "public"."detect_total_count_id_seq"
INCREMENT 1
MINVALUE  1
MAXVALUE 2147483647
START 1
CACHE 1;

-- ----------------------------
-- Table structure for detect_total_count
-- ----------------------------
DROP TABLE IF EXISTS "public"."detect_total_count";
CREATE TABLE "public"."detect_total_count" (
  "id" int4 NOT NULL DEFAULT nextval('detect_total_count_id_seq'::regclass),
  "type" int4 NOT NULL DEFAULT 1,
  "num" int4 NOT NULL,
  "user_detection_id" int4 NOT NULL
)
;
COMMENT ON COLUMN "public"."detect_total_count"."type" IS '1 钱包检测 2token检测';
COMMENT ON TABLE "public"."detect_total_count" IS '检测总数';

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."detect_total_count_id_seq"
OWNED BY "public"."detect_total_count"."id";
SELECT setval('"public"."detect_total_count_id_seq"', 5, true);

-- ----------------------------
-- Primary Key structure for table detect_total_count
-- ----------------------------
ALTER TABLE "public"."detect_total_count" ADD CONSTRAINT "detect_total_count_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table detect_total_count
-- ----------------------------
ALTER TABLE "public"."detect_total_count" ADD CONSTRAINT "detect_total_count_user_detection_id_fkey" FOREIGN KEY ("user_detection_id") REFERENCES "public"."user_detection" ("id") ON DELETE CASCADE ON UPDATE NO ACTION;
