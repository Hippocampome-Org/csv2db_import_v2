"""
#************************************************************************************************************************************************
Updated on Dec 1 2023 to import data from GA and write to csv files
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


################Insert Statements

## -- data_content -- INSERT INTO hippocampome_v2.ga_analytics_data_content (page_path_level, page_views, unique_page_views, avg_time_on_page, bounce_rate, percentage_exit) VALUES('', 0, 0, 0, '', '');
## -- data_content_views -- INSERT INTO hippocampome_v2.ga_analytics_data_content_views (day_index, views) VALUES('', 0);
## -- exit_pages -- INSERT INTO hippocampome_v2.ga_analytics_exit_pages (page, exits, page_views, percentage_exit) VALUES('', 0, 0, '');
## -- exit_pages_views -- INSERT INTO hippocampome_v2.ga_analytics_exit_pages_views (day_index, views) VALUES('', 0);
## -- landing_pages -- INSERT INTO hippocampome_v2.ga_analytics_landing_pages (landing_page, sessions, percentage_new_sessions, new_users, bounce_rate, pages_sessions, avg_sessions, goal_conversion, goal_completion, goal_value) VALUES('', 0, '', 0, '', 0, 0, '', 0, 0);
## -- landing_pages_views -- INSERT INTO hippocampome_v2.ga_analytics_landing_pages_views (day_index, views) VALUES('', 0);
## --  pages -- INSERT INTO hippocampome_v2.ga_analytics_pages (page, page_views, unique_page_views, avg_time_on_page, entrances, bounce_rate, percentage_exit, page_value) VALUES('', 0, 0, 0, 0, '', '', 0);
## -- pages_views -- INSERT INTO hippocampome_v2.ga_analytics_pages_views (day_index, views) VALUES('', 0);

"""

import re
import errno
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import Dimension, Metric, DateRange, RunReportRequest, OrderBy
import pandas as pd
from datetime import date, timedelta
from datetime import datetime
import shutil
import logging

import glob                             
import mysql.connector          
from pandas import to_datetime 

import logging

from dotenv import load_dotenv
import os, csv

dir_path = os.path.dirname(os.path.realpath(__file__));
load_dotenv(os.path.join(dir_path, 'dotenv.env'))

dir_name = os.getenv('DIR_NAME')
property = os.getenv('PROPERTY')

cnx = mysql.connector.connect(user='root', database='hippocampome_v2', password='DBeaver@123')
cursor = cnx.cursor()

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

db_data_select_viewssql = { 'analytics_data_exit_pages':"SELECT * FROM hippocampome_v2.ga_analytics_exit_pages_views ORDER BY day_index DESC LIMIT 1",
             'analytics_data_pages':"SELECT * FROM hippocampome_v2.ga_analytics_pages_views ORDER BY day_index DESC limit 1",
             'analytics_data_content':"SELECT * FROM hippocampome_v2.ga_analytics_data_content_views ORDER BY day_index DESC LIMIT 1",
             'analytics_data_landing_pages':"SELECT * FROM hippocampome_v2.ga_analytics_landing_pages_views ORDER BY day_index DESC LIMIT 1",
             'analytics_data_events':"SELECT * FROM hippocampome_v2.ga_analytics_data_events_views ORDER BY day_index DESC LIMIT 1"}

db_data_select_viewssql_date = { 'analytics_data_exit_pages':"SELECT * FROM hippocampome_v2.ga_analytics_exit_pages_views WHERE day_idex =",
             'analytics_data_pages':"SELECT * FROM hippocampome_v2.ga_analytics_pages_views WHERE day_index = ",
             'analytics_data_content':"SELECT * FROM hippocampome_v2.ga_analytics_data_content_views WHERE day_index = ",
             'analytics_data_landing_pages':"SELECT * FROM hippocampome_v2.ga_analytics_landing_pages_views WHERE day_index = ",
             'analytics_data_events':"SELECT * FROM hippocampome_v2.ga_analytics_data_events_views WHERE day_index = "}
        
## Till Here


'''
#Check GA_data if any csv files are there 
#Check if they exist in the database
#If they dont exist in the database then process and move them to historical or year
#Loop from July 1 2023 to today and process data

'''

def remov_spaces(str):
	removal_list = [' ', '\t', '\n']
	for s in removal_list:
		str = str.replace(s, '')
	return str

def get_insert_str(str_val):
	#return ', value: "' + str_val +'%'
	return str_val +'%'

