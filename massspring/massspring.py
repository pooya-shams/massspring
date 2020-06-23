#!/usr/bin/env python3
# -- In the name of God --
# Project: massspring (mass+spring)
# File: massspring.py
# Author: Pooya Shams kolahi
# Inspired by Saeed Sarkarati

"""
massspring

using this library you can create great
simulations of most of physical environments
which can be calculated precisely.
you can create many types of objects from which
"mass" and "spring" are main ones.
"""

import functools
import warnings
from math import hypot, pi

import pygame

import massspring.Exceptions as Exceptions

# variables
# physical constants
# dt is delta time -> time difference between two sections; measured in seconds.
#      value: 0.001
# G is newtonian constant of gravitation; measured in m^3*kg^-1*s^-2 or
#   N*m^2*kg^-2 where m is meters, kg is kilograms, s is seconds, N is newtons.
#       value: 6.67384e-11
# e0 is vacuum permittivity; measured in m^-2*N^-1*C^2 where m is meters,
#   N is newton, C is coulomb.
#       value: 8.854187817e-12
# k is coulomb constant(electrostatic constant); measured in m^2*N*C^-2
#   where m is meters, N is newton, C is coulomb.
#       value: 1 / (4 * pi * e0) = 8987551787.997911
# Cd is drag coefficient -> 0.47 for sphere; non-united
#       value: 0.47
# da is ro -> density of air; measured in kg*m^-3
#   where kg is kilograms, m is meters.
#       value: 1.2
# ge is earth's gravity acceleration; measured in m*s^-2.
#       value: 9.8
# c is speed of light; measured in m/s where m is meters and s is seconds
#   will be used to check if a mass has exceeded speed limit and raise an error
#       value: 299792458

dt = .001
G = 6.67384e-11
# e0 = 8.854187817e-12
k = 8987551787.997911  # 1 / (4 * pi * e0)
Cd = .47
da = 1.2
ge = 9.8
c = 299792458

# programming variables
mass_lis = []  # list of all masses
spring_lis = []  # list of all springs
gravity_lis = []  # list of all gravity forces
electricity_lis = []  # list of all electricity forces
collision_lis = []  # list of all possible collisions made by masses
air_resistance_lis = []  # list of masses having air resistance force enabled
same_pos_warn_message = "Objects %s and %s with indexes of %d and %d in\
 the list mass_lis are at the same position. can't set %s force to them."
ms = "mass"
sp = "spring"
el = "electricity"
gv = "gravity"
cl = "collision"
ar = "air resistance"
INT_MIN = -2147483648  # -2 ** 31
INT_MAX = +2147483647  # 2 ** 31 - 1


# graphical variables
WINW = 600  # window width  (_)
WINH = 600  # window height (|)
WIND = 600  # window depth  (.)


# functions

def sign(x):
    """ returns the sign of x -> -1, 0, 1 """
    if x < 0:
        return -1
    if x > 0:
        return 1
    return 0


def warn_same_pos(m1, m2, name):
    """ warns when two masses are exactly on the same position """
    warnings.warn(Exceptions.SamePosition(
        same_pos_warn_message %
        (m1, m2, m1._index(), m2._index(), name)))


def assert_type_error(*objects, preferred_type=None, name="", msg=""):
    """
    makes sure that all the objects passed
    to the function are of preferred type
    """
    assert all(map(lambda obj: type(obj) == preferred_type, objects)), TypeError(
        f"object {name} -> {objects} should all be of type '{preferred_type}' not '{list(map(type, objects))}'.{msg} ")


def similarity(dx1, dy1, dz1, d1, d2):
    """
    uses the rules of similarity in geometry to calculate lengths
    of edges of a pyramid similar to another pyramid
    """
    dx2 = d2 * dx1 / d1
    dy2 = d2 * dy1 / d1
    dz2 = d2 * dz1 / d1
    return dx2, dy2, dz2


# decorators

def two_object_force(func):
    """
    makes sure that the second object in a force subclass
    is not None so we can return the dx, dy and dz
    """
    @functools.wraps(func)
    def wrapper(self):
        if self.m2 is None:
            return 0
        return func(self)
    return wrapper


# variable holders (namespaces)


