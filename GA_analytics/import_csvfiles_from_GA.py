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
import os, csv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import Dimension, Metric, DateRange, RunReportRequest, OrderBy
import pandas as pd
from datetime import date, timedelta
from datetime import datetime
import shutil


dir_name = "./GA_data";
dir_path = os.path.dirname(os.path.realpath(__file__));
print("Directory path: "+dir_path);

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
			views += int(row_data.get("sessions"))
		elif data_name == "events":
			row_data = insert_after(row_data, "eventCountPerUser", "Total revenue", "$0.00")
			views += int(row_data.get("sessions"))

		all_data.append(row_data)
	#datetime.datetime.strptime("21/12/2008", "%d/%m/%Y").strftime("%Y-%m-%d")
	day_index = datetime.strptime(day_index, "%Y-%m-%d").strftime("%d/%m/%y")
	views_data.append({"Day Index":day_index, "Pageviews": views})

	df_1 = pd.DataFrame(all_data)
	df_2 = pd.DataFrame(views_data)

	lst_dfs = [df_1, df_2]
	return lst_dfs

def get_ga4_report_df(property_id, dimensions_ga4, metrics_ga4, start_date, end_date, data_name, header_rows):
	os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Applications/XAMPP/hippocampome-1687549016291-058d852a885b-trackinggmail.json'
	client = BetaAnalyticsDataClient()
	request = RunReportRequest(
			property = "properties/367925539",
			dimensions=dimensions_ga4,
			metrics=metrics_ga4,
			date_ranges=[DateRange(start_date=start_date,end_date=end_date)],
		 	)
	response = client.run_report(request)
	return ga4_response_to_df(response, data_name, header_rows, start_date)

def write_csv(dir_name, file_name, header_row, df_list):
	try:
		file = os.path.join(dir_path, dir_name, file_name)
		check_file = os.path.isfile(file)
		print("file exists:"+file+"--")
		print(check_file)
		destination = 'archived_data_new'
		destinationPath = os.path.join(dir_path,dir_name,destination)

		if os.path.isfile(file):
			if not os.path.exists(destinationPath):
				os.mkdir(destinationPath)
				print("directory created"+destinationPath)
		
			dest_file = os.path.join(destinationPath, file_name)

			if os.path.isfile(dest_file):
				file_write_dest = open(dest_file, "a")
				file_write_dest.write("\n")

				with open(file_name, "r") as scan:
					file_write_dest.write(scan.read())

				#file_write_dest.write(file.read()) #append content from source to destination
				os.unlink(file) ##remove the source file after appending its content
			else:
				shutil.copy(file, destinationPath)
				os.unlink(file) ##remove the source file after appending its content

		f = open(file, 'a')
		for df in df_list:
			df.to_csv(f, index=False, header=True)
			f.write("\n")
		f.close()
	except Exception as e:
		print("Error is: ",e)

def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days)):
        yield start_date + timedelta(n)

property = "properties/367925539"

start_date = date(2023, 7, 1)
end_date = date.today() #'today' # 2023-07-02

for single_date in daterange(start_date, end_date):
	date_input = single_date.strftime("%Y-%m-%d")

	##########For landing page Data
	dimensions=[Dimension(name="landingPagePlusQueryString")]
	metrics=[{"name":"sessions"}, {"name":"newUsers"}, {"name":"bounceRate"}, {"name":"averageSessionDuration"}, {"name":"engagedSessions"}]
	header_rows='Landing Page,Sessions,% New Sessions,New Users,Bounce Rate,Pages / Session,Avg. Session Duration,Goal Conversion Rate,Goal Completions,Goal Value,Views'
	#df = get_ga4_report_df(property, dimensions, metrics, start_date, end_date, "landing_page", header_rows)
	df = get_ga4_report_df(property, dimensions, metrics, date_input, date_input, "landing_page", header_rows)

	# To add date to filename
	file_name = 'analytics_data_landing_pages'+'-'+date_input+'.csv'
	write_csv(dir_name, file_name, header_rows, df)
	#write_csv(dir_name, 'analytics_data_landing_pages.csv', header_rows, df)
	
	
	##########For date pages Data
	#Page,Pageviews,Unique Pageviews,Avg. Time on Page,Entrances,Bounce Rate,% Exit,Page Value
	
	dimensions=[Dimension(name="landingPagePlusQueryString")]
	metrics=[{"name":"screenPageViews"}, {"name":"screenPageViewsPerUser"}, {"name":"userEngagementDuration"}, {"name":"sessions"}, {"name":"bounceRate"}]
	header_rows='Page,Pageviews,Unique Pageviews, Avg. Time on Page, Entrances, Bounce Rate, % Exit, Page Value'
	#df = get_ga4_report_df(property, dimensions, metrics, start_date, end_date, "pages", header_rows)
	df = get_ga4_report_df(property, dimensions, metrics, date_input, date_input, "pages", header_rows)
	#write_csv(dir_name, 'analytics_data_pages.csv', header_rows, df)
	# To add date to filename
	file_name = 'analytics_data_pages'+'-'+date_input+'.csv'
	write_csv(dir_name, file_name, header_rows, df)

	##########For date Events Data
	#Event name,Event count,Total users,Event count per user,Total revenue
        
	dimensions=[Dimension(name="eventName")]
	metrics=[{"name":"eventCount"}, {"name":"sessions"}, {"name":"eventCountPerUser"}]
	header_rows='Event name, Event Count, Total users, Event count per user' #, Total revenue'
	df = get_ga4_report_df(property, dimensions, metrics, date_input, date_input, "events", header_rows)
	#write_csv(dir_name, 'analytics_data_events.csv', header_rows, df)
	# To add date to filename
	file_name = 'analytics_data_events'+'-'+date_input+'.csv'
	write_csv(dir_name, file_name, header_rows, df)
	exit()

