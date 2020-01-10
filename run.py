#!/usr/bin/python
# -*- coding: UTF-8 -*-

# v1.0 run dataclean.py and analysis.py

import sys, os
import getopt
from dataclean import DataClean
from analysis import StatSummary

def parse_arg(optargs):

	usage = """\n./run.py -d [csv file or directory] -o [output csv]\nclean data and summary stats\n"""

	global FILE, OUTPUT
	OUTPUT = "summary_{0}.csv"

	try:
		opts, args = getopt.getopt(optargs, "d:o:h")
	except getopt.GetoptError as err:
		sys.stderr.write("[ERROR] Invalid Syntax\n")
		sys.stderr.write(usage)
		sys.exit(1)

	for o, a in opts:
		if o in ('-d'):
			FILE = a
		elif o in ('-o'):
			OUTPUT = a
			if not OUTPUT.endswith('.csv'):
				sys.stderr.write("[ERROR]: Please input a filename endswith '.csv'\n")
				sys.exit(1)
			if OUTPUT.split('.')[0][-3:] != "{0}":
				OUTPUT = OUTPUT.split('.')[0] + "_{0}.csv"
		elif o in ('-h'):
			print usage
			sys.exit(0)


def main():

	parse_arg(sys.argv[1:])
	dc = DataClean(FILE)
	total_info = "Total_Info_Table.csv"
	print "Total house infomation written in {0}" + total_info

	ss = StatSummary(total_info)

	community_info = OUTPUT.format("community")
	ss._stat_community(community_info)
	print u"小区信息统计在 " + community_info

	ss2 = StatSummary(community_info)
	neighbor_info = OUTPUT.format("neighborhood")
	ss2._stat_neighborhood(neighbor_info)
	print u"片区信息统计在 " + neighbor_info

if __name__ == "__main__":

	main()

