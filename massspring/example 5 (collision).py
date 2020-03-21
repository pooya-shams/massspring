import massspring as m

m1 = m.mass(m=20, r=20, x=-100, y=0, z=0, vx=20, vy=0, vz=0,
            moveable=True, solid=True, bound=True,
            color=(255, 0, 0), visible=True)
m2 = m.mass(m=20, r=20, x=100, y=0, z=0, vx=-20, vy=0, vz=0,
            moveable=True, solid=True, bound=True,
            color=(0, 255, 0), visible=True)

m.mainloop(1, 0)
