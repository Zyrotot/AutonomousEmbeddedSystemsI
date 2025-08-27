import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os
import csv
import numpy as np
import math

def numberOfRows(csvFile: str):
    with open(csvFile, "rt") as f:
        reader = csv.reader(f)
        return sum(1 for _ in reader)

def checkNameInCSV(name: str, csvFile: str):
    with open(csvFile, "rt") as f:
        reader = csv.reader(f, delimiter=",")
        for row in reader:
            if name in row:
                return True, row.index(name)
    return False, 0

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_folder", help="Folder containing CSV files")
    parser.add_argument("-s", type=float, required=True, help="Sample rate")
    parser.add_argument("-y", type=str, nargs="+", required=True, help="Columns to plot")
    parser.add_argument("-ng", action="store_false", help="No GUI. Save PNG file with combined name.")
    return parser.parse_args()

def main():
    args = parseArguments()
    sampleRate = args.s

    # Collect all CSV files from folder
    if not os.path.isdir(args.csv_folder):
        print(f"{args.csv_folder} is not a valid folder")
        exit(1)

    csv_files = [os.path.join(args.csv_folder, f) 
                 for f in os.listdir(args.csv_folder) if f.endswith(".csv")]

    if not csv_files:
        print("No CSV files found in folder.")
        exit(1)

    # Validate all files
    for csv_file in csv_files:
        for name in args.y + ["vd_double_track/x_dot_vec/v_x_mps"]:
            if not checkNameInCSV(name, csv_file)[0]:
                print(f"[{name}] not found in {csv_file}")
                exit(1)

    # Setup subplot grid
    nPlots = math.ceil(math.sqrt(len(args.y)))
    fig, ax = plt.subplots(nPlots, nPlots, sharex="row", squeeze=False)

    # For each file, plot each variable (after aligning start point)
    for csv_file in csv_files:
        df = pd.read_csv(csv_file)

        # Align start point: find first positive velocity index
        first_positive_idx = df[df['vd_double_track/x_dot_vec/v_x_mps'] > 0].index[0]
        filtered = df.loc[first_positive_idx:].reset_index(drop=True)

        # Time axis recomputed for filtered data
        time_axis = np.linspace(0, len(filtered-1)*sampleRate, len(filtered))
        label_prefix = os.path.basename(csv_file)

        ax_idx_row = 0
        ax_idx_col = 0
        for name in args.y:
            ax[ax_idx_row, ax_idx_col].plot(time_axis, filtered[name], label=label_prefix)
            ax[ax_idx_row, ax_idx_col].set_title(name)
            ax[ax_idx_row, ax_idx_col].legend()

            ax_idx_col += 1
            if ax_idx_col == nPlots:
                ax_idx_col = 0
                ax_idx_row += 1

    fig.tight_layout()

    if args.ng:
        plt.show()
    else:
        out_name = os.path.basename(os.path.normpath(args.csv_folder))
        plt.savefig(out_name + ".png")

if __name__ == "__main__":
    main()
