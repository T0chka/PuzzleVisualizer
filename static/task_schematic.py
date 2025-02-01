import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Ellipse

def calculate_positions(center, radius, num_circles, start_angle):
    """Calculate positions of circles in a ring formation"""
    positions = []
    for i in range(num_circles):
        angle = np.radians(start_angle + i * (360 / num_circles))
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        positions.append((x, y))
    return positions

def draw_three_puzzles():
    # Create a common field
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_aspect('equal')
    ax.axis('off')

    circle_radius = 0.3

    ##################################################################
    # 1. LRX
    ##################################################################
    ax.text(1.5, 2.5, "LRX", fontsize=14, ha='center')

    # 4 circles in a row
    for i in range(4):
        x = i * 1.2
        y = 0

        highlight_indices = (0, 1)
        circle = Circle(
            (x, y), radius=circle_radius, edgecolor='black',
            facecolor='white' if i not in highlight_indices else 'lightgreen'
        )
        ax.add_patch(circle)
        ax.text(x, y, str(i+1), ha='center', va='center', fontsize=10)

    ##################################################################
    # 2. TopSpin
    ##################################################################
    center_topspin = (8.0, 0.0)
    ax.text(center_topspin[0], 2.5, "TopSpin", fontsize=14, ha='center')
    
    num_circles = 10
    R_y = 1.5
    R_x = 1.2 + 0.1 * num_circles

    # index 0 is at the TOP (π/2) and go clockwise
    angles = np.linspace(np.pi/2, np.pi/2 - 2*np.pi, num_circles, endpoint=False)
    highlight_indices = {0, 1, num_circles - 1}

    for i, angle in enumerate(angles):
        x = center_topspin[0] + R_x * np.cos(angle)
        y = center_topspin[1] + R_y * np.sin(angle)
        color = 'lightgreen' if i in highlight_indices else 'white'
        circle = Circle((x, y), radius=circle_radius, edgecolor='black', facecolor=color)
        ax.add_patch(circle)
        ax.text(x, y, str(i+1), ha='center', va='center', fontsize=10)

    ##################################################################
    # 3. Hungarian Rings
    ##################################################################
    center_hungarian = (14, 0)
    ax.text(center_hungarian[0], 2.5, "Hungarian Rings", fontsize=14, ha='center')

    # Ring parameters
    R = 1.2  # Radius of the rings
    num_circles = 8
    start_angle_ring1 = 0
    start_angle_ring2 = 0
    i, j = 1, 3  # indices of the circles to overlap

    # Calculate centers of rings
    theta1 = np.radians(start_angle_ring1 + i*(360/num_circles))
    theta2 = np.radians(start_angle_ring2 + j*(360/num_circles))
    d = -R*(np.cos(theta2) - np.cos(theta1))/2

    # Set the centers of the rings
    center_ring1 = (center_hungarian[0] - d, 0)
    center_ring2 = (center_hungarian[0] + d, 0)

    # Calculate positions for both rings
    positions_ring1 = calculate_positions(center_ring1, R, num_circles, start_angle_ring1)
    positions_ring2 = calculate_positions(center_ring2, R, num_circles, start_angle_ring2)

    # Define numbering for the circles
    numbers_ring1 = [2, 3, 4, 5, 6, 7, 8, 1]
    numbers_ring2 = [11, 12, 13, 3, 15, 1, 9, 10]

    # Draw first ring
    for idx, (x, y) in enumerate(positions_ring1):
        circle = Circle((x, y), circle_radius, edgecolor='black', facecolor='lightcoral')
        ax.add_patch(circle)
        ax.text(x, y, str(numbers_ring1[idx]),
                color='black', ha='center', va='center', fontsize=10)

    # Draw second ring
    for idx, (x, y) in enumerate(positions_ring2):
        circle = Circle((x, y), circle_radius, edgecolor='black', facecolor='lightgreen')
        ax.add_patch(circle)
        ax.text(x, y, str(numbers_ring2[idx]),
                color='black', ha='center', va='center', fontsize=10)

    # Set the limits
    ax.set_xlim(-1, 18)
    ax.set_ylim(-2, 3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_three_puzzles()
