import massspring as m

m.ax0 = 0
m.ay0 = -m.ge
m.az0 = 0

NM = 20
d = 10

m.mass(m=5, r=5, x=0, y=200, z=0, vx=0, vy=0, vz=0, moveable=False,
       solid=True, bound=True, resistable=True,
       color=(255, 0, 0), visible=True)

for i in range(NM):
    m.mass(m=10, r=5, x=i*d+d, y=200, z=i*d, vx=0, vy=0, vz=0, moveable=True,
           solid=True, resistable=True, bound=True,
           color=(255, 0, 0), visible=True)
    m.spring(k=1000, nl=0, m1=m.mass_lis[i+1],
             m2=m.mass_lis[i], color=(255, 255, 255), visible=True)

m.mainloop(10)
