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

################Insert Statements

## -- data_content -- INSERT INTO hippocampome_v2.ga_analytics_data_content (page_path_level, page_views, unique_page_views, avg_time_on_page, bounce_rate, percentage_exit) VALUES('', 0, 0, 0, '', '');
## -- data_content_views -- INSERT INTO hippocampome_v2.ga_analytics_data_content_views (day_index, views) VALUES('', 0);
## -- exit_pages -- INSERT INTO hippocampome_v2.ga_analytics_exit_pages (page, exits, page_views, percentage_exit) VALUES('', 0, 0, '');
## -- exit_pages_views -- INSERT INTO hippocampome_v2.ga_analytics_exit_pages_views (day_index, views) VALUES('', 0);
## -- landing_pages -- INSERT INTO hippocampome_v2.ga_analytics_landing_pages (landing_page, sessions, percentage_new_sessions, new_users, bounce_rate, pages_sessions, avg_sessions, goal_conversion, goal_completion, goal_value) VALUES('', 0, '', 0, '', 0, 0, '', 0, 0);
## -- landing_pages_views -- INSERT INTO hippocampome_v2.ga_analytics_landing_pages_views (day_index, views) VALUES('', 0);
## --  pages -- INSERT INTO hippocampome_v2.ga_analytics_pages (page, page_views, unique_page_views, avg_time_on_page, entrances, bounce_rate, percentage_exit, page_value) VALUES('', 0, 0, 0, 0, '', '', 0);
## -- pages_views -- INSERT INTO hippocampome_v2.ga_analytics_pages_views (day_index, views) VALUES('', 0);


#************************************************************************************************************************************************
"""

import csv
import os
import glob
import mysql.connector
import logging
from datetime import datetime
from pandas import to_datetime


dir_name = "./GA_data";
dir_path = os.path.dirname(os.path.realpath(__file__));
print(dir_path)
logging.debug("Directory path: "+dir_path);

cnx = mysql.connector.connect(user='root', database='hippocampome_v2', password='DBeaver@123')
cursor = cnx.cursor()

## Global Variables
###*************************************************************************************************************************************************
"""
csv_data = { 'analytics_data_exit_pages.csv':'Page',
             'analytics_data_pages.csv':'Page', 
             'analytics_data_content.csv':'Page path level 1',
             'analytics_data_landing_pages.csv':'Landing Page'}

db_data_insert_sql = { 'analytics_data_exit_pages.csv':"INSERT INTO hippocampome_v2.ga_analytics_exit_pages (page, exits, page_views, percentage_exit, day_index) VALUES (%s, %s, %s, %s, %s)",
             'analytics_data_pages.csv':"INSERT INTO hippocampome_v2.ga_analytics_pages (page, page_views, unique_page_views, avg_time_on_page, entrances, bounce_rate, percentage_exit, page_value, day_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ",
             'analytics_data_content.csv':"INSERT INTO hippocampome_v2.ga_analytics_data_content (page_path_level, page_views, unique_page_views, avg_time_on_page, bounce_rate, percentage_exit, day_index) VALUES (%s, %s, %s, %s, %s, %s, %s) ",
             'analytics_data_landing_pages.csv':"INSERT INTO hippocampome_v2.ga_analytics_landing_pages (landing_page, sessions, percentage_new_sessions, new_users, bounce_rate, pages_sessions, avg_sessions, goal_conversion, goal_completion, goal_value, day_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) "}

db_data_insert_sql_cols = {'analytics_data_exit_pages.csv':['page', 'exits', 'page_views', 'percentage_exit'],
             'analytics_data_pages.csv':['page', 'page_views', 'unique_page_views', 'avg_time_on_page', 'entrances', 'bounce_rate', 'percentage_exit', 'page_value'],
             'analytics_data_content.csv':['page_path_level', 'page_views', 'unique_page_views', 'avg_time_on_page', 'bounce_rate', 'percentage_exit'],
             'analytics_data_landing_pages.csv':['landing_page', 'sessions', 'percentage_new_sessions', 'new_users', 'bounce_rate', 'pages_sessions', 'avg_sessions', 'goal_conversion', 'goal_completion', 'goal_value']}

######## For the Views

csv_dates_data = { 'analytics_data_exit_pages.csv':'Day Index',
             'analytics_data_pages.csv':'Day Index',
             'analytics_data_content.csv':'Day Index',
             'analytics_data_landing_pages.csv':'Day Index'}

db_data_insert_viewssql = { 'analytics_data_exit_pages.csv':"INSERT INTO hippocampome_v2.ga_analytics_exit_pages_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_pages.csv':"INSERT INTO hippocampome_v2.ga_analytics_pages_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_content.csv':"INSERT INTO hippocampome_v2.ga_analytics_data_content_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_landing_pages.csv':"INSERT INTO hippocampome_v2.ga_analytics_landing_pages_views (day_index, views) VALUES (%s, %s)"}

