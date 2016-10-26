#!/usr/bin/env python

from joblib import Parallel, delayed
import math, numpy

num_iter = 24
n = 2.0
resolution = 100
length = 1.1

def check (c):
	p = [0.0, 0.0, 0.0]
	r = norm(c)
	for i in range(num_iter):
		p = triplexPow(p, 8) + c
		if norm(p) > 20:
			return False
	return True

def norm (p):
	x = p[0]
	y = p[1]
	z = p[2]
	return math.sqrt(x*x + y*y + z*z)

def triplexPow (p, n):
	x = p[0]
	y = p[1]
	z = p[2]
	r = norm(p)
	if r == 0.0:
		return 0.0
	theta = n * math.atan2(y, x)
	phi = n * math.asin(z / r)
	sintheta = math.sin(theta)
	cosphi = math.cos(phi)
	sinphi = math.sin(phi)
	return math.pow(r, n) * numpy.array([math.cos(theta) * cosphi, sintheta * cosphi, -sinphi])

def process (x):
	pcd = []
	for y in range(-resolution, resolution):
		for z in range(-resolution, resolution):
			c = length * numpy.array([float(x) / resolution, float(y) / resolution, float(z) / resolution])
			res = check(c)
			# print "check:%s:%s" % (str(c), str(res))
			if res:
				pcd.append((x, y, z))
	return pcd

flag = numpy.zeros([2*resolution, 2*resolution, 2*resolution])
pcd_array = Parallel(n_jobs=-1)( [delayed(process)(x) for x in range(-resolution, resolution)] )
for pcd in pcd_array:
	for p in pcd:
		flag[p[0] + resolution][p[1] + resolution][p[2] + resolution] = 1
		# print "%f,%f,%f" % (p[0], p[1], p[2])
for x in range(-resolution + 1, resolution - 1):
	for y in range(-resolution + 1, resolution - 1):
		for z in range(-resolution + 1, resolution -1):
			xi = x + resolution
			yi = y + resolution
			zi = z + resolution
			if flag[xi][yi][zi] == 1:
				if (flag[xi-1][yi][zi] == 1 and flag[xi+1][yi][zi] == 1 and 
				    flag[xi][yi-1][zi] == 1 and flag[xi][yi+1][zi] == 1 and 
				    flag[xi][yi][zi-1] == 1 and flag[xi][yi][zi+1] == 1):
				    pass
				else:
					p = length * numpy.array([float(x) / resolution, float(y) / resolution, float(z) / resolution])
					print "%f,%f,%f" % (p[0], p[1], p[2])