def get_percentage_newsessions(sessions, new_users):
	percentage = ( int(new_users) / int(sessions)) * 100
	percentage_new_sessions = get_insert_str(str(round(percentage, 2)))
	return percentage_new_sessions

def insert_after(mydict, search_value, key, value):
	pos = list(mydict.keys()).index(search_value)+1
	items = list(mydict.items())
	items.insert(pos, (key,value))
	mydict = dict(items)
	return mydict

def delete_key(mydict, col_key):
	r = dict(mydict)
	del r[col_key]
	return r

def ga4_response_to_df(response, data_name, header_rows, day_index):
	dim_len = len(response.dimension_headers)
	headers = header_rows.split(',')
	metric_len = len(response.metric_headers)
	all_data = []
	views_data = []
	views = 0
	for row in response.rows:
		row_data = {}
		for i in range(0, dim_len):
			row_data.update({headers[i]: row.dimension_values[i].value})
			#row_data.update({response.dimension_headers[i].name: row.dimension_values[i].value})
		for i in range(0, metric_len):
			row_data.update({response.metric_headers[i].name: row.metric_values[i].value})
		if data_name == "landing_page":
			percentage_newsessions = get_percentage_newsessions(row_data.get("sessions"), row_data.get("newUsers"))
			row_data = insert_after(row_data, "sessions", "% New Sessions", percentage_newsessions)	
			row_data = insert_after(row_data, "bounceRate", "Pages / Session", "0.00")	
			row_data = insert_after(row_data, "averageSessionDuration", "Goal Conversion Rate", "0.00%")
			row_data = insert_after(row_data, "Goal Conversion Rate", "Goal Completions", "0")
			row_data = insert_after(row_data, "Goal Completions", "Goal Value", "$0.00")	
			if row_data["Landing Page"] != "/php/":
				views += int(row_data.get("engagedSessions"))
			row_data = delete_key(row_data, "engagedSessions")
		elif data_name == "pages":
			#to convert 58927 => '16:22:07'
			time_data = int(row_data.get("userEngagementDuration"))
			user_engagement = "{}".format(str(timedelta(seconds=time_data)))
			row_data['userEngagementDuration'] = "{}".format(str(timedelta(seconds=time_data)))
			#row_data = insert_after(row_data, "screenPageViewsPerUser", "Avg. Time on Page", user_engagement)	
			row_data = insert_after(row_data, "bounceRate", "% Exit", "00.00%")	
			row_data = insert_after(row_data, "% Exit", "Page Value", "$0.00")	
			if row_data["Page"] != "/php/":
				views += int(row_data.get("screenPageViews"))
		elif data_name == "events":
			row_data = insert_after(row_data, "eventCountPerUser", "Total revenue", "$0.00")
			###TO have count of page view only as we dont need session_start count or first_visit count or user count
			if row_data["Event name"] == "page_view":
				views = int(row_data.get("sessions"))
			## To add / so that load to database wil handle it
			row_data["Event name"] = ''.join(("/",row_data["Event name"]))

		all_data.append(row_data)
	#datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")
	day_index = datetime.strptime(day_index, "%Y-%m-%d").strftime("X%m/X%d/%y").replace('X0','X').replace('X','')

	if data_name == "pages":
		views_data.append({"Day Index":day_index, "Pageviews": views})
	else:
		views_data.append({"Day Index":day_index, "Sessions": views})

	df_1 = pd.DataFrame(all_data)
	df_2 = pd.DataFrame(views_data)

	lst_dfs = [df_1, df_2]
	return lst_dfs

def get_ga4_report_df(property_id, dimensions_ga4, metrics_ga4, start_date, end_date, data_name, header_rows):
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Applications/XAMPP/hippocampome-1687549016291-058d852a885b-trackinggmail.json'
	client = BetaAnalyticsDataClient()
	request = RunReportRequest(
			property=property_id, 
			dimensions=dimensions_ga4,
			metrics=metrics_ga4,
			date_ranges=[DateRange(start_date=start_date,end_date=end_date)],
		 	)
	response = client.run_report(request)
	return ga4_response_to_df(response, data_name, header_rows, start_date)

