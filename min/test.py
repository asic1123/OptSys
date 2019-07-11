import raytracing as rt
import visualize as vis
import numpy as np
import re

pattern = re.compile('scanangle')

with open('scanrule','r') as f:
        rulename=f.readlines()
        rule=[]
        for line in rulename:
            m=pattern.match(line)
            if m:
                rule.append(line.strip('\n'))

angle=[]
for i in rule:
    angle.append(int(i.split(':')[1]))

f.closed

components = []
components.append(rt.Mirror(
			  aperture=300,
			  pos=[100,-100],
			  theta=np.pi/2))

components.append(rt.Mirror(
			  aperture=300,
			  pos=[300,0],
			  theta=0))
rays = []
n1 = 180/float(angle[0])
n2 = 180/float(angle[1])
rays.append([75, 100, -(np.pi/2 - np.pi/n1)])
rays.append([125, 100, -(np.pi/2 - np.pi/n2)])
ray_bundles = rt.propagate_rays(components, rays)



# Color for the rays
colors = ['r','b']

# Create a new canvas
canvas = vis.Canvas([-100, 300], [-100, 100])

# Draw the components
#canvas.draw_components(components)

# Draw the rays
canvas.draw_rays(ray_bundles, colors)

# Show the system
#canvas.show()

# Save a copy
canvas.save('example.png')
