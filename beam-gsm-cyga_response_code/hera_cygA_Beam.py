import aipy as a, capo as c, numpy as n, pylab as p
from CygArecurazalt import listazalt
'''
Adjust date for listazalt before running
May need to change path: hera_hmap location for img
May need to change path: gsm fits file lcoation for img_gsm
'''


az_list, alt_list, LST_list = listazalt('2014-07-10')
az_rad = n.deg2rad(az_list)
alt_rad = n.deg2rad(alt_list)

theta_phi_ls = []
for i, j in zip(az_rad, alt_rad):
	thetaphi = (n.pi/2.-j, n.pi/2.-i)    # theta from z-axis, phi is azimuthal angle 
	theta_phi_ls.append(thetaphi)
theta_phi_arr = n.array(theta_phi_ls)


#####======================================######
#####=======interpolate hera beam hmap======######
#####=====================================######
#topocentric pointing up the sky
img = a.map.Map(fromfits = "./hera_0.150.hmap")    # hmap (beam) from Aaron, 150MHz topocentric
img.map.map = 10. ** (img.map.map/10.)    # img.map.map is the value of the healpix, log to lin
img.map.map /= img[0, 0, 1]    # referencing to zenith
px, wgts = img.crd2px(theta_phi_arr[:,0], theta_phi_arr[:,1], interpolate=1)
value = n.sum(img[px] * wgts, axis=1)
p.figure(1)
p.plot(value, label='Coordinates through beam')
p.title('Beam Response at Coordinates of object')
p.ylabel('Linear')

obj_jy = value * 10900    # Jansky
p.figure(2)
p.plot(obj_jy, label='CygA through beam')
p.ylabel('Jansky')

#####=======================================######
#######======GSM at those Coordinates=======######
#####=======================================######
#GSM are in galactic coordinates (l, b), Sun as the origin in the disk or our galaxy
#Eq (Ra, dec) celestial sphere

img_gsm = a.map.Map(fromfits="./gsm_out1005.fits", interp=True)    # galactic
solid_angle = 4. * n.pi / img_gsm.npix()    # gsm pixels over the sky
temp2jy = 2./(2.998e10)**2  * 1.38e-16 * (150.e6)**2 * solid_angle /1.e-23   # cgs to Jansky
img_gsm.map.map *= temp2jy     # Unit conversion

# In order to map the gsm px values in galactic to other coordinate system
crd_ga = img_gsm.px2crd(n.arange(img_gsm.npix()))     # map the pixel to the default coordinate system
ga2eq = a.coord.convert_m('ga', 'eq')   # matrix transformation from galactic to equatorial
crd_eq = n.dot(ga2eq, crd_ga)    # convert ga in gsm to eq

HERA = a.phs.ArrayLocation(('37.980012', '-122.185800'))
#for jd in n.arange(2456853, 2456854, .1):   # 1/10 of a day#
#	HERA.set_jultime(jd)
#	print HERA.date
#	LST = HERA.sidereal_time()

# Eq to Top is time dependent and location on earth dependent
gsm_beam_ls = []
for i, LST in enumerate(LST_list):
	#print i, LST
	LST = LST * n.pi / 12.    # LST_list is in hours, convert to radian
	#print LST
	eq2top = a.coord.eq2top_m(LST, HERA.lat)
	tx, ty, tz = n.dot(eq2top, crd_eq)    # transform eq to top at each LST
	beam_ga = n.where(tz > 0, img[tx, ty, tz], 0)   # n.where(conditionTRUE, TRUE operation, else); to mask out beam value for z<0 such that no sky sources passes through the beam
	print beam_ga
	print
	print img_gsm[n.arange(img_gsm.npix())]   # the values
	gsm_beam = n.sum(beam_ga * img_gsm[n.arange(img_gsm.npix())])
	gsm_beam_ls.append(gsm_beam)

p.plot(gsm_beam_ls, label='gsm at same coordinate')
p.title('GSM beam, CygA response at those CygA coordinates')
p.ylabel('Jy')
p.grid()
p.legend(loc='best')
p.show()










