from pathlib import Path
import hashlib

import numpy as np
import pandas as pd
from astropy.io import fits

source = Path("data/kplr008462852-2009259160929_llc.fits")
destination = Path("data/lightcurve.csv")

expected_sha256 = (
    "26d64427416a415bb6f7e330279f9581cc3a02f209a93292da13e2f17fbf2957"
)

actual_sha256 = hashlib.sha256(source.read_bytes()).hexdigest()

if actual_sha256 != expected_sha256:
    raise ValueError("Source FITS checksum mismatch")

with fits.open(source, checksum=True) as hdul:
    observations = hdul["LIGHTCURVE"].data

    df = pd.DataFrame({
        "time": np.asarray(observations["TIME"], dtype="float64"),
        "flux": np.asarray(observations["PDCSAP_FLUX"], dtype="float64"),
        "quality": np.asarray(observations["SAP_QUALITY"], dtype="int64"),
    })

if len(df) != 4354:
    raise ValueError("Unexpected source row count")

if df["quality"].isna().any():
    raise ValueError("Missing quality flags")

# The original CSV was generated with pandas' default CSV settings.
df.to_csv(destination, index=False)

print("SOURCE SHA-256:", actual_sha256)
print("ROWS EXTRACTED:", len(df))
print("MISSING TIME:", int(df["time"].isna().sum()))
print("MISSING FLUX:", int(df["flux"].isna().sum()))
print("OUTPUT:", destination)
