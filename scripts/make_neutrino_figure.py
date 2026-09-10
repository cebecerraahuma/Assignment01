from pathlib import Path
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


PROJECT_ROOT = Path(__file__).resolve().parents[1] # This give us the path on the project root

DATA_PATH       = PROJECT_ROOT/"data"/"raw"/"neutrino_data.csv"
SIMULATION_PATH = PROJECT_ROOT/"data"/"raw"/"neutrino_simulation.csv"
FIGURE_PATH     = PROJECT_ROOT/"figures"/"neutrino_data_simulation_ratio.png"

# Defining the variables
# Histogram
ENERGY_MIN_GEV = 0.0
ENERGY_MAX_GEV = 20.0
N_BINS = 20
# Scale
EXPOSURE_SCALE = 0.1
# Numerical data
DELTA_M2 = 2.5e-3
SIN2_2THETA = 0.87
BASELINE_KM = 735.0


def survival_probability(energy_GeV, delta_m2, sin2_2theta, baseline_km):
    return 1 - sin2_2theta*np.sin(1.27*delta_m2*baseline_km / energy_GeV)**2

def main():
    # Read the data
    data_events         = pd.read_csv(DATA_PATH      ,header=None,names=["energy_GeV"])
    simulation_events   = pd.read_csv(SIMULATION_PATH,header=None,names=["energy_GeV"])
    # Select the analysis window
    data_energy         = data_events.loc[data_events["energy_GeV"].between(ENERGY_MIN_GEV,ENERGY_MAX_GEV),"energy_GeV"].to_numpy()
    simulation_energy   = simulation_events.loc[simulation_events["energy_GeV"].between(ENERGY_MIN_GEV,ENERGY_MAX_GEV),"energy_GeV"].to_numpy()
    # Histogram bins
    bin_edges   = np.linspace(ENERGY_MIN_GEV,ENERGY_MAX_GEV,N_BINS + 1)
    bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
    # Histogram counts
    data_counts, _          = np.histogram(data_energy,bins=bin_edges)
    simulation_counts, _    = np.histogram(simulation_energy,bins=bin_edges)

    scaled_simulation_counts = EXPOSURE_SCALE * simulation_counts
    histogram_table = pd.DataFrame(
    {
        "energy_center_GeV": bin_centers,
        "data_counts": data_counts,
        "scaled_simulation_counts": scaled_simulation_counts,
    }
    )
    # Compute data/simulation ratios only where the denominator is nonzero.
    ratio = np.divide(
        data_counts,
        scaled_simulation_counts,
        out=np.full_like(scaled_simulation_counts, np.nan, dtype=float),
        where=scaled_simulation_counts > 0,
    )

    # Propagate approximate Poisson counting uncertainty for the ratio.
    data_relative_variance = np.divide(
        1.0,
        data_counts,
        out=np.full_like(data_counts, np.nan, dtype=float),
        where=data_counts > 0,
    )
    simulation_relative_variance = np.divide(
        1.0,
        simulation_counts,
        out=np.full_like(simulation_counts, np.nan, dtype=float),
        where=simulation_counts > 0,
    )
    ratio_uncertainty = ratio * np.sqrt(data_relative_variance + simulation_relative_variance)
    # Store the transformed result in a table for inspection.
    ratio_table = histogram_table.copy()
    ratio_table["data_simulation_ratio"] = ratio
    ratio_table["ratio_uncertainty"] = ratio_uncertainty
    # Oscillation curve
    energy_grid = np.linspace(0.2,ENERGY_MAX_GEV,250)
    survival_curve = survival_probability(energy_grid, DELTA_M2,SIN2_2THETA,BASELINE_KM)

    # Final figure
    fig, ax = plt.subplots(figsize=(7, 4))

    # TODO: Draw the ratio points from ratio_table and your survival-probability curve on ax.

    # Data
    ax.errorbar(
        ratio_table["energy_center_GeV"],
        ratio_table["data_simulation_ratio"],
        yerr=ratio_table["ratio_uncertainty"],
        fmt="o",
        capsize=2,
    )
    # Model
    ax.plot(energy_grid,survival_curve,label=rf"$\Delta m^2={DELTA_M2:.2}$, $\sin^2(2\theta)={SIN2_2THETA}$")
    ax.set_xlabel("Energy ($GeV$)")
    ax.set_ylabel("data / model")
    ax.set_title("Data / simulation ratio vs. model")
    ax.legend()
    ax.axhline(1.0,linewidth=0.75, linestyle = '--',color='black')

    # Save the figure into the repository so it can be committed.
    FIGURE_DIR  = PROJECT_ROOT/"figures"
    FIGURE_PATH = FIGURE_DIR/"neutrino_data_simulation_ratio.png"
    # Save the figure to FIGURE_PATH with good resolution.
    plt.savefig(FIGURE_PATH,dpi=650)
    # plt.show()
    print(f"Saved figure to: {FIGURE_PATH}")


if __name__ == "__main__":
    main()
    print('Done!!!')