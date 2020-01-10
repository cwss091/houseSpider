#!/usr/bin/python
# -*- coding: utf-8 -*-

# v1.0 Summary community's average unit price, neighborhood's average unit price, 
#	   higest/lowest total price of community and highest/lowest unit_price neighborhood

import os, sys
import pandas as pd
 
class StatSummary:

	def __init__(self, csvfile):

		self.df_csv = pd.read_csv(csvfile, encoding="utf-8")

	def _stat_community(self, output):

		"""
		get community's average unit price, highest/lowest total price
		"""

		ave_unit = {}
		high_total = {}
		low_total = {}
		num = {}

		year ={}
		dist = {}
		street = {}
		ring = {}
		building = {}

		for index, row in self.df_csv.iterrows():
			isnew = False
			try:
				num[row[u"小区"]] += 1
			except KeyError:
				num[row[u"小区"]] = 1
				isnew = True

			if (isnew):
				high_total[row[u"小区"]] = int(row[u"总价"])
				low_total[row[u"小区"]] = int(row[u"总价"])
				ave_unit[row[u"小区"]] = int(row[u"单价"].split(u"元")[0])

				year[row[u"小区"]] = row[u"年代"]
				dist[row[u"小区"]] = row[u"行政区"]
				street[row[u"小区"]] = row[u"街道"]
				ring[row[u"小区"]] = row[u"环位"]
				building[row[u"小区"]] = row[u"建筑类型"]

			else:
				if int(row[u"总价"]) > high_total[row[u"小区"]]:
					high_total[row[u"小区"]] = int(row[u"总价"])
				if int(row[u"总价"]) < low_total[row[u"小区"]]:
					low_total[row[u"小区"]] = int(row[u"总价"])
				ave_unit[row[u"小区"]] += int(row[u"单价"].split(u"元")[0])

		for c in ave_unit:
			ave_unit[c] /= num[c]

		summary = {}
		summary[u"小区"] = ave_unit.keys()
		summary[u"平均单价"] = ave_unit.values()
		summary[u"最高总价"] = high_total.values()
		summary[u"最低总价"] = low_total.values()
		summary[u"挂牌数"] = num.values()
		summary[u"年代"] = year.values()
		summary[u"行政区"] = dist.values()
		summary[u"街道"] = street.values()
		summary[u"环数"] = ring.values()
		summary[u"建筑类型"] = building.values()

		summary_df = pd.DataFrame(summary)
		summary_df.to_csv(output, index=False, encoding="utf-8")



	def _stat_neighborhood(self, output):

		"""
		get neighborhood's average unit price, highest/lowest unit price
		each community get the same weight in average calc
		"""


		ave_unit = {}
		high_unit = {}
		high_com = {}
		low_unit = {}
		low_com = {}
		num = {}
		house_num = {}


		for index, row in self.df_csv.iterrows():
			isnew = False
			try:
				num[row[u"街道"]] += 1
			except KeyError:
				num[row[u"街道"]] = 1
				isnew = True

			if (isnew):
				high_unit[row[u"街道"]] = int(row[u"平均单价"])
				low_unit[row[u"街道"]] = int(row[u"平均单价"])
				ave_unit[row[u"街道"]] = int(row[u"平均单价"])
				high_com[row[u"街道"]] = row[u"小区"]
				low_com[row[u"街道"]] = row[u"小区"]
				house_num[row[u"街道"]] = int(row[u"挂牌数"])

			else:
				if int(row[u"平均单价"]) > high_unit[row[u"街道"]]:
					high_unit[row[u"街道"]] = int(row[u"平均单价"])
					high_com[row[u"街道"]] = row[u"小区"]
				if int(row[u"平均单价"]) < low_unit[row[u"街道"]]:
					low_unit[row[u"街道"]] = int(row[u"平均单价"])
					low_com[row[u"街道"]] = row[u"小区"]
				ave_unit[row[u"街道"]] += int(row[u"平均单价"])
				house_num[row[u"街道"]] += int(row[u"挂牌数"])

		for c in ave_unit:
			ave_unit[c] /= num[c]

		summary = {}
		summary[u"街道"] = ave_unit.keys()
		summary[u"平均单价"] = ave_unit.values()
		summary[u"最高单价"] = high_unit.values()
		summary[u"最低单价"] = low_unit.values()
		summary[u"小区数"] = num.values()
		summary[u"房源数"] = house_num.values()
		summary[u"最高小区"] = high_com.values()
		summary[u"最低小区"] = low_com.values()

		summary_df = pd.DataFrame(summary)
		summary_df.to_csv(output, index=False, encoding="utf-8")


	def _test(self):
		for index, row in self.df_csv.iterrows():
			a = row[u'单价'].split(u'元')[0]
			print type(a)
			print (int(a))
			break

def main():
	file = sys.argv[1]
	output = sys.argv[2]
	ss = StatSummary(file)
	ss._stat_neighborhood(output)

if __name__ == "__main__":
	main()




