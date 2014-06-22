'''
astronomical object by default is Cygnus A, see function time2angle 
ephem always takes in and produce result in UTC
calculate:
the corresponding altitude at the time the CSV file was saved
the transit time, rise, set time and altitude of the object on a given date
'''

import ephem as ep, numpy as n
from pytz import timezone, datetime
import pytz

def formatdate_time(venue_data):
	'''
	trim out date information from csv file date format
	output d_local2utc -> input for local2UTC function format (python datetime type)
	'''
	day = venue_data[1:9]
	time = venue_data[12:]		
	hr = int(time[0:2])
	minute = int(time[3:5])
	sec = int(time[6:8])
	year = int('20'+day[6:8])
	month = int(day[0:2])
	date = int(day[3:5])
	#combine = ((year, month, date, hr, minute, sec))
	d_local2utc = datetime.datetime(year, month, date, hr, minute, sec)    # becomes this fmt 2014-06-16 15:59:18.371930
	return d_local2utc    # , combine

def local2UTC(localtime=datetime.datetime.today(), zone='US/Pacific'):
	'''
	convert local time in python datetime format to UTC before feeding into Pyephem
	default region is Pacific US for Berkeley, CA
	localtime format needs to be same as pytz.datetime.datetime.now() 2014-06-16 15:59:18.371930
	output UTC in tuple format for ephem
	'''	
	tz = timezone(zone)
	d_tz = tz.normalize(tz.localize(localtime))
	utc = pytz.utc
	utc_time = d_tz.astimezone(utc)    # in datetime python type
	utc_yr = int(utc_time.strftime("%Y"))
	utc_month = int(utc_time.strftime("%m"))
	utc_date = int(utc_time.strftime("%d"))
	utc_hr = int(utc_time.strftime("%H"))
	utc_minute = int(utc_time.strftime("%M"))
	utc_sec = int(utc_time.strftime("%S"))
	utc_tuple = (utc_yr, utc_month, utc_date, utc_hr, utc_minute, utc_sec)    # to work with ephem
	return utc_tuple, localtime

def time2angle(venue):
	'''
	Cygnus A RA: 19h 59m 28.3566s
	Cygnus A Dec: +40 deg 44' 02.096"

	At Carl's using http://www.latlong.net/convert-address-to-lat-long.html
	37.980012 deg lat
	-122.185800 deg long

	venue format is tuple
	'''
	HERA = ep.Observer()
	HERA.long =  ep.degrees('-122.185800')
	HERA.lat = ep.degrees('37.980012')
	HERA.date = venue
	HERA.epoch = ep.date(venue)
	sidereal_time = HERA.sidereal_time()
	#print ('Sidereal time:  %s') %str(sidereal_time)

	astro_obj = ep.FixedBody()
	astro_obj._ra = ep.hours('19:59:28.3566')
	astro_obj._dec = ep.degrees('40:44:02.096')
	astro_obj.compute(HERA)

	coordinates_given_time = (ep.degrees(astro_obj.az), ep.degrees(astro_obj.alt))
	transit_time = ep.localtime(astro_obj.transit_time)
	transit_alt = ep.degrees(astro_obj.transit_alt)
	rise_time_on_given_date = ep.localtime(astro_obj.rise_time)
	rise_az_on_given_date = ep.degrees(astro_obj.rise_az)
	set_time_on_given_date = ep.localtime(astro_obj.set_time)
	set_az_on_given_date = ep.degrees(astro_obj.set_az)
	return coordinates_given_time, transit_time, \
		transit_alt, rise_time_on_given_date, rise_az_on_given_date, \
		set_time_on_given_date, set_az_on_given_date, sidereal_time


#===================############################=======================

if __name__ == '__main__':
	data = n.loadtxt('../Data/cyg_a_6.6.2014/TRACE388.csv', delimiter=',', dtype=str)
	data_dateandtime = data[0,0]

	data_localdate = formatdate_time(data_dateandtime)
	utc_tuple, date_to_observe = local2UTC(localtime=data_localdate)
	coordinates_given_time, transit_time, \
		transit_alt, rise_time_on_given_date, \
		rise_az_on_given_date, set_time_on_given_date, \
		set_az_on_given_date, LST = time2angle(utc_tuple)
	print 'The az: %s deg, alt: %s deg of Cygnus A at time (%s) \n' \
		%(coordinates_given_time[0], coordinates_given_time[1], date_to_observe)
	print 'Transit time of Cygnus A: %s, and the alt: %s deg \n' \
		%(transit_time, transit_alt)
	print 'Cygnus A rise time on the given date: %s, and the as: %s deg \n' \
		%(rise_time_on_given_date, rise_az_on_given_date)
	print 'Cygnus A set time on the given date: %s, and the az: %s deg' \
		%(set_time_on_given_date, set_az_on_given_date)
