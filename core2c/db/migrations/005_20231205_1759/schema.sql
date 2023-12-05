ALTER TABLE user_detection ADD COLUMN medium_risk integer;
ALTER TABLE user_detection ADD COLUMN high_stake integer;
--

UPDATE user_detection as a SET
  medium_risk = (
	select (
				SUM(b.cs_medium_risk)+
				SUM(b.ts_medium_risk)
		) as medium_sum from token_detection as b WHERE a.id = b.user_detection_id limit 1
	)::integer,
	high_stake = (
	select (
				SUM(b.cs_high_stake)+
				SUM(b.cs_high_stake)
		) as medium_sum from token_detection as b WHERE a.id = b.user_detection_id limit 1
	)::integer;

CREATE INDEX mr_hs ON user_detection (medium_risk, high_stake);