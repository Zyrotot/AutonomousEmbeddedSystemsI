import pandas as pd
import matplotlib.pyplot as plt
import argparse
import os.path
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

def checkFileExists(filePath: str):
    return os.path.isfile(filePath)

def parseArguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("csv_files", nargs="+", help="CSV file(s) to process")
    parser.add_argument("-s", type=float, required=True, help="Sample rate")
    parser.add_argument("-y", type=str, nargs="+", required=True, help="Columns to plot")
    parser.add_argument("-ng", action="store_false", help="No GUI. Save PNG file with same csv_file_name.")
    return parser.parse_args()

def main():
    args = parseArguments()
    sampleRate = args.s

    # Validate all files
    for csv_file in args.csv_files:
        if not checkFileExists(csv_file):
            print(f"File {csv_file} does not exist")
            exit(1)
        for name in args.y:
            if not checkNameInCSV(name, csv_file)[0]:
                print(f"[{name}] not found in {csv_file}")
                exit(1)

    # Setup subplot grid
    nPlots = math.ceil(math.sqrt(len(args.y)))
    fig, ax = plt.subplots(nPlots, nPlots, sharex="row", squeeze=False)

    # For each file, plot each variable
    for csv_file in args.csv_files:
        df = pd.read_csv(csv_file)

        # Align start point: find first positive velocity index
        first_positive_idx = df[df['vd_double_track/x_dot_vec/v_x_mps'] > 0].index[0]
        filtered = df.loc[first_positive_idx:].reset_index(drop=True)

        time_axis = np.linspace(0, (len(filtered)-1)*sampleRate, len(filtered))
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
        # Save one PNG per variable set
        out_name = "_".join([os.path.splitext(os.path.basename(f))[0] for f in args.csv_files])
        plt.savefig(out_name + ".png")

if __name__ == "__main__":
    main()
