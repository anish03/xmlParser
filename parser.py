import xml.etree.ElementTree as ET
import pandas as pd
import datetime
import sys
import os

files = os.listdir('./xmlFiles')
xml_file_data = []
headers = []

def parse_all_xml_files(files):

	'''
	:param files: list of all xml files
	:return: headers for csv and parsed xml data
	'''

	# loop through all the xml files
	for file in files:
		tree = ET.parse('xmlFiles/'+file)
		root = tree.getroot()

		newroot = ET.Element('data')
		newroot.insert(0,root)

		data = []

		# aggregation of parsed data
		for item in root.findall('DeviceID'):
			if item.tag not in headers:
				headers.append(item.tag)
			data.append(item.text)

		for item in root.findall('Timestamp'):
			if item.tag not in headers:
				headers.append(item.tag)
			data.append(item.text)

		for item in root.findall('TextMeasured'):
			for subitem in item:
				if subitem.text.__contains__('_'):
					if subitem.text not in headers:
						headers.append(subitem.text)
				else:
					data.append(subitem.text)
		xml_file_data.append(list(pd.Series(data)))
	return headers,xml_file_data

def generate_performance_metrics_csv(headers,xml_data):

	'''
	:param headers: headers for generating csv
	:param xml_data: data parsed from the xml files
	:return: DataFrame
	'''

	df = pd.DataFrame(xml_data,columns=headers)
	df.set_index('DeviceID',inplace=True)
	df.to_csv('performance_metrics.csv')
	return df

def calculate_cumm_stress_time(id,df):

	'''
	:param id: Device ID
	:param df: DataFrame for a particular Device
	:return: Cumulative Stress Time
	'''
	#id = raw_input('Cummulative Stress Time: Enter Device ID:')
	temp_df = df.loc[id]
	print '\n\n',temp_df

	max_time = max(temp_df['Timestamp'])
	min_time = min(temp_df['Timestamp'])

	a = datetime.datetime.strptime(min_time, "%Y-%m-%dT%H:%M:%S")
	b = datetime.datetime.strptime(max_time, "%Y-%m-%dT%H:%M:%S")
	c = b - a

	days = str(c).split(',')[0]
	hours,minutes,seconds = str(c).split(',')[1].split(':')

	print '\n\nCummulative Stress time for Device '+id+':',days,hours+' hr',minutes+' mins',seconds+' sec','\n\n'

def main():

	id = sys.argv[1]
	headers,xml_data = parse_all_xml_files(files)
	df = generate_performance_metrics_csv(headers,xml_data)
	calculate_cumm_stress_time(id,df)

if __name__ == '__main__':
	main()

#3107607
