CREATE VIEW SynproNPS AS
SELECT 
    lhv.source_id,
    lhv.target_id,
    lhv.subregion,
    lhv.parcel,
    GROUP_CONCAT((constant*axonal_length_mean*dendritic_length_mean)/volume) as NPS_mean,
    GROUP_CONCAT(((constant*axonal_length_mean*dendritic_length_mean)/volume)*
    SQRT(POW((axonal_length_std/axonal_length_mean),2)+
    (POW((dendritic_length_std/dendritic_length_mean),2)))) as NPS_std
FROM
    SynproPairsLHV as lhv, 
    SynproErrPropConstants as pec, 
    SynproParcelVolumes as pv
WHERE
	pv.subregion = lhv.subregion
AND pv.parcel = lhv.parcel
GROUP BY lhv.source_id, lhv.target_id, lhv.subregion, lhv.parcel;