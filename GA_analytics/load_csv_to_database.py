"""
#************************************************************************************************************************************************
Created on Nov 21 2023 to read csv files and write to database
#************************************************************************************************************************************************
# File names and headers
#### analytics_data_pages         --  Page,Pageviews,Unique Pageviews,Avg. Time on Page,Entrances,Bounce Rate,% Exit,Page Value
				  --  Day Index,Pageviews
#### analytics_data_content       --  Page path level 1,Pageviews,Unique Pageviews,Avg. Time on Page,Bounce Rate,% Exit
				  --  Day Index,Pageviews
#### analytics_data_exit_pages    --  Page,Exits,Pageviews,% Exit
				  --  Day Index,Exits
#### analytics_data_landing_pages --  Landing Page,Sessions,% New Sessions,New Users,Bounce Rate,Pages / Session,Avg. Session Duration,Goal Conversion Rate,Goal Completions,Goal Value
				  --  Day Index,Sessions
#### analytics_data_events_pages  --  Event name,Event count,Total users,Event count per user,Total revenue
				  --  Day Index,Sessions
#************************************************************************************************************************************************
"""

import csv
import os
import glob
import logging
from datetime import datetime
from pandas import to_datetime
import time
import import_load

from dotenv import load_dotenv
load_dotenv()

dir_name = os.getenv('DIR_NAME')
property = os.getenv('PROPERTY')
dir_path = os.path.dirname(os.path.realpath(__file__));

## Global Variables
###*************************************************************************************************************************************************


datatable_columns = {}
from import_load import get_datatable_columns, get_cnx_cursor
datatable_columns = get_datatable_columns(datatable_columns)

csv_data = { 'analytics_data_exit_pages':'Page',
             'analytics_data_pages':'Page',
             'analytics_data_content':'Page path level 1',
             'analytics_data_landing_pages':'Landing Page', 
	     'analytics_data_events':'Event name'}

######## For the Views

csv_dates_data = { 'analytics_data_exit_pages':'Day Index',
             'analytics_data_pages':'Day Index',
             'analytics_data_content':'Day Index',
             'analytics_data_landing_pages':'Day Index',
             'analytics_data_events':'Day Index'}

## Till Here

def dynamic_select_stmt(table_name, datatable_columns, file_date=None):
	# Construct the INSERT INTO statement
	sql = f"SELECT * FROM {table_name} ORDER BY day_index DESC limit 1"
	if file_date is not None:
		sql = f"SELECT * FROM {table_name} WHERE day_index = '{file_date}'"
	return sql



def if_file_is_loaded_into_db(file_path, file_name):
	##get the file name without extension
	## get the last line of the file and last line of the views file for that file

	with open(os.path.join(file_path, file_name), 'r') as f: 
		##Call function
		file_name, file_date = get_modified_filename(file_name)
		if file_date is None:
			last_line_date = f.readlines()[-2]
			from import_load import file_table_map
			sql = dynamic_select_stmt(file_table_map[file_name][0], datatable_columns)
		else:
			last_line_date = f.readlines()[-1]
			from import_load import file_table_map
			sql = dynamic_select_stmt(file_table_map[file_name][1], datatable_columns, file_date)
	##Make sure last line exists in the db or not
	##get the file or sql from the execute sql and if the date in the database is greater than or equal to the file_date then return true and move the file  
	from import_load import get_cnx_cursor
	cnx, cursor = get_cnx_cursor()
	cursor.execute(sql)
	time.sleep(0.025)
	results = cursor.fetchall()
	inserted_date = None
	for x in results:
		inserted_date = x[1]
	
	cursor.close()
	cnx.close()

	if(inserted_date):
		date_str = last_line_date.split(',')[0]
		datetime_object = datetime.strptime(date_str, '%m/%d/%y').date()

		return(inserted_date >= datetime_object)

def is_date_matching(date_str):
    try:
        return bool(datetime.strptime(date_str, '%Y-%m-%d'))
    except ValueError:
        return False

def dynamic_insert(table_name, datatable_columns, row_data, file_date):
	int_columns = ['page_views', 'unique_page_views', 'entrances', 'views', 'sessions', 'new_users', 'goal_completion', 'exits', 'event_count', 'total_users']

	# Construct column names and placeholders strings
	row_columns = datatable_columns[table_name]
	columns = ",".join(row_columns)
	# Loop through each row
	try:
		for index, row_column in enumerate(row_columns):

			# Loop through each column that needs to be an integer
			if(row_column in int_columns):
				# Convert the column value to an integer
				row_data[index] = row_data[index].replace(',', '')
				row_data[index] = int(row_data[index])
			else:
				if(index == len(row_data)):
					if file_date is not None:
						row_data.append(file_date)
					else:
						modified_s = ','.join(columns.rsplit(',', 1)[:-1])
						columns = modified_s
				elif(index < len(row_data)):
					row_data[index] = row_data[index]

	except Exception as e:
		# Catch all other exceptions
		print(f"An unexpected error occurred: {e} INDEX:{index}")

	placeholders = ', '.join(['%s'] * len(row_data))

	# Construct the INSERT INTO statement
	sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"
	val = tuple(row_data)
	return sql, val


