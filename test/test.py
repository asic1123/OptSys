import raytracing as rt
import visualize as vis
import numpy as np

components = []
components.append(rt.Mirror(
			  aperture=200,
			  pos=[100,-100],
			  theta=np.pi/2))

rays = []
rays.append([-20, 100, -np.pi/3])
ray_bundles = rt.propagate_rays(components, rays)



# Color for the rays
colors = 'r'

# Create a new canvas
canvas = vis.Canvas([-200, 600], [-100, 100])

# Draw the components
#canvas.draw_components(components)

# Draw the rays
canvas.draw_rays(ray_bundles, colors)

# Show the system
#canvas.show()

# Save a copy
canvas.save('example.png')
