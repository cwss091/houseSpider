#!/usr/bin/python
# -*- coding: utf-8 -*-
# v1.0  selenium to get house data in Lianjia 01/04/2019
# v1.1 update search results. Handle more situation

from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from pyquery import PyQuery as pq
import sys
import time
import random
from unicodecsv import UnicodeWriter
import getopt


chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--proxy-server=127.0.0.1:8080 --disable-extensions')
chrome_options.add_argument('--disable-extensions')
global browser
browser = webdriver.Chrome(executable_path="./chromedriver", chrome_options=chrome_options)
wait = WebDriverWait(browser, 10)


def get_house_urls(root_url, needPage=False):

	"""
	get houses' urls in every root (searching result) page
	"""

	browser.get(root_url)
	urls_html = browser.page_source
	doc = pq(urls_html)

	urls = []
	for a in doc('.sellListContent .title a').items():
		url = a.attr.href
		urls.append(url)

	if needPage:
		total_pages = doc('.page-box.house-lst-page-box').attr["page-data"].split(',')[0].split(':')[-1]
		return urls, int(total_pages)
	else:
		return urls, 0

	#browser.close()


def get_data(url):

	"""
	get house information
	"""

	browser.get(url)
	data_html = browser.page_source
	data_doc = pq(data_html)

	info = {}
	info[u"总价"] = data_doc('.overview .total').text()
	info[u"单价"] = data_doc('.unitPriceValue').text()
	info[u"年代"] = data_doc('.houseInfo .area .subInfo').text()[0:4]
	info[u"小区"] = data_doc('.communityName .info').text()

	info[u"区域"] = data_doc('.areaName .info').text() 

	for bi in data_doc('.box-l .base .content li').items():
		info[bi.text()[0:4]] = bi.text()[4:]

	if info.has_key(u"别墅类型"):
		info[u"建筑类型"] = u"别墅"
		info[u"户型结构"] = u"未知"
		info[u"配备电梯"] = u"无"
		info[u"梯户比例"] = u"无"
		del info[u"别墅类型"]

	#for ti in data_doc('.transaction .content li').items():
	#	info[ti.text()[0:4]] = ti.text()[4:]

	return info

def write_csv(info_dics, output):

	"""
	write infomation to csv
	"""

	with open(output, 'w+') as o:
		fw = UnicodeWriter(o, encoding="utf-8")
		fw.writerow(info_dics[0].keys())
		for d in info_dics:
			fw.writerow(d.values())



def test():

	temp_burl = LINK.split('/')
	if temp_burl[-1] == "":
		base_url = "/".join(temp_burl[0:-2]) + "/{0}" + temp_burl[-2] + "/"
	else:
		base_url = "/".join(temp_burl[0:-1]) + "/{0}" + temp_burl[-1] + "/"

	print base_url
	house_urls = get_house_urls(base_url.format(''), False)[0]
	print house_urls
	time.sleep(2+random.uniform(0,2.0))

	for u in house_urls:
		print u

	house_info = []
	for u in house_urls:
		house_info.append(get_data(u))
		time.sleep(2+random.uniform(0,2.0))


	output = "./Pudong_Cixin_1.csv"
	write_csv(house_info, output)
	browser.close()

def main():

	temp_burl = LINK.split('/')
	if temp_burl[-1] == "ershoufang":
		base_url = LINK + "/{0}"
	elif temp_burl[-1] == "" and temp_burl[-2] == "ershoufang":
		base_url = LINK + "{0}"
	elif temp_burl[-1] == "" and temp_burl[-2] != "ershoufang":
		base_url = "/".join(temp_burl[0:-2]) + "/{0}" + temp_burl[-2] + "/"
	elif temp_burl[-1] != "" and temp_burl[-1] != "ershoufang":
		base_url = "/".join(temp_burl[0:-1]) + "/{0}" + temp_burl[-1] + "/"
	else:
		raise ValueError("[Error]: invalid webpage link!\n")
	house_urls, total_pages = get_house_urls(base_url.format(''), True)
	time.sleep(2+random.uniform(0,2.0))

	print "total pages: " + str(total_pages)
	print "Start parsing houses in page 1"

	house_info = []
	for u in house_urls:
		try:
			house_info.append(get_data(u))
			print "Parsing {0} successfully".format(u)
		except:
			print "Parseing {0} failed.".format(u)
		time.sleep(2+random.uniform(0,2.0))


	write_csv(house_info, OUTPUT.format('1'))
	time.sleep(random.uniform(3.0,7.0))

	for i in range(2, total_pages+1):
		house_urls, total_pages = get_house_urls(base_url.format('pg'+str(i)))
		time.sleep(2+random.uniform(0,2.0))

		print "Start parsing houses in page {0}".format(i)

		house_info = []
		for u in house_urls:
			try:
				house_info.append(get_data(u))
				print "Parsing {0} successfully".format(u)
			except:
				print "Parseing {0} failed.".format(u)
			time.sleep(2+random.uniform(0,2.0))

		write_csv(house_info, OUTPUT.format(str(i)))
		time.sleep(5+random.uniform(3.0,7.0))

	browser.close()

def web_test():
	url = "http://whatismyipaddress.com"
	browser.get(url)
	#browser.close()
	#browser.quit()

def driver_quit():
	browser.quit()


def parse_arg(optargs):

	usage = """\n./spider.py -l [link of search results] -o [output csv] -q (quit browser if has)\nget raw data from target houses and write in csv (in utf-8)\n"""

	global LINK, OUTPUT, ISQUIT
	OUTPUT = "result_{0}.csv"
	ISQUIT = False
	LINK = None

	try:
		opts, args = getopt.getopt(optargs, "l:o:qh")
	except getopt.GetoptError as err:
		sys.stderr.write("[ERROR] Invalid Syntax\n")
		sys.stderr.write(usage)
		sys.exit(1)

	for o, a in opts:
		if o in ('-l'):
			LINK = a
		elif o in ('-o'):
			OUTPUT = a
			if not OUTPUT.endswith('.csv'):
				sys.stderr.write("[ERROR]: Please input a filename endswith '.csv'\n")
				sys.exit(1)
			if OUTPUT.split('.')[0][-3:] != "{0}":
				OUTPUT = OUTPUT.split('.')[0] + "_{0}.csv"
		elif o in ('-q'):
			ISQUIT = True
		elif o in ('-h'):
			print usage
			sys.exit(0)

	if (not ISQUIT) and (LINK is None):
		sys.stderr.write("[ERROR]: No searching result link\n")
		sys.exit(1)


if __name__ == "__main__":
	#web_test()
	parse_arg(sys.argv[1:])
	if ISQUIT:
		driver_quit()
	else:
		main()
		print "Your result csv files in {0}".format('/'.join(OUTPUT.split('/')[0:-1]))
