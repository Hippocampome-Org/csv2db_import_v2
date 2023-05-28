#!/bin/bash

###############################
#
# Build propagate errors values
#
###############################

command="sed -n 6p ../../database_save.sh" # username
command2=$(eval $command)
command3="echo $command2 | cut -c19-10000"
USER=$(eval $command3)
command="sed -n 7p ../../database_save.sh" # password
command2=$(eval $command)
command3="echo $command2 | cut -c23-10000"
PASS=$(eval $command3)
command="sed -n 8p ../../database_save.sh" # database
command2=$(eval $command)
command3="echo $command2 | cut -c22-10000"
DB=$(eval $command3)
ADDR=localhost # db address
CSV_DIR=csv # import csv files location
EXP_DIR="/var/tmp/SynproExports/" # export csv files directory
NOC_CSV="$EXP_DIR/number_of_contacts.csv" # exported number_of_contacts table
NOCR_CSV="$EXP_DIR/number_of_contacts_reformat.csv" # reformatted number_of_contacts table

echo "Dropping old views" &&
mysql -h $ADDR -u $USER -p$PASS $DB < drop_views.sql
echo "Creating SynproErrPropConstants view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < constants.sql &&
echo "Creating SynproLengthsHullVols view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < lengths_hull_vols.sql &&

# reformat number_of_contacts data
echo "Creating number_of_contacts csv file" &&
command="rm $EXP_DIR/number_of_contacts.csv" &&
eval $command &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.number_of_contacts INTO OUTFILE '$EXP_DIR/number_of_contacts.csv' \
FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '' \
LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
echo "Setting permissions of export directory to everyone. Sudo password may be needed." &&
command="sudo chmod -R 777 $EXP_DIR" &&
eval $command &&
echo "Reformatting number_of_contacts csv file" &&
./split_layers/split_layers $NOC_CSV $NOCR_CSV &&
echo "Creating NOC reformatted data table" &&
mysql -h $ADDR -u $USER -p$PASS $DB < create_NOCR.sql &&
echo "Importing reformatted NOC data" &&
echo "LOAD DATA LOCAL INFILE '$NOCR_CSV' INTO TABLE SynproNOCR \
 COLUMNS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '' \
 LINES TERMINATED BY '\n';" > import_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < import_table.sql &&

echo "Creating SynproPairsOrder view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < order_of_pairs.sql &&
echo "Creating SynproPairsLHV view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < pairs_lengths_hull_vols.sql &&
echo "Creating SynproNumberOfParcels view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < number_of_parcels.sql &&
echo "Creating SynproParcelVolumes table" &&
mysql -h $ADDR -u $USER -p$PASS $DB < create_synpro_parcel_volumes.sql &&
echo "Adding data to parcel volumes table" &&
mysqlimport --ignore-lines=1 --fields-terminated-by=, --verbose --local -u $USER -p$PASS $DB $CSV_DIR/SynproParcelVolumes.csv > /dev/null 2>&1 &&
echo "Creating SynproVolumeOfOverlap view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < volume_of_overlap.sql &&
echo "Creating SynproNPS view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < nps.sql &&
echo "Creating SynproNumberOfContacts view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < number_of_contacts.sql &&
echo "Creating SynproConnProb view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < connection_probability.sql &&
echo "Creating SynproTotalNPS view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < total_nps.sql &&
echo "Creating SynproTotalNOC view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < total_noc.sql &&
echo "Creating SynproTotalCP view" &&
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