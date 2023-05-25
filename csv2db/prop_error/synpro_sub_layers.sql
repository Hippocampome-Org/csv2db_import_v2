CREATE VIEW SynproSubLayers AS
SELECT unique_id as neuron_id, SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1) as sub_layer
FROM hippocampome_v1.neurite_quantified 
WHERE unique_id != ''
GROUP BY unique_id, SUBSTRING_INDEX(SUBSTRING_INDEX(neurite,':',1),':',-1);