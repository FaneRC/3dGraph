from stl import mesh
import numpy as np

# Define your data (scaling the x-positions)
x_range = np.linspace(-10, 10, 100)
scale_factor = 0.1  # Scale factor to reduce overall width
x_positions = x_range * scale_factor

# Calculate the bar width based on the minimum distance between x positions
dx = np.min(np.diff(np.sort(x_positions)))  # This ensures no gaps
dy = 0.2 * scale_factor  # Scale bar depth accordingly

# Adjusting heights by a suitable scale factor for visibility
heights1 = np.exp(-0.5 * ((x_range - 0) / 2)**2) / (2 * np.pi)**0.5 * 5
heights2 = np.exp(-0.5 * ((x_range - 3) / 2)**2) / (2 * np.pi)**0.5 * 5

# Function to generate a single bar's mesh
def create_bar_mesh(x, y, z, dx, dy, height):
    # Adjust vertex positions to center bars around x positions
    vertices = np.array([
        [x - dx / 2, y, z],
        [x + dx / 2, y, z],
        [x + dx / 2, y + dy, z],
        [x - dx / 2, y + dy, z],
        [x - dx / 2, y, z + height],
        [x + dx / 2, y, z + height],
        [x + dx / 2, y + dy, z + height],
        [x - dx / 2, y + dy, z + height]
    ])
    
    # Define the twelve faces of the prism (two triangles per face)
    faces = np.array([
        [0, 3, 1], [1, 3, 2],  # bottom
        [0, 1, 5], [0, 5, 4],  # side
        [1, 2, 6], [1, 6, 5],  # side
        [2, 3, 7], [2, 7, 6],  # side
        [3, 0, 4], [3, 4, 7],  # side
        [4, 5, 6], [4, 6, 7]   # top
    ])

    # Create the mesh
    bar = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            bar.vectors[i][j] = vertices[f[j], :]
    return bar

# Create mesh objects for each bar
bars = []
for x, height1, height2 in zip(x_positions, heights1, heights2):
    bars.append(create_bar_mesh(x, 0, 0, dx, dy, height1))
    bars.append(create_bar_mesh(x, 5 * scale_factor, 0, dx, dy, height2))  # Scale Y-offset as well

# Combine all bars into a single mesh
combined_mesh = mesh.Mesh(np.concatenate([bar.data for bar in bars]))

# Save the mesh to file
combined_mesh.save('combined_distribution.stl')
