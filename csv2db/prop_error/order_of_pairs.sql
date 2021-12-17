CREATE VIEW SynproPairsOrder AS
SELECT DISTINCT
    nc.source_ID,
    nc.target_ID,
    sl.sub_layer AS subregion,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.neurite, ':', 2),':', - 1) AS parcel,
    SUBSTRING_INDEX(nc.neurite, ':', - 1) AS neurite,
    nc.neurite AS full_loc
FROM
    number_of_contacts as nc,
    SynproSubLayers as sl
WHERE
    nc.neurite NOT LIKE '%:All:%'
AND nc.neurite != ''
AND nc.source_id = sl.neuron_id;