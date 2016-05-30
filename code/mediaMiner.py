"""
mediaMiner.py holds class media
that contains functions designed to extract
media sources from websites (rss/youtube)
"""

from selenium import webdriver
import time, random, csv, os, re
from selenium.webdriver.common.keys import Keys
import pandas as pd
import numpy as np
from numpy import genfromtxt
from random import randint

class Media:

	def rssMiner(driver, tag_type, expression_match):
		"""
		rssMiner() identifies webpage's rss feed
		:param driver: selenium webdriver object
		:param tag_type: string, designates html tag type
		:param string_match: regular expression to match
		"""
		
		##identify all elements that might hold rss feed
		elements = driver.find_elements_by_tag_name(tag_type)
		
		##loop through elements and extract rss_feed when parameters are met
		for element in elements:
			try:
				m = re.search(expression_match, \
				element.get_attribute('href'))
				
				if m is not None:
					rss_feed = m.group(0)
					break
			except:
				pass
		else:
			rss_feed = ''
		
		return rss_feed
	
	def youTube(driver):
		"""
		youTube() scrapes website's youtube channel href.
		:param driver: selenium webdriver object
		"""
		
		##identify all elements that might hold youtube channel href
		
		elements = driver.find_elements_by_tag_name('a')
		
		##lop through elements and extract youtube channel href
		for element in elements:
			if element.get_attribute('href') is not None and \
			'youtube.com/user' in element.get_attribute('href'):
				results = element.get_attribute('href')
				break
		else:
			results = ''
		
		return results
