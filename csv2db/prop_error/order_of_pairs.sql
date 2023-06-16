# WHERE statement with potential_synapses, number_of_contacts, and probability
# is for filtering out excluded connections, e.g., perisomatic connections that
# don't target a dendrite, which is represented as a neuron pair to exclude by
# the entries for these columns being absent in the SynproNOCR data
CREATE VIEW SynproPairsOrder AS
SELECT DISTINCT
    nc.source_ID,
    nc.target_ID,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.layers, ':', 1),':', - 1) AS subregion,
    SUBSTRING_INDEX(SUBSTRING_INDEX(nc.layers, ':', 2),':', - 1) AS parcel
FROM
    SynproNOCR as nc
WHERE
    potential_synapses != ''
AND number_of_contacts != ''
AND probability != ''