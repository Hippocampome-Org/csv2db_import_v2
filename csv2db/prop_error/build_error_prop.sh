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
CSV_DIR=csv # csv files location

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
mysql -h $ADDR -u $USER -p$PASS $DB < total_cp.sql
