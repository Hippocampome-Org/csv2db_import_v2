#!/bin/sh

#iconv -UTF-8tin1 UTF-88 file_as_latin1.csv > file_as_utf8.csv

iconv -f latin1 -t UTF-8 iconv/latin1/all.csv > iconv/utf8/all.csv
iconv -f latin1 -t UTF-8 iconv/latin1/article.csv > iconv/utf8/article.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_ephys.csv > iconv/utf8/attachment_ephys.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_fp.csv > iconv/utf8/attachment_fp.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_marker.csv > iconv/utf8/attachment_marker.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_morph.csv > iconv/utf8/attachment_morph.csv
iconv -f latin1 -t UTF-8 iconv/latin1/conn_fragment.csv > iconv/utf8/conn_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/conndata.csv > iconv/utf8/conndata.csv
iconv -f latin1 -t UTF-8 iconv/latin1/ep_fragment.csv > iconv/utf8/ep_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/epdata.csv > iconv/utf8/epdata.csv
iconv -f latin1 -t UTF-8 iconv/latin1/fp_definitions.csv > iconv/utf8/fp_definitions.csv
iconv -f latin1 -t UTF-8 iconv/latin1/fp_fragment.csv > iconv/utf8/fp_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/fp_parameters.csv > iconv/utf8/fp_parameters.csv
iconv -f latin1 -t UTF-8 iconv/latin1/known_connections.csv > iconv/utf8/known_connections.csv
iconv -f latin1 -t UTF-8 iconv/latin1/marker_fragment.csv > iconv/utf8/marker_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/izhmodels_single.csv > iconv/utf8/izhmodels_single.csv
iconv -f latin1 -t UTF-8 iconv/latin1/markerdata.csv > iconv/utf8/markerdata.csv
#iconv -f latin1 -t UTF-8 iconv/latin1/markerdata1.csv > iconv/utf8/markerdata1.csv
#iconv -f latin1 -t UTF-8 iconv/latin1/markerdata2.csv > iconv/utf8/markerdata2.csv
iconv -f latin1 -t UTF-8 iconv/latin1/material_method.csv > iconv/utf8/material_method.csv
iconv -f latin1 -t UTF-8 iconv/latin1/morph_fragment.csv > iconv/utf8/morph_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/morphdata.csv > iconv/utf8/morphdata.csv
iconv -f latin1 -t UTF-8 iconv/latin1/onhold_types_pmids.csv > iconv/utf8/onhold_types_pmids.csv
iconv -f latin1 -t UTF-8 iconv/latin1/packet_notes.csv > iconv/utf8/packet_notes.csv
for i in $(ls iconv/latin1/packet_notes | egrep -e '.*\.txt'); do iconv -f latin1 -t UTF-8 iconv/latin1/packet_notes/$i > iconv/utf8/packet_notes/$i; done
iconv -f latin1 -t UTF-8 iconv/latin1/synonym.csv > iconv/utf8/synonym.csv
iconv -f latin1 -t UTF-8 iconv/latin1/term.csv > iconv/utf8/term.csv
iconv -f latin1 -t UTF-8 iconv/latin1/type.csv > iconv/utf8/type.csv
iconv -f latin1 -t UTF-8 iconv/latin1/user.csv > iconv/utf8/user.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_neurite.csv > iconv/utf8/attachment_neurite.csv
iconv -f latin1 -t UTF-8 iconv/latin1/neurite_quantified.csv > iconv/utf8/neurite_quantified.csv
iconv -f latin1 -t UTF-8 iconv/latin1/neurite.csv > iconv/utf8/neurite.csv
iconv -f latin1 -t UTF-8 iconv/latin1/potential_synapses.csv > iconv/utf8/potential_synapses.csv
iconv -f latin1 -t UTF-8 iconv/latin1/number_of_contacts.csv > iconv/utf8/number_of_contacts.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_conn.csv > iconv/utf8/attachment_conn.csv
iconv -f latin1 -t UTF-8 iconv/latin1/fragment_nbyk.csv > iconv/utf8/fragment_nbyk.csv
iconv -f latin1 -t UTF-8 iconv/latin1/evi_pro_type_rel_nbyk.csv > iconv/utf8/evi_pro_type_rel_nbyk.csv
iconv -f latin1 -t UTF-8 iconv/latin1/fragment_nbym.csv > iconv/utf8/fragment_nbym.csv
iconv -f latin1 -t UTF-8 iconv/latin1/evi_pro_type_rel_nbym.csv > iconv/utf8/evi_pro_type_rel_nbym.csv
iconv -f latin1 -t UTF-8 iconv/latin1/synpro_prop_parcel_rel.csv > iconv/utf8/synpro_prop_parcel_rel.csv
iconv -f latin1 -t UTF-8 iconv/latin1/synpro_type_type_rel.csv > iconv/utf8/synpro_type_type_rel.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_neurite_rar.csv > iconv/utf8/attachment_neurite_rar.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproCP.csv > iconv/utf8/SynproCP.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproCPTotal.csv > iconv/utf8/SynproCPTotal.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproNOC.csv > iconv/utf8/SynproNOC.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproNOCTotal.csv > iconv/utf8/SynproNOCTotal.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproNoPS.csv > iconv/utf8/SynproNoPS.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproNPSTotal.csv > iconv/utf8/SynproNPSTotal.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproParcelVolumes.csv > iconv/utf8/SynproParcelVolumes.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproSubLayers.csv > iconv/utf8/SynproSubLayers.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproVolumesSelected.csv > iconv/utf8/SynproVolumesSelected.csv
iconv -f latin1 -t UTF-8 iconv/latin1/phases.csv > iconv/utf8/phases.csv
iconv -f latin1 -t UTF-8 iconv/latin1/phases_fragment.csv > iconv/utf8/phases_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_phases.csv > iconv/utf8/attachment_phases.csv
iconv -f latin1 -t UTF-8 iconv/latin1/phases_evidence_type_rel.csv > iconv/utf8/phases_evidence_type_rel.csv
iconv -f latin1 -t UTF-8 iconv/latin1/phases_evidence_fragment_rel.csv > iconv/utf8/phases_evidence_fragment_rel.csv
iconv -f latin1 -t UTF-8 iconv/latin1/counts.csv > iconv/utf8/counts.csv
iconv -f latin1 -t UTF-8 iconv/latin1/counts_fragment.csv > iconv/utf8/counts_fragment.csv
iconv -f latin1 -t UTF-8 iconv/latin1/counts_evidence_type_rel.csv > iconv/utf8/counts_evidence_type_rel.csv
iconv -f latin1 -t UTF-8 iconv/latin1/counts_evidence_fragment_rel.csv > iconv/utf8/counts_evidence_fragment_rel.csv
iconv -f latin1 -t UTF-8 iconv/latin1/attachment_counts.csv > iconv/utf8/attachment_counts.csv
iconv -f latin1 -t UTF-8 iconv/latin1/citations.csv > iconv/utf8/citations.csv
iconv -f latin1 -t UTF-8 iconv/latin1/Hippocampome_to_NMO.csv > iconv/utf8/Hippocampome_to_NMO.csv
iconv -f latin1 -t UTF-8 iconv/latin1/ModelDB_mapping.csv > iconv/utf8/ModelDB_mapping.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproIBD.csv > iconv/utf8/SynproIBD.csv
iconv -f latin1 -t UTF-8 iconv/latin1/SynproPairsOrder.csv > iconv/utf8/SynproPairsOrder.csv

cp -vr iconv/utf8/* static/csv2db/dat/

printf "\n"
python3 manage.py makemigrations
python3 manage.py migrate
python3 manage.py flush
printf "\n\n"
python3 manage.py load
printf "\n"

./database_save.sh
