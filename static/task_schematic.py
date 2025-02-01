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

def draw_rounded_rectangle_chain(ax, center, puzzle_width, num_circles, highlight_indices, circle_radius, fontsize_numbers, highlight_color):
    """
    Draws a chain of circles in the form of a rectangle with rounded corners
    """
    w = puzzle_width/3  # width of the rectangle
    h = puzzle_width/4  # height of the rectangle
    r = puzzle_width/15  # radius of corners
    
    # Calculate the perimeter
    perimeter_horizontal = w - 2 * r
    perimeter_vertical = h - 2 * r
    arc_length = np.pi * r / 2
    total_perimeter = 2 * (perimeter_horizontal + perimeter_vertical) + 4 * arc_length

    # Number of circles along the perimeter
    n_total = num_circles
    
    def generate_points(start, length, n, is_arc=False, center=None, radius=None, start_angle=None, end_angle=None):
        if is_arc:
            angles = np.linspace(start_angle, end_angle, n, endpoint=False)
            return center[0] + radius * np.cos(angles), center[1] + radius * np.sin(angles)
        else:
            n = int(n)
            return np.linspace(start[0], start[0] + length, n, endpoint=False), np.full(n, start[1])
    
    # Calculate all segments
    x_top, y_top = generate_points((center[0] - w/2 + r, center[1] + h/2), perimeter_horizontal, 
                                 int(n_total * perimeter_horizontal / total_perimeter))
    
    x_tr, y_tr = generate_points(None, None, int(n_total * arc_length / total_perimeter),
        is_arc=True, center=(center[0] + w/2 - r, center[1] + h/2 - r), 
        radius=r, start_angle=np.pi/2, end_angle=0)
    
    x_right, y_right = generate_points((center[0] + w/2, center[1] + h/2 - r), -perimeter_vertical,
                                     int(n_total * perimeter_vertical / total_perimeter))
    
    x_br, y_br = generate_points(None, None, int(n_total * arc_length / total_perimeter),
        is_arc=True, center=(center[0] + w/2 - r, center[1] - h/2 + r),
        radius=r, start_angle=0, end_angle=-np.pi/2)
    
    x_bottom, y_bottom = generate_points((center[0] + w/2 - r, center[1] - h/2), -perimeter_horizontal,
                                       int(n_total * perimeter_horizontal / total_perimeter))
    
    x_bl, y_bl = generate_points(None, None, int(n_total * arc_length / total_perimeter),
        is_arc=True, center=(center[0] - w/2 + r, center[1] - h/2 + r),
        radius=r, start_angle=-np.pi/2, end_angle=-np.pi)
    
    x_left, y_left = generate_points((center[0] - w/2, center[1] - h/2 + r), perimeter_vertical,
                                   int(n_total * perimeter_vertical / total_perimeter))
    
    x_tl, y_tl = generate_points(None, None, int(n_total * arc_length / total_perimeter),
        is_arc=True, center=(center[0] - w/2 + r, center[1] + h/2 - r),
        radius=r, start_angle=-np.pi, end_angle=-3*np.pi/2)
    
    # Combine all coordinates
    xs = np.concatenate([x_top, x_tr, x_right, x_br, x_bottom, x_bl, x_left, x_tl])
    ys = np.concatenate([y_top, y_tr, y_right, y_br, y_bottom, y_bl, y_left, y_tl])
    
    # Draw circles
    for i, (x, y) in enumerate(zip(xs, ys)):
        color = highlight_color if i in highlight_indices else 'white'
        circle = Circle((x, y), radius=circle_radius, edgecolor='black', facecolor=color)
        ax.add_patch(circle)
        ax.text(x, y, str(i+1), ha='center', va='center', fontsize=fontsize_numbers)

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
    # 1. LRX (2 circles swap)
    ##################################################################

    center_lrx = centers[0]
    ax.text(center_lrx[0], title_y, "LRX", fontsize=fontsize_title, ha='center')
    draw_rounded_rectangle_chain(
        ax = ax,
        center = center_lrx,
        puzzle_width = puzzle_width,
        num_circles = 16,
        highlight_indices = {1, 2},
        circle_radius = circle_radius,
        fontsize_numbers = fontsize_numbers,
        highlight_color = highlight_color
    )
    
    ##################################################################
    # 2. TopSpin
    ##################################################################
    center_topspin = centers[1]
    ax.text(center_topspin[0], title_y, "TopSpin", fontsize=fontsize_title, ha='center')
    draw_rounded_rectangle_chain(
        ax = ax,
        center = center_topspin,
        puzzle_width = puzzle_width,
        num_circles = 16,
        highlight_indices = {0, 1, 2, 3},
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
    R = puzzle_width / 4  # Radius of the rings
    num_circles_hungarian = 8
    start_angle_ring1 = 0
    start_angle_ring2 = 0
    i, j = 1, 3  # indices of the circles to overlap

    # Calculate centers of rings
    theta1 = np.radians(start_angle_ring1 + i*(360/num_circles_hungarian))
    theta2 = np.radians(start_angle_ring2 + j*(360/num_circles_hungarian))
    d = -R*(np.cos(theta2) - np.cos(theta1))/2

    # Set the centers of the rings
    center_ring1 = (center_hungarian[0] - d, 0)
    center_ring2 = (center_hungarian[0] + d, 0)

    # Calculate positions for both rings
    positions_ring1 = calculate_positions(center_ring1, R, num_circles_hungarian, start_angle_ring1)
    positions_ring2 = calculate_positions(center_ring2, R, num_circles_hungarian, start_angle_ring2)

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
        circle = Circle((x, y), circle_radius, edgecolor='black', facecolor=highlight_color)
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