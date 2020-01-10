# houseSpider

Parsing house data from LJ website

# Environment

MacOS Catalina 10.15.2

browser: chrome (need driver first). If you choose another browser please change the head of spider.py.

chrome driver download: https://chromedriver.chromium.org/downloads

python version: 2.7

python package required: selenium, pyquery, pandas

# Instruction

Step 1: get raw data from target house and store in a directory or file of csv, For example, https://sh.lianjia.com/ershoufang/l3p2/ or https://sh.lianjia.com/ershoufang/
  ./spider.py -l [link of search results] -o [output csv] -q (quit browser if has)
  
Step 2: clean data and summary stats (including two files, stats of community (xiaoqu) and neighborhood (bankuai))
  ./run.py -d [csv file or directory (output of the directory of output which in step 1] -o [output csv]
 
