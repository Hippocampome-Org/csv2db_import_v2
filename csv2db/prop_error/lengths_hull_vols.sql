# Note: nullif(val,'') is used to avoid counting blank entries as 0 in averaging results
CREATE VIEW SynproLengthsHullVols AS
SELECT unique_id, 
GROUP_CONCAT(DISTINCT SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1)) as subregion,
GROUP_CONCAT(DISTINCT SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',2),':',-1)) as parcel, 
GROUP_CONCAT(DISTINCT SUBSTRING_INDEX(neurite,':',-1)) as neurite,
neurite as full_loc, COUNT(nullif(nq.filtered_total_length,'')) as values_count,
AVG(nullif(nq.filtered_total_length,'')) as length_mean, STD(nullif(nq.filtered_total_length,'')) as length_std, 
AVG(nullif(nq.convexhull,'')) as convex_hull_mean, STD(nullif(nq.convexhull,'')) as convex_hull_std
FROM neurite_quantified as nq#, SynproSubLayers as sl
WHERE nq.unique_id!=''
#AND nq.filtered_total_length != 0
#AND nq.filtered_total_length != ''
AND nq.neurite not like "%:All:%"
#AND nq.convexhull != 0
#AND nq.convexhull != ''
#AND nq.unique_id = sl.neuron_id
#AND ((sl.sub_layer = SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1))
#OR (sl.sub_layer = 'MEC' AND SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1) = 'EC')
#OR (sl.sub_layer = 'LEC' AND SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1) = 'EC'))
GROUP BY unique_id, SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1), SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',2),':',-1), nq.neurite
#LIMIT 10;
# Note: SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1) is the subregion extracted from the neurite column