def parse_data_insert(inRecordingMode, csvreader, file_name, starts_with, ends_with, file_date):
	if ends_with is None:
		ends_with = ""
		inRecordingMode = True
		
	for line in csvreader:
		if line == []:
			continue
		else:
			if not inRecordingMode:
				if line[0].startswith(starts_with):
					inRecordingMode = True
				elif line[0].startswith(ends_with):
					inRecordingMode = False
			elif inRecordingMode:
				from import_load import get_cnx_cursor
				cnx, cursor = get_cnx_cursor()
				if line[0] == []:
					continue
				elif len(line[0]) <= 1:
					#inRecordingMode = False
					continue
				elif len(ends_with) > 1 and (line[0].startswith(("/")) or line[0].startswith(("(not set)"))):
					if(ends_with=='EVENTS'):
						line[0] = line[0][1:]
					if line[0].startswith('Day Index'):
						continue
					if(file_date) and not is_date_matching(file_date):
						d = datetime.strptime(file_date, '%Y-%m-%d')
						file_date = d.strftime("%m/%d/%y")

					from import_load import file_table_map 
					sql, val = dynamic_insert(file_table_map[file_name][0], datatable_columns, line, file_date)
					##print(sql)
					##print(val)
					try:
						cursor.execute(sql, val)
						time.sleep(0.025)
						cnx.commit()
						cursor.close()
						cnx.close()
					except Exception as e:
						logging.debug("Error happened")
						logging.debug(e)
						print(e)
						exit();
				elif len(ends_with) > 1 and line[0].startswith(ends_with):
					## When we reach "line before views"
					continue
				else:
					if line[0].startswith('Day Index'):
						continue
					line[0] = datetime.strptime(line[0], "%m/%d/%y")
					from import_load import file_table_map
					sql, val = dynamic_insert(file_table_map[file_name][1], datatable_columns, line, file_date)

					##print(sql)
					##print(val)
					cursor.execute(sql, val)
					time.sleep(0.025)
					cnx.commit()
					cursor.close()
					cnx.close()

def get_modified_filename(file_name, get_file_date=None):
	str_beforecsv  = file_name.split(".")[0] #split and get the string before.csv
	ext = file_name.split(".")[1]
	file_date = None
	if '-' in str_beforecsv:
		[ file_name1, file_date ] = str_beforecsv.split("-", 1)
	else:
		file_name1 = str_beforecsv
        #file_name = ''.join((file_name1,'.',ext))
	if get_file_date is None:
		return file_name1, file_date
	else:
		return file_date

def read_csv_file(dir_name, csv_file):
	with open(os.path.join(dir_path, dir_name, csv_file), 'r') as file: 
		csvreader = csv.reader(file)
		inRecordingMode = False
		## To insert Data
		
		old_path = os.path.join(dir_path, dir_name)
		##Call function
		if(if_file_is_loaded_into_db(old_path, csv_file)):
			return True
		else:
			file_name, file_date = get_modified_filename(csv_file)
			if(file_name == 'analytics_data_events'):
				parse_data_insert(inRecordingMode, csvreader, file_name, csv_data[file_name], 'EVENTS', file_date)
				return True
			else:
				parse_data_insert(inRecordingMode, csvreader, file_name, csv_data[file_name], csv_dates_data[file_name], file_date)
				return True
		return None

############
#Program Starts From here
############


def load_process_files(csv_files = None):
	try:
		if csv_files is None:
			extension = 'csv'
			os.chdir(dir_name)
			csv_files = glob.glob('*.{}'.format(extension))
		##Loop thru the csv files
		for csv_file in csv_files:
			print("Started processing file: "+csv_file+" at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			if(read_csv_file('GA_data', csv_file)):
				print("Completed processing file: "+csv_file+" at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
				## Move Processed File
				file_name, file_date = get_modified_filename(csv_file)
				from import_load import get_new_path
				new_path = get_new_path(file_date)
				from import_load import move_files
				move_files(old_path, new_path, csv_file)
	except Exception as e:
		logging.debug("Error happened")
		logging.debug(e)
def main():
	load_process_files()

if __name__ == '__main__':
	main()
