# Stellar Anomaly ML

## Project overview

**Stellar Anomaly ML** investigates anomaly detection in real
NASA Kepler observations of KIC 8462852 (Tabby's Star).

The experiment compares a robust statistical method (median
absolute deviation, or MAD) against an unsupervised machine-learning
model (Isolation Forest).

Both methods were evaluated on a chronological held-out segment
containing 48 artificially injected brightness reductions.

### Key result

| Metric | MAD baseline | Isolation Forest |
|---|---:|---:|
| Precision | 0.7164 | 0.4898 |
| Recall | 1.0000 | 1.0000 |
| F1 score | **0.8348** | 0.6575 |

Both methods recovered all 48 injected disturbances. Under the
tested configurations, the simpler MAD baseline produced fewer
additional flags and achieved a higher F1 score.

**Scientific limitation:** These results measure recovery of
synthetic, single-observation brightness reductions. They do
not establish accuracy at detecting genuine astronomical events.
The source FITS file also has documented internal checksum
verification failures.

### Technologies

Python 3.13, NumPy, pandas, scikit-learn, Astropy, Matplotlib,
and Git.

---


## Dataset

Mission: NASA Kepler
Archive: Mikulski Archive for Space Telescopes (MAST)
Target: KIC 8462852
Observation: Quarter 2, long cadence
MAST observation ID: 491351

Original FITS filename:
kplr008462852-2009259160929_llc.fits

Download:
https://mast.stsci.edu/api/v0.1/Download/file?uri=mast:KEPLER/url/missions/kepler/lightcurves/0084/008462852/kplr008462852-2009259160929_llc.fits

Original FITS SHA-256:
26d64427416a415bb6f7e330279f9581cc3a02f209a93292da13e2f17fbf2957

## Data preparation

Source observations: 4,354

Selected columns:
- TIME
- PDCSAP_FLUX
- SAP_QUALITY

Initial analysis requires:
- Finite timestamps
- Finite corrected flux
- SAP_QUALITY == 0

Eligible observations: 3,217

The raw FITS file and derived CSV are excluded from Git.

## Methods

Statistical baseline:
- Median absolute deviation (MAD)
- Absolute robust z-score greater than 3.5

Machine-learning model:
- Isolation Forest
- One feature: corrected flux
- 100 estimators
- Contamination: 0.03
- Random seed: 42

## Initial results

MAD baseline flagged: 89 observations
Isolation Forest flagged: 97 observations
Both methods flagged: 77
Baseline only: 12
ML only: 20
Jaccard agreement: 0.7064

These are exploratory anomaly flags, not confirmed
astronomical events or validated detection accuracy.

## Reproduction

Install dependencies into a Python virtual environment:

python -m pip install numpy pandas scikit-learn astropy matplotlib

The existing data/lightcurve.csv was generated from the FITS
LIGHTCURVE extension using TIME, PDCSAP_FLUX, and SAP_QUALITY,
preserving all source rows.

Run:

python analyze.py
python evaluate.py
python train.py

## Limitations

Only one observing quarter is analyzed.
The model uses brightness alone and ignores temporal structure.
The Isolation Forest is evaluated on its training observations.
No independently labeled real stellar anomalies are available.
Synthetic-injection evaluation remains to be implemented.

## Source integrity verification

The original FITS file was downloaded twice from the NASA MAST
endpoint. Both copies contained 466,560 bytes and had identical
SHA-256 hashes:

26d64427416a415bb6f7e330279f9581cc3a02f209a93292da13e2f17fbf2957

Astropy FITS-internal CHECKSUM verification results:
- PRIMARY: PASS
- LIGHTCURVE: FAIL
- APERTURE: FAIL

No DATASUM keywords were present.

The cause of the FITS-internal checksum failures remains
unresolved. Matching downloads establish byte consistency
with the current MAST response, not independent scientific
validation of the measurements.

The extraction script reproduces the original CSV byte-for-byte.

CSV SHA-256:
e54525769b69787f3751a6800cd00f162a45664fd32afdab2e73d8fe12d9b20d

## Held-out synthetic-injection experiment

Executable: experiment.py

Dataset:
- 3,217 quality-filtered observations
- Chronological 70/30 train/test split
- Training observations: 2,251
- Test observations: 966

Synthetic intervention:
- Random seed: 42
- 48 test observations selected without replacement
- Each selected flux reduced by 0.2% of training median
- No synthetic changes to training observations

Methods:
- MAD baseline: training median and MAD, threshold 3.5
- Isolation Forest: 100 estimators, contamination 0.03
- Both methods fitted using training data only

Results:

| Metric | MAD | Isolation Forest |
|---|---:|---:|
| Flagged | 67 | 98 |
| Precision | 0.7164 | 0.4898 |
| Recall | 1.0000 | 1.0000 |
| F1 | 0.8348 | 0.6575 |

Two consecutive executions produced byte-identical text output.

Interpretation:
Under these specific settings, MAD achieved higher precision
and F1 while both methods recovered all injected observations.

Limitations:
- Synthetic single-point disturbances are not realistic stellar events.
- Non-injected observations are not independently verified as normal.
- Results do not establish real astronomical detection accuracy.
- Thresholds were not calibrated to equal false-positive rates.
- Only one random seed and injection magnitude were evaluated.
- Neither method uses temporal relationships between observations.
