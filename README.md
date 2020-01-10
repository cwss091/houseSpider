# houseSpider

Parsing house data from LJ website

# Environment

MacOS Catalina 10.15.2

browser: chrome

python version: 2.7

python package required: selenium, pyquery, pandas

# Instruction

Step 1: get raw data from target house and store in a directory or file of csv
  ./spider.py -l [link of search results] -o [output csv] -q (quit browser if has)
  
Step 2: clean data and summary stats (including community (xiaoqu) and neighborhood (bankuai)
  ./run.py -d [csv file or directory] -o [output csv]
 
