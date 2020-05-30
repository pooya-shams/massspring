import massspring as m

m1 = m.mass(m=20, r=45, x=-50, y=5, z=0, vx=20, vy=0, vz=0,
            moveable=True, solid=True, bound=True,
            color=m.colors.RED, visible=True)
m2 = m.mass(m=30, r=60, x=50, y=0, z=5, vx=-20, vy=0, vz=0,
            moveable=True, solid=True, bound=True,
            color=m.colors.GREEN, visible=True)

m.mainloop(100, 0)
