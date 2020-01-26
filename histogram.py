# Quick visualization of student final submissions produced by autograder.io
#
# EXAMPLE USAGE: python histogram_all.py -f project_scores.csv -l
#
# (c)Steve Zekany Winter 2020

import csv
import seaborn as sns
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import numpy as np


def make_histogram(filename, log_plot, output_filename, title):
	df = pd.read_csv(filename)

	# print(df) # uncomment to show dataframe

	sns.set(style="whitegrid")

	columnname = 'Total Points'

	ax = sns.distplot(df[columnname], color=sns.xkcd_rgb["windows blue"], kde=False, rug=False, hist_kws={"alpha": 1})
	if log_plot == True:
		ax.set(yscale="log")

	ax.set_title(title)

	ax.set_ylabel("# Students")
	ax.grid(False)
	# plt.xlim(0, 40)

	# plt.show()

	sns_plot = ax.get_figure()
	sns_plot.savefig(fname=output_filename)

	print('\n\n\n ---- Project Stats ----')
	print('Number of submissions: ' + str(len(df[columnname])))
	print('Average: ' + str('%.2f'%np.average(df[columnname])))
	print('Median: ' + str('%.2f'%np.median(df[columnname])))
	print('Standard Deviation: ' + str('%.2f'%np.std(df[columnname])))
	print('High Score: ' + str('%.2f'%np.max(df[columnname])))
	print('Low Score: ' + str('%.2f'%np.min(df[columnname])))


if __name__ == "__main__":
	#--- Setup Argument Parsing ---#
	parser = argparse.ArgumentParser(prog='histogram_all',
	 		description='Create a histogram of all final grades from the autograder.io csv')
	parser.add_argument("-f", "--filename", dest="filename",
			required=True, help='path to csv file from autograder.io')
	
	# parser.add_argument("-l", "--log_plot", dest='log_plot', 
 #                    action='store_true', help='plot y axis as log plot')

	args = parser.parse_args()
	title = 'Histogram of Project Scores for Project 1a W2020'
	title_log = 'Histogram (logplot) of Project Scores for Project 1a W2020'
	make_histogram(args.filename, False, 'score_plot.png', title)
	make_histogram(args.filename, True, 'score_plot_log.png', title_log)



