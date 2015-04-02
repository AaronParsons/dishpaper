import numpy as n, scipy as s, pylab as p
import glob
'''
Plot csv files spectrum in different frequency range as catagorized into directories
throughout the night of observing
to indentify quiet regions
changes color darkness as a function of time
'''

csv_120130 = glob.glob('../Data/June 20/120-130/*.CSV')
print csv_120130

csv_155160 = glob.glob('../Data/June 20/155-160/*.CSV')
print csv_155160


csv_165175 = glob.glob('../Data/June 20/165-175/*.CSV')
print csv_165175

blues = p.get_cmap('Blues')
reds = p.get_cmap('Reds')


#for i, fname in enumerate(csv_155160):
#	data = n.loadtxt(fname, skiprows=15, delimiter=',', usecols=(0,1))
#	freq_MHz = data[:,0]/1.e6
#	db = data[:,1]
#	color_b = blues(float(i)/(len(csv_155160)-1))
#	p.plot(freq_MHz, db, color=color_b)
#p.title('HERA Spectrum from 155MHz - 160MHz')

#for i, fname in enumerate(csv_120130):
#	data2 = n.loadtxt(fname, skiprows=15, delimiter=',', usecols=(0,1))
#	freq_MHz2 = data2[:,0]/1.e6
#	db2 = data2[:,1]
#	color_r = reds(float(i)/(len(csv_120130)-1))
#	p.plot(freq_MHz2, db2, color=color_r)
#p.title('HERA Spectrum from 120MHz - 130MHz')

for i, fname in enumerate(csv_165175):
	data3 = n.loadtxt(fname, skiprows=15, delimiter=',', usecols=(0,1))
	freq_MHz3 = data3[:,0]/1.e6
	db3 = data3[:,1]
	color_r = reds(float(i)/(len(csv_165175)-1))
	p.plot(freq_MHz3, db3, color=color_r)
p.title('HERA Spectrum from 165MHz - 175MHz')



#p.plot(freq_MHz, data[:,1], label='100-200' )
#p.plot(data2[:,0]/1.e6, data2[:,1], label='120-130' )
#p.plot(data3[:,0]/1.e6, data3[:,1], label='155-160' )
#print n.compress(n.abs(data3[:,0]/1.e6 - 157.0) < 0.5, data3[:,1])
#p.plot(data4[:,0]/1.e6, data4[:,1], label='165-175' )
p.xlabel('Freq MHz')
p.ylabel('dBm')
p.grid()
#p.legend(loc='best')
#p.xticks(n.arange(min(freq_MHz), max(freq_MHz)+1, 10.0))
#p.title('HERA Spectrum from 100MHz - 200MHz, June 19')
p.show()
