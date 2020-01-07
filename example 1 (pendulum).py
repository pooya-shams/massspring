import massspring as m

m.ay0 = -10

m1 = m.mass(x=0, y=0, z=0, vx=0, vy=0, vz=0, m=10, r=10, q=0, moveable=False, solid=True, bound=True, gravitateable=False, resistable=False, electrical=False, conductive=False, color=(0, 255, 0), visible=True)
m2 = m.mass(x=200, y=-100, z=0, vx=0, vy=0, vz=0, m=100, r=10, q=0, moveable=True, solid=True, bound=True, gravitateable=False, resistable=False, electrical=False, conductive=False, color=(255, 0, 255), visible=True)
s1 = m.spring(k=1500000, l=0, m1=m1, m2=m2, color=(255, 0, 0), visible=True)

m.mainloop(10)
