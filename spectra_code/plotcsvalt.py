'''
takes directory to csv
loop through csv files in a directory for the same night, 
differ by some minute interval
and plot the power vs altitude at different time
'''

import CygnusA_info, numpy as n, pylab as p, ephem as ep, math
import glob, sys, os



def csv2power(csvfile):
	'''
	read in the csv in string for time and date
	read in the csv another time in float for actual data
	compute the sum of the power
	'''
	data_str = n.loadtxt(csvfile, delimiter=',', dtype=str)
	data_time = data_str[0,0]     # data and time in string
	data_float = n.loadtxt(csvfile, delimiter=',', usecols=(0,1), skiprows=15)
	freq, amp_db = data_float[:,0], data_float[:,1]     # freq in Hz, dBm
	power_rat = 10. ** (amp_db/10.)
	power_sum = sum(power_rat)    # perhaps improve by choosing a quiet region?
	return power_sum, data_time



def time2alt(time_of_data):
	'''
	input time_of_data from csv file
	output the alt of the time
	'''
	data_localdate = CygnusA_info.formatdate_time(time_of_data)
	utc_tuple, date_to_observe = CygnusA_info.local2UTC(localtime=data_localdate)
	coordinates_given_time, transit_time, \
	transit_alt, rise_time_on_given_date, rise_az_on_given_date, \
	set_time_on_given_date, set_az_on_given_date, LST_given_time = CygnusA_info.time2angle(utc_tuple)
	return coordinates_given_time[1]    # ephem.angle format


if __name__ == '__main__':
	if len(sys.argv) != 2:
		print "Usage: ", os.path.basename(sys.argv[0]), "'directory containing the csv files'"
		sys.exit(1)

	dirt = sys.argv[1]
	csv_arr = glob.glob(dirt+'/*.CSV')
	for i, fname in enumerate(csv_arr):
		power, time = csv2power(fname)
		alt_radian_str = repr(time2alt(time))
		alt = math.degrees(float(alt_radian_str))     # actual python degree format
		
		blues = p.get_cmap('Blues')
		color_b = blues(float(i)/(len(csv_arr)-1))   # blues(x) returns a color for each x between 0.0 and 1.0
		
		p.plot(alt, power, 'o', color=color_b)
		p.annotate(' '+time, (alt, power))
	p.xlabel('Altitude [deg]')
	p.ylabel('Power [mW]')
	p.title(dirt+'  power VS altitude of CygnusA')
	p.grid()
	p.show()