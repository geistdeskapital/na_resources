"""
pre_processing.py cleans html elements
from scraped article and removes extraneous text
"""

import requests
from bs4 import BeautifulSoup
import re, os, csv, time
import pandas as pd
import numpy as np
from numpy import genfromtxt


def getArticleText(url):
	r = requests.request('GET', url, timeout=.02)
	print('Scraping: ' + url)
	
	
	soup=BeautifulSoup(r.content)
	
	##remove all script and style elements
	for script in soup(['script', 'style']):
		script.extract()
	
	text = soup.get_text()

	return text

def filterArticle(rawText, title):
	filterText = re.sub('^.*'+title, '', rawText, re.IGNORECASE, \
	re.DOTALL)
	m = re.search('\n[A-Z][^\n\.]+\.(.|\n){150,1500}[^\.\n{2,10}?]*?\.', \
	filterText, re.DOTALL)
	if m is not None:
		filterText = m.group(0)
	return filterText

def main():
	"""
	import rss results
	"""
	data = pd.read_csv('Sources/rss_test.csv', sep=',', encoding='cp1252')
	data = data[:20]

	"""
	Iterate through urls and scrape/filter text
	"""

	for url, title in zip(data['url'], data['title']):
		text = getArticleText(url)
		cleanText = filterArticle(text, title)
		
		results = pd.DataFrame([[url, title, cleanText]])
		try:
			with open('Sources/test_clean.csv', 'a') as file:
				results.to_csv(file, sep=',', index=False, header=False, \
				encoding='UTF-8')
		except:
			pass
		

if __name__ in "__main__":
	main()
