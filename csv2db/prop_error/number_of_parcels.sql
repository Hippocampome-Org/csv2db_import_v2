CREATE VIEW SynproNumberOfParcels AS
SELECT 
    source_id,
    target_id,
    COUNT(DISTINCT source_id,
        target_id,
        subregion,
		 parcel) as parcel_count
FROM
    SynproPairsLHV
GROUP BY source_id , target_id;