table=$1;
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

command="rm /var/tmp/SynproExports/$table.csv";
eval $command;

echo "SET STATEMENT max_statement_time=0 FOR SELECT * FROM \
$DB.$table INTO OUTFILE '$EXP_DIR/$table.csv' FIELDS TERMINATED BY ',' \
OPTIONALLY ENCLOSED BY '' LINES TERMINATED BY '\n';" > export_table.sql &&
mysql -h $ADDR -u $USER -p$PASS $DB < export_table.sql

sudo chmod -R 777 /var/tmp/SynproExports/*