class acceleration:
    """
    x, y, z are default acceleration in 3 directions; measured in m*s^-2
    where m is meters, s is seconds.
    """
    x = 0
    y = 0
    z = 0


class position:
    """ x, y, z are default 0 point position in pygame surface """
    x = WINW // 2
    y = WINH // 2
    z = WIND // 2


class limit:
    """ limits for variables and properties of objects """
    class MIN:
        """ the minimums """
        x = INT_MIN
        y = INT_MIN
        z = INT_MIN
        vx = -c
        vy = -c
        vz = -c

    class MAX:
        """ the maximums """
        x = INT_MAX
        y = INT_MAX
        z = INT_MAX
        vx = c
        vy = c
        vz = c
        v = c

# objects(physical meaning) classes
# mass


class mass:
    """
    the main mass object class.
    ALL attributes are available in the __init__ method.
    ALL methods are available in the class.
    no attribute or method will be added
    to objects unless the user adds it to objects.

    parameters / attributes:
    x, y, z are the object's position.
    vx, vy, vz are the object's velocity.
    fx, fy, fz are the sum of forces applied to the object.
        they will be added by calling the set_force method
        in each force's object to the force's masses (m1, m2).
    m is mass of object.
    r is radius of object (each mass is consumed as a sphere).
    q is electrical charge of the object.
    moveable means if the object can move or not.
    solid means if the object can hit other objects or not.
    bound means if the object stays in the screen or not.
    gravitational means if the object is affected by gravity force or not.
    resistible means if the object is
        affected by air resistance force or not.
    electrical means if the object is affected by other objects' electrical
        force and can affect them by electrical force or not.
    conductive means if the object will share
        electrical charge with others or not.
    color is the objects default color.
        visible means if the object is seen or not.
    """

    def __init__(self,
                 x=0, y=0, z=0, vx=0, vy=0, vz=0,
                 m=1, r=1, q=0,
                 moveable=True, solid=True, bound=True, gravitational=False,
                 resistible=False, electrical=False, conductive=False,
                 color=(255, 255, 255), visible=True):
        if m == 0:
            raise Exceptions.ZeroMass("Can't produce an object with zero mass")
        if m < 0:
            raise Exceptions.NegativeMass(
                "Can't produce an object with negative mass : %d" % m)
        if r == 0:
            raise Exceptions.ZeroRadius(
                "Can't produce an object with zero radius")
        if not electrical and conductive:
            raise Exceptions.NonElectricalConductive(
                "Not electrical but conductive")
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
        self.gravitational = gravitational
        self.resistible = resistible
        self.electrical = electrical
        self.conductive = conductive
        self.color = color
        self.visible = visible
        mass_lis.append(self)

    def _index(self):
        """ returns the index of the object in the mass_lis """
        for i, m in enumerate(mass_lis):
            if m == self:
                return i

    def __del__(self):
        """ deletes the mass and removes it from mass list """
        try:
            mass_lis.remove(self)
        except Exception as e:
            print(f"[Error] when deleting {ms}: {e}")

    def v(self):
        """ returns the velocity of the object """
        return hypot(self.vx, self.vy, self.vz)

    def A(self):
        """
        returns the cross sectional area of the object assumed as sphere
        -> cross sectional area is a circle, the circle's area is pi*r^2
        """
        return pi * self.r ** 2

    def f(self):
        """ returns the force of the object from all directions """
        return hypot(self.fx, self.fy, self.fz)

    def empty_forces(self):
        """ sets the objects forces to 0 """
        self.fx, self.fy, self.fz = 0, 0, 0

    def update_forces(self, fx, fy, fz):
        """ adds the given forces to the mass """
        self.fx += fx
        self.fy += fy
        self.fz += fz

    def reflect(self):
        """ reflects the object if it hits the walls """
        # checking if the mass WILL go out of the screen to avoid it.
        if self.bound:
            if not -WINW // 2 + self.r < self.x + self.vx * dt < WINW // 2 - self.r:
                self.vx *= -1
            if not -WINH // 2 + self.r < self.y + self.vy * dt < WINH // 2 - self.r:
                self.vy *= -1
            if not -WIND // 2 + self.r < self.z + self.vz * dt < WIND // 2 - self.r:
                self.vz *= -1

    def check_speed_exceeds_limit(self):
        """
        raises a warning if the mass has reached the speed of light
        in vacuum which is highest speed an object can have.
        """
        tmpv = self.v()
        if tmpv >= limit.MAX.v:  # tmpv is higher than 0
            # the mass has reached the speed of light in vacuum (or MORE)
            warnings.warn(Exceptions.FasterThanSpeedLimitException(
                f"can't go faster than {c}, the speed is {tmpv}"))

    def check_position_exceeds_limit(self):
        """
        raises a warning if the position is
        higher than INT_MAX or lower than INT_MIN
        """
        if not limit.MIN.x < self.x < limit.MAX.x:
            warnings.warn(Exceptions.FurtherThanPositionLimitException(
                f"can't place mass.x out of ({limit.MIN.x},{limit.MAX.x}), x is {self.x}"))
        if not limit.MIN.y < self.y < limit.MAX.y:
            warnings.warn(Exceptions.FurtherThanPositionLimitException(
                f"can't place mass.y out of ({limit.MIN.y},{limit.MAX.y}), y is {self.y}"))
        if not limit.MIN.z < self.z < limit.MAX.z:
            warnings.warn(Exceptions.FurtherThanPositionLimitException(
                f"can't place mass.z out of ({limit.MIN.z},{limit.MAX.z}), z is {self.z}"))

    def move(self):
        """
        moves the object according to
        newtons second law -> f = ma => a = f/m
        """
        if self.moveable:
            # attention! self.ax(), self.ay() and self.az() are
            # calculated by vx/dt, vy/dt and vz/dt
            ax, ay, az = self.fx / self.m, self.fy / self.m, self.fz / self.m
            ax += acceleration.x
            ay += acceleration.y
            az += acceleration.z
            self.vx += ax * dt
            self.vy += ay * dt
            self.vz += az * dt
            self.check_speed_exceeds_limit()
            self.x += self.vx * dt
            self.y += self.vy * dt
            self.z += self.vz * dt
            self.check_position_exceeds_limit()

    def show_pos_xy(self):
        """ returns the position of the mass on the screen (just x and y) """
        return int(position.x + self.x), int(position.y - self.y)

    def show_pos_zy(self):
        """ returns the position of the mass on the screen (just z and y) """
        return int(position.z + self.z), int(position.y - self.y)

    def show_color(self):
        """
        returns the color of the drawn circle on the screen
        it can be different from the mass radius depending on mass.z
        """
        if not self.bound:
            return self.color
        r, g, b = self.color
        x = (WIND + self.z) / (2 * WIND)
        r = int(abs(r * x))
        g = int(abs(g * x))
        b = int(abs(b * x))
        return r, g, b

    def show_xy(self, win):
        """ draws the mass on the screen (x and y dimensions) """
        if self.visible:
            pygame.draw.circle(win, self.show_color(),
                               self.show_pos_xy(), self.r)

    def show_zy(self, win):
        """ draws the mass on the screen (z and y dimensions) """
        if self.visible:
            pygame.draw.circle(win, self.show_color(),
                               self.show_pos_zy(), self.r)

    def show(self, win_xy, win_zy):
        """ draws the mass on the screen """
        if self.visible:
            self.show_xy(win_xy)
            self.show_zy(win_zy)


