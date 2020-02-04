#!/usr/bin/env python3
# -- In the name of god --
# Project : massspring (mass+spring)
# Author : Pooya.Sh.K 
# Inspired by Saeed Sarkarati

"""
massspring

using this library you can create great
simulations of most of physical environments
which can be calculated presizely.
you can create many types of objects from which
"mass" and "spring" are main ones.
"""

import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'
import pygame, sys, warnings
from math import *

# vairables
# physical variables
dt  = .001 # delta time -> time difference between two sections; measured in seconds
G   = 6.67384e-11 # newtonian constant of gravitation; measured in m^3*kg^-1*s^-2 or N*m^2*kg^-2 where m is meters, kg is kilograms, s is seconds, N is newtons
e0 = 8.854187817e-12 # vacuum permittivity; measured in m^-2*N^-1*C^2 where m is meters, N is newton, C is coulomb
k = 1/(4*pi*e0) # coulomb constant(electrostatic constant); measured in m^2*N*C^-2 where m is meters, N is newton, C is coulomb
Cd  = .47 # drag coefficient -> 0.47 for sphere; non-united
da = 1.2 # ro -> density of air; measured in kg*m^-3 where kg is kilograms, m is meters
ax0 = 0 # acceleration in x direction; measured in m*s^-2 where m is meters, s is seconds
ay0 = 0 # acceleration in y direction; measured in m*s^-2 where m is meters, s is seconds
az0 = 0 # acceleration in z direction; measured in m*s^-2 where m is meters, s is seconds
ge = 9.8 # earth's gravity acceleration; measured in m*s^-2

# programming variables
mass_lis   = [] # list of all masses
spring_lis = [] # list of all springs
gravity_lis = [] # list of all gravity forces
electricity_lis = [] # list of all electricity forces
collision_lis = [] # list of all possible collisions made by masses
same_pos_warn_message = "Objects %s and %s with indexes of %d and %d in the list mass_lis are at the same position"
sp = "spring"
el = "electricity"
gv = "gravity"
cl = "collision"


# graphical variables
WINW = 600 # window width  (_)
WINH = 600 # window height (|)
WIND = 600 # window depth  (.)
x0 = WINW/2 # the graphical x of the 0 point
y0 = WINH/2 # the graphical y of the 0 point
z0 = WIND/2 # the graphical z of the 0 point

# colors
#				= ( R ,  G ,  B )
WHITE			= (255, 255, 255)
SMOKE			= (225, 224, 224)
DARK_SMOKE		= (192, 192, 192)
SILVER			= (157, 157, 157)
GREY			= (128, 128, 128)
GRAY			= GREY
BLUE_GREY		= ( 94, 124, 139)
BLUE_GRAY		= BLUE_GREY
BLACK			= (  0,   0,   0)

DARK_RED		= (128,   0,   0)
PURE_RED		= (255,   0,   0)
RED				= (246,  64,  44)

PINK			= (235,  19,  96)
PURE_PINK		= (255,   0, 128)
ROSE			= (246,  39, 157)

MAGENTA			= (255,   0, 255)
VIOLET			= (238, 130, 239)
PURPLE			= (156,  26, 177)
PURE_PURPLE		= (128,   0, 128)
DARK_PURPLE		= (102,  51, 185)

INDEGO			= ( 61,  76, 183)
DARK_BLUE		= (  0,   0, 128)
NAVY			= DARK_BLUE
BLUE			= ( 15, 147, 245)
PURE_BLUE		= (  0,   0, 255)
WATER			= (  0, 166, 246)
SKY				= (140, 220, 250)

PURE_CYAN		= (  0, 255, 255)
AQUA			= PURE_CYAN
CYAN			= (  0, 187, 213)
TEAL			= (  0, 149, 135)
DARK_CYAN		= (  0, 128, 128)

DARK_GREEN		= (  0, 128,   0)
GREEN			= ( 70, 175,  74)
GRASS			= (136, 196,  64)
PURE_GREEN		= (  0, 255,   0)

OLIVE			= (128, 128,   0)
LIME			= (204, 221,  30)
YELLOW			= (255, 236,  22)
PURE_YELLOW		= (255, 255,   0)

