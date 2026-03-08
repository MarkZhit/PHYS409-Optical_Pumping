
import matplotlib.pyplot as plt
import pandas as pd


def multi_lorentz(x, A, h1, g1, x0_1, h2, g2, x0_2, h3, g3, x0_3):
    dip1 = h1 * (g1**2) / ((x - x0_1)**2 + g1**2)
    dip2 = h2 * (g2**2) / ((x - x0_2)**2 + g2**2)
    dip3 = h3 * (g3**2) / ((x - x0_3)**2 + g3**2)
    return A - (dip1 + dip2 + dip3)

def plot_normalized_transmission(time, y2_norm, x0s, savename):
    plt.figure(figsize=(10, 6))
    # Plot CH1 and CH2
    # plt.plot(df['Sequence'], df['CH1'], label='Channel 1', color='blue', alpha=0.7)
    plt.plot(time, y2_norm, label='Channel 2', color='red', alpha=0.7)
    plt.scatter(x0s, [0,0.6,0.4], label='Dip Estimates', color='blue')
    # plt.plot(time,y2_norm, label='Channel 2 normalized', color='red', alpha=0.7)

    # Labels and formatting
    plt.xlabel('Time [s]')
    plt.ylabel('Transmission (normalized)')
    plt.title('Optical Pumping Transmission Signal')
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig("figures/" + savename, dpi=300)

    plt.show()
    return


def read_transmission_csv(filepath):
    df = pd.read_csv(filepath, skiprows=2, usecols=[0, 1, 2],
                     names=['Sequence', 'CH1', 'CH2'])
    dfTimevals = pd.read_csv(filepath, skiprows=1, usecols=[3, 4],
                             names=['Start', 'Increment'])

    # Access the columns as arrays for your fitting function
    x = df['Sequence'].values
    y1 = df['CH1'].values
    y2 = df['CH2'].values

    timeStep = dfTimevals["Increment"].values[0]

    time = x * timeStep
    y2_norm = y2 - min(y2)
    y2_norm = y2_norm / max(y2_norm)

    return time, y1, y2, y2_norm

def plot_fitted_transmission(time, y2_norm, popt, savename):
    plt.figure(figsize=(10, 6))

    # Plot CH1 and CH2
    # plt.plot(df['Sequence'], df['CH1'], label='Channel 1', color='blue', alpha=0.7)
    plt.plot(time, y2_norm, label='Channel 2', color='red', alpha=0.7)
    plt.plot(time, multi_lorentz(time, *popt), label='Lorentzian Fit', color='blue', alpha=0.7)

    # Labels and formatting
    plt.xlabel('Time (s)')
    plt.ylabel('transmission (normalized)')
    plt.title('Optical Pumping Transmission Signal')
    plt.legend()
    plt.legend(loc="lower right")
    plt.grid(True)
    plt.savefig("figures/" + savename, dpi=300)

    plt.show()
    return