# Force's classes
# main force

class force:
    """
    the main force class.
    this class is a raw class used to create other classes of forces.
    the subclasses are 'spring', 'gravity', 'electricity', 'collision'
    and air_resistance. since all forces in OUR universe are between
    two objects, the force class has two 'm1' and 'm2' that the force
    occurs between them. However we don't have the second object in some
    forces like air resistance and we just calculate the result of these
    forces on one object so the m2 attribute is set to None in these cases,
    meaning that we don't have any second object and we are just using the
    first one.

    there are two other attributes too:
    1. name: is just a string of the force name which will be used when
    raising exceptions
    2. object_list: is the list containing all of the forces of the same type.

    takes three parameters:
    1. m1: first mass the force will be assigned to.
    2. m2: second mass.
    3. name: is just a string of the force name which will be used when
    raising exceptions
    """
    object_list: list
    name: str

    def __init__(self, *, m1: mass, m2: mass = None):
        if m2 is not None:
            assert_type_error(m1, m2,
                              preferred_type=mass,
                              name="m1 and m2",
                              msg=f"can't set {self.name} force to them.")
        else:
            assert_type_error(m1,
                              preferred_type=mass,
                              name="m1",
                              msg=f"can't set {self.name} force to it.")
        assert_type_error(self.object_list,
                          preferred_type=list,
                          name="object_list",
                          msg=f"can't append a {self.name} force to it.")

        self.m1 = m1
        self.m2 = m2
        # self.name = name
        self.object_list.append(self)

    def __del__(self):
        """ tries to remove the object from it's object_list """
        try:
            self.object_list.remove(self)
        except Exception as e:
            print(f"[Error] when deleting {self.name}: {e}")

    @two_object_force
    def dx(self):
        """ returns the delta x of first object and second object """
        return self.m1.x - self.m2.x

    @two_object_force
    def dy(self):
        """ returns the delta y of first object and second object """
        return self.m1.y - self.m2.y

    @two_object_force
    def dz(self):
        """ returns the delta z of first object and second object """
        return self.m1.z - self.m2.z

    @two_object_force
    def d(self):
        """
        returns the distance between first object
        and second object and delta x, y, z
        """
        dx = self.dx()
        dy = self.dy()
        dz = self.dz()
        d = hypot(dx, dy, dz)
        if d == 0:
            warn_same_pos(self.m1, self.m2, self.name)
        return d, dx, dy, dz

    @two_object_force
    def h(self):
        """
        just returns the distance between
        first object and second object
        """
        return self.d()[0]

