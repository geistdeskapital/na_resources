"""
rssFeed.py is an rss aggregator
"""

import feedparser, os, csv
from future import Future
import pandas as pd
import numpy as np
from numpy import genfromtxt

def main():
	"""
	import rss feeds to aggregate
	"""
	rssDF = pd.read_csv('Sources/rss_feeds.csv', sep=',')

	"""
	delist series holding rss feed values
	"""
	rssFeeds = rssDF['rss_feed'].tolist()
	
	"""
	use Future thread to pull five feeds at once
	"""
	
	##pull down all feeds
	future_calls = [Future(feedparser.parse, rss_url) for rss_url in rssFeeds]
	
	##block until they are all in
	feeds = [future_obj() for future_obj in future_calls]
	
	##extract all entries
	for feed in feeds:
		for item in feed['items']:
			results = [item['title'], item['link'], feed['url']]
			results = pd.DataFrame([results])
			
			##write line to .csv
			try:
				with open('', 'a') as file:
					results.to_csv(file, sep=',', header=False, index=False, \
					encoding='cp1252')
			except:
				pass
		
if __name__ in "___main__":
	main()
