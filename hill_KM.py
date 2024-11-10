import numpy as np
import matplotlib.pyplot as plt
import random
import time

legmagassabbpont = 0  
count_of_max_peaks = 0  
given_seed = 7231
sim_delay_sec = 0
number_of_runs = 4  
max_steps_per_run = 900  

rXStart = np.random.randint(0, 30)
rYStart = np.random.randint(0, 30)

def set_seed(seed):
    np.random.seed(seed)
    random.seed(seed)

def RandomSzamGeneralas(min_val, max_val):
    return random.randint(min_val, max_val)

# Gaussy csúcsok
def terkep_gen(x, y):
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

def max_csucsok(Z):
    global legmagassabbpont
    legmagassabbpont = np.max(Z)
    return legmagassabbpont

def max_csucs_db(Z, max_height):
    return np.sum(Z == max_height)

# Palya elkeszítése
def palya_elkeszit(X, Y, Z, seed):
    fig = plt.figure(figsize=(8, 6))
    ax3d = fig.add_subplot(111, projection='3d')
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    ax3d.set_xlabel("X")
    ax3d.set_ylabel("Y")
    ax3d.set_zlabel("Magasság")
    ax3d.set_title(f"Generált domborzat (Seed={seed})")
    return fig, ax3d

# Térkép frissít
def plot_terrain(ax3d, Z, dot_coords=None):
    for collection in ax3d.collections:
        collection.remove()
    ax3d.plot_surface(X, Y, Z, cmap='viridis', alpha=0.7)
    if dot_coords is not None:
        x, y = dot_coords
        x_idx = (np.abs(x_vals - x)).argmin()
        y_idx = (np.abs(y_vals - y)).argmin()
        z = Z[y_idx, x_idx]
        ax3d.scatter(x, y, z, color='red', s=100, label="Hegymászónk")
        ax3d.legend()
    plt.draw()
    plt.pause(0.1)

# Pötty mozgatása
def move_red_dot():
    global count_of_max_peaks
    found_peaks = set()
    visited = np.zeros((30, 30), dtype=bool)
    step_count = 0
    count_of_found_max_peaks = 0
   
    current_x = rXStart 
    current_y = rYStart

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
            best_move = max(neighbors, key=lambda n: n[3])  
            _, new_x, new_y, new_height = best_move
        else:
            unvisited_cells = np.argwhere(visited == False)
            if len(unvisited_cells) == 0:
                break
            new_x, new_y = random.choice(unvisited_cells)
            new_height = Z[new_y, new_x]

        current_x, current_y = new_x, new_y
        step_count += 1

        if new_height == legmagassabbpont and (current_x, current_y) not in found_peaks:
            found_peaks.add((current_x, current_y))
            count_of_found_max_peaks += 1

        plot_terrain(ax3d, Z, dot_coords=(current_x, current_y))
        time.sleep(sim_delay_sec)

        if step_count > max_steps_per_run:            
            break

        if count_of_max_peaks == count_of_found_max_peaks:
            break

    return step_count

seed = given_seed
set_seed(seed)

x_vals = np.linspace(0, 30, 30)
y_vals = np.linspace(0, 30, 30)
X, Y = np.meshgrid(x_vals, y_vals)
Z = terkep_gen(X, Y)

print("Magasság mátrix:")
for row in Z:
    print(" ".join(map(str, row)))

legmagassabbpont = max_csucsok(Z)
count_of_max_peaks = max_csucs_db(Z, legmagassabbpont)

fig, ax3d = palya_elkeszit(X, Y, Z, seed)

total_step_counts = []

for run in range(number_of_runs):
    print(f"\nSzimuláció futtatása {run + 1}/{number_of_runs}")

    # Reset mindent
    rXStart = np.random.randint(0, 30)
    rYStart = np.random.randint(0, 30)
    steps = move_red_dot()
    total_step_counts.append(steps)
    print(f"Szimuláció {run + 1}/{number_of_runs} lefutott {steps} lépésből")

# Átlag számolás
average_steps = sum(total_step_counts) / len(total_step_counts) if total_step_counts else 0
print(f"\nSzimuláció vége. lépészám:  {number_of_runs} átlag: {average_steps:.2f}")
