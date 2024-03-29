#!/bin/bash

###############################
#
# Build propagate errors values
#
###############################

command="sed -n 6p ../../database_save.sh" # username
command2=$(eval $command)
command3="echo $command2 | cut -c12-10000"
USER=$(eval $command3)
command="sed -n 7p ../../database_save.sh" # password
command2=$(eval $command)
command3="echo $command2 | cut -c16-10000"
PASS=$(eval $command3)
command="sed -n 8p ../../database_save.sh" # database
command2=$(eval $command)
command3="echo $command2 | cut -c15-10000"
DB=$(eval $command3)
ADDR=localhost # db address
CSV_DIR=csv # import csv files location
EXP_DIR="/var/tmp/SynproExports/" # export csv files directory
DOT_CSV=".csv";
REFORMAT="_reformat";
NOC_CSV="$EXP_DIR/number_of_contacts" # exported number_of_contacts table
NOCR_CSV="$NOC_CSV$REFORMAT" # reformatted number_of_contacts table
NOCR_CSV="$NOCR_CSV$DOT_CSV"
NOC_CSV="$NOC_CSV$DOT_CSV"

echo "Dropping old views" &&
mysql -h $ADDR -u $USER -p$PASS $DB < drop_views.sql
echo "Creating SynproLengthsHullVols view" &&
mysql -h $ADDR -u $USER -p$PASS $DB < lengths_hull_vols.sql &&

# reformat number_of_contacts data
echo "Creating number_of_contacts csv file" &&
command="rm $EXP_DIR/number_of_contacts.csv" &&
eval $command
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
command="rm $EXP_DIR/SynproPairsOrder.csv; \
rm $EXP_DIR/SynproNoPS.csv; rm $EXP_DIR/SynproNOC.csv; \
rm $EXP_DIR/SynproCP.csv; rm $EXP_DIR/SynproNPSTotal.csv; \
rm $EXP_DIR/SynproNOCTotal.csv; rm $EXP_DIR/SynproCPTotal.csv;" &&
eval $command
echo "Setting permissions of export directory to mysql. Sudo password may be needed." &&
command="sudo chown -R mysql:mysql $EXP_DIR" &&
eval $command &&

##### SynproPairsOrder #####
echo "Exporting SynproPairsOrder" &&
# export view data into csv
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproPairsOrder INTO OUTFILE '$EXP_DIR/SynproPairsOrder.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,subregion,parcel\n/' $EXP_DIR/SynproPairsOrder.csv && # add column names
cp $EXP_DIR/SynproPairsOrder.csv ../../iconv/latin1/ &&
echo "Importing SynproPairsOrder" &&
# import csv into permanent table
echo "DROP VIEW IF EXISTS SynproPairsOrder;" > import_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < import_table.sql &&
echo "CREATE TABLE \`SynproPairsOrder\` (\`id\` int(11) NOT NULL AUTO_INCREMENT, \
  \`source_id\` bigint(20) DEFAULT NULL, \`target_id\` bigint(20) DEFAULT NULL, \
  \`subregion\` longtext DEFAULT NULL, \`parcel\` longtext DEFAULT NULL, PRIMARY KEY (\`id\`) \
) ENGINE=InnoDB AUTO_INCREMENT=4945 DEFAULT CHARSET=utf8;" > import_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < import_table.sql &&
sed -i 's/^/,/' $EXP_DIR/SynproPairsOrder.csv && # add comma for id column
sed -i '1d' $EXP_DIR/SynproPairsOrder.csv && # remove row with column names for import
echo "LOAD DATA LOCAL INFILE '$EXP_DIR/SynproPairsOrder.csv' INTO TABLE SynproPairsOrder \
 COLUMNS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '' \
 LINES TERMINATED BY '\n';" > import_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < import_table.sql &&
############################

##### Export Other Tables #####
echo "Exporting SynproNoPS" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproNPS INTO OUTFILE '$EXP_DIR/SynproNoPS.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,subregion,parcel,NPS_mean,NPS_std\n/' $EXP_DIR/SynproNoPS.csv && # add column names
sed -i 's/\\//g' $EXP_DIR/SynproNoPS.csv && # fix issue with backslash appearing in some entries
echo "Exporting SynproNOC" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproNumberOfContacts INTO OUTFILE '$EXP_DIR/SynproNOC.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,subregion,parcel,NC_mean,NC_std\n/' $EXP_DIR/SynproNOC.csv && # add column names
echo "Exporting SynproCP" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproConnProb INTO OUTFILE '$EXP_DIR/SynproCP.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,subregion,parcel,CP_mean,CP_std\n/' $EXP_DIR/SynproCP.csv && # add column names
echo "Exporting SynproNPSTotal" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproTotalNPS INTO OUTFILE '$EXP_DIR/SynproNPSTotal.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,NPS_mean_total,NPS_stdev_total,parcel_count\n/' $EXP_DIR/SynproNPSTotal.csv && # add column names
echo "Exporting SynproNOCTotal" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproTotalNOC INTO OUTFILE '$EXP_DIR/SynproNOCTotal.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,NC_mean_total,NC_stdev_total,parcel_count\n/' $EXP_DIR/SynproNOCTotal.csv && # add column names
echo "Exporting SynproCPTotal" &&
echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.SynproTotalCP INTO OUTFILE '$EXP_DIR/SynproCPTotal.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql &&
sed -i '1s/^/source_id,target_id,CP_mean_total,CP_stdev_total,parcel_count\n/' $EXP_DIR/SynproCPTotal.csv && # add column names
echo "Setting permissions of export directory to everyone. Sudo password may be needed." &&
command="sudo chmod -R 777 $EXP_DIR" &&
eval $command &&
echo "Copying csv result files to /iconv/latin1 directory. The user should copy all updated files in /iconv/latin1 to source control (Github) for backing them up." 
cp $EXP_DIR/SynproNoPS.csv ../../iconv/latin1/ &&
cp $EXP_DIR/SynproNOC.csv ../../iconv/latin1/ &&
cp $EXP_DIR/SynproCP.csv ../../iconv/latin1/ &&
cp $EXP_DIR/SynproNPSTotal.csv ../../iconv/latin1/ &&
cp $EXP_DIR/SynproNOCTotal.csv ../../iconv/latin1/ &&
cp $EXP_DIR/SynproCPTotal.csv ../../iconv/latin1/ &&
echo "All operations completed."