db_data_insert_viewssql_cols = { 'analytics_data_exit_pages.csv':['day_index', 'views'],
             'analytics_data_pages.csv':['day_index', 'views'],
             'analytics_data_content.csv':['day_index', 'views'],
             'analytics_data_landing_pages.csv':['day_index', 'views']}

"""

csv_data = { 'analytics_data_exit_pages':'Page',
             'analytics_data_pages':'Page',
             'analytics_data_content':'Page path level 1',
             'analytics_data_landing_pages':'Landing Page', 
	     'analytics_data_events':'Event name'}

db_data_insert_sql = { 'analytics_data_exit_pages':"INSERT INTO hippocampome_v2.ga_analytics_exit_pages (page, exits, page_views, percentage_exit, day_index) VALUES (%s, %s, %s, %s, %s)",
             'analytics_data_pages':"INSERT INTO hippocampome_v2.ga_analytics_pages (page, page_views, unique_page_views, avg_time_on_page, entrances, bounce_rate, percentage_exit, page_value, day_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s) ",
             'analytics_data_content':"INSERT INTO hippocampome_v2.ga_analytics_data_content (page_path_level, page_views, unique_page_views, avg_time_on_page, bounce_rate, percentage_exit, day_index) VALUES (%s, %s, %s, %s, %s, %s, %s) ",
             'analytics_data_landing_pages':"INSERT INTO hippocampome_v2.ga_analytics_landing_pages (landing_page, sessions, percentage_new_sessions, new_users, bounce_rate, pages_sessions, avg_sessions, goal_conversion, goal_completion, goal_value, day_index) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) ",
             'analytics_data_events':"INSERT INTO hippocampome_v2.ga_analytics_data_events (event_name, event_count, total_users, event_count_per_user, total_revenue, day_index) VALUES (%s, %s, %s, %s, %s, %s) "}

db_data_insert_sql_cols = {'analytics_data_exit_pages':['page', 'exits', 'page_views', 'percentage_exit'],
             'analytics_data_pages':['page', 'page_views', 'unique_page_views', 'avg_time_on_page', 'entrances', 'bounce_rate', 'percentage_exit', 'page_value'],
             'analytics_data_content':['page_path_level', 'page_views', 'unique_page_views', 'avg_time_on_page', 'bounce_rate', 'percentage_exit'],
             'analytics_data_landing_pages':['landing_page', 'sessions', 'percentage_new_sessions', 'new_users', 'bounce_rate', 'pages_sessions', 'avg_sessions', 'goal_conversion', 'goal_completion', 'goal_value'],
             'analytics_data_events':['event_name', 'event_count', 'total_users', 'event_count_per_user', 'total_revenue', 'day_index']}

######## For the Views

csv_dates_data = { 'analytics_data_exit_pages':'Day Index',
             'analytics_data_pages':'Day Index',
             'analytics_data_content':'Day Index',
             'analytics_data_landing_pages':'Day Index',
             'analytics_data_events':'Day Index'}

db_data_insert_viewssql_cols = { 'analytics_data_exit_pages':['day_index', 'views'],
             'analytics_data_pages':['day_index', 'views'],
             'analytics_data_content':['day_index', 'views'],
             'analytics_data_landing_pages':['day_index', 'views'],
             'analytics_data_events':['day_index', 'views']}

db_data_insert_viewssql = { 'analytics_data_exit_pages':"INSERT INTO hippocampome_v2.ga_analytics_exit_pages_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_pages':"INSERT INTO hippocampome_v2.ga_analytics_pages_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_content':"INSERT INTO hippocampome_v2.ga_analytics_data_content_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_landing_pages':"INSERT INTO hippocampome_v2.ga_analytics_landing_pages_views (day_index, views) VALUES (%s, %s)",
             'analytics_data_events':"INSERT INTO hippocampome_v2.ga_analytics_data_events_views (day_index, views) VALUES (%s, %s)"}

db_data_select_viewssql = { 'analytics_data_exit_pages':"SELECT * FROM hippocampome_v2.ga_analytics_exit_pages_views ORDER BY ID DESC LIMIT 1",
             'analytics_data_pages':"SELECT * FROM hippocampome_v2.ga_analytics_pages_views ORDER BY ID DESC",
             'analytics_data_content':"SELECT * FROM hippocampome_v2.ga_analytics_data_content_views ORDER BY ID DESC LIMIT 1",
             'analytics_data_landing_pages':"SELECT * FROM hippocampome_v2.ga_analytics_landing_pages_views ORDER BY ID DESC LIMIT 1",
             'analytics_data_events':"SELECT * FROM hippocampome_v2.ga_analytics_data_events_views ORDER BY ID DESC LIMIT 1"}


## Till Here

def get_cnx_cursor():
	cnx = mysql.connector.connect(user='root', database='hippocampome_v2', password='DBeaver@123')
	cursor = cnx.cursor()
	return cnx, cursor
	
def if_file_is_loaded_into_db(file_path, file_name):
	##get the file name without extension
	## get the last line of the file and last line of the views file for that file

	with open(os.path.join(file_path, file_name), 'r') as f: 
		##Call function
		file_name, file_date = get_new_file_name(file_name)
		if file_date is None:
			last_line_date = f.readlines()[-2]
		else:
			last_line_date = f.readlines()[-1]
	print(last_line_date)
	##Make sure last line exists in the db or not
	##get the file or sql from the execute sql and if the date in the database is greater than or equal to the file_date then return true and move the file  
	cnx, cursor = get_cnx_cursor()
	sql = db_data_select_viewssql[file_name]
	cursor.execute(sql)
	results = cursor.fetchall()
	inserted_date = None
	for x in results:
		inserted_date = x[1]
	
	cursor.close()
	cnx.close()

	#print(type(inserted_date))
	##print(inserted_date)
	#print(type(last_line_date))
	##print(last_line_date)
	##print(last_line_date.split(',')[0])
	
	if(inserted_date):
		print("Inside is inserted_date")
		date_str = last_line_date.split(',')[0]
		print(date_str)
		datetime_object = datetime.strptime(date_str, '%m/%d/%y').date()

		print(type(datetime_object))
		print(type(inserted_date))
		#print(datetime_object)
		print((inserted_date >= datetime_object))
		return(inserted_date >= datetime_object)
		if(inserted_date >= datetime_object):
			return true
		else:
			return false
	
def nonblank_lines(f):
    for l in f:
        line = l.rstrip()
        if line:
            yield line

def is_date_matching(date_str):
    try:
        return bool(datetime.strptime(date_str, '%Y-%m-%d'))
    except ValueError:
        return False

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
				cnx = mysql.connector.connect(user='root', database='hippocampome_v2', password='DBeaver@123')
				cursor = cnx.cursor()
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
					sql = db_data_insert_sql[file_name]
					if(file_date) and not is_date_matching(file_date):
						d = datetime.strptime(file_date, '%Y-%m-%d')
						file_date = d.strftime("%m/%d/%y")

					#print(tuple(line))print(file_date)print(tuple(file_date,))	
					val = tuple(line) + (file_date, ) #to add date too
					#print(sql)
					#print(val)
					cursor.execute(sql, val)
					cnx.commit()
					cursor.close()
					cnx.close()
				elif len(ends_with) > 1 and line[0].startswith(ends_with):
					## When we reach "line before views"
					continue
				else:
					##print("IN FINAL ELSE")
					##print(line[0])
					if line[0].startswith('Day Index'):
						continue
					sql = db_data_insert_viewssql[file_name]
					line[0] = datetime.strptime(line[0], "%m/%d/%y")
					val = tuple(line)
					#print(sql)
					#print(val)
					cursor.execute(sql, val)
					cnx.commit()
					cursor.close()
					cnx.close()

def get_new_file_name(file_name, get_file_date=None):
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

def read_csv_file(dir_name, file_name):
	print("in read_csv_file")
	with open(os.path.join(dir_path, dir_name, file_name), 'r') as file: 
		csvreader = csv.reader(file)
		inRecordingMode = False
		## To insert Data
		
		file_date = None # Default None for the downloaded files

		##Call function
		file_name, file_date = get_new_file_name(file_name)
		if(file_name == 'analytics_data_events'):
			parse_data_insert(inRecordingMode, csvreader, file_name, csv_data[file_name], 'EVENTS', file_date)
		else:
			parse_data_insert(inRecordingMode, csvreader, file_name, csv_data[file_name], csv_dates_data[file_name], file_date)
	print("After read_csv_file")

############
#Program Starts From here
############


def process_files(csv_files = None):
	try:
		if csv_files is None:
			extension = 'csv'
			os.chdir(dir_name)
			csv_files = glob.glob('*.{}'.format(extension))
		##Loop thru the csv files
		for csv_file in csv_files:
			print("Started processing file: "+csv_file+" at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			#logging.debug("Started processing file: "+csv_file+" at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			read_csv_file('GA_data', csv_file)
			#logging.debug("Completed processing file: "+csv_file+" at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
			print("Completed processing file: "+csv_file+" at: "+datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
	except Exception as e:
		logging.debug("Error happened")
		logging.debug(e)
def main():
	process_files()

if __name__ == '__main__':
	main()
