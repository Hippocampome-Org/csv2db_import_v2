CREATE VIEW SynproSelectedVolumes AS
# reference: https://stackoverflow.com/questions/13887616/mysql-if-elseif-in-select-query
SELECT 
    lhv.source_id,
    lhv.target_id,
    GROUP_CONCAT(DISTINCT sl1.sub_layer) AS subregion,
    lhv.parcel,
    GROUP_CONCAT(DISTINCT pv1.volume) AS volume_1,
    GROUP_CONCAT(DISTINCT pv2.volume) AS volume_2,
    (
    CASE
		WHEN GROUP_CONCAT(DISTINCT sl1.sub_layer) = 'EC' AND GROUP_CONCAT(DISTINCT sl2.sub_layer) = "LEC" 
		THEN GROUP_CONCAT(DISTINCT pv1.volume)
		WHEN GROUP_CONCAT(DISTINCT sl1.sub_layer) = 'EC' AND GROUP_CONCAT(DISTINCT sl2.sub_layer) = "MEC" 
		THEN GROUP_CONCAT(DISTINCT pv1.volume)
		WHEN GROUP_CONCAT(DISTINCT sl1.sub_layer) = 'LEC' AND GROUP_CONCAT(DISTINCT sl2.sub_layer) = "EC" 
		THEN GROUP_CONCAT(DISTINCT pv2.volume)
		WHEN GROUP_CONCAT(DISTINCT sl1.sub_layer) = 'MEC' AND GROUP_CONCAT(DISTINCT sl2.sub_layer) = "EC" 
		THEN GROUP_CONCAT(DISTINCT pv2.volume)
		ELSE GROUP_CONCAT(DISTINCT pv1.volume)
    END) as selected_volume
FROM
    SynproPairsLHV AS lhv,
    SynproParcelVolumes AS pv1,
    SynproParcelVolumes AS pv2,
    SynproSubLayers AS sl1,
    SynproSubLayers AS sl2
WHERE
    sl1.neuron_id = lhv.source_id
AND sl1.sub_layer = pv1.subregion
AND sl2.neuron_id = lhv.target_id
AND sl2.sub_layer = pv2.subregion
AND lhv.parcel = pv1.parcel
AND lhv.parcel = pv2.parcel
GROUP BY lhv.source_id , lhv.target_id , lhv.subregion , lhv.parcel;