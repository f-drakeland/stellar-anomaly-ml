import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest

df = pd.read_csv("data/lightcurve.csv")

usable = df.loc[
    np.isfinite(df["time"])
    & np.isfinite(df["flux"])
    & (df["quality"] == 0)
].copy()

# One feature: measured brightness.
X = usable[["flux"]].to_numpy()

model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=42,
)

predictions = model.fit_predict(X)

usable["ml_anomaly"] = predictions == -1
usable["ml_score"] = -model.score_samples(X)

print("Observations:", len(usable))
print("ML anomalies:", int(usable["ml_anomaly"].sum()))

print("\nTEN HIGHEST ANOMALY SCORES")
print(
    usable.nlargest(10, "ml_score")[
        ["time", "flux", "ml_score"]
    ].to_string(index=False)
)
