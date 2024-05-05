import numpy as np
import pandas as pd
from stl import mesh

# Read data from CSV
df = pd.read_csv('C:\\Users\\LAB-ADMIN\\OneDrive - Syddansk Universitet\\Desktop\\3d graph 2\\data_clean.csv')  # Update this to the path of your CSV file

# Define the bins for BonusA
bins = np.linspace(0, 10000, 1000)  # Adjust bins as necessary, covering from 0 to 12000 with equal intervals
histograms = df.groupby('RF_numerical')['BonusA'].apply(lambda x: np.histogram(x, bins=bins)[0])
hist_data = np.vstack(histograms)

# Define x_positions and dimensions
x_positions = (bins[:-1] + bins[1:]) / 2
dx = (x_positions[1] - x_positions[0]) * 0.8  # Adjust width to 80% of the bin width to avoid gaps
dy = 1.0  # Set a fixed depth for each bar

# Adjust heights to be visible but not too elongated
max_height = hist_data.max()
height_scale = 50 / max_height  # Scale heights to a max of 50 mm

def create_bar_mesh(x, y, z, dx, dy, height):
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
    faces = np.array([
        [0, 3, 1], [1, 3, 2],  # bottom
        [0, 1, 5], [0, 5, 4],  # side
        [1, 2, 6], [1, 6, 5],  # side
        [2, 3, 7], [2, 7, 6],  # side
        [3, 0, 4], [3, 4, 7],  # side
        [4, 5, 6], [4, 6, 7]   # top
    ])
    bar = mesh.Mesh(np.zeros(faces.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            bar.vectors[i][j] = vertices[f[j], :]
    return bar

# Create mesh objects for each bar
bars = []
z_position = 0  # Starting z-position for the first category
for condition_data in hist_data:
    for x, height in zip(x_positions, condition_data * height_scale):  # Scale the height
        bars.append(create_bar_mesh(x, z_position, 0, dx, dy, height))
    z_position += dy + 10  # Increase z-position for the next category with a 10 mm gap

# Combine all bars into a single mesh
combined_mesh = mesh.Mesh(np.concatenate([bar.data for bar in bars]))
combined_mesh.save('scaled_distribution.stl')