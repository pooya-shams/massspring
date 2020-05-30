import massspring as m

m.acceleration.x = 0
m.acceleration.y = -m.ge
m.acceleration.z = 0

NM = 20
d = 10

m.mass(m=5, r=5, x=0, y=200, z=0, vx=0, vy=0, vz=0, moveable=False,
       solid=True, bound=True, resistible=True,
       color=m.colors.RED, visible=True)

for i in range(NM):
    m.mass(m=10, r=5, x=i*d+d, y=200, z=i*d, vx=0, vy=0, vz=0, moveable=True,
           solid=True, resistible=True, bound=True,
           color=m.colors.RED, visible=True)
    m.spring(k=1000, nl=0, m1=m.mass_lis[i+1],
             m2=m.mass_lis[i], color=m.colors.WHITE, visible=True)

m.mainloop(10)
