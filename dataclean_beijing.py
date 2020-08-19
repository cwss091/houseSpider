#!/usr/bin/python
# -*- coding: UTF-8 -*-

# v1.0  clean data. todo: update csv proccessing with pandas
# v1.01 It is a version for Beijing

import os, sys
import getopt
import chardet
#import pandas as pd 
from unicodecsv import utf_csv_reader, UnicodeWriter

table_title = [u"小区", u"总价", u"单价", u"建筑面积", u"套内面积", u"年代", u"行政区", u"街道", u"环位", u"所在楼层", u"房屋户型", u"房屋朝向", u"梯户比例", u"户型结构", u"装修情况", u"配备电梯", u"建筑类型", u"供暖方式"]
#table_title = ["community", "TotalPrice", "UnitPrice", "SpaceArea", "ActureArea", "Year", "District", "Neighborhood", "Ring", "Floor", "RoomNum", "RoomDirection", "LiftUnit", "AptStructure", "Decoration", "Elevator", "BuidlingStructure", "OwnershipYear"]

class DataClean:

	def __init__(self, files):

		if os.path.isfile(files):
			self.files = [files]
		elif os.path.isdir(files):
			tmp_files = os.listdir(files)
			self.files = [ os.path.join(files, f) for f in os.listdir(files) ]
		else:
			raise ValueError("Not valid file or director!\n")

	def _read_restruct_csv(self, file):

		"""
		read csv file and restruct it by eliminating space
		"""

		print "Processing " + file
		info_table = []
		with open(file, 'r') as f:
			freader = utf_csv_reader(f)
			for row in freader:
				if row[0] == unicode("梯户比例", "utf-8"):
					continue
				# total price need revised 
				if len(row) < 17:
					print ','.join(row).encode('utf-8')
					continue
				community = row[11]
				total_price = row[2].split(u" ")[0]
				unit_price = row[4]
				space_area = row[12]
				actual_space_area = row[6]
				year = row[16]
				#area = row[3].split(" ".encode("utf-8"))
				#print type(row[3])
				#print repr(row[3])
				area = row[9].split(u'\xa0')

				#print area 
				dist = area[0]
				try:
					street = area[1]
				except IndexError:
					street = u"未知"
				try:
					ring = area[2]
				except IndexError:
					ring = u"未知"
				floor = row[14]
				room = row[8]
				room_face = row[3]
				unit_lift = row[0]
				room_structure = row[5]
				decor = row[1]
				islift = row[10]
				building = row[7]
				heat = row[15]
				info = [community, total_price, unit_price, space_area, actual_space_area, year, dist, street, ring, floor, room, room_face, unit_lift, room_structure, decor, islift, building, heat]
				info_table.append(info)

		return info_table

	def _combine_csv(self, output):

		with open(output, 'w+') as o:
			fw = UnicodeWriter(o)
			fw.writerow(table_title)
			for file in self.files:
				if not file.endswith('.csv'):
					continue
				itable = self._read_restruct_csv(file)
				for i in itable:
					fw.writerow(i)

def parse_arg(optargs):

	usage = """./dataclean.py -d [csv file or directory] -o [output csv]\nClean data and combine file (in utf-8)\n"""

	global FILE, OUTPUT
	OUTPUT = "Total_Info_Table.csv"

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
		elif o in ('-h'):
			print usage
			sys.exit(0)

def main():
	parse_arg(sys.argv[1:])
	dc = DataClean(FILE)
	dc._combine_csv(OUTPUT)

if __name__ == "__main__":
	main()