def get_new_file_name(file_name, get_file_date=None):
	str_beforecsv  = file_name.split(".")[0] #split and get the string before.csv
	ext = file_name.split(".")[1]
	file_date = None
	if '-' in str_beforecsv:
		[ file_name1, file_date ] = str_beforecsv.split("-", 1)
	else:
		file_name1 = str_beforecsv
	file_name = ''.join((file_name1,'.',ext))
	if get_file_date is None:
		return file_name
	else:
		return file_date	

def write_csv(dir_name, file_name, header_row, df_list, date_input):
	try:
		file = os.path.join(dir_path, dir_name, file_name)
		if file_exists(file):
			print("IN IF FILE EXISTS")
		else:
			print("IN ELSE FILE WRITE")
			f = open(file, 'a')
			for df in df_list:
				df.to_csv(f, index=False, header=True)
			f.close()
		get_csv_files(dir_name, [file_name])
	except Exception as e:
		print("Error is: ",e)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

def create_directory(path):
	try:
		os.makedirs(path)
	except OSError as exception:
		if exception.errno != errno.EEXIST:
			raise
def get_new_path(date_val):
	if date_val is None:
		new_dir_name = dir_name+'/archive_new/historical/'
		new_path = os.path.join(dir_path, new_dir_name)#, '/archive_new/historical/') 
	else:
		date_object = datetime.strptime(date_val, '%Y-%m-%d').date()
		year_val = date_object.year
		month_val = date_object.month
		new_dir_name = dir_name+'/archive_new/'+str(year_val)+'/'+str(month_val)
		new_path = os.path.join(dir_path, new_dir_name)#, '/archive_new/{year_val}/{month_val}')
	return new_path		
	
def process_csv_file(dir_name, csv_file):
	old_path = os.path.join(dir_path, dir_name)
	file_date = None
	file_date = get_new_file_name(csv_file, 'file_date')
	if file_date is None:
		##Move to GA_data/archive_new/historical
		new_path = get_new_path(None)
	else:
		##Move to GA_data/archive_new/year/month	
		new_path = get_new_path(file_date)
		
	##Check last line of file and get the date and test if it exists using load_csv_to_database function
	from load_csv_to_database import if_file_is_loaded_into_db
	if(if_file_is_loaded_into_db(old_path, csv_file)):
		move_files(old_path, new_path, csv_file)
	else:
		if file_exists(os.path.join(new_path, csv_file)):
			print("File "+csv_file+" exists in destination "+new_path+" and its processed")
		else:
			from load_csv_to_database import process_files
			process_files([csv_file])
		move_files(old_path, new_path, csv_file)

def get_csv_files(dir_name, csv_files = None):
	extension = 'csv'
	os.chdir(os.path.join(dir_path, dir_name))
	if csv_files is None:
		csv_files = glob.glob('*.{}'.format(extension))
	##Loop thru the csv files
	for csv_file in csv_files:
		process_csv_file(dir_name, csv_file)

def move_files(source, destination, csv_file):
	create_directory(destination)
	src_path = os.path.join(source, csv_file)
	dst_path = os.path.join(destination, csv_file)
	shutil.move(src_path, dst_path)
	return True

def file_exists(file_path):
	return os.path.isfile(file_path)

def get_cnx_cursor():                   
        cnx = mysql.connector.connect(user='root', database='hippocampome_v2', password='DBeaver@123')
        cursor = cnx.cursor()   
        return cnx, cursor

def get_views_day_count(sql):
	cnx, cursor = get_cnx_cursor()
	cursor.execute(sql)
	results = cursor.fetchall()
	count=results[0][0]
	cursor.close()
	cnx.close()
	return count

def get_date_last_processed():
	start_date = None
	cnx, cursor = get_cnx_cursor()
	table_names = ['ga_analytics_landing_pages_views', 'ga_analytics_landing_pages', 'ga_analytics_data_events', 'ga_analytics_data_events_views', 'ga_analytics_pages', 'ga_analytics_pages_views']
	dates = []
	for table_name in table_names:
		sql = "SELECT day_index from hippocampome_v2."+table_name+" gapv ORDER BY gapv.day_index DESC LIMIT 1"
		cursor.execute(sql)
		results = cursor.fetchall()
		if len(results) > 0:
			dates.append(results[0][0]) 
		else:
			dates.append(None) 
	res = list(filter(lambda item: item is not None, dates))
	start_date = min(res)
	cursor.close()
	cnx.close()
	return start_date

############ 
#Program Starts From here 
############

