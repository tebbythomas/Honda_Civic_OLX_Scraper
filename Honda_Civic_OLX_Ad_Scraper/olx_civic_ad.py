'''
Description:
Python code to scrape olx.com for Honda Civic ads and store each individual car
advertisement's details like year, fuel, price, km driven, description in a csv
'''


import urllib2
import cookielib
import sys
import os
links = ["https://www.olx.in/bangalore/cars/q-civic","https://www.olx.in/bangalore/cars/q-civic/?page=2","https://www.olx.in/bangalore/cars/q-civic/?page=3","https://www.olx.in/bangalore/cars/q-civic/?page=4"]
hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
count = 0
for site in links:
	print site
	req = urllib2.Request(site, headers=hdr)

	try:
	    page = urllib2.urlopen(req)
	except urllib2.HTTPError, e:
	    print e.fp.read()

	content = page.read()
	with open('Civic_Ads.txt', 'a') as the_file:
	    the_file.write(content)
with open('Civic_Ads.txt') as fp:
    for line in fp:
        if '<a href="https://www.olx.in/item/' in line:
        	with open('Civic_Ads_links.txt', 'a') as the_file2:
    			line = line.replace("\t","")
    			line = line[ line.find('"')+1 : line.find('"',line.find('"') +1)]
    			line = line + '\n'
    			the_file2.write(line)
adCount = 0
try:
	os.remove('Car_Details.csv')
except OSError:
	pass
with open('Car_Details.csv', 'a') as csv_pointer:
	csv_pointer.write('"Title","Model", "Brand", "Year", "Fuel", "Price", "KM_Driven", "Description","URL"\n')
	with open('Civic_Ads_links.txt', 'r') as the_file3:
		for line in the_file3:
			URL = line.replace("\n","")
			print "URL = " + URL
			req = urllib2.Request(line, headers=hdr)
			try:
			    page = urllib2.urlopen(req)
			except urllib2.HTTPError, e:
			    print e.fp.read()

			content = page.read()
			try:
				os.remove('Single_Car_Ad.txt')
			except OSError:
				pass
			with open('Single_Car_Ad.txt', 'a') as the_file:
				the_file.write(content)
			with open('Single_Car_Ad.txt') as ad_file:
				for line in ad_file:
					if '<meta name="description" content="' in line:
						description = line.replace('<meta name="description" content="','')
						nxtLine = ad_file.next();
						while '<meta property' not in nxtLine:
							description = description + nxtLine
							nxtLine = ad_file.next();
						description = description.replace('" />','')
						description = description.lstrip()
						print "Description = " + description
					if '<title>' in line:#Get the title of the ad
						title = line[ line.find('<title>') + 7 : line.find('</title>')]
						print "Title = " + title
					if '<strong class="xxxx-large margintop7 inlblk not-arranged">' in line:#Get the price of the ad
						price = line[ line.find('<strong class="xxxx-large margintop7 inlblk not-arranged">') + 58 : line.find('</strong>')]
						price = price.replace("\n","")
						print "Price = " + price
					if '<div class="pding5_10">' in line:#Get the price of the ad
						attribute = ad_file.next();
						if 'Brand:' in attribute:
							ad_file.next();
							ad_file.next();
							brand = ad_file.next();
							brand = brand.replace("\t","")
							brand = brand.replace(" ","")
							brand = brand.replace("</a>","")
							brand = brand.replace("\n","")
							print "Brand = " + brand
						if 'Fuel:' in attribute:
							ad_file.next();
							ad_file.next();
							fuel = ad_file.next();
							fuel = fuel.replace("\t","")
							fuel = fuel.replace(" ","")
							fuel = fuel.replace("</a>","")
							fuel = fuel.replace("\n","")
							print "Fuel = " + fuel
						if 'Model:' in attribute:
							ad_file.next();
							ad_file.next();
							model = ad_file.next();
							model = model.replace("\t","")
							model = model.replace(" ","")
							model = model.replace("</a>","")
							model = model.replace("\n","")
							print "Model = " + model
						if 'Year:' in attribute:
							ad_file.next();
							year = ad_file.next();
							year = year.replace("\t","")
							year = year.replace(" ","")
							year = year.replace("</strong>","")
							year = year.replace("\n","")
							print "Year = " + year
						if 'KM Driven:' in attribute:
							ad_file.next();
							km_driven = ad_file.next();
							km_driven = km_driven.replace("\t","")
							km_driven = km_driven.replace(" ","")
							km_driven = km_driven.replace("</strong>","")
							km_driven = km_driven.replace("\n","")
							print "KM_Driven = "+ km_driven
			adCount = adCount + 1
			csv_line = '"'+title+'",' + '"'+model+'",' + '"'+brand+'",' + '"'+year+'",' + '"'+fuel+'",' + '"'+price+'",' + '"'+km_driven+'",' + '"'+description+'",' + '"'+URL+'"\n'
			csv_pointer.write(csv_line)
