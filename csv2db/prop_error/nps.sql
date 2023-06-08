CREATE VIEW SynproNPS AS
SELECT 
    lhv.source_id,
    lhv.target_id,
    lhv.subregion,
    lhv.parcel,
    # note: ((4/3)*PI()*8/(ibd*1.09)) is volume_int/(length_bouton*length_spine)
    GROUP_CONCAT((((4/3)*PI()*8/(ibd*1.09))*axonal_length_mean*dendritic_length_mean)/volume) as NPS_mean,
    GROUP_CONCAT(((((4/3)*PI()*8/(ibd*1.09))*axonal_length_mean*dendritic_length_mean)/volume)*
    SQRT(POW((axonal_length_std/axonal_length_mean),2)+
    (POW((dendritic_length_std/dendritic_length_mean),2)))) as NPS_std
FROM
    SynproPairsLHV as lhv, 
    #SynproErrPropConstants AS pec
    SynproIBD AS ibd,
    SynproParcelVolumes as pv
WHERE
	pv.subregion = lhv.subregion
AND pv.parcel = lhv.parcel
AND lhv.source_id = ibd.source_id
AND lhv.target_id = ibd.target_id
AND lhv.subregion = ibd.subregion
AND lhv.parcel = ibd.layer
GROUP BY lhv.source_id, lhv.target_id, lhv.subregion, lhv.parcel;