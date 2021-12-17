CREATE VIEW SynproNumberOfContacts AS
SELECT 
    lhv.source_id,
    lhv.target_id,
    lhv.subregion,
    lhv.parcel,
    (1 / parcel_count) + (constant * axonal_length_mean * dendritic_length_mean) 
    / overlap_volume_mean AS NC_mean,
    ((1 / parcel_count) + (constant * axonal_length_mean * dendritic_length_mean) 
    / overlap_volume_mean) * SQRT(POW((axonal_length_std/axonal_length_mean),2)+
    POW((dendritic_length_std/dendritic_length_mean),2)+
    POW((overlap_volume_std/overlap_volume_mean),2)) as NC_std
FROM
    SynproPairsLHV AS lhv,
    SynproNumberOfParcels AS np,
    SynproVolumeOfOverlap AS vo,
    SynproErrPropConstants AS pec
WHERE
    lhv.source_id = np.source_id
        AND lhv.target_id = np.target_id
        AND lhv.source_id = vo.source_id
        AND lhv.target_id = vo.target_id
        AND lhv.subregion = vo.subregion
        AND lhv.parcel = vo.parcel        
GROUP BY lhv.source_id, lhv.target_id, lhv.subregion, lhv.parcel;