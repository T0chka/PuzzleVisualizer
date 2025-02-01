import numpy as np
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.widgets import Button
from matplotlib.patches import Circle, Rectangle
from matplotlib.animation import FuncAnimation

class PuzzleVisualizer:
    def __init__(self):
        self.fig = plt.figure(figsize=(15, 8))
        self.gs = GridSpec(2, 3, height_ratios=[4, 1])
        
        # Define the states
        self.current_states = {
            'LRX': np.array([1, 2, 3, 4]),
            'TopSpin': np.array([1, 2, 3, 4, 5, 6, 7, 8]),
            'HungarianRing': np.array([1, 2, 3, 4, 5, 6, 7, 8])
        }
        
        # Split the Hungarian rings into upper and lower
        self.ring_upper = self.current_states['HungarianRing'][:4]
        self.ring_lower = self.current_states['HungarianRing'][4:]
        
        self.frames = 20  # Number of animation frames
        
        self.setup_plots()
        self.setup_buttons()
        self.update_all_visualizations()

    def setup_plots(self):
        """Create three axes for each task."""
        self.ax_lrx = self.fig.add_subplot(self.gs[0, 0])
        self.ax_lrx.set_title('LRX (2-element swap)')
        
        self.ax_topspin = self.fig.add_subplot(self.gs[0, 1])
        self.ax_topspin.set_title('TopSpin')
        
        self.ax_hungarian = self.fig.add_subplot(self.gs[0, 2])
        self.ax_hungarian.set_title('Hungarian Ring')

    def setup_buttons(self):
        """Buttons under each visualization."""
        ax_btn_lrx = self.fig.add_subplot(self.gs[1, 0])
        ax_btn_topspin = self.fig.add_subplot(self.gs[1, 1])
        ax_btn_hungarian = self.fig.add_subplot(self.gs[1, 2])
        
        self.btn_lrx = Button(ax_btn_lrx, 'Swap LRX')
        self.btn_topspin = Button(ax_btn_topspin, 'Flip segment')
        self.btn_hungarian = Button(ax_btn_hungarian, 'Rotate Ring')
        
        self.btn_lrx.on_clicked(self.perform_lrx_swap)
        self.btn_topspin.on_clicked(self.perform_topspin_move)
        self.btn_hungarian.on_clicked(self.perform_hungarian_move)

    #####
    # 1. LRX
    #####
    
    def animate_lrx(self, frame, i, j):
        """
        Animation of smooth displacement of two elements (i and j).
        """
        self.ax_lrx.clear()
        self.ax_lrx.set_title('LRX (2-element swap)')
        self.ax_lrx.set_xlim(-1, 4)
        self.ax_lrx.set_ylim(-1, 1)
        self.ax_lrx.set_aspect('equal') 
        self.ax_lrx.axis('off')

        self.circles = []
        self.texts = []
        for idx, val in enumerate(self.current_states['LRX']):
            color = 'lightgreen' if idx in [i, j] else 'white'
            circle = Circle(
                (idx, 0),
                0.4,
                edgecolor='black',
                facecolor=color
            )
            self.ax_lrx.add_patch(circle)
            self.circles.append(circle)
            txt = self.ax_lrx.text(
                idx, 0, str(val),
                ha='center', va='center',
                fontsize=12,
                color='black'
            )
            self.texts.append(txt)
        
        t = frame / (self.frames - 1)  # normalized progress from 0 to 1

        # Initial and final positions along X
        start_i, start_j = i, j
        end_i, end_j = j, i
        
        # Calculate current X-coordinates for circles
        new_x_i = (1 - t) * start_i + t * end_i
        new_x_j = (1 - t) * start_j + t * end_j
        
        # Shift circles
        self.circles[i].center = (new_x_i, 0)
        self.circles[j].center = (new_x_j, 0)
        
        # Similarly shift labels using set_position
        self.texts[i].set_position((new_x_i, 0))
        self.texts[j].set_position((new_x_j, 0))
        
        # When animation ends, change real indices
        if frame == self.frames - 1:
            self.current_states['LRX'][i], self.current_states['LRX'][j] = \
                self.current_states['LRX'][j], self.current_states['LRX'][i]
            # Swap objects in lists
            self.circles[i], self.circles[j] = self.circles[j], self.circles[i]
            self.texts[i], self.texts[j] = self.texts[j], self.texts[i]

    def perform_lrx_swap(self, event):
        """
        Starts animation using saved indices.
        """
        # Используем сохраненные индексы
        self.animation = FuncAnimation(
            self.fig,
            self.animate_lrx,
            frames=self.frames,
            fargs=(self.lrx_i, self.lrx_j),
            interval=50,
            repeat=False
        )
        plt.draw()

    #####
    # 2. TopSpin
    #####

    def animate_topspin(self, frame, segment_size=4):
        self.ax_topspin.clear()
        self.ax_topspin.set_title("TopSpin")
        self.ax_topspin.set_xlim(-1.5, 1.5)
        self.ax_topspin.set_ylim(-1.5, 1.5)
        self.ax_topspin.set_aspect('equal')
        self.ax_topspin.axis('off')

        total = len(self.current_states['TopSpin'])
        angles = np.linspace(np.pi, 3 * np.pi, total, endpoint=False)

        # Current state (do not change during animation)
        displayed = self.current_states['TopSpin'].copy()

        # Animation progress (0 → 1)
        t = frame / (self.frames - 1)

        # Create a display array (without changing the real order)
        final_display = self.current_states['TopSpin'].copy()
        if frame == self.frames - 1:
            final_display[:segment_size] = final_display[:segment_size][::-1]

        # Calculate the movement of elements
        positions = []
        for i in range(total):
            angle = angles[i]

            # Move elements inside the segment to flip
            if i < segment_size:
                start_angle = angles[i]
                end_angle = angles[segment_size - 1 - i]
                angle = (1 - t) * start_angle + t * end_angle  # Smooth movement

            x, y = np.cos(angle), np.sin(angle)
            positions.append((x, y))

        # Draw elements at their new positions
        for i, (x, y) in enumerate(positions):
            color = "lightgreen" if i < segment_size else "white"
            self.ax_topspin.add_patch(Circle((x, y), 0.15, color=color, ec='black'))
            self.ax_topspin.text(x, y, str(displayed[i]), ha="center", va="center", fontsize=10)

        # Update the array at the end of the animation
        if frame == self.frames - 1:
            self.current_states['TopSpin'][:segment_size] = self.current_states['TopSpin'][:segment_size][::-1]


    def perform_topspin_move(self, event):
        self.animation = FuncAnimation(
            self.fig,
            self.animate_topspin,
            frames=self.frames,
            interval=50,
            repeat=False
        )
        plt.draw()

    #####
    # 3. Hungarian Rings
    #####

    def animate_hungarian(self, frame):
        """
        Animation of rotation of the upper ring by 1 position clockwise, 
        and the lower ring by 1 position counterclockwise for the entire animation.
        """
        self.ax_hungarian.clear()
        self.ax_hungarian.set_title("Hungarian Ring")
        self.ax_hungarian.set_xlim(-1.5, 1.5)
        self.ax_hungarian.set_ylim(-1.5, 1.5)
        self.ax_hungarian.set_aspect('equal')
        self.ax_hungarian.axis('off')

        radius = 0.8
        n = 4        
        t = frame / (self.frames - 1)  # animation progress (0 → 1)
        angle_shift = (2 * np.pi / n)  # angle shift

        # Save the initial state
        if frame == 0:
            self.anim_ring_upper = self.ring_upper.copy()
            self.anim_ring_lower = self.ring_lower.copy()

        # Upper ring — rotate forward
        center_upper = (0, 0.4)
        angles_upper = np.linspace(0, 2*np.pi, n, endpoint=False)
        for i in range(n):
            current_angle = angles_upper[i] - t * angle_shift
            x = center_upper[0] + radius * np.cos(current_angle)
            y = center_upper[1] + radius * np.sin(current_angle)

            self.ax_hungarian.add_patch(
                Circle((x, y), 0.15, color='lightblue', ec='black')
            )
            self.ax_hungarian.text(
                x, y, str(self.anim_ring_upper[i]),
                ha='center', va='center'
            )

        # Lower ring — rotate in the other direction
        center_lower = (0, -0.4)
        angles_lower = np.linspace(0, 2*np.pi, n, endpoint=False)
        for i in range(n):
            current_angle = angles_lower[i] + t * angle_shift
            x = center_lower[0] + radius * np.cos(current_angle)
            y = center_lower[1] + radius * np.sin(current_angle)

            self.ax_hungarian.add_patch(
                Circle((x, y), 0.15, color='lightgreen', ec='black')
            )
            self.ax_hungarian.text(
                x, y, str(self.anim_ring_lower[i]),
                ha='center', va='center'
            )
        
        # Update the state only at the end of the animation
        if frame == self.frames - 1:
            self.ring_upper = np.roll(self.ring_upper, 1)
            self.ring_lower = np.roll(self.ring_lower, -1)
            self.current_states['HungarianRing'] = np.concatenate(
                [self.ring_upper, self.ring_lower]
            )

    def perform_hungarian_move(self, event):
        self.animation = FuncAnimation(
            self.fig,
            self.animate_hungarian,
            frames=self.frames,
            interval=50,
            repeat=False
        )
        plt.draw()

    #####
    # Service — run «updating» animations at the beginning (to see the state)
    #####
    def update_all_visualizations(self):
        """
        Call animations for one frame to draw initial pictures.
        """
        # LRX
        self.lrx_i, self.lrx_j = 0, 1
        self.animate_lrx(frame=0, i=self.lrx_i, j=self.lrx_j)

        # TopSpin
        self.animate_topspin(frame=0, segment_size=4)
        
        # Hungarian Rings
        self.animate_hungarian(frame=0)

        plt.draw()

    def show(self):
        plt.show()

if __name__ == "__main__":
    visualizer = PuzzleVisualizer()
    visualizer.show()
