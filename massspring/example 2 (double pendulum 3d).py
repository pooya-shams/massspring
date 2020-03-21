import massspring as m

m.ax0 = 0
m.ay0 = -m.ge
m.az0 = -m.ge

m1 = m.mass(x=0, y=0, z=0, vx=0, vy=0, vz=0, m=20, r=10, q=0, moveable=False,
            solid=True, bound=True, gravitateable=False, resistable=False,
            electrical=False, conductive=False,
            color=(255, 255, 255), visible=True)
m2 = m.mass(x=-50, y=-50, z=-100, vx=0, vy=0, vz=0, m=200, r=10, q=0,
            moveable=True, solid=True, bound=True, gravitateable=False,
            resistable=False, electrical=False, conductive=False,
            color=(255, 0, 0), visible=True)
m3 = m.mass(x=0, y=0, z=-100, vx=0, vy=0, vz=0, m=20, r=10, q=0,
            moveable=True, solid=True, bound=True, gravitateable=False,
            resistable=False, electrical=False, conductive=False,
            color=(0, 255, 0), visible=True)
s1 = m.spring(k=1000000, nl=0, m1=m1, m2=m2, color=(0, 255, 255), visible=True)
s2 = m.spring(k=1000000, nl=0, m1=m2, m2=m3, color=(255, 0, 255), visible=True)

m.mainloop(10, 0)
