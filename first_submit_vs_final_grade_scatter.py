# Quick visualization of students first submissions vs final date produced by autograder.io
#
# EXAMPLE USAGE: python first_submit_vs_final_grade_scatter.py -f project_scores.csv
#
# (c)Steve Zekany EECS 370 Winter 2020

import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse
from datetime_z import parse_datetime
import datetime
import time


def make_histogram(filename, output_file):
	df = pd.read_csv(filename)

	# print(df) # uncomment to show dataframe

	# dictionarize the dataframe
	score_dict = pd.DataFrame.to_dict(df)

	# find all unique student names
	students = set(score_dict['Username 1'].values())
	print('number of student names: ' + str(len(students))) # debugging

	# get earliest date and max score for each student
	score_table = pd.DataFrame(columns=['First Submission', 'First Submission DatetimeObj', 'Last Submission', 'Final Score'])

	first_submission = df['Timestamp'].min()
	last_submission = df['Timestamp'].max()

	for student in students:
		subs = df.loc[df['Username 1'] == student]
		# print(subs['Timestamp'])

		# print(subs.qindex['Timestamp', 0])
		# print(subs['Timestamp'].min())
		first_submit_time = subs['Timestamp'].min()
		last_submit_time = subs['Timestamp'].max()
		max_score = subs['Total'].max()

		# build date
		first_date = parse_datetime(first_submit_time)
		last_date = parse_datetime(first_submit_time)
		# unixtime = time.mktime(date.timetuple())
		first_date_str = str('%04d'%first_date.year) + '-' + str('%02d'%first_date.month) + '-' + str('%02d'%first_date.day) 
		last_date_str = str(last_date.year) + '-' + str(last_date.month) + '-' + str(last_date.day) 

		# build the dataframe iterativelyfirst_date_str
		score_table.loc[student] = pd.Series({'First Submission':pd.to_datetime(first_date_str), 'First Submission DatetimeObj':first_submit_time, 'Last Submission':pd.to_datetime(last_date_str), 'Final Score':max_score})

	print(score_table)


	sns.set(style="whitegrid")


	# sns.regplot(x=score_table['First Submission DatetimeObj'], y=score_table['Final Score']);
	ax = sns.scatterplot(x=score_table['First Submission'], y=score_table['Final Score'], color=sns.xkcd_rgb["windows blue"])

	ax.set_ylabel("Final Score")
	ax.grid(False)
	# x_dates = score_table['First Submission'].dt.strftime('%Y-%m-%d').sort_values().unique()
	# ax.set_xticklabels(labels=x_dates, rotation=45, ha='right')

	plt.xlim(first_submission, last_submission)

	# plt.show()
	sns_plot = ax.get_figure()
	sns_plot.savefig(fname=output_file)

if __name__ == "__main__":
	#--- Setup Argument Parsing ---#
	parser = argparse.ArgumentParser(prog='histogram_all',
	 		description='Create a histogram of all final grades from the autograder.io csv')
	parser.add_argument("-f", "--filename", dest="filename",
			required=True, help='path to csv file from autograder.io')

	args = parser.parse_args()
	make_histogram(args.filename, 'output.pdf')


