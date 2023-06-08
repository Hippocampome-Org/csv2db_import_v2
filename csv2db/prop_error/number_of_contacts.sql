CREATE VIEW SynproNumberOfContacts AS
SELECT 
    lhv.source_id,
    lhv.target_id,
    lhv.subregion,
    lhv.parcel,
    # note: ((4/3)*PI()*8/(ibd*1.09)) is volume_int/(length_bouton*length_spine)
    (1 / parcel_count) + (((4/3)*PI()*8/(ibd*1.09)) * axonal_length_mean * dendritic_length_mean) 
    / overlap_volume_mean AS NC_mean,
    ((1 / parcel_count) + (((4/3)*PI()*8/(ibd*1.09)) * axonal_length_mean * dendritic_length_mean) 
    / overlap_volume_mean) * SQRT(POW((axonal_length_std/axonal_length_mean),2)+
    POW((dendritic_length_std/dendritic_length_mean),2)+
    POW((overlap_volume_std/overlap_volume_mean),2)) as NC_std
FROM
    SynproPairsLHV AS lhv,
    SynproNumberOfParcels AS np,
    SynproVolumeOfOverlap AS vo,
    #SynproErrPropConstants AS pec
    SynproIBD AS ibd
WHERE
    lhv.source_id = np.source_id
        AND lhv.target_id = np.target_id
        AND lhv.source_id = vo.source_id
        AND lhv.target_id = vo.target_id
        AND lhv.subregion = vo.subregion
        AND lhv.parcel = vo.parcel
        AND lhv.source_id = ibd.source_id
        AND lhv.target_id = ibd.target_id
        AND lhv.subregion = ibd.subregion
        AND lhv.parcel = ibd.layer
GROUP BY lhv.source_id, lhv.target_id, lhv.subregion, lhv.parcel;