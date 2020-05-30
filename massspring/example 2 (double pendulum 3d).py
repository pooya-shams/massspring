import massspring as m

m.acceleration.x = 0
m.acceleration.y = -m.ge
m.acceleration.z = -m.ge

m1 = m.mass(x=0, y=0, z=0, vx=0, vy=0, vz=0, m=20, r=10, q=0, moveable=False,
            solid=True, bound=True, gravitational=False, resistible=False,
            electrical=False, conductive=False,
            color=m.colors.WHITE, visible=True)
m2 = m.mass(x=-50, y=-50, z=-100, vx=0, vy=0, vz=0, m=200, r=10, q=0,
            moveable=True, solid=True, bound=True, gravitational=False,
            resistible=False, electrical=False, conductive=False,
            color=m.colors.RED, visible=True)
m3 = m.mass(x=0, y=0, z=-100, vx=0, vy=0, vz=0, m=20, r=10, q=0,
            moveable=True, solid=True, bound=True, gravitational=False,
            resistible=False, electrical=False, conductive=False,
            color=m.colors.GREEN, visible=True)
s1 = m.spring(k=1000000, nl=0, m1=m1, m2=m2,
              color=m.colors.CYAN, visible=True)
s2 = m.spring(k=1000000, nl=0, m1=m2, m2=m3,
              color=m.colors.MAGENTA, visible=True)

m.mainloop(10, 0)
