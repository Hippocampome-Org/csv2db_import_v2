#!/bin/bash

###############################
#
# Build propagate errors values
#
###############################

command="sed -n 5p ../../database_save.sh" # username
command2=$(eval $command)
command3="echo $command2 | cut -c12-10000"
USER=$(eval $command3)
command="sed -n 6p ../../database_save.sh" # password
command2=$(eval $command)
command3="echo $command2 | cut -c16-10000"
PASS=$(eval $command3)
command="sed -n 7p ../../database_save.sh" # database
command2=$(eval $command)
command3="echo $command2 | cut -c15-10000"
DB=$(eval $command3)
ADDR=localhost # db address
CSV_DIR=csv # import csv files location
EXP_DIR="/var/tmp/SynproExports/" # export csv files directory

echo "Dropping old views" &&
mysql -h $ADDR -u $USER -p$PASS $DB < drop_views.sql

echo "Creating constants table"
mysql -h $ADDR -u $USER -p$PASS $DB < constants.sql &&

#echo "Creating subregions and layers table" &&
#mysql -h $ADDR -u $USER -p$PASS $DB < create_synpro_sub_layers.sql &&

#echo "Adding data to subregions and layers table" &&
#mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u $USER -p$PASS $DB $CSV_DIR/SynproSubLayers.csv > /dev/null 2>&1 &&

echo "Running lengths_hull_vols.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < lengths_hull_vols.sql &&
echo "Running order_of_pairs.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < order_of_pairs.sql &&
echo "Running pairs_lengths_hull_vols.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < pairs_lengths_hull_vols.sql &&
echo "Running number_of_parcels.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < number_of_parcels.sql &&

#echo "Creating parcel volumes table" &&
#mysql -h $ADDR -u $USER -p$PASS $DB < create_synpro_parcel_volumes.sql &&

#echo "Adding data to parcel volumes table" &&
#mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u $USER -p$PASS $DB $CSV_DIR/SynproParcelVolumes.csv > /dev/null 2>&1 &&

echo "Running selected_volumes.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < selected_volumes.sql &&
echo "Running volume_of_overlap.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < volume_of_overlap.sql &&
echo "Running nps.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < nps.sql &&
echo "Running number_of_contacts.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < number_of_contacts.sql &&
echo "Running connection_probability.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < connection_probability.sql &&
echo "Running total_nps.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < total_nps.sql &&
echo "Running total_noc.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < total_noc.sql &&
echo "Running total_cp.sql" &&
mysql -h $ADDR -u $USER -p$PASS $DB < total_cp.sql &&

echo "Exporting tables (can take several minutes)" &&
echo "Tables will be exported to csv files in $EXP_DIR" &&
command="mkdir $EXP_DIR" &&
eval $command
echo "Setting permissions of export directory to everyone. Sudo password may be needed." &&
command="sudo chmod -R 777 $EXP_DIR" &&
eval $command &&
echo "Removing old csv files" &&
command="rm $EXP_DIR/SynproNoPS.csv; rm $EXP_DIR/SynproNOC.csv; \
rm $EXP_DIR/SynproCP.csv; rm $EXP_DIR/SynproNPSTotal.csv; \
rm $EXP_DIR/SynproNOCTotal.csv; rm $EXP_DIR/SynproCPTotal.csv;" &&
eval $command
echo "Setting permissions of export directory to mysql. Sudo password may be needed." &&
command="sudo chown -R mysql:mysql $EXP_DIR" &&
eval $command &&
echo "Exporting SynproNoPS" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproNPS INTO OUTFILE '$EXP_DIR/SynproNoPS.csv';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Exporting SynproNOC" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproNumberOfContacts INTO OUTFILE '$EXP_DIR/SynproNOC.csv';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Exporting SynproCP" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproConnProb INTO OUTFILE '$EXP_DIR/SynproCP.csv';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Exporting SynproNPSTotal" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproTotalNPS INTO OUTFILE '$EXP_DIR/SynproNPSTotal.csv';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Exporting SynproNOCTotal" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproTotalNOC INTO OUTFILE '$EXP_DIR/SynproNOCTotal.csv';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Exporting SynproCPTotal" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproTotalCP INTO OUTFILE '$EXP_DIR/SynproCPTotal.csv';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Setting permissions of export directory to everyone. Sudo password may be needed." &&
command="sudo chmod -R 777 $EXP_DIR" &&
eval $command &&
echo "All operations completed."