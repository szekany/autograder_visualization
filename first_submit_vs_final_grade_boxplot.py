# Quick visualization of students first submissions vs final date produced by autograder.io
#
# EXAMPLE USAGE: python first_submit_vs_final_grade_boxplot.py -f project_scores.csv
#
# (c)Steve Zekany EECS 370 Winter 2020

import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import argparse
from util.datetime_z import parse_datetime
import datetime
import time
from textwrap import wrap



def make_histogram(filename, output_file, title):
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
		# print(type(first_submit_time))

		# build date
		first_date = parse_datetime(first_submit_time)
		last_date = parse_datetime(first_submit_time)
		# unixtime = time.mktime(date.timetuple())
		# first_date_str = str('%04d'%first_date.year) + '-' + str('%02d'%first_date.month) + '-' + str('%02d'%first_date.day) 
		first_date_str = str('%02d'%first_date.month) + '-' + str('%02d'%first_date.day) 
		last_date_str = str(last_date.year) + '-' + str(last_date.month) + '-' + str(last_date.day) 

		# build the dataframe iteratively
		score_table.loc[student] = pd.Series({'First Submission':first_date_str, 'First Submission DatetimeObj':first_submit_time, 'Last Submission':pd.to_datetime(last_date_str), 'Final Score':max_score})

	# print(score_table)


	sns.set(style="whitegrid")

	# sorting dataframe
	score_table.sort_values('First Submission', ascending=True, inplace=True)
	# print(score_table)

	# sns.regplot(x=score_table['First Submission DatetimeObj'], y=score_table['Final Score']);
	# ax = sns.scatterplot(x=score_table['First Submission'], y=score_table['Final Score'], color=sns.xkcd_rgb["windows blue"])
	ax = sns.boxplot(x=score_table['First Submission'], y=score_table['Final Score'])
	

	# ax.set_title(title)
	ax.set_title("\n".join(wrap(title, 60)))

	ax.set_ylabel("Final Score", fontweight="bold")
	ax.set_xlabel("Date of First Submission", fontweight="bold")

	ax.grid(False)
	# x_dates = score_table['First Submission'].dt.strftime('%Y-%m-%d').sort_values().unique()
	# ax.set_xticklabels(labels=x_dates, rotation=45, ha='right')

	# plt.xlim(first_submission, last_submission)

	ax.set_xticklabels(ax.get_xticklabels(), rotation=90)
	# ax.xaxis_date()
	# ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
	
	# fix layout
	plt.tight_layout()
	# plt.gcf().subplots_adjust(bottom=0.2)


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

	title = "Project 1a, Winter 2020 - Final score based on date of first submission to autograder.io"
	make_histogram(args.filename, 'output.png', title)


