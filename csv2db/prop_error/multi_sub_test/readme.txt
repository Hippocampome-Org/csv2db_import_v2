These scripts were created to find neuron connection pairs that have connection points in more than one subregion.
If such pairs are present, additional programming may be needed for displaying the results on the site.
As of hippocampome v2 06/17/2023 there was only one neuron pair found that could have such connection points
in more than one subregion. 

This is also including the list of excluded neurons in pre- and post-synaptic
positions that are found by no results reported in the potential_synapses, number_of_contacts, and probability
columns in number_of_contacts or Synpro_NOCR (number_of_contacts reformatted). The where clause in sub_view.sql
has the condition that those columns must not be empty. The exclusion list avoids including neurons such as
perisomatic-targeting instead of dendrite-targeting neurons the synaptic probability calculations are not
designed to make probability preditions for.

Usage:
Run sub_view.sql or sub_view_alt.sql then sub_count.sql. sub_view.sql and sub_view_alt.sql are two different
ways of producing the same results. Sort the sub_count.sql results by the sub_count column.
Any pairs with more than one subregion listed will be visable as having a greater
than 1 value in the sub_count column.

Results:
The one neuron pair detected to have multi-subregion connections was
neuron id 2020 to 3007.
However, as can be seen by running the lines of code in sub_vals.sql,
neuron 2020 only contains an axon length + volume measurements for CA1 and CA3. Neuron 3007
also contains dendrite length + volume measurement for CA1 and CA2.
The other subregions did not contain length + volume measurements. Therefore,
even through there were some other measurements in different subregions, the only
subregion with enough data to compute a probability for this pair was CA1.

Conclusion
Because of this, there were no neuron pairs found to need probabilities reported
for them in more than one subregion and code was not added to any site displays to detect and
adapt to displaying more than one subregion at this time.