# double mass forces
# spring


class spring(force):
    """
    the main spring class derived from force class.
    this force is calculated according to the Hooke's law.
    attributes are:
    m1, m2: the objects between which the force will happen.
    k: is the constant of the spring in the formula of Hookes's law.
    nl: is the natural length of the spring used to
    calculate the delta x in the formula.
    color: the color shown on the screen.
    visible (boolean): indicates if the object
    will be shown on the screen or not.
    """
    object_list = spring_lis
    name = sp

    def __init__(self, m1: mass, m2: mass, k=1,
                 nl=0, color=(255, 255, 255), visible=True):
        super().__init__(m1=m1, m2=m2)
        self.k = k
        self.nl = nl
        if nl == 0:
            self.nl = self.length()
        self.color = color
        self.visible = visible

    def length(self):
        """
        returns the length of object using length
        of the line between two masses (m1 and m2).
        """
        return self.h()

    def get_force(self):
        """ calculates the force which should be applied to the masses. """
        return - self.k * (self.length() - self.nl)

    def set_force(self):
        """ applies the force to the masses. """
        f = self.get_force()
        d, dx, dy, dz = self.d()
        if d == 0:
            return 0
        m1 = self.m1
        m2 = self.m2
        fx, fy, fz = similarity(dx, dy, dz, d, f)
        m1.update_forces(fx, fy, fz)
        m2.update_forces(-fx, -fy, -fz)

    def show_xy(self, win):
        """ method for showing the spring on the screen of x-y coordinates. """
        pygame.draw.line(win, self.color, self.m1.show_pos_xy(),
                         self.m2.show_pos_xy())

    def show_zy(self, win):
        """ method for showing the spring on the screen of z-y coordinates. """
        pygame.draw.line(win, self.color, self.m1.show_pos_zy(),
                         self.m2.show_pos_zy())

    def show(self, win_xy, win_zy):
        """
        gets the win_xy and win_zy, the screens which will be
        shown on the main screen.
        and then calls the show_xy and show_zy methods using them.
        """
        if self.visible:
            self.show_xy(win_xy)
            self.show_zy(win_zy)

# gravity


