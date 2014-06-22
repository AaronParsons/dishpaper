'''
to use:
run CygnusA_today in python
returns az, alt now, rise and set-- time and az, transit time and alt, LST of now
'''


import CygnusA_info, datetime, matplotlib

utc_today_tuple, local_today = CygnusA_info.local2UTC()

coordinates_now, transit_time_today, \
		transit_alt, rise_time_today, \
		rise_az_today, set_time_on_today, \
		set_az_today, LST_now = CygnusA_info.time2angle(utc_today_tuple)

#print coordinates_now, transit_time_today, transit_alt, \
#	rise_time_today, rise_az_today, \
#	set_time_on_today, set_az_today, LST_now


LST = datetime.datetime.strptime(str(LST_now), '%H:%M:%S.%f')
print 'Local Sidereal time: %s' %(LST.time())
#LST_dum = matplotlib.dates.date2num(LST)
#print LST_dum

