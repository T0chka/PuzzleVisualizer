import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def calculate_positions(center, radius, num_circles, start_angle):
    """Calculate positions of circles in a ring formation"""
    positions = []
    for i in range(num_circles):
        angle = np.radians(start_angle + i * (360 / num_circles))
        x = center[0] + radius * np.cos(angle)
        y = center[1] + radius * np.sin(angle)
        positions.append((x, y))
    return positions

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Circle

def draw_rounded_rectangle_chain(ax, center, puzzle_width, num_circles, 
                                 highlight_indices, circle_radius, 
                                 fontsize_numbers, highlight_color):
    cx, cy = center
    base_width = puzzle_width / 3
    h = puzzle_width / 4
    r = puzzle_width / 15

    w = base_width + (num_circles - 10) * circle_radius * 2

    x_left, x_right = cx - w / 2, cx + w / 2
    y_top, y_bottom = cy + h / 2, cy - h / 2

    if num_circles < 8:
        raise ValueError("Минимум 8 кружков")

    top_extra = (num_circles - 8) // 2
    bottom_extra = num_circles - 8 - top_extra

    coords = []

    coords.append((x_left + r, y_top))
    if top_extra > 0:
        spacing_top = (x_right - r - (x_left + r)) / (top_extra + 1)
        coords.extend([(x_left + r + i * spacing_top, y_top) for i in range(1, top_extra + 1)])
    coords.append((x_right - r, y_top))
    coords.extend([(x_right, y) for y in np.linspace(y_top - r, y_bottom + r, 2)])
    coords.append((x_right - r, y_bottom))
    if bottom_extra > 0:
        spacing_bottom = (x_right - r - (x_left + r)) / (bottom_extra + 1)
        coords.extend([(x_left + r + i * spacing_bottom, y_bottom) for i in range(1, bottom_extra + 1)])
    coords.append((x_left + r, y_bottom))
    coords.extend([(x_left, y) for y in np.linspace(y_bottom + r, y_top - r, 2)])
    coords.append((x_left + r, y_top))

    coords = coords[:num_circles]

    for i, (x, y) in enumerate(coords):
        color = highlight_color if i in highlight_indices else 'white'
        circle = Circle((x, y), radius=circle_radius, edgecolor='black', facecolor=color)
        ax.add_patch(circle)
        ax.text(x, y, str(i + 1), ha='center', va='center', fontsize=fontsize_numbers)

def draw_three_puzzles():
    # Create a common field
    fig, ax = plt.subplots(figsize=(12, 4))
    ax.set_aspect('equal')
    ax.axis('off')

    plot_width = 18
    num_puzzles = 3
    puzzle_width = plot_width / num_puzzles
    circle_radius = puzzle_width / 30

    fontsize_title = 14
    fontsize_numbers = 10
    highlight_color = 'lightgreen'

    centers = [
        (puzzle_width * (i + 0.2), 0) for i in range(num_puzzles)
    ]

    title_y = puzzle_width / 2

    ##################################################################
    # 1. LRX (generates 10 circles)
    ##################################################################
    center_lrx = centers[0]
    ax.text(center_lrx[0], title_y, "LRX", fontsize=fontsize_title, ha='center')
    draw_rounded_rectangle_chain(
        ax = ax,
        center = center_lrx,
        puzzle_width = puzzle_width,
        num_circles = 12,
        highlight_indices = {1, 2},
        circle_radius = circle_radius,
        fontsize_numbers = fontsize_numbers,
        highlight_color = highlight_color
    )
    
    ##################################################################
    # 2. TopSpin (generates 12 circles)
    ##################################################################
    center_topspin = centers[1]
    ax.text(center_topspin[0], title_y, "TopSpin", fontsize=fontsize_title, ha='center')
    draw_rounded_rectangle_chain(
        ax = ax,
        center = center_topspin,
        puzzle_width = puzzle_width,
        num_circles = 16,
        highlight_indices = {1, 2, 3, 4},
        circle_radius = circle_radius,
        fontsize_numbers = fontsize_numbers,
        highlight_color = highlight_color
    )
    
    ##################################################################
    # 3. Hungarian Rings
    ##################################################################
    center_hungarian = centers[2]
    ax.text(center_hungarian[0], title_y, "Hungarian Rings", fontsize=fontsize_title, ha='center')

    # Ring parameters
    R = 0.8
    num_circles_hungarian = 8
    start_angle_ring1 = 0
    start_angle_ring2 = 0
    i, j = 1, 3 # indices of the circles to overlap

    # Solve for d given the angles
    theta1 = np.radians(start_angle_ring1 + i*(360/num_circles_hungarian))
    theta2 = np.radians(start_angle_ring2 + j*(360/num_circles_hungarian))
    d = -R*(np.cos(theta2) - np.cos(theta1))/2

    # Set the centers of the rings
    center_ring1 = (center_hungarian[0] - d, center_hungarian[1])
    center_ring2 = (center_hungarian[0] + d, center_hungarian[1])

    # Calculate positions for both rings
    positions_ring1 = calculate_positions(center_ring1, R, num_circles_hungarian, 0)
    positions_ring2 = calculate_positions(center_ring2, R, num_circles_hungarian, 0)

    # Define numbering
    numbers_ring1 = [2, 3, 4, 5, 6, 7, 8, 1]
    numbers_ring2 = [11, 12, 13, 3, 15, 1, 9, 10]

    # Draw first ring (red)
    for idx, (x, y) in enumerate(positions_ring1):
        circle = Circle((x, y), circle_radius, edgecolor='black', facecolor='lightcoral')
        ax.add_patch(circle)
        ax.text(x, y, str(numbers_ring1[idx]), ha='center', va='center', fontsize=fontsize_numbers)

    # Draw second ring (green)
    for idx, (x, y) in enumerate(positions_ring2):
        circle = Circle((x, y), circle_radius, edgecolor='black', facecolor=highlight_color)
        ax.add_patch(circle)
        ax.text(x, y, str(numbers_ring2[idx]), ha='center', va='center', fontsize=fontsize_numbers)

    ax.set_xlim(-1, plot_width + 1)
    ax.set_ylim(-2, 3)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    draw_three_puzzles()