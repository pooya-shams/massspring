import massspring as m

m.ax0 = -m.ge
m.ay0 = -m.ge
m.az0 = -m.ge

n = 5

m.mass(m=20, r=20, x=-50, y=-50, z=0, vx=0, vy=0, vz=0, moveable=True, solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x= 50, y=-50, z=0, vx=0, vy=0, vz=0, moveable=True, solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x=-50, y= 50, z=0, vx=0, vy=0, vz=0, moveable=True, solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x= 50, y= 50, z=0, vx=0, vy=0, vz=0, moveable=True, solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x=0, y=0, z=(3**.5/2) * 100, vx=0, vy=0, vz=0, moveable=True, solid=True, bound=True, color=(255, 0, 0), visible=True)

for i in range(n):
    for j in range(i+1, n):
        m.spring(k=100000, l=0, m1=m.mass_lis[i], m2=m.mass_lis[j], color=(0, 255, 0), visible=True)

m.mainloop(10)
