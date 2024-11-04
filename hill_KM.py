import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import random
import tkinter as tk
from tkinter import simpledialog

# Function to set the seed for both random and numpy
def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)

# Function to generate a random integer between min and max
def RandomSzamGeneralas(min, max):
    return random.randint(min, max)

# Complex terrain generation with multiple Gaussian peaks
def terrain_function(x, y):
    num_peaks = RandomSzamGeneralas(5, 20)  # Randomized number of peaks based on the seed
    terrain = np.zeros_like(x)
    for _ in range(num_peaks):
        peak_x = np.random.uniform(-5, 5)
        peak_y = np.random.uniform(-5, 5)
        height = np.random.uniform(1, 3)
        width = np.random.uniform(0.5, 1.5)
        terrain += height * np.exp(-((x - peak_x) ** 2 + (y - peak_y) ** 2) / (2 * width ** 2))
    return terrain

# Function to plot the terrain
def plot_terrain(seed=4):
    # Set seed for reproducibility
    set_seed(seed)

    # Generating a 30x30 grid for the terrain
    x_vals = np.linspace(-5, 5, 30)
    y_vals = np.linspace(-5, 5, 30)
    X, Y = np.meshgrid(x_vals, y_vals)
    Z = terrain_function(X, Y)
    
    # Plotting the 3D terrain
    fig = plt.figure(figsize=(12, 8))
    ax = fig.add_subplot(111, projection='3d')
    ax.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    
    # Setting labels
    ax.set_xlabel("X")
    ax.set_ylabel("Y")
    ax.set_zlabel("Terrain height")
    ax.set_title("Generated 3D Terrain with Multiple Peaks (Seed={})".format(seed))
    plt.show()

# Function to get seed from a popup window
def get_seed_from_user():
    root = tk.Tk()
    root.withdraw()  # Hide the main tkinter window

    seed = simpledialog.askinteger("Input", "Please enter a seed value:", minvalue=0, maxvalue=9999999)
    if seed is not None:
        plot_terrain(seed)
    else:
        print("No seed entered. Exiting.")

# Run the get_seed_from_user function to start
get_seed_from_user()
