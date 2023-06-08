SELECT DISTINCT source_id, target_id, subregion, parcel
FROM SynproPairsOrder as po
WHERE NOT EXISTS (SELECT * 
                  FROM  SynproIBD   as ibd
                  WHERE po.source_id = ibd.source_id
					AND po.target_id = ibd.target_id
					AND po.subregion = ibd.subregion
					AND po.parcel    = ibd.layer);