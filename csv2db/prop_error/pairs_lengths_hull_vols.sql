CREATE VIEW SynproPairsLHV AS
SELECT 
    source_id, 
    target_id,
    po.subregion,
    po.parcel,
    GROUP_CONCAT(DISTINCT lhv1.length_mean) AS axonal_length_mean,
    GROUP_CONCAT(DISTINCT lhv1.length_std) AS axonal_length_std,
    GROUP_CONCAT(DISTINCT lhv1.convex_hull_mean) AS axonal_convex_hull_mean,
    GROUP_CONCAT(DISTINCT lhv1.convex_hull_std) AS axonal_convex_hull_std,
    GROUP_CONCAT(DISTINCT lhv2.length_mean) AS dendritic_length_mean,
    GROUP_CONCAT(DISTINCT lhv2.length_std) AS dendritic_length_std,
    GROUP_CONCAT(DISTINCT lhv2.convex_hull_mean) AS dendritic_convex_hull_mean,
    GROUP_CONCAT(DISTINCT lhv2.convex_hull_std) AS dendritic_convex_hull_std
FROM
    SynproPairsOrder AS po,
    SynproLengthsHullVols AS lhv1,
    SynproLengthsHullVols AS lhv2
WHERE
    po.source_id = lhv1.unique_id
AND ((po.subregion = lhv1.subregion AND po.subregion = lhv2.subregion)
OR  (lhv1.subregion LIKE '%EC%' AND lhv2.subregion LIKE '%EC%'))
AND po.parcel    = lhv1.parcel
AND lhv1.neurite = 'A'
AND po.target_id = lhv2.unique_id
AND po.parcel    = lhv2.parcel
AND lhv2.neurite = 'D'
GROUP BY po.source_id, po.target_id, po.subregion, po.parcel
#LIMIT 10
#Note about why GROUP_CONCAT(DISTINCT ...) is used:
#Newer version of MySQL have a condition by default that is only_full_group_by [1].
#This condition adds extra safety by restricting queries to need all columns selected
#when using "group by" to depend on the grouping. Otherwise a random value among
#those in the total set of values for that column are returned. GROUP_CONCAT(}
#allows all values in the set for a given column to be returned, therefore not
#raising the error. DISTINCT is used because in this case the values are duplicates.
#Only a single value is therefore expected in the cases included with this synpro
#software with GROUP_CONCAT(DISTINCT ...), and it avoids the error.
#[1] https://www.percona.com/blog/2019/05/13/solve-query-failures-regarding-only_full_group_by-sql-mode/