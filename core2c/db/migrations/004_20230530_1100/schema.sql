ALTER TABLE "public"."user_detection" ADD COLUMN update_time timestamptz(6) NOT NULL DEFAULT CURRENT_TIMESTAMP;

COMMENT ON COLUMN "public"."user_detection"."update_time" IS '修改时间';


ALTER TABLE token_detection ADD COLUMN cs_medium_risk integer;
ALTER TABLE token_detection ADD COLUMN cs_high_stake integer;

ALTER TABLE token_detection ADD COLUMN ts_medium_risk integer;
ALTER TABLE token_detection ADD COLUMN ts_high_stake integer;

ALTER TABLE token_detection ADD COLUMN ts_sell_tax text;
ALTER TABLE token_detection ADD COLUMN ts_is_honeypot integer;
ALTER TABLE token_detection ADD COLUMN ts_slippage_modifiable integer;

UPDATE token_detection SET
  cs_medium_risk = (contract_security->>'medium_risk')::integer,
  ts_medium_risk = (trading_security->>'medium_risk')::integer,
  cs_high_stake = (contract_security->>'high_stake')::integer,
  ts_high_stake = (trading_security->>'high_stake')::integer,
  ts_sell_tax = trading_security->>'sell_tax',
  ts_is_honeypot = (trading_security->>'is_honeypot')::integer,
  ts_slippage_modifiable = (trading_security->>'slippage_modifiable')::integer;

-- CREATE INDEX token_detection_ts_ih_ts_sm_ts_st ON token_detection (ts_is_honeypot,ts_slippage_modifiable, ts_sell_tax);
-- CREATE INDEX user_detection_type_user_address_ctime_idx ON user_detection (type,user_address, create_time);
-- CREATE INDEX token_detection_udid_idx ON token_detection (user_detection_id);

-- 2023-12-04
ALTER TABLE token_detection ADD COLUMN honeypot integer;

UPDATE token_detection SET
  honeypot =
	CASE
		WHEN ts_is_honeypot = 1 THEN 1
		WHEN ts_slippage_modifiable = 1 THEN 1
		WHEN ts_sell_tax = '1' THEN 1
		ELSE 0
	END;

DROP INDEX token_detection_ts_ih_ts_sm_ts_st;
DROP INDEX user_detection_type_user_address_ctime_idx;
DROP INDEX token_detection_udid_idx;
CREATE INDEX token_detection_honeypot_ud_idx ON token_detection (honeypot, user_detection_id);
