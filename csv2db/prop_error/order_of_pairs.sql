CREATE VIEW SynproPairsOrder AS
SELECT DISTINCT
    nc.source_ID,
    nc.target_ID,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.layers, ':', 1),':', - 1) AS subregion,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.layers, ':', 2),':', - 1) AS parcel
FROM
    SynproNOCR as nc