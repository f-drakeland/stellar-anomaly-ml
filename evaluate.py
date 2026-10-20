import numpy as np
import pandas as pd

df = pd.read_csv("data/lightcurve.csv")

usable = df.loc[
    np.isfinite(df["time"])
    & np.isfinite(df["flux"])
    & (df["quality"] == 0)
].copy()

flux = usable["flux"].to_numpy()

median = np.median(flux)
mad = np.median(np.abs(flux - median))

if mad == 0:
    raise ValueError("MAD is zero; cannot compute baseline.")

robust_z = (flux - median) / (1.4826 * mad)

usable["baseline_score"] = robust_z
usable["baseline_anomaly"] = np.abs(robust_z) > 3.5

print("Median flux:", median)
print("MAD:", mad)
print("Baseline anomalies:", int(usable["baseline_anomaly"].sum()))

print("\nTEN MOST NEGATIVE DEVIATIONS")
print(
    usable.nsmallest(10, "baseline_score")[
        ["time", "flux", "baseline_score"]
    ].to_string(index=False)
)
