import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.metrics import precision_score, recall_score, f1_score

SEED = 42

df = pd.read_csv("data/lightcurve.csv")

usable = df.loc[
    np.isfinite(df["time"])
    & np.isfinite(df["flux"])
    & (df["quality"] == 0)
].copy()

usable = usable.sort_values("time").reset_index(drop=True)

flux = usable["flux"].to_numpy()

split = int(len(flux) * 0.70)

train = flux[:split]
test = flux[split:].copy()

rng = np.random.default_rng(SEED)

# Inject artificial brightness dips into 5% of test observations.
n_injected = round(len(test) * 0.05)
positions = rng.choice(len(test), n_injected, replace=False)

labels = np.zeros(len(test), dtype=int)
labels[positions] = 1

# Fixed-size dimming relative to the training median.
train_median = np.median(train)
test[positions] -= train_median * 0.002

# Baseline: fitted on training observations only.
mad = np.median(np.abs(train - train_median))
if mad == 0:
    raise ValueError("Training MAD is zero")

baseline_scores = np.abs(
    (test - train_median) / (1.4826 * mad)
)
baseline_predictions = (baseline_scores > 3.5).astype(int)

# ML model: fitted on training observations only.
model = IsolationForest(
    n_estimators=100,
    contamination=0.03,
    random_state=SEED,
)

model.fit(train.reshape(-1, 1))

ml_predictions = (
    model.predict(test.reshape(-1, 1)) == -1
).astype(int)

def report(name, predictions):
    print(f"\n{name}")
    print("Flagged:", int(predictions.sum()))
    print("Precision:", round(precision_score(
        labels, predictions, zero_division=0
    ), 4))
    print("Recall:", round(recall_score(
        labels, predictions, zero_division=0
    ), 4))
    print("F1:", round(f1_score(
        labels, predictions, zero_division=0
    ), 4))

print("Training observations:", len(train))
print("Test observations:", len(test))
print("Injected observations:", n_injected)
print("Injection magnitude: 0.2% of training median flux")
print("Random seed:", SEED)

report("MAD BASELINE", baseline_predictions)
report("ISOLATION FOREST", ml_predictions)
