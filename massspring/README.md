# massspring

## Author : Pooya Shams kolahi

Inspired by Saeed Sarkarati

## Brief

using this library you can create great simulations of most of physical environments which can be calculated precisely. you can create many types of objects from which "mass" and "spring" are main ones.  
more on [project homepage on github](https://github.com/pooya-shams/massspring) and [README](https://github.com/pooya-shams/massspring/blob/master/massspring/README.md)

## license

licensed under MIT License.
you can freely use and modify this package, but please let me know if you are doing something interesting.

## Installation

you can install the package via pip:

```bash
pip install massspring
```

for user-only installation use `--user` switch:

```bash
pip install --user massspring
```

if you have massspring installed and you are wishing to upgrade, you can upgrade via `--upgrade` switch:

```bash
pip install --upgrade massspring
```

all combined:

```bash
pip install --user --upgrade massspring
```

## usage

you can import the library by using the following code (it is recommended to import as m or ms)

```python
import massspring as m
```

### mass

mass is the only type of **object** you can create right now.  
you can create a mass object by using the mass class. you can learn more about the arguments and their usage in the [mass class document](https://github.com/pooya-shams/massspring/blob/master/massspring/massspring.py#mass)

```python
m1 = m.mass(x=0, y=0, z=0, vx=0, vy=0, vz=0, m=10, r=10, q=0, moveable=False, solid=True, bound=True, gravitational=False, resistible=False, electrical=False, conductive=False, color=(0, 255, 0), visible=True)
```

### force

there are four types of forces (technically force subclass) you can create:  
1.gravity  
2.electricity  
3.spring  
4.collision  

#### gravity

the gravity class provides a gravity force between two masses according to the **"Newton's law of universal gravitation"** which you can see bellow:  
![gravity formula](https://raw.githubusercontent.com/pooya-shams/massspring/master/massspring/images/gravity.svg)  
more information is available at [Newton's law of universal gravitation](https://en.wikipedia.org/wiki/Newton%27s_law_of_universal_gravitation) wikipedia page.  
you can create a gravity force between two masses using the code bellow:

```python
g1 = m.gravity(m1=m1, m2=m2)
```

(m1 and m2 are the two mass objects between which you want to set gravity force.)

#### electricity

the electricity class provides an electricity force between two masses according to the **"Coulomb's law"** (the vector version) which you can see bellow:  
![Coulomb's law](https://raw.githubusercontent.com/pooya-shams/massspring/master/massspring/images/Coulomb.svg)  
more information is available at [Coulomb's law](https://en.wikipedia.org/wiki/Coulomb%27s_law) wikipedia page.
you can create an electricity force between two masses using the code bellow:

```python
e1 = m.electricity(m1=m1, m2=m2)
```

(m1 and m2 are the two mass objects between which you want to set electricity force.)

#### spring

spring can also be known as an object. However, spring class is a subclass of force class. So technically spring is a force. the force will be calculated using the **"Hooke's law"**:  
![Hooke's law](https://raw.githubusercontent.com/pooya-shams/massspring/master/massspring/images/Hooke.svg)  
more information is available on [Hooke's law](https://en.wikipedia.org/wiki/Hooke%27s_law) wikipedia page.  
you can create a spring object by using the spring class. you can learn more about the arguments and their usage in the [spring class document](https://github.com/pooya-shams/massspring/blob/master/massspring/massspring.py#spring).

```python
s1 = m.spring(k=1500000, l=0, m1=m1, m2=m2, color=(255, 0, 0), visible=True)
```

#### collision

uses the conservation of momentum and kinetic energy and the equations presented at the [Elastic Collision](https://en.wikipedia.org/wiki/Elastic_collision) wikipedia page.

```python
c1 = m.collision(m1=m1, m2=m2)
```

### mainloop

after creating all of the objects and forces you want, you should call the mainloop function which is an infinite while loop and ends when the user closes the window or presses the ESCape button.  
arguments are:  
1.speed: the more this number is the faster your program runs. it will decrease the number of frames in which the screen will be updated(increases the space between them).  
2.FPS: sets the fps parameter for the pygame.time.Clock().tick(FPS) function. the less this number is the less your cpu will be under pressure.  
3.frame: it's a function which will be called every frame of the program.  
4.\*args: the arguments you want to give to the frame function.

```python
m.mainloop(speed=2, FPS=0, frame=None, *args)
```

## examples

You can see a simple example of using massspring library to create a pendulum.
It has an acceleration of -g in the Y ordinate.
!["pendulum"](https://raw.githubusercontent.com/pooya-shams/massspring/master/massspring/images/massspring%20(pendulum).gif)

available at [example 1](https://github.com/pooya-shams/massspring/blob/master/massspring/example%201%20(pendulum).py)

Here is another example of using this library.  
As you can see there is a double pendulum shown in the image. However, it is show in both x-y and z-y coordinates (x-y at left and z-y at right). you might feel they are completely different objects but they are just showing one object from two different points of view.

![double pendulum](https://raw.githubusercontent.com/pooya-shams/massspring/master/massspring/images/massspring%20(double%20pendulum).gif)

available at [example 2](https://github.com/pooya-shams/massspring/blob/master/massspring/example%202%20(double%20pendulum%203d).py).

3.[example 3](https://github.com/pooya-shams/massspring/blob/master/massspring/example%203%20(3d%20pyramid).py)  
4.[example 4](https://github.com/pooya-shams/massspring/blob/master/massspring/example%204%20(rope).py)  
5.[example 5](https://github.com/pooya-shams/massspring/blob/master/massspring/example%205%20(collision).py)  

## Requirements

python >= 3.6  
pygame >= 1.9.2
Note: if you want to hide the pygame support message, place this code before importing massspring.

```python
import os
os.environ["PYGAME_HIDE_SUPPORT_PROMPT"] = '1'
```

## TODO

(feel free to complete these tasks)

- [x] Add position checker to avoid integer too big error of pygame and python itself.
- [x] Update the Elastic collision.
- [ ] divide massspring.py to separate modules.
- [ ] Divide the collision to Elastic collision and Inelastic collision.
- [ ] Create non-sphere/non-mass objects.
- [ ] Collision between mass and spring (mass: sphere with mass, spring: line without mass).
- [ ] Collision between non-sphere objects, sphere objects and line objects(spring).
- [ ] Add statistic screen.
- [ ] Create the c/c++ project.
