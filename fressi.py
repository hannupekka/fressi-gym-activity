#!/usb/bin/env python
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
from mechanize import Browser
from optparse import OptionParser, OptionGroup
from datetime import date
from ConfigParser import SafeConfigParser

def login(options):
	""" Used to login and get training data

	Args:
		options: an object containing values for all of your command line options

	Return:
		data: list of objects that BeautifulSoup found
	"""

	# New mechanize browser
	br = Browser()
	# Ignore robots.txt
	br.set_handle_robots(False)

	# Open login page
	login_page_url = 'https://fressi.bypolar.fi/web/1/webPage.html'
	login_page = br.open(login_page_url)

	# Select login form
	br.select_form(nr=1)

	# Set login and password and submit form
	br.form['login'] = options.username
	br.form['password'] = options.password
	br.submit()

	# Open data page
	data_page_url = 'http://fressi.bypolar.fi/mobile/1/history.html'
	try:
		data = br.open(data_page_url).read()
	except:
		print "Could not login, please check your login credentials. Also make sure your character encoding is set to UTF-8"
		return False

	# Make soup from data
	bs = BeautifulSoup(data)

	# Parse activity infos
	data = bs.find('ul', {'id': 'hour-container'}).findAll('a', {'class': 'hour-wrapper'})

	if not data:
		print "Could not parse training activity"
		return False

	return data

def parse(data, options):
	""" Parses and outputs training data

	Args:
		data: list of objects BeautifulSoup found
		options: an object containing values for all of your command line options
	"""
			
	# Start output with correct formatting
	if options.format_csv:
		output = '"date","activity"\n'
	elif options.format_html:
		output = """
<!DOCTYPE html>
<html lang="en">
<head>
	<meta charset="utf-8">
	<title>Fressi | Stats</title>
</head>
<body>
	<div id="content">
		<table id="result">	
"""
	duplicates = []
	# Parse data
	for act in data:
		# Get date for activity
		(day, month, year) = act.find('h5').text.strip().split(' ')[0].split('.')

		# Create new date object and get actitivy type
		act_date = date(int(year), int(month), int(day))
		act_type = act.find('h3').text.strip()

		# Skip duplicates by default. Otherwise save dates for comparison
		if not options.duplicates:
			if act_date.__str__() in duplicates:
				continue
			else:
				duplicates.append(act_date.__str__())

		# Format row
		if options.format_csv:
			output += '"%s","%s"\n' % (act_date, act_type)
		elif options.format_html:
			output += "<tr><td>%s</td><td>%s</td></tr>" % (act_date, act_type)
		else:
			print "%s\t%s" % (act_date, act_type)			

	# Finalize formatting and print output
	if options.format_csv:
		print output
	elif options.format_html:
		output += "</table></body></html>"
		print output

def main():
	""" Collects command line arguments from user """

	# Create new option parser and add options
	parser = OptionParser()
	parser.add_option("-u", "--username", dest="username", help="username to log in with", type="string")
	parser.add_option("-p", "--password", dest="password", help="password to go with username", type="string")
	parser.add_option("--csv", action="store_true", dest="format_csv", help="format output to CSV")
	parser.add_option("--html", action="store_true", dest="format_html", help="format output to HTML ")

	group = OptionGroup(parser, "Duplicate entry fix",
		"Polar's system sometimes marks duplicates when checking in to gym")
	group.add_option("-d", "--duplicates", action="store_true", dest="duplicates", help="show multiple entries for same day")
	parser.add_option_group(group)

	# Read options and arguments
	(options, args) = parser.parse_args()

	cparser = SafeConfigParser()
	cparser.read('.fressi.ini')

	config = {}
	config['username'] = cparser.get('auth', 'username')
	config['password'] = cparser.get('auth', 'password')

	# Basic validation for options
	if not options.username:
		if config['username']:
			options.username = config['username']
		else:
			parser.error('username is required')
	if not options.password:
		if config['password']:
			options.password = config['password']
		else:
			parser.error('password is required')
	if options.format_html and options.format_csv:
		parser.error('use either --html or --csv')

	# Log in and get data
	data = login(options)

	# Parse, format and output data
	parse(data, options)

if __name__ == '__main__':
	main()