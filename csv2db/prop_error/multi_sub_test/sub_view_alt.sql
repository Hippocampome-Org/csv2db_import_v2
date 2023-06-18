CREATE view subregions AS
SELECT DISTINCT
    nc.source_ID,
    nc.target_ID,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.neurite, ':', 1),':', - 1) as subregion
FROM
    SynproNOCR as nc
    #number_of_contacts as nc
WHERE
neurite!=''