import matplotlib.pyplot as plt

O1 = (0, 0)
obj_O1 = (15, -3)
O2 = (10, 2)

obj_O2 = (obj_O1[0] - O2[0], obj_O1[1] - O2[1])

fig, ax = plt.subplots()
ax.set_aspect('equal')
ax.grid(True, linestyle='--', alpha=0.6)

ax.plot(O1[0], O1[1], 'bo', label='O3 (Vehicle 1)')
ax.text(O1[0]+0.3, O1[1]+0.3, 'O3', color='blue')

ax.plot(O2[0], O2[1], 'go', label='O4 (Vehicle 2)')
ax.text(O2[0]+0.3, O2[1]+0.3, 'O4', color='green')

ax.plot(obj_O1[0], obj_O1[1], 'ro', label='Object')
ax.text(obj_O1[0]+0.3, obj_O1[1]+0.3, 'Object (O3 frame)', color='red')

ax.arrow(O2[0], O2[1], obj_O2[0], obj_O2[1], 
         head_width=0.3, head_length=0.5, fc='orange', ec='orange', 
         length_includes_head=True, label='Vector O4→Object')



ax.set_xlabel('East [m]')
ax.set_ylabel('North [m]')
ax.set_title('Object Position Relative to Vehicles')
ax.set_xlim(-1, 16)
ax.set_ylim(-4, 3)
ax.legend()

plt.show()
