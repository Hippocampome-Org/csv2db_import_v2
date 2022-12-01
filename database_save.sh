#!/bin/zsh

today=`date '+%Y%m%d%H%M%S'`;
mkdir mysqldump

mysql_user='root' # add your username
mysql_password='newpassword' # add your password
mysql_db_name='HC' # add the local database name

mysql -u $mysql_user -p$mysql_password $mysql_db_name < insert_hit_counter_ids.sql
mysqldump -u $mysql_user -p$mysql_password $mysql_db_name > ./mysqldump/HC_$today.sql
mysqldump -u $mysql_user -p$mysql_password $mysql_db_name > ./mysqldump/hippodevur2_$today.sql
mysqldump -u $mysql_user -p$mysql_password $mysql_db_name > ./mysqldump/hippocampome_v2_$today.sql
mysqldump -u $mysql_user -p$mysql_password $mysql_db_name > ./mysqldump/hipporevome_$today.sql
mysql -u $mysql_user -p$mysql_password $mysql_db_name < user_permissions_update_hippocampome.sql
mysqldump -u $mysql_user -p$mysql_password $mysql_db_name > ./mysqldump/hippocampome_$today.sql
mysql -u $mysql_user -p$mysql_password $mysql_db_name < user_permissions_update_hippodevome.sql
mysqldump -u $mysql_user -p$mysql_password $mysql_db_name > ./mysqldump/hippodevome_$today.sql
mysql -u $mysql_user -p$mysql_password $mysql_db_name < user_permissions_update_HC.sql