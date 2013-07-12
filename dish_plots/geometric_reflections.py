#! /usr/bin/env python
import numpy as n, pylab as p, aipy as a

F = 350.
def parabola(r, f):
    '''Equation of parabolic dish.  Returns z for given r and focal height f, in cm.'''
    return r**2 / (4*f)

def parabola_ring(r, f, angres=.1):
    '''Return points around the ring of a parabola with provided r coordinate 
    with an angular resolution of angres (in radians).'''
    ang = n.arange(0, 2*n.pi, angres)
    x = r*n.cos(ang)
    y = r*n.sin(ang)
    z = parabola(r,f=f) * n.ones_like(x)
    return n.array([x,y,z]).transpose()

def ring_dist(crd, r, f, angres=.1):
    rng = parabola_ring(r, f, angres=angres)
    d = rng - crd
    d = n.sqrt(d[:,0]**2 + d[:,1]**2 + d[:,2]**2)
    return d

def ring_dly(crd, r, f, dlybins, angres=.1):
    'dlyres in nanoseconds'
    d = ring_dist(crd,r,f,angres=angres) / a.const.len_ns
    h,b = n.histogram(d, dlybins)
    return h

dlymax = 1e3
dlyres = 5
bins = n.arange(-dlymax,dlymax+dlyres, dlyres)
bincen = 0.5*(bins[1:] + bins[:-1])

crd = n.array([[0.,0,F]])

dr = 100.
rs = n.arange(0,1400,dr)

#p.plot(rs, parabola(rs,F)); p.show()
#p.plot(rs, [ring_dist(crd,r,F) for r in rs]); p.show()

feed_to_r_coupling = [0.] * len(rs)
for cnt,r in enumerate(rs):
    area = 2*n.pi*r*dr / a.const.len_ns**2 / (2*n.pi/0.1)
    rng_wgt = area / (4*n.pi*bincen**2)
    dly = ring_dly(crd, r, F, bins)
    feed_to_r_coupling[cnt] = dly * rng_wgt
    

feed_state = 1.
new_feed_state = 0.
rstates = [0.] * len(rs)
for cnt,(rstate,r) in enumerate(zip(rstates,rs)):
    new_feed_state += n.convolve(rstate[cnt], feed_to_r_coupling[cnt])
    rstate[cnt] = n.convolve(feed_state, feed_to_r_coupling[cnt])
p.plot(bincen, dly_tot)

p.show()
