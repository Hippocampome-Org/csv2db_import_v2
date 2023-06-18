CREATE view subregions AS
SELECT DISTINCT
    nc.source_ID,
    nc.target_ID,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.layers, ':', 1),':', - 1) as subregion
FROM
    SynproNOCR as nc
    #number_of_contacts as nc
WHERE
    potential_synapses != ''
AND number_of_contacts != ''
AND probability != ''
#GROUP BY nc.source_ID, nc.target_ID, SUBSTRING_INDEX(SUBSTRING_INDEX(nc.layers, ':', 1),':', - 1)