import numpy as np
import matplotlib.pyplot as plt
import random
import time

# Initialize global variables
legmagassabbpont = 0  
count_of_max_peaks = 0  
count_of_found_max_peaks = 0
given_seed = 340
sim_delay_sec = 0.05

rXStart = np.random.randint(0, 30)
rYStart = np.random.randint(0, 30)

# Function to set the seed for reproducibility
def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)

# Generate a random integer between min and max
def RandomSzamGeneralas(min_val, max_val):
    return random.randint(min_val, max_val)

# Terrain generation with integer-based Gaussian peaks and valleys
def terrain_function(x, y):
    num_peaks = RandomSzamGeneralas(10, 30)
    terrain = np.zeros_like(x, dtype=int) + 8

    for _ in range(num_peaks):
        peak_x = np.random.uniform(0, 30)
        peak_y = np.random.uniform(0, 30)
        height = RandomSzamGeneralas(1, 3)
        width = RandomSzamGeneralas(1, 2)
        terrain += np.round(height * np.exp(-((x - peak_x) ** 2 + (y - peak_y) ** 2) / (2 * width ** 2))).astype(int)

    num_valleys = RandomSzamGeneralas(5, 10)
    for _ in range(num_valleys):
        valley_x = np.random.uniform(0, 30)
        valley_y = np.random.uniform(0, 30)
        depth = RandomSzamGeneralas(1, 3)
        terrain -= np.round(depth * np.exp(-((x - valley_x) ** 2 + (y - valley_y) ** 2) / (2 * 1 ** 2))).astype(int)

    return terrain

def find_highest_peak(Z):
    global legmagassabbpont
    legmagassabbpont = np.max(Z)
    return legmagassabbpont


def count_max_peaks(Z, max_height):
    return np.sum(Z == max_height)

# Initialize the plot
def init_plot(X, Y, Z, seed):
    fig = plt.figure(figsize=(8, 6))
    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Terrain height")
    ax3d.set_title(f"Generated 3D Terrain with Peaks and Valleys (Seed={seed})")
    return fig, ax3d

def plot_terrain(ax3d, Z, dot_coords=None):
    for collection in ax3d.collections:
        collection.remove()
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    if dot_coords is not None:
        x, y = dot_coords
        x_idx = (np.abs(x_vals - x)).argmin()
        y_idx = (np.abs(y_vals - y)).argmin()
        z = Z[y_idx, x_idx]
        ax3d.scatter(x, y, z, color='red', s=100, label="Red Dot")
        ax3d.legend()
    plt.draw()
    plt.pause(0.1)

def move_red_dot():

    current_x = rXStart
    current_y = rYStart

    step_count = 0
    found_peaks = set()

    #Latogatott mezök mátrix
    visited = np.zeros((30, 30), dtype=bool)

    global count_of_max_peaks
    
    count_of_found_max_peaks = 0

    for row in Z:
        print(" ".join(map(str, row)))

    while count_of_max_peaks != count_of_found_max_peaks:
        visited[current_y, current_x] = True

        current_height = Z[current_y, current_x]
        neighbors = [] 
        if current_y < 29 and not visited[current_y + 1, current_x]:
            neighbors.append(('up', current_x, current_y + 1, Z[current_y + 1, current_x]))
        if current_y > 0 and not visited[current_y - 1, current_x]:
            neighbors.append(('down', current_x, current_y - 1, Z[current_y - 1, current_x]))
        if current_x > 0 and not visited[current_y, current_x - 1]:
            neighbors.append(('left', current_x - 1, current_y, Z[current_y, current_x - 1]))
        if current_x < 29 and not visited[current_y, current_x + 1]:
            neighbors.append(('right', current_x + 1, current_y, Z[current_y, current_x + 1]))


        if neighbors:
            best_move = neighbors[0]
            for neighbor in neighbors:
                if neighbor[3] > best_move[3]:
                    best_move = neighbor
            direction, new_x, new_y, new_height = best_move
        else:
            unvisited_cells = np.argwhere(visited == False)
            if len(unvisited_cells) == 0:
                print("Nincs több mezö")
                break 
            new_x, new_y = random.choice(unvisited_cells)
            new_height = Z[new_y, new_x]

        current_x, current_y = new_x, new_y
        step_count += 1

        if new_height == legmagassabbpont and (current_x, current_y) not in found_peaks:
            found_peaks.add((current_x, current_y))
            count_of_found_max_peaks += 1

        print(f"Lépés {step_count}. Helyzet: ({current_x}, {current_y}), Magasság: {new_height}, Globális Maximum: {legmagassabbpont}, Globális maximum szám: {count_of_max_peaks}, Megtalált globális maximumok száma: {count_of_found_max_peaks}")
        plot_terrain(ax3d, Z, dot_coords=(current_x, current_y))
        time.sleep(sim_delay_sec)

        if count_of_max_peaks == count_of_found_max_peaks:
            print(f"Minden csúcs megtalálva {step_count} lépésből.")
            rekordLetrehoz(f"{count_of_max_peaks} db Globális maximum {step_count} lépésből seed: {given_seed}",f"{given_seed}.txt")
            break

def rekordLetrehoz(text, filename):
    try:
        step_count = int(text.split(' lépésből ')[0].split()[-1])
        
        with open(filename, 'a') as file:
            file.write(text + '\n') 

        with open(filename, 'r') as file:
            lines = file.readlines()

        total_step_count = 0
        for line in lines:
            try:
                step_count_value = int(line.split(' lépésből ')[0].split()[-1])
                total_step_count += step_count_value
            except ValueError:
                pass

        average_step_count = total_step_count / len(lines) if len(lines) > 0 else 0

        # Átlag
        with open(filename, 'a') as file:
            file.write(f"Átlag : {average_step_count:.2f}\n")

    except Exception as e:
        print()

# Seed beállítása
seed = given_seed
set_seed(seed)

x_vals = np.linspace(0, 30, 30)
y_vals = np.linspace(0, 30, 30)
X, Y = np.meshgrid(x_vals, y_vals)
Z = terrain_function(X, Y)

legmagassabbpont = find_highest_peak(Z)
count_of_max_peaks = count_max_peaks(Z, legmagassabbpont)

fig, ax3d = init_plot(X, Y, Z, seed)
move_red_dot()