# massspring

## Author : Pooya.Sh.K 
Inspired by Saeed Sarkarati

## Brief
<p>
using this library you can create great simulations of most of physical environments which can be calculated presizely. you can create many types of objects from which "mass" and "spring" are main ones.
</p>

## license
licensed under GNU General Public License version 3

## usage
<div>
<ul>
<li>
<p>
you can import the library by using the following code (it is recommended to import as m or ms)

```python
import massspring as m
```
</p>
</li>
<li>
<p>
you can create a mass object by using the mass class. you can learn more about the arguments and their usage in the <a href="./massspring.py#mass">mass class documention</a>

```python
m1 = m.mass(x=0, y=0, z=0, vx=0, vy=0, vz=0, m=10, r=10, q=0, moveable=False, solid=True, bound=True, gravitateable=False, resistable=False, electrical=False, conductive=False, color=(0, 255, 0), visible=True)
```
</p>
</li>
<li>
<p>
you can create a spring object by using the spring class. you can learn more about the arguments and their usage in the <a href="./massspring.py#spring">spring class documention</a>

```python
s1 = m.spring(k=1500000, l=0, m1=m1, m2=m2, color=(255, 0, 0), visible=True)
```
</p>
</li>
<li>
<p>
similarly you can create other objects which play the roll of forces between masses.
you can see them here:
	<ol type="1">
		<li><a href="./massspring.py#force">the base force class</a></li>
		<li><a href="./massspring.py#gravity">the gravity class</a></li>
		<li><a href="./massspring.py#electricity">the electricity class</a></li>
	</ol>
</p>
</li>
</ul>
</div>

## examples
<div>
<ol type="1">
<li>
	<p>
	You can see a simple example of using massspring library to create a pendulum.</br>
	It has an acceleration of -g in the Y ordinate.
	</br>
	<img src="./examples/massspring (pendulum).gif" alt="pendulum" style="border-radius:20px;width:500px;"></img>
	</br>
	available at <a href="./example 1 (pendulum).py">example 1</a>
	</p>
</li>
<li>
	<p>
	Here is anothere example of using this library.</br>
	As you can see there is a double pendulum shown in the image. However, it is show in both x-y and z-y coordinates (x-y at left and z-y at right). you might feel they are completely different objects but they are just showing one object from two different points of veiw.
	</br>
	<img src="./examples/massspring (double pendulum).gif" alt="double pendulum" style="border-radius:20px;width:500px;"></img>
	</br>
	available at <a href="./example 2 (double pendulum 3d).py">example 2</a>
	</p>
</li>
</ol>
<ul>
<li>
	<p>
	Other examples are available here (more to be added in future):
	<ol start="3" type="1">
		<li><a href="./example 3 (3d pyramid).py">example 3</a></li>
		<li><a href="./example 4 (rope).py">example 3</a></li>
		<li><a href="./example 5 (collision).py">example 3</a></li>
	</ol>
	</p>
</li>
</ul>
</div>
