# EXP(SUM(LOG(COALESCE()))) is equivalent to PRODUCT(). For more info see
# https://lists.mysql.com/mysql/166184
CREATE VIEW SynproTotalCP AS
SELECT 
    source_id,
    target_id,
    1 - EXP(SUM(LOG(COALESCE(1 - CP_mean)))) AS CP_mean_total,
    IF ((1 - EXP(SUM(LOG(COALESCE(1 - CP_mean))))) * SQRT(SUM(POW(CP_std/CP_mean,2))) != 0,
    (1 - EXP(SUM(LOG(COALESCE(1 - CP_mean))))) * SQRT(SUM(POW(CP_std/CP_mean,2))), 'N/A') AS CP_stdev_total,
    COUNT(CP_std) AS parcel_count
FROM
    SynproConnProb
GROUP BY source_id , target_id;