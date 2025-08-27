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
        header = next(reader)
        if name in header:
            return True, header.index(name)
    return False, 0

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_paths", nargs="+", help="Folder(s) or CSV file(s)")
    parser.add_argument("-s", type=float, required=True, help="Sample rate")
    parser.add_argument("-y", type=str, nargs="+", required=True, help="Columns to plot")
    parser.add_argument("-ng", action="store_false", help="No GUI. Save PNG file with combined name.")
    parser.add_argument("--labels", type=str, nargs="+", help="Optional labels for each CSV file")
    return parser.parse_args()

def collect_csv_files(paths):
    csv_files = []
    for path in paths:
        if os.path.isdir(path):
            csv_files += [os.path.join(path, f) for f in os.listdir(path) if f.endswith(".csv")]
        elif os.path.isfile(path) and path.endswith(".csv"):
            csv_files.append(path)
        else:
            print(f"Warning: {path} is not a valid CSV file or directory, skipping.")
    return csv_files

def main():
    args = parseArguments()
    sampleRate = args.s

    csv_files = collect_csv_files(args.csv_paths)

    if not csv_files:
        print("No CSV files found in the given paths.")
        exit(1)

    # Validate all files
    for csv_file in csv_files:
        for name in args.y + ["vd_double_track/x_dot_vec/v_x_mps"]:
            if not checkNameInCSV(name, csv_file)[0]:
                print(f"[{name}] not found in {csv_file}")
                exit(1)

    # Validate labels if provided
    if args.labels:
        if len(args.labels) != len(csv_files):
            print("Number of labels must match the number of CSV files.")
            exit(1)

    # Setup subplot grid
    nPlots = math.ceil(math.sqrt(len(args.y)))
    fig, ax = plt.subplots(nPlots, nPlots, sharex="row", squeeze=False)

    # Plot each variable from each file
    for idx, csv_file in enumerate(csv_files):
        df = pd.read_csv(csv_file)

        # Align start point: find first positive velocity index
        first_positive_idx = df[df['vd_double_track/x_dot_vec/v_x_mps'] > 0].index[0]
        filtered = df.loc[first_positive_idx:].reset_index(drop=True)

        # Time axis recomputed for filtered data
        time_axis = np.linspace(0, (len(filtered)-1)*sampleRate, len(filtered))
        label_prefix = args.labels[idx] if args.labels else os.path.basename(csv_file)

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
        out_name = "combined_plot"
        plt.savefig(out_name + ".png")

if __name__ == "__main__":
    main()
