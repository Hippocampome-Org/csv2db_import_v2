CREATE VIEW SynproVolumeOfOverlap AS
SELECT 
    source_id,
    target_id,
    subregion,
    parcel,
    ((axonal_convex_hull_mean + dendritic_convex_hull_mean) / 4) AS overlap_volume_mean,
    SQRT(POW(axonal_convex_hull_std,2) + POW(dendritic_convex_hull_std,2)) AS overlap_volume_std
FROM
    SynproPairsLHV;