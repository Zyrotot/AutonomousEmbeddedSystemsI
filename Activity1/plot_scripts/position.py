import pandas as pd
import matplotlib.pyplot as plt
import argparse

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Plot vehicle X vs Y from one or more CSV files")
parser.add_argument("csv_files", type=str, nargs='+', help="Path(s) to the CSV file(s)")
args = parser.parse_args()

# Columns for X and Y
x_col = "vd_double_track/x_vec/x_m"
y_col = "vd_double_track/x_vec/y_m"

# Plot
plt.figure(figsize=(8, 6))
for csv_file in args.csv_files:
	df = pd.read_csv(csv_file)
	plt.plot(df[x_col], df[y_col], label=csv_file)

plt.xlabel("X position (m)")
plt.ylabel("Y position (m)")
plt.title("Vehicle X vs Y")
plt.grid(True)
plt.legend()
plt.axis('equal')  # Keep aspect ratio
plt.show()
