import numpy as np
import matplotlib.pyplot as plt
import random
import time

legmagassabbpont = 0  # Variable to store the height of the highest peak
count_of_max_peaks = 0  # Variable to store the count of maximum peaks
given_seed = 3

# Function to set the seed for both random and numpy
def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)

# Function to generate a random integer between min and max
def RandomSzamGeneralas(min, max):
    return random.randint(min, max)

# Integer-based terrain generation with multiple Gaussian peaks and valleys
def terrain_function(x, y):
    num_peaks = RandomSzamGeneralas(10, 30)  # Randomized number of peaks based on the seed
    terrain = np.zeros_like(x, dtype=int) + 8  # Elevate terrain by 8

    # Add peaks
    for _ in range(num_peaks):
        peak_x = np.random.uniform(0, 30)  # Peaks in the range [0, 30]
        peak_y = np.random.uniform(0, 30)  # Peaks in the range [0, 30]
        height = RandomSzamGeneralas(1, 3)  # Integer height
        width = RandomSzamGeneralas(1, 2)   # Integer width
        
        # Adding integer-based peaks to the terrain
        terrain += np.round(height * np.exp(-((x - peak_x) ** 2 + (y - peak_y) ** 2) / (2 * width ** 2))).astype(int)
    
    # Introduce valleys randomly
    num_valleys = RandomSzamGeneralas(5, 10)  # Random number of valleys
    for _ in range(num_valleys):
        valley_x = np.random.uniform(0, 30)
        valley_y = np.random.uniform(0, 30)
        depth = RandomSzamGeneralas(1, 3)  # Depth of the valley
        
        # Creating valleys by subtracting from the terrain
        terrain -= np.round(depth * np.exp(-((x - valley_x) ** 2 + (y - valley_y) ** 2) / (2 * 1 ** 2))).astype(int)

    return terrain

# Function to find the height of the highest peak in the terrain
def find_highest_peak(Z):
    global legmagassabbpont  # Use the global variable to store the highest peak
    for i in range(Z.shape[0]):  # Iterate through each row
        for j in range(Z.shape[1]):  # Iterate through each column
            if Z[i, j] > legmagassabbpont:
                legmagassabbpont = Z[i, j]  # Update the highest peak height
    return legmagassabbpont

# Function to count how many times the highest peak occurs
def count_max_peaks(Z, max_height):
    count = 0
    for i in range(Z.shape[0]):  # Iterate through each row
        for j in range(Z.shape[1]):  # Iterate through each column
            if Z[i, j] == max_height:
                count += 1  # Increment count if the peak matches the maximum height
    return count

# Function to initialize the plot
def init_plot(X, Y, Z, seed):
    fig = plt.figure(figsize=(8, 6))
    ax3d = fig.add_subplot(111, projection='3d')
    
    # Plot the 3D terrain surface
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Terrain height")
    ax3d.set_title("Generated 3D Terrain with Peaks and Valleys (Seed={})".format(seed))
    
    return fig, ax3d

# Function to plot the terrain and include a red dot if specified
def plot_terrain(ax3d, Z, dot_coords=None):
    # Remove the previous red dot if it exists
    for collection in ax3d.collections:
        collection.remove()
    
    # Replot the terrain surface
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    
    # Add a red dot at the specified (x, y) coordinates
    if dot_coords is not None:
        x, y = dot_coords
        # Find the closest index in the grid to the specified (x, y) coordinates
        x_idx = (np.abs(x_vals - x)).argmin()
        y_idx = (np.abs(y_vals - y)).argmin()
        z = Z[y_idx, x_idx]  # Get the z value at the closest point
        
        # Plot the red dot on top of the terrain
        ax3d.scatter(x, y, z, color='red', s=100, label="Red Dot")
        ax3d.legend()
    
    plt.draw()  # Redraw the current figure
    plt.pause(0.1)  # Pause to allow the plot to update

# Function to move the red dot randomly
def move_red_dot():
    # Generate random starting coordinates within the bounds of the terrain
    current_x = random.randint(0, 29)
    current_y = random.randint(0, 29)
    step_count = 0  # Counter for the number of steps

    # Log the initial terrain matrix without tabs
    print("Initial Terrain Matrix (Z):")
    for row in Z:
        print(" ".join(map(str, row)))

    while True:  # Infinite loop for continuous movement
        # Randomly select a direction: up, down, left, right
        direction = random.choice(['up', 'down', 'left', 'right'])
        
        # Check if moving out of bounds, if so, select a new direction
        if direction == 'up' and current_y < 29:  # Adjusted to avoid index out of bounds
            current_y += 1
        elif direction == 'down' and current_y > 0:
            current_y -= 1
        elif direction == 'left' and current_x > 0:
            current_x -= 1
        elif direction == 'right' and current_x < 29:  # Adjusted to avoid index out of bounds
            current_x += 1

        # Increment the step count
        step_count += 1
        
        # Get the current height
        current_height = Z[current_y, current_x]

        # Count how many times the highest peak occurs
        global count_of_max_peaks
        count_of_max_peaks = count_max_peaks(Z, legmagassabbpont)

        # Log the current step count and height, along with the highest peak and its count
        print(f"Step {step_count}: Current Coordinates ({current_x}, {current_y}), Height: {current_height}, Highest Peak: {legmagassabbpont}, Count of Highest Peaks: {count_of_max_peaks}")
        
        # Plot the terrain with the new dot position
        plot_terrain(ax3d, Z, dot_coords=(current_x, current_y))
        
        # Pause for one second between steps
        time.sleep(1)

# Set the seed for reproducibility
seed = given_seed
set_seed(seed)

# Generating a 30x30 grid for the terrain in the first quadrant
x_vals = np.linspace(0, 30, 30)  # x values from 0 to 30
y_vals = np.linspace(0, 30, 30)  # y values from 0 to 30
X, Y = np.meshgrid(x_vals, y_vals)
Z = terrain_function(X, Y)

# Find the highest peak and store it in legmagassabbpont
legmagassabbpont = find_highest_peak(Z)

# Count the number of times the highest peak occurs
count_of_max_peaks = count_max_peaks(Z, legmagassabbpont)

# Print the height of the highest peak and its count
print(f"The height of the highest peak is: {legmagassabbpont}")
print(f"The count of highest peaks is: {count_of_max_peaks}")

# Initialize the plot
fig, ax3d = init_plot(X, Y, Z, seed)

# Start moving the red dot from a random coordinate
move_red_dot()
