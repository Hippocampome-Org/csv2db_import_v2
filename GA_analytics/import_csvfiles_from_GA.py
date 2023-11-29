import os, csv
from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import Dimension, Metric, DateRange, RunReportRequest, OrderBy

os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '/Applications/XAMPP/hippocampome-1687549016291-058d852a885b-trackinggmail.json'
client = BetaAnalyticsDataClient()
property = "properties/367925539"
dimensions=[Dimension(name="city")]
metrics=[Metric(name="activeUsers")]
date_ranges=[DateRange(start_date="2023-07-01", end_date="today")]

request = RunReportRequest(
		property = "properties/367925539",
		dimensions=[Dimension(name="city")],
		metrics=[Metric(name="activeUsers")],
		date_ranges=[DateRange(start_date="2023-07-01", end_date="today")],
		)
print("Line after request")
try:    
	response = client.run_report(request)
	print("Report result:")
	header_row = [dim.name for dim in dimensions] + [metric.name for metric in metrics]
	data_rows = []
	for row in response.rows:
		dimension_values = [dim.value for dim in row.dimension_values]
		metric_values = [metric.value for metric in row.metric_values]
		data_row = dimension_values + metric_values
		data_rows.append(data_row)

	##for row in response.rows:
	##	print(row.dimension_values[0].value, row.metric_values[0].value)
	with open('file.csv', 'w', newline='') as file:
		csv.writer(file).writerow(header_row)
		csv.writer(file).writerows(data_rows)
except Exception as e:
	print("Error is: ",e)
