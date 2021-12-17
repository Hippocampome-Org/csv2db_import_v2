CREATE VIEW SynproTotalNOC AS
SELECT 
    source_id,
    target_id,
    SUM(NC_mean) AS NC_mean_total,
    IF (SQRT(SUM(POW(NC_std,2))) != 0,
    SQRT(SUM(POW(NC_std,2))), 'N/A') AS NC_stdev_total,
    COUNT(NC_std) as parcel_count
FROM
    SynproNumberOfContacts
GROUP BY source_id , target_id;