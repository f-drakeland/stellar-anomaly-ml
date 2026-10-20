import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/lightcurve.csv")

usable = df.loc[
    np.isfinite(df["time"])
    & np.isfinite(df["flux"])
    & (df["quality"] == 0)
].copy()

median_flux = usable["flux"].median()

# Express changes relative to the typical observed brightness.
usable["relative_flux"] = usable["flux"] / median_flux

fig, ax = plt.subplots(figsize=(11, 5))

ax.scatter(
    usable["time"],
    usable["relative_flux"],
    s=5,
    alpha=0.7,
)

ax.axhline(1.0, linestyle="--", linewidth=1)

ax.set(
    title="Tabby's Star — Kepler Quarter 2",
    xlabel="Time (BKJD, days)",
    ylabel="Relative brightness",
)

fig.tight_layout()
fig.savefig("data/lightcurve.png", dpi=150)

print("Plot saved: data/lightcurve.png")
print("Observations plotted:", len(usable))
print("Minimum relative brightness:", usable["relative_flux"].min())
print("Maximum relative brightness:", usable["relative_flux"].max())