class gravity(force):
    """
    the main gravity force class.
    uses the newton's law of gravity.
    """
    object_list = gravity_lis
    name = gv

    def __init__(self, m1: mass, m2: mass):
        """
        parameters:
        m1 and m2: masses.
        """
        super().__init__(m1=m1, m2=m2)

    @staticmethod
    def condition(m1: mass, m2: mass):
        return m1.gravitational and m2.gravitational

    def get_force(self):
        """
        returns the force that two objects apply to each other
        as gravity force according to f = G.m1.m2/r^2
        """
        h = self.h()
        if h == 0:
            return 0
        return (G * self.m1.m * self.m2.m) / (h ** 2)

    def set_force(self):
        """ sets the gravity force to the object and its gravitational pair """
        f = self.get_force()
        d, dx, dy, dz = self.d()
        if d == 0:
            return 0
        fx, fy, fz = similarity(dx, dy, dz, d, f)
        self.m1.update_forces(-fx, -fy, -fz)
        self.m2.update_forces(fx, fy, fz)

# electricity


class electricity(force):
    """
    the main electricity force class.
    uses the Coulomb law for calculating
    the electricity force between two particles.
    """
    object_list = electricity_lis
    name = el

    def __init__(self, m1: mass, m2: mass):
        """
        parameters:
        m1 and m2: masses.
        """
        super().__init__(m1=m1, m2=m2)

    @staticmethod
    def condition(m1: mass, m2: mass):
        return m1.electrical and m2.electrical

    def get_force(self):
        """
        returns the electricity force that two charged objects apply to
        each other according to f = k.q1.q2/r^2
        """
        h = self.h()
        if h == 0:
            return 0
        return k * abs(self.m1.q * self.m2.q) / h ** 2

    def re(self):
        """ returns the side of the electrical force """
        return 1 if sign(self.m1.q) == sign(self.m2.q) else -1

    def set_force(self):
        """ sets the electrical force to the object and its electrical pair """
        f = self.get_force()
        d, dx, dy, dz = self.d()
        if d == 0:
            return 0
        re = self.re()
        fx, fy, fz = similarity(dx, dy, dz, d, f)
        fx, fy, fz = fx * re, fy * re, fz * re
        self.m1.update_forces(fx, fy, fz)
        self.m2.update_forces(-fx, -fy, -fz)

    def equalise_charge(self):
        """
        checks if two objects are conductive and then
        equalises the electrical charge between them.
        """
        if self.m1.conductive and self.m2.conductive:
            q = (self.m1.q + self.m2.q) / 2
            self.m1.q = q
            self.m2.q = q

# collision


class collision(force):
    """
    the main collision class
    uses the momentum and kinetic conservation and
    I don't know why it works but according to wikipedia
    the formula and equation are driven from these two equations.
    """
    object_list = collision_lis
    name = cl

    def __init__(self, m1: mass, m2: mass):
        super().__init__(m1=m1, m2=m2)

    @staticmethod
    def condition(m1: mass, m2: mass):
        return m1.solid and m2.solid

    def check_collision(self):
        """ checks if two objects are collided or not """
        h = self.h()
        if h <= self.m1.r + self.m2.r:
            return True
        return False

    def set_force(self):
        """ collides two objects """
        # checking if the objects has collided
        if not self.check_collision():
            return
        # saving variables
        d, dx, dy, dz = self.d()
        if d == 0:
            return 0
        m1 = self.m1.m
        m2 = self.m2.m
        u1x = self.m1.vx
        u1y = self.m1.vy
        u1z = self.m1.vz
        u2x = self.m2.vx
        u2y = self.m2.vy
        u2z = self.m2.vz
        u1 = self.m1.v()
        u2 = self.m2.v()
        # starting collision
        # calculating new velocities
        v1 = (u1 * (m1 - m2) + u2 * 2 * m2) / (m1 + m2)
        v2 = (u2 * (m2 - m1) + u1 * 2 * m1) / (m1 + m2)
        # dividing v to vx, vy, vz
        v1x, v1y, v1z = similarity(dx, dy, dz, d, v1)
        v2x, v2y, v2z = similarity(-dx, -dy, -dz, d, v2)
        # calculating delta v
        dv1x = v1x - u1x
        dv1y = v1y - u1y
        dv1z = v1z - u1z
        dv2x = v2x - u2x
        dv2y = v2y - u2y
        dv2z = v2z - u2z
        # calculating acceleration
        a1x = dv1x / dt
        a1y = dv1y / dt
        a1z = dv1z / dt
        a2x = dv2x / dt
        a2y = dv2y / dt
        a2z = dv2z / dt
        # calculating forces
        fx1, fy1, fz1 = a1x * m1, a1y * m1, a1z * m1
        fx2, fy2, fz2 = a2x * m2, a2y * m2, a2z * m2
        self.m1.update_forces(fx1, fy1, fz1)
        self.m2.update_forces(fx2, fy2, fz2)
        # the collision is done!
        # equalising the electrical charges of two objects
        # (if they are conductive)
        electricity.equalise_charge(self)