def main():
	try:
		## if .csv file exists move to arvhice/historical/
		get_csv_files(dir_name)	

		## if date file is there then see if the folder exists if not create it
		### Got to database and get the last date in all tha tables --
		start_date = get_date_last_processed()
		## if date is none ie like in server no data is processed or less than July 1 2023 which will be June 30 2023 then take July 1 2023 
		if(start_date is None or start_date == date(2023, 6, 30)):
			start_date = date(2023, 7, 1) #start from that date
		### Till Here
		end_date = date.today() #'today' # 2023-07-02
		if(start_date >= end_date):
			print("Start Date"+start_date+" is greater than end date:"+end_date+" There is nothing to process")
		else: 
			for single_date in daterange(start_date, end_date):
				date_input = single_date.strftime("%Y-%m-%d")
				new_file_path = get_new_path(date_input)

				##########For landing page Data
				dimensions=[Dimension(name="landingPagePlusQueryString")]
				metrics=[{"name":"sessions"}, {"name":"newUsers"}, {"name":"bounceRate"}, {"name":"averageSessionDuration"}, {"name":"engagedSessions"}]
				header_rows='Landing Page,Sessions,% New Sessions,New Users,Bounce Rate,Pages / Session,Avg. Session Duration,Goal Conversion Rate,Goal Completions,Goal Value,Views'
				# To add date to filename
				file_name = 'analytics_data_landing_pages'+'-'+date_input+'.csv'
				sql = "select count(*) from hippocampome_v2.ga_analytics_landing_pages_views gapv WHERE gapv.day_index='"+date_input+"'"
				count = get_views_day_count(sql)

				file_exists = os.path.isfile(os.path.join(new_file_path, file_name))
				print("If file :"+file_name+" in path: "+new_file_path+" exists? "+file_exists)
				if count < 1 and not file_exists:
					df = get_ga4_report_df(property, dimensions, metrics, date_input, date_input, "landing_page", header_rows)
					write_csv(dir_name, file_name, header_rows, df, date_input)
				else:
					print(os.path.join(new_file_path, file_name))
					print(" exists and processed to database")

				##########For date pages Data
				#Page,Pageviews,Unique Pageviews,Avg. Time on Page,Entrances,Bounce Rate,% Exit,Page Value
				dimensions=[Dimension(name="landingPagePlusQueryString")]
				metrics=[{"name":"screenPageViews"}, {"name":"screenPageViewsPerUser"}, {"name":"userEngagementDuration"}, {"name":"sessions"}, {"name":"bounceRate"}]
				header_rows='Page,Pageviews,Unique Pageviews, Avg. Time on Page, Entrances, Bounce Rate, % Exit, Page Value'
				# To add date to filename
				file_name = 'analytics_data_pages'+'-'+date_input+'.csv'
				sql = "select count(*) from hippocampome_v2.ga_analytics_pages_views gapv WHERE gapv.day_index='"+date_input+"'"
				count = get_views_day_count(sql)
				file_exists = os.path.isfile(os.path.join(new_file_path, file_name))
				if count < 1 and not file_exists:
					df = get_ga4_report_df(property, dimensions, metrics, date_input, date_input, "pages", header_rows)
					write_csv(dir_name, file_name, header_rows, df, date_input)
				else:
					print(os.path.join(new_file_path, file_name))
					print(" exists and processed to database")

				##########For date Events Data
				#Event name,Event count,Total users,Event count per user,Total revenue
				dimensions=[Dimension(name="eventName")]
				metrics=[{"name":"eventCount"}, {"name":"sessions"}, {"name":"eventCountPerUser"}]
				header_rows='Event name, Event Count, Total users, Event count per user' #, Total revenue'
				# To add date to filename
				file_name = 'analytics_data_events'+'-'+date_input+'.csv'
				sql = "select count(*) from hippocampome_v2.ga_analytics_data_events_views gapv WHERE gapv.day_index='"+date_input+"'"
				count = get_views_day_count(sql)
				file_exists = os.path.isfile(os.path.join(new_file_path, file_name))
				if count < 1 and not file_exists:
					df = get_ga4_report_df(property, dimensions, metrics, date_input, date_input, "events", header_rows)
					write_csv(dir_name, file_name, header_rows, df, date_input)
				else:
					print(os.path.join(new_file_path, file_name))
					print(" exists and processed to database")
	except Exception as e:
              logging.debug("Error happened")
              logging.debug(e)

if __name__ == '__main__':
	main()
