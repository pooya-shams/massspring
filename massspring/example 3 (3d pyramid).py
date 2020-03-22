import massspring as m

m.acceleration.x = -m.ge
m.acceleration.y = -m.ge
m.acceleration.z = -m.ge

n = 5

m.mass(m=20, r=20, x=-50, y=-50, z=0, vx=0, vy=0, vz=0, moveable=True,
       solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x=50, y=-50, z=0, vx=0, vy=0, vz=0, moveable=True,
       solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x=-50, y=50, z=0, vx=0, vy=0, vz=0, moveable=True,
       solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x=50, y=50, z=0, vx=0, vy=0, vz=0, moveable=True,
       solid=True, bound=True, color=(255, 0, 0), visible=True)
m.mass(m=20, r=20, x=0, y=0, z=(3**.5/2) * 100, vx=0, vy=0, vz=0,
       moveable=True, solid=True, bound=True, color=(255, 0, 0), visible=True)

for i in range(n):
    for j in range(i+1, n):
        m.spring(k=100000, nl=0, m1=m.mass_lis[i], m2=m.mass_lis[j], color=(
            0, 255, 0), visible=True)

m.mainloop(10)
