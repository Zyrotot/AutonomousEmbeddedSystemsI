import matplotlib.pyplot as plt
import matplotlib.patches as patches

def draw_square(ax, x, y, width, height, color="blue"):
    square = patches.Rectangle((x, y), width, height, linewidth=2,
                               edgecolor=color, facecolor="none")
    ax.add_patch(square)

def main():
    fig, ax = plt.subplots()
    ax.set_aspect("equal")
    
    draw_square(ax, 0, 0, 4, 3, "red")
    draw_square(ax, 2, 1, 4, 4, "blue")
    
    ax.set_xlim(-1, 7)
    ax.set_ylim(-1, 7)
    ax.grid(True, linestyle="--", alpha=0.6)
    ax.axhline(0, color="black", linewidth=1)
    ax.axvline(0, color="black", linewidth=1)
    
    plt.show()

if __name__ == "__main__":
    main()
