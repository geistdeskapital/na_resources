from selenium import webdriver
import time, random, csv, os, re
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from numpy import genfromtxt
from random import randint
from mediaMiner import Media

"""
rssMiner.py scrapes rss feeds from webpages
and stores as exported .csv file
"""

def main():
	
	##connect to phantom js
	driver = webdriver.PhantomJS(executable_path='')
	print('Driver connected...')
	
	##load websites
	os.chdir('')
	siteData = pd.read_csv('websites.csv', sep=',')

	##loop through websites and scrape rss feeds
	for site, url in zip(siteData['site_name'], siteData['url']):
		print('Scraping: ' + url)
		driver.get(url)
		time.sleep(1)
		
		rss = Media.rssMiner(driver, 'link', '.*(/rss.*|/feed(/.*|$)|\.xml$)')
		
		if rss == '':
			rss = Media.rssMiner(driver, 'a', '.*(/rss.xml|/feed(/|$)).*')
		
		results = [site, url, rss]
		results = pd.DataFrame([results])
		
		try:
			with open('dataRSSFeeds.csv', 'a') as file:
				results.to_csv(file, sep=',', header=False, index=False,\
				encoding='cp1252')
		except:
			pass

if __name__ in "__main__":
	main()
