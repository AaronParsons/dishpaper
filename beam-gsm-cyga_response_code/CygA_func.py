'''
astronomical object by default is Cygnus A, see function time2angle 
ephem always takes in and produce result in UTC
Input:
Enter a date in datetime format
Returns: 
rise time and set time and list of az, alt
'''

import ephem as ep, numpy as n
from pytz import timezone, datetime
import pytz, math

def format_input(usr_input):
	'''
	user input a date in YYYY-MM-DD format
	'''
	d_local2utc = datetime.datetime.strptime(usr_input, "%Y-%m-%d")
	return d_local2utc

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


def time2obj(venue):
	'''
	Cygnus A RA: 19h 59m 28.3566s
	Cygnus A Dec: +40 deg 44' 02.096"

	At Carl's using http://www.latlong.net/convert-address-to-lat-long.html
	37.980012 deg lat
	-122.185800 deg long

	venue format is tuple utc
	return: obj, observer
	'''
	HERA = ep.Observer()
	HERA.long =  ep.degrees('-122.185800')
	HERA.lat = ep.degrees('37.980012')
	HERA.date = venue
	HERA.epoch = ep.date(venue)

	astro_obj = ep.FixedBody()
	astro_obj._ra = ep.hours('19:59:28.3566')
	astro_obj._dec = ep.degrees('40:44:02.096')
	astro_obj.compute(HERA)
	return astro_obj, HERA

#def epfmt2deg(ep_attribute):
#	return ep.degrees(ep_attribute)

def get_azalt(obj):
	az_deg = ep.degrees(obj.az)
	alt_deg = ep.degrees(obj.alt)
	return az_deg, alt_deg

def get_riseset(obj):
	'''
	A bug in the Pyephem that sometimes set precede rise
	In [13]: run CygArecurazalt.py 2014-04-06
	2014-04-05 23:16:29.000005 2014-04-05 17:06:10.000005 <<local time

	In [14]: run CygArecurazalt.py 2014-04-07
	2014-04-06 23:12:33.000006 2014-04-07 16:58:22 << local time
	

	SOLUTION: add the if statement in this function to force set time > rise time
	'''
	rise_t = obj.rise_time
	set_t = obj.set_time
	if set_t < rise_t:
		set_t = ep.Date(set_t + 1)
		set_t = ep.Date(set_t + ep.minute * -4.)
	#rise_az = ep.degrees(obj.rise_az)
	#set_az = ep.degrees(obj.set_az)
	return rise_t, set_t


def get_transit(obj):
	trans_t = ep.localtime(obj.transit_time)
	trans_alt = ep.degrees(bj.transit_alt)
	return trans_t, trans_alt

def get_sidereal(obs):
	'''
	compute the LST of the at a given date and time of a location
	convert to python math.degrees format i.e. display as hours
	'''
	sidereal_time = obs.sidereal_time()
#	LST_radian_str = repr(sidereal_time)
#	lst_plot = math.degrees(float(LST_radian_str))/15.
	lst_plot = math.degrees(sidereal_time)/15.
	return lst_plot
