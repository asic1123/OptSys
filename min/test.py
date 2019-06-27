import raytracing as rt
import visualize as vis
import numpy as np

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
rays.append([125, 100, -np.pi/3])
rays.append([75, 100, -np.pi*2/3])
ray_bundles = rt.propagate_rays(components, rays)



# Color for the rays
colors = ['r','r']

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
