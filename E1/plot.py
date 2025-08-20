import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV files
df_1400 = pd.read_csv('mass/E1_mass_1400.csv')
df_1200 = pd.read_csv('mass/E1_mass_1200.csv')
df_1000 = pd.read_csv('mass/E1_mass_1000.csv')
df_800 = pd.read_csv('mass/E1_mass_800.csv')

plt.figure(figsize=(10, 6))

for df, label in zip(
    [df_1400, df_1200, df_1000, df_800],
    ['1400 Kg', '1200 Kg', '1000 Kg', '800 Kg']
):
    first_positive_idx = df[df['vd_double_track/x_dot_vec/v_x_mps'] > 0].index[0]
    filtered = df.loc[first_positive_idx:].reset_index(drop=True)
    plt.plot(filtered['vd_double_track/x_vec/v_x_mps'], label=label)

plt.xlabel('Simulation Time [s]')
plt.ylabel('v_x_mps')
plt.title('v_x_mps vs Simulation Time')
plt.legend()
plt.grid(True)
plt.show()
