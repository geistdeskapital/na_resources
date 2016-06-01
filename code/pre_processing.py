"""
pre_processing.py cleans html elements
from scraped article
"""

import requests
from bs4 import BeautifulSoup
import re, os, csv, time
import pandas as pd
import numpy as np
from numpy import genfromtxt


def getArticleText(url):
	try:
		r = requests.request('GET', url, timeout=3.1)
		print('Scraping: ' + url)
	
		soup=BeautifulSoup(r.content)
	
		##remove all script and style elements
		for script in soup(['script', 'style']):
			script.extract()
	
		text = soup.get_text()
	except:
		text = ''

	return text

def filterArticle(rawText, title):

	m = re.search('[A-Z][^\n\.]+\..{,4000}\.\s{,3}[A-Z][^\.\n]*\.', \
	rawText, re.DOTALL)
	
	if m is not None:
		filterText = m.group(0)
		filterText = re.sub('\n', '', filterText)
		print(filterText.encode('utf-8', 'ignore'))
		return filterText
	else:
		return ''

def main():
	"""
	import rss results
	"""
	data = pd.read_csv('Sources/rss_test.csv', sep=',', encoding='cp1252')
	data = data[:100]

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
