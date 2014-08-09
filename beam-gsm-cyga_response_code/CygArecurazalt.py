'''
First calculate the rise time for CygA on the given date
starting from that rise time, compute the az, alt in ep.degree
complete a list of az, alt from rise to set in str 
'''

import CygA_func as Cyg
import os, sys
import ephem as ep
from pytz import datetime
import pylab as p
import numpy as n
import math

def utc2local(epdate):
	'''
	Convert utc time to local time in ep.date
	'''
	return ep.localtime(epdate)

def epdate2datime(epdate):
	'''
	Convert ep.date to datetime.datetime
	'''
	return epdate.datetime()

def utcdatetime2tuple(utcdatetime):
	'''
	convert utc time in python datetime format
	output UTC in tuple format for ephem
	'''	
	utc_yr = int(utcdatetime.strftime("%Y"))
	utc_month = int(utcdatetime.strftime("%m"))
	utc_date = int(utcdatetime.strftime("%d"))
	utc_hr = int(utcdatetime.strftime("%H"))
	utc_minute = int(utcdatetime.strftime("%M"))
	utc_sec = int(utcdatetime.strftime("%S"))
	utc_tuple = (utc_yr, utc_month, utc_date, utc_hr, utc_minute, utc_sec)    # to work with ephem
	return utc_tuple

def add15(last_compute_time, interval=15):
	'''
	last_compute_time is datetime.datetime
	every default = 15 minutes
	starting from rise till set
	next is datetime.datetime
	'''
	diff_sec = interval * 60.
	next = last_compute_time + datetime.timedelta(0,15*60.)
	return next

def addls(new_item, a_list=None):
    if a_list is None:
        a_list = []
    a_list.append(new_item)
    return a_list

def listazalt(datetime):
	'''
	input: specified format date string
	return: az list and alt list from rise through set 
	str element
	'''
	#get rise, set time for the input date
	datetime_fmt = Cyg.format_input(datetime)
	utc, local = Cyg.local2UTC(localtime=datetime_fmt)
	Cyginfo, observer = Cyg.time2obj(utc)
	rise_utc, set_time_utc = Cyg.get_riseset(Cyginfo)    # ep.date format
	
	rise_datetime = epdate2datime(rise_utc)
	print "Rise: ", rise_datetime
	set_datetime = epdate2datime(set_time_utc)
	print "set: ", set_datetime

	#get az, alt at rise time
	riseutc_tuple = utcdatetime2tuple(rise_datetime)    # datetime.datetime utc
	Cyginfo_atrise, observer_atrise = Cyg.time2obj(riseutc_tuple)
	az_rise, alt_rise = Cyg.get_azalt(Cyginfo_atrise)    # ep.angle 00:00:00
	LST_atrise = Cyg.get_sidereal(observer_atrise)
	print "rise az", az_rise
	print "Alt", alt_rise
	print "LST ", LST_atrise

	az_ls = addls(repr(az_rise))    # str
	alt_ls = addls(repr(alt_rise))    # str
	LST_ls = addls(LST_atrise)    # math.degrees [hours]

	next = add15(rise_datetime)    # datetime.datetime

	while next <= set_datetime:
		utc_tuple = utcdatetime2tuple(next)
		Cyginfo_next, observer_next = Cyg.time2obj(utc_tuple)
		az, alt = Cyg.get_azalt(Cyginfo_next)
		LST = Cyg.get_sidereal(observer_next)
	#	print utc2local((ep.date(next)))
		az_ls = addls(repr(az), az_ls)
		alt_ls = addls(repr(alt), alt_ls)
		LST_ls = addls(LST, LST_ls)

		next = add15(next)
	az_ls = [math.degrees(float(i)) for i in az_ls]
	alt_ls = [math.degrees(float(i)) for i in alt_ls]
	return az_ls, alt_ls, LST_ls    # lists of floats for az, alt; math.degrees[hours] for LST

