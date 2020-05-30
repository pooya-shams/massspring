import massspring as m

m.acceleration.y = -m.ge

m1 = m.mass(x=0, y=0, z=0, vx=0, vy=0, vz=0, m=10, r=10, q=0, moveable=False,
            solid=True, bound=True, gravitational=False, resistible=False,
            electrical=False, conductive=False,
            color=m.colors.GREEN, visible=True)
m2 = m.mass(x=200, y=-100, z=0, vx=0, vy=0, vz=0, m=100, r=10, q=0.1,
            moveable=True, solid=True, bound=True, gravitational=True,
            resistible=False, electrical=True, conductive=True,
            color=m.colors.MAGENTA, visible=True)
m3 = m.mass(x=-200, y=-100, z=0, vx=0, vy=0, vz=0, m=100, r=10, q=0.1,
            moveable=True, solid=True, bound=True, gravitational=True,
            resistible=False, electrical=True, conductive=True,
            color=m.colors.MAGENTA, visible=True)
m4 = m.mass(x=0, y=-300, z=0, vx=0, vy=0, vz=0, m=10**10, r=10, q=0,
            moveable=False, solid=True, bound=True, gravitational=True,
            resistible=False, electrical=False, conductive=False,
            color=m.colors.GREEN, visible=True)
s1 = m.spring(k=1500000, nl=0, m1=m1, m2=m2, color=(255, 0, 0), visible=True)
s2 = m.spring(k=1500000, nl=0, m1=m1, m2=m3, color=(255, 0, 0), visible=True)


m.mainloop(10)
