import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load data
exp = pd.read_csv("experiment.csv")
sim = pd.read_csv("simulation.csv")

# Sort by time to ensure proper interpolation
exp = exp.sort_values("time")
sim = sim.sort_values("time")

# Interpolate simulation data onto experimental time points
sim_interp = np.interp(
    exp["time"],        # target time points (experiment)
    sim["time"],        # original simulation time
    sim["velocity"]     # original simulation velocity
)

# Calculate error metrics
error = abs(exp["velocity"] - sim_interp)
avg_error = error.mean()
max_error = error.max()

print(f"Average Error = {avg_error:.2f}")
print(f"Max Error = {max_error:.2f}")

# Identify the point of maximum error
max_error_index = error.idxmax()
max_error_time = exp["time"].iloc[max_error_index]
exp_value = exp["velocity"].iloc[max_error_index]
sim_interp_value = sim_interp[max_error_index]

# Plot results
plt.figure(figsize=(8, 5))

# Experimental data
plt.plot(exp["time"], exp["velocity"], marker="o", label="Experiment")

# Original simulation data
plt.plot(sim["time"], sim["velocity"], marker="s", label="Simulation")

# Interpolated simulation data
plt.plot(
    exp["time"],
    sim_interp,
    linestyle="--",
    marker="x",
    label="Simulation (Interpolated)"
)

# Highlight maximum error
plt.plot(max_error_time, exp_value, marker="o", color="red")
plt.plot(max_error_time, sim_interp_value, marker="o", color="red")

plt.plot(
    [max_error_time, max_error_time],
    [exp_value, sim_interp_value],
    color="red",
    linestyle="--",
    label="Maximum Error"
)

# Conclusion based on average error
if avg_error < 0.1:
    conclusion = "Good Match"
    print("Conclusion: Simulation matches experimental data well.")
elif avg_error < 0.3:
    conclusion = "Moderate Deviation"
    print("Conclusion: Simulation shows moderate deviation.")
else:
    conclusion = "Poor Match"
    print("Conclusion: Simulation has significant deviation from experiment.")

# Add annotation box
plt.text(
    0.05, 0.95,
    f"Avg Error = {avg_error:.2f}\nMax Error = {max_error:.2f}\n{conclusion}",
    transform=plt.gca().transAxes,
    fontsize=10,
    verticalalignment="top",
    bbox=dict(facecolor="white", alpha=0.7)
)

# Labels and formatting
plt.xlabel("Time (s)")
plt.ylabel("Velocity (m/s)")
plt.title("Experiment vs Simulation")
plt.grid()
plt.legend()
plt.tight_layout()

# Save figure
plt.savefig("comparison_plot.png", dpi=300)

plt.show()