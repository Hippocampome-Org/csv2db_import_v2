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
#import datetime
from datetime import timedelta

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

def ga4_response_to_df(response, data_name, header_rows):
	dim_len = len(response.dimension_headers)
	headers = header_rows.split(',')
	metric_len = len(response.metric_headers)
	all_data = []
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
		elif data_name == "pages":
			#to convert 58927 => '16:22:07'
			time_data = int(row_data.get("userEngagementDuration"))
			user_engagement = "{}".format(str(timedelta(seconds=time_data)))
			row_data['userEngagementDuration'] = "{}".format(str(timedelta(seconds=time_data)))
			#row_data = insert_after(row_data, "screenPageViewsPerUser", "Avg. Time on Page", user_engagement)	
			row_data = insert_after(row_data, "bounceRate", "% Exit", "00.00%")	
			row_data = insert_after(row_data, "% Exit", "Page Value", "$0.00")	
		all_data.append(row_data)
	df = pd.DataFrame(all_data)
	return df

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
	return ga4_response_to_df(response, data_name, header_rows)

def write_csv(file_name, header_row, df):
	try:
		df.to_csv(file_name, index=False, header=True)
	except Exception as e:
		print("Error is: ",e)

property = "properties/367925539"

##########For landing page Data
dimensions=[Dimension(name="landingPagePlusQueryString")]
metrics=[{"name":"sessions"}, {"name":"newUsers"}, {"name":"bounceRate"}, {"name":"averageSessionDuration"}]
start_date = '2023-07-01'
end_date = 'today'
header_rows='Landing Page,Sessions,% New Sessions,New Users,Bounce Rate,Pages / Session,Avg. Session Duration,Goal Conversion Rate,Goal Completions,Goal Value'
df = get_ga4_report_df(property, dimensions, metrics, start_date, end_date, "landing_page", header_rows)
write_csv('analytics_data_landing_pagesKNV.csv', header_rows, df)

##########For date pages Data
#Page,Pageviews,Unique Pageviews,Avg. Time on Page,Entrances,Bounce Rate,% Exit,Page Value

dimensions=[Dimension(name="landingPagePlusQueryString")]
metrics=[{"name":"screenPageViews"}, {"name":"screenPageViewsPerUser"}, {"name":"userEngagementDuration"}, {"name":"sessions"}, {"name":"bounceRate"}]
#, {"name":"sessionsPerUser"}, {"name":"screenPageViews"}, {"name":"screenPageViewsPerSession"}, {"name":"screenPageViewsPerUser"},{"name":"userEngagementDuration"}]  
#{"name":"newUsers"}, {"name":"bounceRate"}, {"name":"averageSessionDuration"}]
#Page,Pageviews,Unique Pageviews,Avg. Time on Page,Entrances,Bounce Rate,% Exit,Page Value
start_date = '2023-07-01'
end_date = 'today'
header_rows='Page,Pageviews,Unique Pageviews, Avg. Time on Page, Entrances, Bounce Rate, % Exit, Page Value'
df = get_ga4_report_df(property, dimensions, metrics, start_date, end_date, "pages", header_rows)
write_csv('analytics_data_pagesKNV.csv', header_rows, df)
