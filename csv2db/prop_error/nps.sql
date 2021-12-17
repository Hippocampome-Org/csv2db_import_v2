CREATE VIEW SynproNPS AS
SELECT 
    lhv.source_id,
    lhv.target_id,
    lhv.subregion,
    lhv.parcel,
    GROUP_CONCAT((constant*axonal_length_mean*dendritic_length_mean)/selected_volume) as NPS_mean,
    GROUP_CONCAT(((constant*axonal_length_mean*dendritic_length_mean)/selected_volume)*
    SQRT(POW((axonal_length_std/axonal_length_mean),2)+
    (POW((dendritic_length_std/dendritic_length_mean),2)))) as NPS_std
FROM
    SynproPairsLHV as lhv, 
    SynproSelectedVolumes as sv, 
    SynproErrPropConstants as pec, 
    SynproSubLayers as sl
WHERE
	sl.neuron_id = lhv.source_id
AND sv.source_id = lhv.source_id
AND sv.target_id = lhv.target_id
AND	sv.subregion = lhv.subregion
AND sv.parcel = lhv.parcel
GROUP BY lhv.source_id, lhv.target_id, lhv.subregion, lhv.parcel;