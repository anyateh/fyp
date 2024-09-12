#!/usr/bin/env python3

import logging
from math   import fabs, log10, pi
from random import uniform
from sys    import argv

class RPI:
	x:float   = 0
	y:float   = 0
	dbm:float = 0

# Returns a tuple minx, miny, maxx, maxy
def create_bounding_box(coords:list|tuple[tuple[float, float]]) -> tuple[float, float, float, float]:
	return min(map(lambda a: a[0], coords)), min(map(lambda a: a[1], coords)), max(map(lambda a: a[0], coords)), max(map(lambda a: a[1], coords))

# Returns a tuple: emitter dBm, dBm_at_r1, dBm_at_r2, dBm_at_r3
def gen_one_emitter(wlength:float, r1:RPI, r2:RPI, r3:RPI) -> tuple[float, float, float]:
	min_x, min_y, max_x, max_y = create_bounding_box([(a.x, a.y) for a in (r1, r2, r3)])
	
	em_x, em_y = uniform(min_x, max_x), uniform(min_y, max_y)

	d1 = fabs(((em_x - r1.x) ** 2 + (em_y - r1.y) ** 2) ** 0.5)
	d2 = fabs(((em_x - r2.x) ** 2 + (em_y - r2.y) ** 2) ** 0.5)
	d3 = fabs(((em_x - r3.x) ** 2 + (em_y - r3.y) ** 2) ** 0.5)

	logging.debug(f"d1 = {d1}m, d2 = {d2}m, d3 = {d3}m")

	r1.dbm = 2 * 10 * log10(wlength / (4 * pi * d1))
	r2.dbm = 2 * 10 * log10(wlength / (4 * pi * d2))
	r3.dbm = 2 * 10 * log10(wlength / (4 * pi * d3))

	return r1.dbm, r2.dbm, r3.dbm

def triangulate_pos(rpi_a_coord:tuple[int, int], rpi_b_coord:tuple[int, int], rpi_c_coord:tuple[int, int]) -> tuple[int, int]:
	pass

def main() -> None:
	logging.basicConfig(level = logging.DEBUG, format = '[%(levelname)s] %(message)s')

	r1, r2, r3 = RPI(), RPI(), RPI()

	r2.x = 0
	r2.y = 50

	r3.x = 50
	r3.y = 0

	wlength = 1 / 500_000_000

	logging.debug("RasPi1: %fdbm, RasPi2: %fdbm, RasPi3: %fdbm" % gen_one_emitter(wlength, r1, r2, r3))

if __name__ == '__main__':
	main()
