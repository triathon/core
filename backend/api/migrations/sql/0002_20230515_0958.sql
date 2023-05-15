-- ----------------------------
-- Sequence structure for api_detectioncount_id_seq
-- ----------------------------
DROP SEQUENCE IF EXISTS "public"."api_detectioncount_id_seq";
CREATE SEQUENCE "public"."api_detectioncount_id_seq"
INCREMENT 1
MINVALUE  1
MAXVALUE 9223372036854775807
START 1
CACHE 1;

-- ----------------------------
-- Table structure for api_detectioncount
-- ----------------------------
DROP TABLE IF EXISTS "public"."api_detectioncount";
CREATE TABLE "public"."api_detectioncount" (
  "id" int8 NOT NULL DEFAULT nextval('api_detectioncount_id_seq'::regclass),
  "num" int4 NOT NULL,
  "document_id" int8 NOT NULL
)
;

-- ----------------------------
-- Alter sequences owned by
-- ----------------------------
ALTER SEQUENCE "public"."api_detectioncount_id_seq"
OWNED BY "public"."api_detectioncount"."id";
SELECT setval('"public"."api_detectioncount_id_seq"', 4, true);

-- ----------------------------
-- Indexes structure for table api_detectioncount
-- ----------------------------
CREATE INDEX "api_detectioncount_document_id_4d17a0b6" ON "public"."api_detectioncount" USING btree (
  "document_id" "pg_catalog"."int8_ops" ASC NULLS LAST
);

-- ----------------------------
-- Primary Key structure for table api_detectioncount
-- ----------------------------
ALTER TABLE "public"."api_detectioncount" ADD CONSTRAINT "api_detectioncount_pkey" PRIMARY KEY ("id");

-- ----------------------------
-- Foreign Keys structure for table api_detectioncount
-- ----------------------------
ALTER TABLE "public"."api_detectioncount" ADD CONSTRAINT "api_detectioncount_document_id_4d17a0b6_fk_api_document_id" FOREIGN KEY ("document_id") REFERENCES "public"."api_document" ("id") ON DELETE NO ACTION ON UPDATE NO ACTION DEFERRABLE INITIALLY DEFERRED;
