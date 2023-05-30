ALTER TABLE "public"."user_detection" ADD COLUMN update_time timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP;

COMMENT ON COLUMN "public"."user_detection"."update_time" IS '修改时间';