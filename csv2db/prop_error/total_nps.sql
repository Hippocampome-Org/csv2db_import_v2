CREATE VIEW SynproTotalNPS AS
SELECT 
    source_id, 
    target_id, 
    SUM(NPS_mean) as NPS_mean_total, 
    IF (SQRT(SUM(POW(NPS_std,2))) != 0,
    SQRT(SUM(POW(NPS_std,2))), 'N/A') as NPS_stdev_total,
    COUNT(NPS_mean) as parcel_count
FROM
    SynproNPS
GROUP BY source_id, target_id;