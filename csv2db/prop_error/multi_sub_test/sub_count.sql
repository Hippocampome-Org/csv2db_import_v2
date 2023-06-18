SELECT distinct source_id, target_id, GROUP_CONCAT(subregion) as subregion, count(*) as sub_count
FROM subregions
GROUP BY source_id, target_id