GOLD			= (252, 214,   3)
PURE_ORANGE		= (255, 192,   0)
AMBER			= PURE_ORANGE
ORANGE			= (255, 151,   0)
DARK_ORANGE		= (255,  85,   3)

BROWN			= (121,  84,  70)
LIGHT_CHOCOLATE	= (133,  85,  56)
PURE_BROWN		= (128,  64,   0)
CHOCOLATE		= (105,  58,  42)
DARK_CHOCOLATE	= ( 72,  51,  50)
WHITE_CHOCOLATE	= (234, 225, 201)


# functions
def hypot3d(x, y, z):
	return sqrt(x**2 + y**2 + z**2)

def sign(x):
	return int(copysign(1, x))

def warn_same_pos(m1, m2):
	warnings.warn(SamePosition(
	same_pos_warn_message%
	(m1, m2, m1._index(), m2._index())))

# Exceptions
class ZeroMass(Exception):
	pass

class ZeroRadius(Exception):
	pass

class NegativeMass(Exception):
	pass

class NonElectricalConductive(Exception):
	pass

# Warnings
class SamePosition(Warning):
	pass

# objects
# mass
class mass(object):
	def __init__(self,
		x=0, y=0, z=0, vx=0, vy=0, vz=0,
		m=1, r=1, q=0,
		moveable=True, solid=True, bound=True, gravitateable=False, resistable=False, electrical=False, conductive=False,
		color=(255, 255, 255), visible=True):
		"""
		x, y, z are the object's position | vx, vy, vz are the object's velocity
		m is mass | r is radius | q is electrical charge
		moveable means if the object can move or not
		solid means if the object can hit other objects or not
		bound means if the object stays in the screen or not
		gravitateable means if the object is affected by gravity force or not
		resistable means if the object is affected by air resistance force or not
		electrical means if the object is affected by other electrical objects' electrical force and can affect them by electrical force or not
		conductive means if the object will share electrical charge with others or not
		color is the objects default color | visible means if the object is seen or not
		"""
		if m == 0:
			raise ZeroMass("Can't produce an object with zero mass")
		if m < 0:
			raise NegativeMass("Can't produce an object with negative mass : %d"%m)
		if r == 0:
			raise ZeroRadius("Can't produce an object with zero radius")
		if not electrical and conductive:
			raise NonElectricalConductive("Not electrical but conductive")
		self.x = x
		self.y = y
		self.z = z
		self.vx = vx
		self.vy = vy
		self.vz = vz
		self.fx = 0
		self.fy = 0
		self.fz = 0
		self.m = m
		self.r = r
		self.q = q
		self.moveable = moveable
		self.solid = solid
		self.bound = bound
		self.gravitateable = gravitateable
		self.resistable = resistable
		self.electrical = electrical
		self.conductive = conductive
		self.color = color
		self.visible = visible
		mass_lis.append(self)

	def _index(self):
		""" returns the index of the object in the mass_lis """
		for i, mass in enumerate(mass_lis):
			if mass == self:
				return i

	def __del__(self):
		""" deletes the mass and removes it from mass list """
		try:
			mass_lis.pop(self._index())
		except Exception as e:
			print("[!] Error when deleting : "+str(e))

	def v(self):
		""" returns the velocity of the object """
		return hypot3d(self.vx, self.vy, self.vz)

	def ax(self):
		""" returns the acceleration in direction of x """
		return self.vx / dt

	def ay(self):
		""" returns the acceleration in direction of y """
		return self.vy / dt

	def az(self):
		""" returns the acceleration in direction of z """
		return self.vz / dt

	def a(self):
		""" returns the acceleration """
		ax = self.ax()
		ay = self.ay()
		az = self.az()
		return hypot3d(ax, ay, az), ax, ay, az

	def A(self):
		""" returns the cross sectional area of the object assumed as sphere -> cross sectional area is a circle, the circle's area is pi*r^2 """
		return pi*self.r**2

	def f(self):
		""" returns the force of the object from all directions """
		return hypot3d(self.fx, self.fy, self.fz)

	def force(self):
		""" returns the force of the object according to newtons second law f=ma """
		return self.m * self.a()[0]

	def air_resistance_force(self):
		""" returns the force that is entered to the object because of air resistance according to f = p*v^2*C*A/2 """
		return da*self.v()**2*Cd*self.A()/2

	def empty_forces(self):
		""" sets the objects forces to 0 """
		self.fx, self.fy, self.fz = 0, 0, 0

	def set_air_resistance_force(self):
		""" sets the air resistance force to the object """
		if self.resistable:
			f = self.air_resistance_force()
			v = self.v()
			if v == 0:
				return
			fx = f * self.vx / v
			fy = f * self.vy / v
			fz = f * self.vz / v
			self.fx -= fx
			self.fy -= fy
			self.fz -= fz

	def reflect(self):
		""" reflects the object if it hits the walls """
		if self.bound:
			if not (-WINW//2+self.r < self.x < WINW//2-self.r):
				self.vx *= -1
			if not (-WINH//2+self.r < self.y < WINH//2-self.r):
				self.vy *= -1
			if not (-WIND//2+self.r < self.z < WIND//2-self.r):
				self.vz *= -1

	def move(self):
		""" moves the object according to newtons second law -> f = ma => a = f/m """
		if self.moveable:
			ax, ay, az = self.fx/self.m, self.fy/self.m, self.fz/self.m # attention! self.ax(), self.ay() and self.az() are calculated by vx/dt, vy/dt and vz/dt
			ax += ax0
			ay += ay0
			az += az0
			self.vx += ax*dt
			self.vy += ay*dt
			self.vz += az*dt
			self.x  += self.vx*dt
			self.y  += self.vy*dt
			self.z  += self.vz*dt

	def show_pos_xy(self):
		""" returns the position of the mass on the screen (just x and y) """
		return int(x0+self.x), int(y0-self.y)

	def show_pos_zy(self):
		""" returns the position of the mass on the screen (just z and y) """
		return int(z0+self.z), int(y0-self.y)

	def show_color(self):
		""" returns the color of the drawn circle on the screen
		it can be different from the mass radius depending on mass.z """
		if not self.bound:
			return self.color
		r, g, b = self.color
		x = (WIND+self.z) / (2 * WIND)
		r = int(abs(r * x))
		g = int(abs(g * x))
		b = int(abs(b * x))
		return r, g, b

	def show_xy(self, win):
		""" draws the mass on the screen (x and y dimensions) """
		if self.visible:
			pygame.draw.circle(win, self.show_color(), self.show_pos_xy(), self.r)

	def show_zy(self, win):
		""" draws the mass on the screen (z and y dimensions) """
		if self.visible:
			pygame.draw.circle(win, self.show_color(), self.show_pos_zy(), self.r)

	def show(self, win_xy, win_zy):
		""" draws the mass on the screen """
		if self.visible:
			self.show_xy(win_xy)
			self.show_zy(win_zy)

class force(object):
	def __init__(self, m1 : mass, m2 : mass, name : str, object_list : list):
		assert type(m2) == type(m1) == mass, TypeError(f"can't set {name} force to objects of type {type(m1)} and {type(m2)}\nthey must be from type 'mass'")
		assert type(object_list) == list, TypeError("object list must be from type 'list'")
		self.m1 = m1
		self.m2 = m2
		self.name = name
		self.object_list = object_list
		self.object_list.append(self)

	def _index(self):
		for i, f in enumerate(self.object_list):
			if f == self:
				return i
		return -1

	def __del__(self):
		try:
			self.object_list.pop(self._index())
		except Exception as e:
			print("[!] Error when deleting : "+str(e))

	def dx(self):
		""" returns the delta x of first object and second object """
		return self.m1.x - self.m2.x

	def dy(self):
		""" returns the delta y of first object and second object """
		return self.m1.y - self.m2.y

	def dz(self):
		""" returns the delta z of first object and second object """
		return self.m1.z - self.m2.z

	def d(self):
		""" returns the distance between first object and second object and delta x, y, z """
		dx = self.dx()
		dy = self.dy()
		dz = self.dz()
		return hypot3d(dx, dy, dz), dx, dy, dz

	def h(self):
		""" just returns the distance between first object and second object """
		return self.d()[0]

class spring(force):
	def __init__(self, m1 : mass, m2 : mass, k=1, l=0, color=(255, 255, 255), visible=True):
		force.__init__(self, m1, m2, sp, spring_lis)
		self.k = k
		self.l = l
		if l == 0:
			self.l = self.length()
		self.color = color
		self.visible = visible

	def length(self):
		return self.h()

	def force(self):
		return -self.k*(self.length()-self.l)

	def set_forces(self):
		f = self.force()
		l = self.length()
		if l == 0:
			warn_same_pos(self.m1, self.m2)
			return 0
		m1 = self.m1
		m2 = self.m2
		_, dx, dy, dz = self.d()
		m1.fx += f*(dx)/l
		m1.fy += f*(dy)/l
		m1.fz += f*(dz)/l
		m2.fx += f*(-dx)/l
		m2.fy += f*(-dy)/l
		m2.fz += f*(-dz)/l

	def show_xy(self, win):
		pygame.draw.line(win, self.color, self.m1.show_pos_xy(), self.m2.show_pos_xy())

	def show_zy(self, win):
		pygame.draw.line(win, self.color, self.m1.show_pos_zy(), self.m2.show_pos_zy())

	def show(self, win_xy, win_zy):
		if self.visible:
			self.show_xy(win_xy)
			self.show_zy(win_zy)

class gravity(force):
	def __init__(self, m1 : mass, m2 : mass):
		force.__init__(self, m1, m2, gv, gravity_lis)

	def get_force(self):
		""" returns the force that two objects enter each other as gravity force according to f = G.m1.m2/r^2 """
		h = self.h()
		if h == 0:
			warn_same_pos(self.m1, self.m2)
			return 0
		return (G*self.m1.m*self.m2.m)/(h**2)

	def set_force(self):
		""" sets the gravity force to the object and its gravital pair """
		f = self.get_force()
		d, dx, dy, dz = self.d()
		if d == 0: return 0
		fx = f * dx / d
		fy = f * dy / d
		fz = f * dz / d
		self.m1.fx -= fx
		self.m1.fy -= fy
		self.m1.fz -= fz
		self.m2.fx += fx
		self.m2.fy += fy
		self.m2.fz += fz

class electricity(force):
	def __init__(self, m1 : mass, m2 : mass):
		force.__init__(self, m1, m2, el, electricity_lis)

	def get_force(self):
		""" returns the electricity force that two charged objects enter each other according to f = k.q1.q2/r^2 """
		h = self.h()
		if h == 0:
			warn_same_pos(self.m1, self.m2)
			return 0
		return k*abs(self.m1.q*self.m2.q)/h**2

	def re(self):
		""" returns the side of the electrical force """
		return 1 if sign(self.m1.q) == sign(self.m2.q) else -1

	def set_force(self):
		""" sets the electrical force to the object and its electrical pair """
		f = self.get_force()
		d, dx, dy, dz = self.d()
		if d == 0: return 0
		re = self.re()
		fx = f * dx / d * re
		fy = f * dy / d * re
		fz = f * dz / d * re
		self.m1.fx += fx
		self.m1.fy += fy
		self.m1.fz += fz
		self.m2.fx -= fx
		self.m2.fy -= fy
		self.m2.fz -= fz

	def equalise_charge(self):
		if self.m1.conductive and self.m2.conductive:
			q = (self.m1.q + self.m2.q) / 2
			self.q = q
			self.m2.q = q

class collision(force):
	def __init__(self, m1 : mass, m2 : mass):
		force.__init__(self, m1, m2, cl, collision_lis)

	def check_collision(self):
		""" checks if two objects are collided or not """
		h = self.h()
		if h <= self.m1.r + self.m2.r:
			return True
		return False

	def collide(self):
		""" collides two objects """
		if self.check_collision():
			d, dx, dy, dz = self.d()

			if d == 0:
				warn_same_pos(self.m1, self.m2)
				return 0

			# m1.v1 + m2.v2 = m1.u1 + m2.u2
			# (m1.v1^2) / 2 + (m2.v2^2)/2 = (m1.u1^2) / 2 + (m2.u2^2) / 2
			# => u1 = ? -> x
			# => u2 = ? -> y

			# m = self.m1.m
			# n = self.m2.m
			# v = self.m1.v()
			# u = self.m2.v()
			# y = (-m*u + 2*m*v + n*u) / (m + n)
			# x = (-n*v + 2*n*u + m*v) / (m + n)

			# self.m1.vx += dv1 * dx / d
			# self.m1.vy += dv1 * dy / d
			# self.m1.vz += dv1 * dz / d

			# self.m2.vx += dv2 * -dx / d
			# self.m2.vy += dv2 * -dy / d
			# self.m2.vz += dv2 * -dz / d

			# equalising the electircal charge between two masses

			electricity.equalise_charge(self)

def create_all_collisions():
	for i, m1 in enumerate(mass_lis):
		for _, m2 in enumerate(mass_lis[i+1:]):
			if m1.solid and m2.solid:
				collision(m1, m2)

def create_all_gravities():
	for i, m1 in enumerate(mass_lis):
		for _, m2 in enumerate(mass_lis[i+1:]):
			if m1.gravitateable and m2.gravitateable:
				gravity(m1, m2)

def create_all_electricities():
	for i, m1 in enumerate(mass_lis):
		for _, m2 in enumerate(mass_lis[i+1:]):
			if m1.electrical and m2.electrical:
				electricity(m1, m2)

def empty_all_forces():
	for m in mass_lis:
		m.empty_forces()

def set_all_spring_forces():
	for s in spring_lis:
		s.set_forces()

def collide_all():
	for col in collision_lis:
		col.collide()

def set_all_gravity_forces():
	for gra in gravity_lis:
		gra.set_force()

def set_all_electricity_forces():
	for ele in electricity_lis:
		ele.set_force()

def set_all_air_resistance_forces():
	for m in mass_lis:
		m.set_air_resistance_force()

def set_all_forces():
	set_all_spring_forces()
	set_all_gravity_forces()
	set_all_electricity_forces()
	set_all_air_resistance_forces()

def reflect_all():
	for m in mass_lis:
		m.reflect()

def move_all():
	for m in mass_lis:
		m.move()

def initialize():
	create_all_collisions()
	create_all_gravities()
	create_all_electricities()

def update():
	empty_all_forces()
	reflect_all()
	collide_all()
	set_all_forces()
	move_all()

def sort_by_z():
	global mass_lis
	mass_lis = list( sorted ( mass_lis, key=lambda x: x.z, reverse=True ) )

def show_all_masses(win_xy, win_zy):
	sort_by_z()
	for m in mass_lis:
		m.show(win_xy, win_zy)

def show_all_springs(win_xy, win_zy):
	for s in spring_lis:
		s.show(win_xy, win_zy)

def show_all(win_xy, win_zy):
	show_all_masses(win_xy, win_zy)
	show_all_springs(win_xy, win_zy)

def display(DISPLAYSURF, win_xy, win_zy):
	DISPLAYSURF.fill((0, 0, 0))
	win_xy.fill((0, 0, 0))
	win_zy.fill((0, 0, 0))
	show_all(win_xy, win_zy)
	DISPLAYSURF.blit(win_xy, (0, 0))
	DISPLAYSURF.blit(win_zy, (WINW+1, 0))
	pygame.draw.line(DISPLAYSURF, (255, 0, 0), (WINW, 0), (WINW, WINH))

def mainloop(speed=2, FPS=0, frame=None, *args):
	DISPLAYSURF = pygame.display.set_mode((WINW*2+1, WINH))
	win_xy = pygame.surface.Surface((WINW, WINH))
	win_zy = pygame.surface.Surface((WINW, WINH))
	c = 0
	spa = 1
	updating = True
	initialize()
	while True:
		c += spa
		for e in pygame.event.get():
			if e.type == pygame.QUIT:
				pygame.quit()
				return 0
			elif e.type == pygame.KEYDOWN:
				if e.key == pygame.K_SPACE:
					updating = not updating
				elif e.key == pygame.K_ESCAPE:
					pygame.quit()
					return 0
			elif e.type == pygame.MOUSEBUTTONDOWN:
				updating = not updating
		if FPS!=0:
			pygame.time.Clock().tick(FPS)
		if updating: 
			update()
			if frame is not None:
				frame(*args)
		if c%speed == 0:
			display(DISPLAYSURF, win_xy, win_zy)
			pygame.display.update()