CREATE VIEW SynproConnProb AS
SELECT 
	lhv.source_id, 
    lhv.target_id,
    lhv.subregion,
    lhv.parcel,
    NPS_mean/NC_mean as CP_mean,
    (NPS_mean/NC_mean) * SQRT(POW((NPS_std/NPS_mean),2)+POW((NC_std/NC_mean),2)) as CP_std
FROM
    SynproPairsLHV as lhv, SynproNPS as nps, SynproNumberOfContacts as noc
WHERE
    lhv.source_id = nps.source_id
AND lhv.target_id = nps.target_id
AND lhv.subregion = nps.subregion
AND lhv.parcel = nps.parcel
AND lhv.source_id = noc.source_id
AND lhv.target_id = noc.target_id
AND lhv.subregion = noc.subregion
AND lhv.parcel = noc.parcel    
GROUP BY
	nps.source_id, nps.target_id, nps.subregion, nps.parcel