# single mass forces
# air resistance


class air_resistance(force):
    """
    air resistance force class
    calculates the air resistance force appled to an object by
    the following formula and applies that force to the object.
    f = (p * v^2 * C * A) / 2
    """
    object_list = air_resistance_lis
    name = ar

    def __init__(self, m1: mass):
        super().__init__(m1=m1)

    @staticmethod
    def condition(m1):
        return m1.resistible

    def get_force(self):
        """
        returns the force that is applied to the object because of
        air resistance according to f = p*v^2*C*A/2
        """
        return da * self.m1.v() ** 2 * Cd * self.m1.A() / 2

    def set_force(self):
        """ sets the air resistance force to the object """
        f = self.get_force()
        v = self.m1.v()
        if v == 0:
            return 0
        fx = -f * self.m1.vx / v
        fy = -f * self.m1.vy / v
        fz = -f * self.m1.vz / v
        self.m1.update_forces(fx, fy, fz)


# other variables
# name of all forces kinds
automated = "automated"
manual = "manual"
one_forced = "one forced"
# lists containing all types of forces from that kind
automated_two_object_forces = [gravity, electricity, collision]
automated_one_object_forces = [air_resistance]
manual_two_object_forces = [spring]
# a dictionary containing them all.
# the keys are the list names and the values are the lists.
all_forces = {
    automated: automated_two_object_forces,
    one_forced: automated_one_object_forces,
    manual: manual_two_object_forces,
}


# other functions


def create_all_automated_forces():
    """
    searches all the masses and creates force objects for
    each pair of the masses that the force applies to them
    """
    for i, m1 in enumerate(mass_lis):
        for _, m2 in enumerate(mass_lis[i + 1:]):
            for f in automated_two_object_forces:
                if f.condition(m1, m2):
                    f(m1, m2)
        for f in automated_one_object_forces:
            if f.condition(m1):
                f(m1)


def empty_all_forces():
    for m in mass_lis:
        m.empty_forces()


def set_all_forces():
    for force_lis in all_forces:
        for f in all_forces[force_lis]:
            for obj in f.object_list:
                obj.set_force()


def reflect_all():
    for m in mass_lis:
        m.reflect()


def move_all():
    for m in mass_lis:
        m.move()


def initialize():
    create_all_automated_forces()


def update():
    empty_all_forces()
    reflect_all()
    set_all_forces()
    move_all()


def sort_by_z():
    global mass_lis
    mass_lis = list(sorted(mass_lis, key=lambda x: x.z, reverse=True))


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

# main loop


def mainloop(speed=2, FPS=0, frame=None, *args, displaying=True):
    assert type(speed) == int, TypeError("speed should be of type 'int'.")
    assert type(FPS) == int, TypeError("FPS should be of type 'int'.")
    assert callable(frame) or frame is None, TypeError(
        "frame should be callable.")
    assert type(displaying) == bool, TypeError(
        "displaying value can be either True or False")
    if displaying:
        DISPLAYSURF = pygame.display.set_mode((WINW * 2 + 1, WINH))
        win_xy = pygame.surface.Surface((WINW, WINH))
        win_zy = pygame.surface.Surface((WINW, WINH))
    frame_number = 0
    frames_passing_speed = 1
    updating = True
    initialize()
    while True:
        if displaying:
            frame_number += frames_passing_speed
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
            if FPS != 0:
                pygame.time.Clock().tick(FPS)
            if frame_number % speed == 0:
                display(DISPLAYSURF, win_xy, win_zy)
                pygame.display.update()
        if updating:
            update()
            if frame is not None:
                frame(*args)
